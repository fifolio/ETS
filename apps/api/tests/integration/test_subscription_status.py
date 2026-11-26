from fastapi.testclient import TestClient

from app.dependencies.get_current_user import get_current_user
from app.exceptions.payment_provider_error import PaymentProviderError
from app.exceptions.payments_unavailable_error import PaymentsUnavailableError
from app.exceptions.subscription_action_error import SubscriptionActionError
from app.main import app
from app.schemas.subscription_out import SubscriptionOut
from app.types.authenticated_user import AuthenticatedUser

client = TestClient(app)
STATUS = SubscriptionOut(
    plan="nextmove",
    plan_name="Next Move",
    is_paid=True,
    current_period_end="2026-12-31T00:00:00+00:00",
    cancel_at_period_end=False,
    can_manage=True,
    can_cancel=True,
)
MODULE = "app.routers.subscription_status"


def raising(error):
    def fail(user):
        raise error

    return fail


def test_the_status_is_returned(monkeypatch, logged_in):
    monkeypatch.setattr(f"{MODULE}.get_subscription_status", lambda user: STATUS)

    response = client.get("/subscription")

    assert response.status_code == 200 and response.json() == STATUS.model_dump()


def test_an_unverified_user_cannot_read_the_status(logged_in):
    unverified = AuthenticatedUser("user-2", "Jane Doe", "jane.doe@example.com", False)
    app.dependency_overrides[get_current_user] = lambda: unverified

    assert client.get("/subscription").status_code == 403


def test_reading_the_status_needs_a_login():
    assert client.get("/subscription").status_code == 401


def test_cancelling_returns_the_new_state(monkeypatch, logged_in):
    cancelled = STATUS.model_copy(update={"cancel_at_period_end": True, "can_cancel": False})
    monkeypatch.setattr(f"{MODULE}.cancel_user_subscription", lambda user: cancelled)

    response = client.post("/subscription/cancel")

    assert response.status_code == 200 and response.json()["cancel_at_period_end"] is True


def test_cancelling_without_a_paid_subscription_returns_400(monkeypatch, logged_in):
    monkeypatch.setattr(
        f"{MODULE}.cancel_user_subscription",
        raising(SubscriptionActionError("No subscription.", 400)),
    )

    assert client.post("/subscription/cancel").status_code == 400


def test_a_failing_payment_service_returns_502_on_cancel(monkeypatch, logged_in):
    monkeypatch.setattr(f"{MODULE}.cancel_user_subscription", raising(PaymentProviderError("down")))

    assert client.post("/subscription/cancel").status_code == 502


def test_cancelling_without_a_payment_provider_returns_503(monkeypatch, logged_in):
    monkeypatch.setattr(
        f"{MODULE}.cancel_user_subscription", raising(PaymentsUnavailableError("none"))
    )

    assert client.post("/subscription/cancel").status_code == 503


def test_the_billing_page_address_is_returned(monkeypatch, logged_in):
    monkeypatch.setattr(
        f"{MODULE}.get_user_manage_url", lambda user: "https://whop.com/billing/manage/mem_1"
    )

    response = client.get("/subscription/manage-url")

    assert response.status_code == 200 and response.json() == {
        "url": "https://whop.com/billing/manage/mem_1"
    }


def test_a_missing_billing_page_returns_404(monkeypatch, logged_in):
    monkeypatch.setattr(
        f"{MODULE}.get_user_manage_url", raising(SubscriptionActionError("None.", 404))
    )

    assert client.get("/subscription/manage-url").status_code == 404


def test_a_failing_payment_service_returns_502_for_the_billing_page(monkeypatch, logged_in):
    monkeypatch.setattr(f"{MODULE}.get_user_manage_url", raising(PaymentProviderError("down")))

    assert client.get("/subscription/manage-url").status_code == 502


def test_the_billing_page_without_a_payment_provider_returns_503(monkeypatch, logged_in):
    monkeypatch.setattr(f"{MODULE}.get_user_manage_url", raising(PaymentsUnavailableError("none")))

    assert client.get("/subscription/manage-url").status_code == 503
