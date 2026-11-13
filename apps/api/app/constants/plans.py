from app.types.plan_definition import PlanDefinition

PLANS = (
    PlanDefinition(id="explore", name="Explore", price_usd_per_month=0.0),
    PlanDefinition(id="nextmove", name="Next Move", price_usd_per_month=None),
    PlanDefinition(id="urgent", name="Urgent", price_usd_per_month=None),
)
