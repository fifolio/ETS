from datetime import datetime

from app.services.payments.end_subscription import end_subscription
from app.services.subscriptions.find_subscription_row import find_subscription_row
from app.services.subscriptions.update_subscription_row import update_subscription_row
from app.types.membership_notice import MembershipNotice

ENDED = ("canceled", "expired")
LIVE = ("trialing", "active", "past_due", "canceling")


def apply_membership_update(notice: MembershipNotice, now: datetime) -> str:
    """Follow a membership of the provider. Only the user's CURRENT membership counts."""
    record = find_subscription_row("providerSubscriptionId", notice.membership_id)
    if record is None:
        return "ignored"  # a replaced membership, or one whose first payment isn't applied yet
    if notice.status in ENDED:
        return end_subscription(record, now)
    if notice.status not in LIVE:
        return "ignored"

    changes: dict[str, object] = {
        "cancelAtPeriodEnd": notice.cancel_at_period_end or notice.status == "canceling"
    }
    if notice.period_end is not None:
        changes["currentPeriodEnd"] = notice.period_end.isoformat()
        if notice.period_end != record.period_end:
            changes["renewalReminderSentAt"] = None  # a new period gets a new reminder
    update_subscription_row(record.user_id, changes)
    return "updated"
