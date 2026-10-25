from appwrite.exception import AppwriteException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.testclient import TestClient

from app.core.auth import get_current_user
from app.main import app
from app.services.appwrite_client import AuthenticatedUser

client = TestClient(app)


def test_missing_token_returns_401():
    assert client.get("/cv").status_code == 401


def test_invalid_token_returns_401(monkeypatch):
    def reject(token):
        raise AppwriteException("invalid jwt", 401)

    monkeypatch.setattr("app.core.auth.verify_jwt", reject)
    response = client.get("/cv", headers={"Authorization": "Bearer bad-token"})
    assert response.status_code == 401


def test_appwrite_outage_returns_502(monkeypatch):
    def down(token):
        raise AppwriteException("server error", 500)

    monkeypatch.setattr("app.core.auth.verify_jwt", down)
    response = client.get("/cv", headers={"Authorization": "Bearer some-token"})
    assert response.status_code == 502


def test_valid_token_returns_user(monkeypatch):
    user = AuthenticatedUser("user-1", "Jane Doe", "jane.doe@example.com")
    monkeypatch.setattr("app.core.auth.verify_jwt", lambda token: user)
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="good-token")
    assert get_current_user(credentials) == user
