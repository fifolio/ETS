from app.services.credits.decrement_balance import decrement_balance
from app.services.credits.read_credit_balance import get_credit_balance
from app.services.credits.write_ledger import write_ledger


def revoke_credits(user_id: str, kind: str, amount: int, reason: str, idempotency_key: str) -> int:
    """Take back up to `amount` credits of one kind, once per key. Returns how many were taken.

    Credits that were already spent can't be taken back: the history says how many.
    """
    balance = get_credit_balance(user_id)
    available = getattr(balance, kind) if balance else 0
    taken = min(amount, available)
    note = reason if taken == amount else f"{reason} ({amount - taken} already used)"
    if write_ledger(user_id, -taken, kind, note, None, idempotency_key) is None:
        return 0  # this refund was already handled
    if taken > 0:
        decrement_balance(user_id, kind, taken)  # False if spent meanwhile: harmless
    return taken
