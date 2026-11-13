import pytest
from fastapi.testclient import TestClient

from app.dependencies.get_current_user import get_current_user
from app.main import app
from app.types.authenticated_user import AuthenticatedUser

client = TestClient(app)

UNVERIFIED = AuthenticatedUser("user-2", "Jane Doe", "jane.doe@example.com", False)


@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("get", "/cv"),
        ("delete", "/cv"),
        ("post", "/analyze"),
        ("get", "/extensions"),
        ("delete", "/extensions/ext-1"),
        ("get", "/job-boards/mine"),
    ],
)
def test_unverified_users_are_blocked(logged_in, method, path):
    app.dependency_overrides[get_current_user] = lambda: UNVERIFIED
    payload = {"job_text": "We are hiring a React developer to build our web app. " * 2}

    response = client.request(method, path, json=payload if method == "post" else None)

    assert response.status_code == 403
