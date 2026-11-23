import math

from app.constants.topups import TOPUP_MAX_CENTS, TOPUP_MIN_CENTS, TOPUP_STEP_CENTS
from app.exceptions.checkout_refused_error import CheckoutRefusedError


def validate_topup_amount(amount_usd: float | None) -> int:
    """The amount in cents. Raises CheckoutRefusedError unless it is in range and in steps."""
    if amount_usd is None or not math.isfinite(amount_usd):
        raise CheckoutRefusedError("Choose an amount for the top-up.")
    cents = round(amount_usd * 100)
    if abs(amount_usd * 100 - cents) > 1e-6:
        raise CheckoutRefusedError("Amounts can't have fractions of a cent.")
    if cents < TOPUP_MIN_CENTS or cents > TOPUP_MAX_CENTS:
        raise CheckoutRefusedError(
            f"Choose an amount between ${TOPUP_MIN_CENTS / 100:.2f} "
            f"and ${TOPUP_MAX_CENTS / 100:.2f}."
        )
    if cents % TOPUP_STEP_CENTS:
        raise CheckoutRefusedError(f"Amounts go up in steps of ${TOPUP_STEP_CENTS / 100:.2f}.")
    return cents
