from app.types.plan_definition import PlanDefinition

# Lowest plan first. Prices are in USD.
PLANS = (
    PlanDefinition(
        id="explore",
        name="Explore",
        price_usd_per_month=0.0,
        subscription_credits=15,
        promotional_credits=0,
        topup_price_usd=3.0,
    ),
    PlanDefinition(
        id="nextmove",
        name="Next Move",
        price_usd_per_month=7.0,
        subscription_credits=150,
        promotional_credits=25,
        topup_price_usd=2.0,
    ),
    PlanDefinition(
        id="urgent",
        name="Urgent",
        price_usd_per_month=14.0,
        subscription_credits=300,
        promotional_credits=50,
        topup_price_usd=1.0,
    ),
)
