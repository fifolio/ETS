from fastapi.testclient import TestClient

from app.dependencies.get_current_user import get_current_user
from app.main import app
from app.types.authenticated_user import AuthenticatedUser

client = TestClient(app)

PAYLOAD = {
    "install_id": "install-12345678",
    "browser": "Chrome",
    "browser_version": "130.0",
    "os": "Windows",
    "extension_version": "0.1.0",
}


def fake_register(created):
    registered = []

    def register(user_id, registration):
        registered.append((user_id, registration.install_id))
        return created

    return register, registered


def test_registering_a_new_install_returns_201(monkeypatch, logged_in):
    register, registered = fake_register(created=True)
    monkeypatch.setattr("app.routers.extensions.register.register_extension", register)

    response = client.post("/extensions", json=PAYLOAD)

    assert response.status_code == 201
    assert response.json() == {"created": True}
    assert registered == [("user-1", "install-12345678")]


def test_registering_a_known_install_again_returns_200(monkeypatch, logged_in):
    register, _ = fake_register(created=False)
    monkeypatch.setattr("app.routers.extensions.register.register_extension", register)

    response = client.post("/extensions", json=PAYLOAD)

    assert response.status_code == 200
    assert response.json() == {"created": False}


def test_an_unverified_user_cannot_register(logged_in):
    unverified = AuthenticatedUser("user-2", "Jane Doe", "jane.doe@example.com", False)
    app.dependency_overrides[get_current_user] = lambda: unverified

    assert client.post("/extensions", json=PAYLOAD).status_code == 403


def test_an_invalid_install_id_is_rejected(logged_in):
    response = client.post("/extensions", json={**PAYLOAD, "install_id": "bad id!"})

    assert response.status_code == 422


def test_registering_needs_a_login():
    assert client.post("/extensions", json=PAYLOAD).status_code == 401
