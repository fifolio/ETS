from datetime import datetime

from app.services.credits.apply_plan_credits import apply_plan_credits
from app.services.subscriptions.update_subscription_row import update_subscription_row
from app.types.subscription_record import SubscriptionRecord


def renew_explore_credits(record: SubscriptionRecord, now: datetime) -> None:
    """Reset Explore's 15 credits once for the current day key."""
    apply_plan_credits(record.user_id, "explore", f"explore:{now.date().isoformat()}")
    update_subscription_row(record.user_id, {"creditsRenewedAt": now.isoformat()})
