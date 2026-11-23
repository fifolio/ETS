from app.constants.credits import ROLL_OVER_SUBSCRIPTION_CREDITS
from app.services.credits.decrement_balance import decrement_balance
from app.services.credits.read_credit_balance import get_credit_balance
from app.services.credits.write_ledger import write_ledger


def expire_monthly_credits(user_id: str, idempotency_key: str) -> None:
    """End of a billing period: whatever is left of the monthly allowance expires, once."""
    if ROLL_OVER_SUBSCRIPTION_CREDITS:
        return
    balance = get_credit_balance(user_id)
    remaining = balance.subscription if balance else 0
    if remaining <= 0:
        return
    reason = "Unused monthly credits expired"
    if write_ledger(user_id, -remaining, "subscription", reason, None, idempotency_key) is None:
        return
    decrement_balance(user_id, "subscription", remaining)  # False if spent meanwhile: harmless
