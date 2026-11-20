from contextlib import suppress

from app.constants.credits import CREDIT_COLUMNS
from app.services.credits.delete_ledger_row import delete_ledger_row
from app.services.credits.increment_balance import increment_balance
from app.services.credits.write_ledger import write_ledger


def add_credits(
    user_id: str,
    kind: str,
    amount: int,
    reason: str,
    idempotency_key: str,
    ref_id: str | None = None,
) -> bool:
    """Grant credits once per key. Returns False when this grant was already made."""
    if kind not in CREDIT_COLUMNS:
        raise ValueError(f"Unknown credit kind: {kind}")
    if amount <= 0:
        raise ValueError("Amount must be positive")

    ledger_id = write_ledger(user_id, amount, kind, reason, ref_id, idempotency_key)
    if ledger_id is None:
        return False
    try:
        increment_balance(user_id, kind, amount)
    except Exception:
        # Free the key so a retry (for example Polar sending the webhook again) can succeed.
        with suppress(Exception):
            delete_ledger_row(ledger_id)
        raise
    return True
