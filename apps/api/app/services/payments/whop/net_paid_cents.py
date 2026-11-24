from typing import Any

from app.services.payments.whop.money_to_cents import money_to_cents


def net_paid_cents(data: dict[str, Any]) -> int | None:
    """What the buyer paid for the product itself: the total, without tax added on top."""
    total = money_to_cents(data.get("total"))
    if total is None:
        return None
    if data.get("tax_behavior") != "exclusive":
        return total
    return total - (money_to_cents(data.get("tax_amount")) or 0)
