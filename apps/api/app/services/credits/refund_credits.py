import logging

from app.services.credits.increment_balance import increment_balance
from app.services.credits.write_ledger import write_ledger

logger = logging.getLogger(__name__)


def refund_credits(
    user_id: str, steps: list[tuple[str, int]], reason: str = "Refund: the scan failed"
) -> None:
    """Give back credits that were reserved for something that then failed. Never raises."""
    for kind, amount in steps:
        try:
            increment_balance(user_id, kind, amount)
        except Exception:
            logger.exception("Could not refund %s credits to user %s", kind, user_id)
            continue
        try:
            write_ledger(user_id, amount, kind, reason)
        except Exception:
            logger.exception("Could not write the refund to the credit history")
