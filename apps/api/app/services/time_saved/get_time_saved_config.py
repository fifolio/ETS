from app.constants.credits import CREDITS_PER_SCAN
from app.constants.time_saved import MINUTES_SAVED_PER_SCAN
from app.schemas.time_saved_config_out import TimeSavedConfigOut


def get_time_saved_config() -> TimeSavedConfigOut:
    return TimeSavedConfigOut(
        minutes_per_scan=MINUTES_SAVED_PER_SCAN, credits_per_scan=CREDITS_PER_SCAN
    )
