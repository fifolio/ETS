from app.constants.credits import SPEND_ORDER
from app.types.credit_balance import CreditBalance


def plan_spend(balance: CreditBalance, amount: int) -> list[tuple[str, int]] | None:
    """How to pay `amount` credits: promotional first, then subscription, then purchased.

    Returns None when the balance isn't enough.
    """
    if amount < 0:
        raise ValueError("Amount can't be negative")
    if balance.total < amount:
        return None
    steps: list[tuple[str, int]] = []
    remaining = amount
    for kind in SPEND_ORDER:
        take = min(getattr(balance, kind), remaining)
        if take > 0:
            steps.append((kind, take))
            remaining -= take
    return steps
