from app.constants.topups import (
    TOPUP_CREDITS_PER_STEP,
    TOPUP_MAX_CENTS,
    TOPUP_MIN_CENTS,
    TOPUP_STEP_CENTS,
)
from app.schemas.topup_config_out import TopupConfigOut


def get_topup_config() -> TopupConfigOut:
    return TopupConfigOut(
        min_usd=TOPUP_MIN_CENTS / 100,
        max_usd=TOPUP_MAX_CENTS / 100,
        step_usd=TOPUP_STEP_CENTS / 100,
        credits_per_step=TOPUP_CREDITS_PER_STEP,
        credits_per_usd=(100 // TOPUP_STEP_CENTS) * TOPUP_CREDITS_PER_STEP,
    )
