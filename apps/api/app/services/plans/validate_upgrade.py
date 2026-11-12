from app.constants.account import DEFAULT_SUBSCRIPTION, SUBSCRIPTION_PLANS


def validate_upgrade(current: str, target: str) -> str | None:
    """A message for the first problem with moving from `current` to `target`, or None."""
    if target not in SUBSCRIPTION_PLANS:
        return "Unknown plan."
    if target == DEFAULT_SUBSCRIPTION:
        return "Explore is the free plan."
    current_rank = SUBSCRIPTION_PLANS.index(current) if current in SUBSCRIPTION_PLANS else 0
    target_rank = SUBSCRIPTION_PLANS.index(target)
    if target_rank == current_rank:
        return "You are already on this plan."
    if target_rank < current_rank:
        return "Choose a plan above your current one."
    return None
