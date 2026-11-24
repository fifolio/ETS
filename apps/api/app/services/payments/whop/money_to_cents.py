from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Any


def money_to_cents(value: Any) -> int | None:
    """Whop writes money as {"amount": "5.25", ...} in dollars. Returns cents, or None."""
    if not isinstance(value, dict):
        return None
    try:
        return int((Decimal(str(value["amount"])) * 100).to_integral_value(ROUND_HALF_UP))
    except (KeyError, InvalidOperation):
        return None
