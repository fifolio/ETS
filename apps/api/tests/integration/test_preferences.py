from fastapi.testclient import TestClient

from app.dependencies.get_current_user import get_current_user
from app.main import app
from app.types.authenticated_user import AuthenticatedUser

client = TestClient(app)


def test_a_user_without_saved_preferences_gets_the_defaults(logged_in):
    response = client.get("/preferences")

    assert response.status_code == 200
    assert response.json() == {
        "theme": "light",
        "language": "en",
        "effective_language": "en",
        "direction": "ltr",
    }


def test_saved_preferences_are_returned_and_an_untranslated_language_shows_english(logged_in):
    user = AuthenticatedUser(
        "user-1", "Jane Doe", "jane.doe@example.com", True, {"theme": "dark", "language": "fr"}
    )
    app.dependency_overrides[get_current_user] = lambda: user

    body = client.get("/preferences").json()

    assert (body["theme"], body["language"], body["effective_language"]) == ("dark", "fr", "en")


def test_an_unverified_user_cannot_read_preferences(logged_in):
    unverified = AuthenticatedUser("user-2", "Jane Doe", "jane.doe@example.com", False)
    app.dependency_overrides[get_current_user] = lambda: unverified

    assert client.get("/preferences").status_code == 403


def test_reading_preferences_needs_a_login():
    assert client.get("/preferences").status_code == 401
