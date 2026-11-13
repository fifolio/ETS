from app.constants.account import SUBSCRIPTION_PLANS
from app.services.job_boards.normalize_min_plan import normalize_min_plan
from app.types.job_board import JobBoard


def is_board_in_plan(board: JobBoard, plan_id: str) -> bool:
    """True when the plan is at or above the plan the board belongs to."""
    plan_rank = SUBSCRIPTION_PLANS.index(plan_id) if plan_id in SUBSCRIPTION_PLANS else 0
    board_rank = SUBSCRIPTION_PLANS.index(normalize_min_plan(board.min_plan))
    return plan_rank >= board_rank
