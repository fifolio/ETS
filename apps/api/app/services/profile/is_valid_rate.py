from app.constants.profile import MAX_HOURLY_RATE_USD


def is_valid_rate(value: object) -> bool:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return False
    return 0 <= value <= MAX_HOURLY_RATE_USD
