from app.constants.profile import MAX_YEARS_OF_EXPERIENCE


def is_valid_years(value: object) -> bool:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return False
    return 0 <= value <= MAX_YEARS_OF_EXPERIENCE
