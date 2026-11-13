from fastapi.testclient import TestClient

from app.dependencies.get_current_user import get_current_user
from app.main import app
from app.types.authenticated_user import AuthenticatedUser
from app.types.job_board import JobBoard
from app.types.user_job_boards import UserJobBoards

client = TestClient(app)

LINKEDIN = JobBoard("linkedin", "LinkedIn", "https://www.linkedin.com/jobs", "explore")
INDEED = JobBoard("indeed", "Indeed", "https://www.indeed.com", "nextmove")


def test_the_list_of_job_boards_is_public_cached_and_shows_each_tier(monkeypatch):
    monkeypatch.setattr(
        "app.routers.job_boards.public.list_active_job_boards", lambda: [LINKEDIN, INDEED]
    )

    response = client.get("/job-boards")

    assert response.status_code == 200
    assert [(board["id"], board["plan"], board["plan_name"]) for board in response.json()] == [
        ("linkedin", "explore", "Explore"),
        ("indeed", "nextmove", "Next Move"),
    ]
    assert "max-age=60" in response.headers["cache-control"]


def test_an_empty_list_when_no_board_is_configured(monkeypatch):
    monkeypatch.setattr("app.routers.job_boards.public.list_active_job_boards", lambda: [])

    assert client.get("/job-boards").json() == []


def test_the_users_boards_come_with_their_plan(monkeypatch, logged_in):
    result = UserJobBoards(boards=[LINKEDIN], plan="explore")
    monkeypatch.setattr("app.routers.job_boards.mine.get_user_job_boards", lambda user: result)

    response = client.get("/job-boards/mine")

    assert response.status_code == 200
    body = response.json()
    assert [board["id"] for board in body["boards"]] == ["linkedin"]
    assert body["plan"] == "explore"


def test_an_unverified_user_cannot_read_their_boards(logged_in):
    unverified = AuthenticatedUser("user-2", "Jane Doe", "jane.doe@example.com", False)
    app.dependency_overrides[get_current_user] = lambda: unverified

    assert client.get("/job-boards/mine").status_code == 403


def test_reading_the_users_boards_needs_a_login():
    assert client.get("/job-boards/mine").status_code == 401
