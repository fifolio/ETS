import pytest
from fastapi.testclient import TestClient

from app.dependencies.get_current_user import get_current_user
from app.main import app
from app.schemas.subscription_out import SubscriptionOut
from app.types.authenticated_user import AuthenticatedUser

client = TestClient(app)


def status(**overrides):
    values = {
        "plan": "explore",
        "plan_name": "Explore",
        "is_paid": False,
        "current_period_end": None,
        "cancel_at_period_end": False,
        "can_manage": False,
        "can_cancel": False,
    }
    return SubscriptionOut(**{**values, **overrides})


@pytest.fixture(autouse=True)
def free_plan(monkeypatch):
    monkeypatch.setattr("app.routers.account.get_subscription_status", lambda user: status())


def test_deletes_the_account_of_the_logged_in_user(monkeypatch, logged_in):
    deleted = []
    monkeypatch.setattr("app.routers.account.delete_user_account", deleted.append)

    response = client.delete("/account")

    assert response.status_code == 204
    assert deleted == ["user-1"]


def test_a_user_who_never_verified_can_delete_their_account_too(monkeypatch, logged_in):
    deleted = []
    monkeypatch.setattr("app.routers.account.delete_user_account", deleted.append)
    unverified = AuthenticatedUser("user-2", "Jane Doe", "jane.doe@example.com", False)
    app.dependency_overrides[get_current_user] = lambda: unverified

    response = client.delete("/account")

    assert response.status_code == 204
    assert deleted == ["user-2"]


def test_a_subscription_that_is_still_renewing_must_be_cancelled_first(monkeypatch, logged_in):
    deleted = []
    monkeypatch.setattr("app.routers.account.delete_user_account", deleted.append)
    renewing = status(
        plan="nextmove", plan_name="Next Move", is_paid=True, can_manage=True, can_cancel=True
    )
    monkeypatch.setattr("app.routers.account.get_subscription_status", lambda user: renewing)

    response = client.delete("/account")

    assert response.status_code == 409
    assert "Cancel your subscription" in response.json()["detail"]
    assert deleted == []


def test_a_subscription_that_is_already_cancelled_no_longer_blocks_the_deletion(
    monkeypatch, logged_in
):
    deleted = []
    monkeypatch.setattr("app.routers.account.delete_user_account", deleted.append)
    cancelled = status(
        plan="nextmove",
        plan_name="Next Move",
        is_paid=True,
        can_manage=True,
        cancel_at_period_end=True,
    )
    monkeypatch.setattr("app.routers.account.get_subscription_status", lambda user: cancelled)

    assert client.delete("/account").status_code == 204
    assert deleted == ["user-1"]
