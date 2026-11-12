from app.constants.account import DEFAULT_SUBSCRIPTION, PLAN_LABELS


def read_subscription(labels: list[str]) -> str:
    """The highest plan found in the user's labels, or the default plan."""
    for plan in reversed(PLAN_LABELS):
        if plan in labels:
            return plan
    return DEFAULT_SUBSCRIPTION
