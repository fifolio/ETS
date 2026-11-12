from fastapi.testclient import TestClient

from app.core.config import settings
from app.dependencies.get_current_user import get_current_user
from app.main import app
from app.services.payments.disabled_provider import DisabledProvider
from app.types.authenticated_user import AuthenticatedUser
from app.types.checkout_session import CheckoutSession

client = TestClient(app)


class FakeProvider:
    name = "fake"

    def __init__(self):
        self.calls = []

    def create_checkout(self, user_id, email, plan):
        self.calls.append((user_id, email, plan.id))
        return CheckoutSession(url="https://pay.example/session/1", reference="ref-1")


def use_provider(monkeypatch, provider):
    monkeypatch.setattr("app.routers.subscription.get_payment_provider", lambda: provider)


def test_checkout_returns_the_payment_page(monkeypatch, logged_in):
    provider = FakeProvider()
    use_provider(monkeypatch, provider)

    response = client.post("/subscription/checkout", json={"plan": "nextmove"})

    assert response.status_code == 200
    assert response.json() == {"checkout_url": "https://pay.example/session/1"}
    assert provider.calls == [("user-1", "jane.doe@example.com", "nextmove")]


def test_checkout_is_unavailable_without_a_provider(monkeypatch, logged_in):
    monkeypatch.setattr(settings, "payment_provider", "none")
    use_provider(monkeypatch, DisabledProvider())

    response = client.post("/subscription/checkout", json={"plan": "urgent"})

    assert response.status_code == 503
    assert "not available" in response.json()["detail"]


def test_an_unknown_plan_is_refused(monkeypatch, logged_in):
    use_provider(monkeypatch, FakeProvider())

    assert client.post("/subscription/checkout", json={"plan": "platinum"}).status_code == 400


def test_the_free_plan_cannot_be_bought(monkeypatch, logged_in):
    use_provider(monkeypatch, FakeProvider())

    assert client.post("/subscription/checkout", json={"plan": "explore"}).status_code == 400


def test_the_current_plan_cannot_be_bought_again(monkeypatch, logged_in):
    use_provider(monkeypatch, FakeProvider())
    on_nextmove = AuthenticatedUser(
        "user-1", "Jane Doe", "jane.doe@example.com", True, {}, ["nextmove"], "nextmove"
    )
    app.dependency_overrides[get_current_user] = lambda: on_nextmove

    response = client.post("/subscription/checkout", json={"plan": "nextmove"})

    assert response.status_code == 400
    assert "already" in response.json()["detail"]


def test_an_unverified_user_cannot_start_a_checkout(logged_in):
    unverified = AuthenticatedUser("user-2", "Jane Doe", "jane.doe@example.com", False)
    app.dependency_overrides[get_current_user] = lambda: unverified

    assert client.post("/subscription/checkout", json={"plan": "urgent"}).status_code == 403
