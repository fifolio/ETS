from app.constants.account import DEFAULT_SUBSCRIPTION, SUBSCRIPTION_PLANS


def read_subscription(labels: list[str]) -> str:
    """The highest plan found in the user's labels, or the default plan."""
    for plan in reversed(SUBSCRIPTION_PLANS):
        if plan in labels:
            return plan
    return DEFAULT_SUBSCRIPTION
