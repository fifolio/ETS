import app.services.job_boards.is_job_url_allowed as module
from app.types.authenticated_user import AuthenticatedUser
from app.types.job_board import JobBoard
from app.types.user_job_boards import UserJobBoards

USER = AuthenticatedUser("user-1", "Jane Doe", "jane.doe@example.com", True)
LINKEDIN = JobBoard("linkedin", "LinkedIn", "https://www.linkedin.com/jobs", "explore")
INDEED = JobBoard("indeed", "Indeed", "https://www.indeed.com", "nextmove")


def install(monkeypatch, boards):
    result = UserJobBoards(boards=boards, plan="nextmove")
    monkeypatch.setattr(module, "get_user_job_boards", lambda user: result)


def test_a_page_under_an_active_board_is_allowed(monkeypatch):
    install(monkeypatch, [LINKEDIN])

    assert module.is_job_url_allowed(USER, "https://www.linkedin.com/jobs/view/1") is True


def test_a_page_outside_every_active_board_is_not_allowed(monkeypatch):
    install(monkeypatch, [LINKEDIN])

    assert module.is_job_url_allowed(USER, "https://www.indeed.com/viewjob?jk=1") is False


def test_any_of_several_boards_can_match(monkeypatch):
    install(monkeypatch, [LINKEDIN, INDEED])

    assert module.is_job_url_allowed(USER, "https://www.indeed.com/viewjob?jk=1") is True


def test_nothing_is_allowed_when_there_are_no_boards(monkeypatch):
    install(monkeypatch, [])

    assert module.is_job_url_allowed(USER, "https://www.linkedin.com/jobs/view/1") is False
