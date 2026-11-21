import logging

from app.constants.credits import CREDITS_PER_SCAN, MAX_SPEND_ATTEMPTS
from app.services.credits.apply_spend_steps import apply_spend_steps
from app.services.credits.plan_spend import plan_spend
from app.services.credits.read_credit_balance import get_credit_balance
from app.services.credits.write_ledger import write_ledger

logger = logging.getLogger(__name__)


def reserve_credits(
    user_id: str, amount: int = CREDITS_PER_SCAN, reason: str = "Job scan"
) -> list[tuple[str, int]] | None:
    """Spend credits (promotional first) and return what was taken, or None if not enough.

    Each column is decremented atomically with a minimum of 0, so simultaneous requests can
    never spend the same credit twice. If another request changed the balance in between,
    the balance is read again and we retry. Keep the result: it is what refund_credits needs.
    """
    for _ in range(MAX_SPEND_ATTEMPTS):
        balance = get_credit_balance(user_id)
        steps = plan_spend(balance, amount) if balance is not None else None
        if steps is None:
            return None
        if apply_spend_steps(user_id, steps):
            for kind, taken in steps:
                try:
                    write_ledger(user_id, -taken, kind, reason)
                except Exception:
                    logger.exception("Could not write the credit history")
            return steps
    return None
