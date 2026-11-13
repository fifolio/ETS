import pytest

from app.services.job_boards.is_board_in_plan import is_board_in_plan
from app.types.job_board import JobBoard


@pytest.mark.parametrize(
    ("board_plan", "user_plan", "expected"),
    [
        ("explore", "explore", True),
        ("explore", "nextmove", True),
        ("explore", "urgent", True),
        ("nextmove", "explore", False),
        ("nextmove", "nextmove", True),
        ("nextmove", "urgent", True),
        ("urgent", "explore", False),
        ("urgent", "nextmove", False),
        ("urgent", "urgent", True),
        ("platinum", "nextmove", False),
        ("explore", "platinum", True),
    ],
)
def test_a_board_is_included_from_its_tier_upwards(board_plan, user_plan, expected):
    board = JobBoard("b", "Board", "https://b.example/jobs", board_plan)

    assert is_board_in_plan(board, user_plan) is expected
