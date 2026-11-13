from app.services.job_boards.is_board_in_plan import is_board_in_plan
from app.types.job_board import JobBoard


def select_boards_for_plan(boards: list[JobBoard], plan_id: str) -> list[JobBoard]:
    return [board for board in boards if is_board_in_plan(board, plan_id)]
