import pytest

from app.core.auth import get_current_user_id
from app.main import app


@pytest.fixture
def logged_in():
    app.dependency_overrides[get_current_user_id] = lambda: "user-1"
    yield "user-1"
    app.dependency_overrides.clear()
