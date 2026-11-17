DEFAULT_CURRENCY = "usd"


def normalize_currency(value: object, available_codes: set[str]) -> str:
    if isinstance(value, str) and value in available_codes:
        return value
    return DEFAULT_CURRENCY
