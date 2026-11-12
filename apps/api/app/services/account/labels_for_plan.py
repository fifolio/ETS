from app.constants.account import PLAN_LABELS, SUBSCRIPTION_PLANS


def labels_for_plan(current_labels: list[str], plan: str) -> list[str]:
    """The user's labels after switching to `plan`: other labels are kept, plan labels replaced."""
    if plan not in SUBSCRIPTION_PLANS:
        raise ValueError(f"Unknown plan: {plan}")
    labels = {label for label in current_labels if label not in PLAN_LABELS}
    if plan in PLAN_LABELS:
        labels.add(plan)
    return sorted(labels)
