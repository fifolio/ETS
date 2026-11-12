from app.constants.plans import PLANS
from app.types.plan_definition import PlanDefinition


def find_plan(plan_id: str) -> PlanDefinition | None:
    return next((plan for plan in PLANS if plan.id == plan_id), None)
