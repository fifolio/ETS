from app.services.job_boards.select_boards_for_plan import select_boards_for_plan
from app.types.job_board import JobBoard

LINKEDIN = JobBoard("linkedin", "LinkedIn", "https://www.linkedin.com/jobs", "explore")
INDEED = JobBoard("indeed", "Indeed", "https://www.indeed.com", "nextmove")
GLASSDOOR = JobBoard("glassdoor", "Glassdoor", "https://www.glassdoor.com/Job", "nextmove")
WELLFOUND = JobBoard("wellfound", "Wellfound", "https://wellfound.com/jobs", "urgent")
BOARDS = [LINKEDIN, INDEED, GLASSDOOR, WELLFOUND]


def ids(boards):
    return [board.id for board in boards]


def test_explore_gets_only_linkedin():
    assert ids(select_boards_for_plan(BOARDS, "explore")) == ["linkedin"]


def test_next_move_gets_linkedin_indeed_and_glassdoor():
    assert ids(select_boards_for_plan(BOARDS, "nextmove")) == ["linkedin", "indeed", "glassdoor"]


def test_urgent_gets_every_board():
    assert ids(select_boards_for_plan(BOARDS, "urgent")) == [
        "linkedin",
        "indeed",
        "glassdoor",
        "wellfound",
    ]


def test_an_unknown_plan_is_treated_as_explore():
    assert ids(select_boards_for_plan(BOARDS, "platinum")) == ["linkedin"]
