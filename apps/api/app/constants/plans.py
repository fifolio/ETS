from app.types.plan_definition import PlanDefinition

PLANS = (
    PlanDefinition(id="explore", name="Explore", max_job_boards=1, price_usd_per_month=0.0),
    PlanDefinition(id="nextmove", name="Next Move", max_job_boards=3, price_usd_per_month=None),
    PlanDefinition(id="urgent", name="Urgent", max_job_boards=None, price_usd_per_month=None),
)
