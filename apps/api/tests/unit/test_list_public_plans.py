from app.services.plans.list_public_plans import list_public_plans
from app.types.job_board import JobBoard

BOARDS = [
    JobBoard("linkedin", "LinkedIn", "https://www.linkedin.com/jobs", "explore"),
    JobBoard("indeed", "Indeed", "https://www.indeed.com", "nextmove"),
    JobBoard("glassdoor", "Glassdoor", "https://www.glassdoor.com/Job", "nextmove"),
    JobBoard("wellfound", "Wellfound", "https://wellfound.com/jobs", "urgent"),
]


def test_lists_the_three_plans_from_lowest_to_highest():
    plans = list_public_plans(BOARDS)

    assert [plan.id for plan in plans] == ["explore", "nextmove", "urgent"]
    assert [plan.name for plan in plans] == ["Explore", "Next Move", "Urgent"]


def test_each_plan_shows_how_many_job_boards_it_includes():
    counts = {plan.id: plan.job_board_count for plan in list_public_plans(BOARDS)}

    assert counts == {"explore": 1, "nextmove": 3, "urgent": 4}
