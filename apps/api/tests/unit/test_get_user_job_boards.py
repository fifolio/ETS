import app.services.job_boards.get_user_job_boards as module
from app.types.authenticated_user import AuthenticatedUser
from app.types.job_board import JobBoard

LINKEDIN = JobBoard("linkedin", "LinkedIn", "https://www.linkedin.com/jobs", "explore")
INDEED = JobBoard("indeed", "Indeed", "https://www.indeed.com", "nextmove")
GLASSDOOR = JobBoard("glassdoor", "Glassdoor", "https://www.glassdoor.com/Job", "nextmove")
WELLFOUND = JobBoard("wellfound", "Wellfound", "https://wellfound.com/jobs", "urgent")
BOARDS = [LINKEDIN, INDEED, GLASSDOOR, WELLFOUND]


def make_user(plan):
    return AuthenticatedUser("user-1", "Jane Doe", "jane.doe@example.com", True, {}, [], plan)


def test_an_explore_user_gets_only_linkedin(monkeypatch):
    monkeypatch.setattr(module, "list_active_job_boards", lambda: BOARDS)

    result = module.get_user_job_boards(make_user("explore"))

    assert [board.id for board in result.boards] == ["linkedin"]
    assert result.plan == "explore"


def test_a_next_move_user_gets_linkedin_indeed_and_glassdoor(monkeypatch):
    monkeypatch.setattr(module, "list_active_job_boards", lambda: BOARDS)

    result = module.get_user_job_boards(make_user("nextmove"))

    assert [board.id for board in result.boards] == ["linkedin", "indeed", "glassdoor"]


def test_an_urgent_user_gets_every_board(monkeypatch):
    monkeypatch.setattr(module, "list_active_job_boards", lambda: BOARDS)

    result = module.get_user_job_boards(make_user("urgent"))

    assert len(result.boards) == 4
