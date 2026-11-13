from app.services.job_boards.to_job_board_out import to_job_board_out
from app.types.job_board import JobBoard


def test_a_board_comes_with_its_tier_and_the_tier_name():
    board = JobBoard("indeed", "Indeed", "https://www.indeed.com", "nextmove")

    assert to_job_board_out(board).model_dump() == {
        "id": "indeed",
        "name": "Indeed",
        "url": "https://www.indeed.com",
        "plan": "nextmove",
        "plan_name": "Next Move",
    }
