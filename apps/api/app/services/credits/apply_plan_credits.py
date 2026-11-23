from app.services.credits.add_credits import add_credits
from app.services.credits.expire_monthly_credits import expire_monthly_credits
from app.services.plans.find_plan import find_plan


def apply_plan_credits(user_id: str, plan_id: str, period_key: str) -> bool:
    """Give the plan's monthly allowance for one billing period, replacing the leftover.

    Used for activation, renewal, and upgrades. Once per period (False when it was already
    applied), and it never grants the welcome bonus.
    """
    plan = find_plan(plan_id)
    if plan is None:
        raise ValueError(f"Unknown plan: {plan_id}")
    base = f"plan-credits:{user_id}:{plan.id}:{period_key}"
    expire_monthly_credits(user_id, f"{base}:expire")
    return add_credits(
        user_id,
        "subscription",
        plan.subscription_credits,
        f"{plan.name} monthly credits",
        f"{base}:grant",
    )
