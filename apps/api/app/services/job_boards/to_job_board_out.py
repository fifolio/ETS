from app.schemas.job_board_out import JobBoardOut
from app.services.plans.find_plan import find_plan
from app.types.job_board import JobBoard


def to_job_board_out(board: JobBoard) -> JobBoardOut:
    plan = find_plan(board.min_plan)
    return JobBoardOut(
        id=board.id,
        name=board.name,
        url=board.url,
        plan=board.min_plan,
        plan_name=plan.name if plan else board.min_plan,
    )
