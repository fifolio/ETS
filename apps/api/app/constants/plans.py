from app.types.plan_definition import PlanDefinition

# Lowest plan first. Prices are in USD. Top-up rules are in constants/topups.py.
PLANS = (
    PlanDefinition(id="explore", name="Explore", price_usd_per_month=0.0, subscription_credits=15),
    PlanDefinition(
        id="nextmove", name="Next Move", price_usd_per_month=7.0, subscription_credits=150
    ),
    PlanDefinition(id="urgent", name="Urgent", price_usd_per_month=14.0, subscription_credits=300),
)
