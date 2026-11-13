from app.constants.plans import PLANS
from app.schemas.plan_out import PlanOut
from app.services.job_boards.select_boards_for_plan import select_boards_for_plan
from app.types.job_board import JobBoard


def list_public_plans(boards: list[JobBoard]) -> list[PlanOut]:
    return [
        PlanOut(
            id=plan.id,
            name=plan.name,
            job_board_count=len(select_boards_for_plan(boards, plan.id)),
            price_usd_per_month=plan.price_usd_per_month,
        )
        for plan in PLANS
    ]
