import pytest

from app.core.auth import get_current_user
from app.main import app
from app.services.appwrite_client import AuthenticatedUser

TEST_USER = AuthenticatedUser(id="user-1", name="Jane Doe", email="jane.doe@example.com")


@pytest.fixture
def logged_in():
    app.dependency_overrides[get_current_user] = lambda: TEST_USER
    yield TEST_USER
    app.dependency_overrides.clear()
