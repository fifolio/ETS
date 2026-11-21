from fastapi.testclient import TestClient

from app.dependencies.get_current_user import get_current_user
from app.main import app
from app.schemas.credits_out import CreditsOut
from app.types.authenticated_user import AuthenticatedUser

client = TestClient(app)

CREDITS = CreditsOut(subscription=10, promotional=2, purchased=5, total=17, credits_per_scan=1)


def test_returns_the_balances_of_the_logged_in_user(monkeypatch, logged_in):
    asked = []
    monkeypatch.setattr(
        "app.routers.credits.read_user_credits", lambda user_id: asked.append(user_id) or CREDITS
    )

    response = client.get("/credits")

    assert response.status_code == 200
    assert response.json() == CREDITS.model_dump()
    assert asked == ["user-1"]


def test_an_unverified_user_cannot_read_credits(logged_in):
    unverified = AuthenticatedUser("user-2", "Jane Doe", "jane.doe@example.com", False)
    app.dependency_overrides[get_current_user] = lambda: unverified

    assert client.get("/credits").status_code == 403


def test_reading_credits_needs_a_login():
    assert client.get("/credits").status_code == 401
