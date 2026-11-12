from app.constants.plans import PLANS
from app.schemas.plan_out import PlanOut


def list_public_plans() -> list[PlanOut]:
    return [
        PlanOut(
            id=plan.id,
            name=plan.name,
            max_job_boards=plan.max_job_boards,
            price_usd_per_month=plan.price_usd_per_month,
        )
        for plan in PLANS
    ]
