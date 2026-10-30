import pytest

from app.dependencies.get_current_user import get_current_user
from app.main import app
from app.types.authenticated_user import AuthenticatedUser

TEST_USER = AuthenticatedUser(id="user-1", name="Jane Doe", email="jane.doe@example.com")


@pytest.fixture
def logged_in():
    app.dependency_overrides[get_current_user] = lambda: TEST_USER
    yield TEST_USER
    app.dependency_overrides.clear()
