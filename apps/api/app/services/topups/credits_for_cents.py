from app.constants.topups import TOPUP_CREDITS_PER_STEP, TOPUP_STEP_CENTS


def credits_for_cents(cents: int) -> int:
    """The only place the conversion lives: 2 credits for every $0.25."""
    return cents // TOPUP_STEP_CENTS * TOPUP_CREDITS_PER_STEP
