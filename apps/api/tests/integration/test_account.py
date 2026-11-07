from fastapi.testclient import TestClient

from app.dependencies.get_current_user import get_current_user
from app.main import app
from app.types.authenticated_user import AuthenticatedUser

client = TestClient(app)


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
