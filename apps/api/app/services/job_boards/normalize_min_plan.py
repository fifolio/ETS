from app.constants.account import SUBSCRIPTION_PLANS


def normalize_min_plan(value: str | None) -> str:
    """The tier written on a board, or the highest tier when it is missing or unknown."""
    return value if value in SUBSCRIPTION_PLANS else SUBSCRIPTION_PLANS[-1]
