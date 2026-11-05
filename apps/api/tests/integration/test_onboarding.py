from fastapi.testclient import TestClient

from app.dependencies.get_current_user import get_current_user
from app.main import app
from app.types.authenticated_user import AuthenticatedUser

client = TestClient(app)


def test_status_for_a_verified_user_without_a_cv(monkeypatch, logged_in):
    monkeypatch.setattr("app.routers.onboarding.get_cv", lambda user_id: None)

    response = client.get("/onboarding/status")

    assert response.status_code == 200
    body = response.json()
    assert body["next_step"] == "cv"
    assert body["steps"] == {"verify": True, "cv": False, "profile": False}


def test_status_is_available_before_the_email_is_verified(logged_in):
    unverified = AuthenticatedUser("user-2", "Jane Doe", "jane.doe@example.com", False)
    app.dependency_overrides[get_current_user] = lambda: unverified

    response = client.get("/onboarding/status")

    assert response.status_code == 200
    assert response.json()["next_step"] == "verify"
