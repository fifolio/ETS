from app.constants.credits import ROLL_OVER_SUBSCRIPTION_CREDITS


def compute_renewal_delta(
    current: int, allowance: int, roll_over: bool = ROLL_OVER_SUBSCRIPTION_CREDITS
) -> int:
    """The change to apply to the subscription credits at renewal.

    Reset: the new allowance replaces what is left (so the change can be negative).
    Roll over: the allowance is added on top.
    """
    return allowance if roll_over else allowance - current
