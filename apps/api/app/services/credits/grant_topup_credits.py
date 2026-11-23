from app.services.credits.add_credits import add_credits
from app.services.topups.credits_for_cents import credits_for_cents


def grant_topup_credits(user_id: str, amount_cents: int, payment_id: str) -> bool:
    """Credits for a paid top-up, once per payment. The plan is never touched."""
    credits = credits_for_cents(amount_cents)
    if credits <= 0:
        raise ValueError("The amount buys no credits")
    return add_credits(user_id, "purchased", credits, "Credit top-up", f"topup:{payment_id}")
