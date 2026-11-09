from app.constants.metrics import STORED_DECIMALS


def minutes_to_cash(minutes: float, hourly_rate_usd: float) -> float:
    return round(hourly_rate_usd / 60 * minutes, STORED_DECIMALS)
