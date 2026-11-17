from app.constants.metrics import STORED_DECIMALS


def convert_usd(amount_usd: float, rate_from_usd: float) -> float:
    """Multiply USD by the stored rate. That's it."""
    return round(amount_usd * rate_from_usd, STORED_DECIMALS)
