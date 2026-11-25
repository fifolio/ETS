from datetime import datetime

from app.services.account.set_user_plan import set_user_plan
from app.services.credits.apply_plan_credits import apply_plan_credits
from app.services.notifications.send_notification import send_notification
from app.services.subscriptions.update_subscription_row import update_subscription_row
from app.types.subscription_record import SubscriptionRecord


def end_subscription(record: SubscriptionRecord, now: datetime) -> str:
    """A paid plan ended: back to Explore. The welcome bonus and purchased credits are kept.

    The row is updated last: until then a retry finds the subscription again and repeats
    steps that are safe to repeat.
    """
    if record.plan == "explore":
        return "ignored"
    key = f"end:{record.membership_id or record.user_id}"
    apply_plan_credits(record.user_id, "explore", key)  # the leftover expires, Explore's 15 arrive
    set_user_plan(record.user_id, "explore")
    update_subscription_row(
        record.user_id,
        {
            "plan": "explore",
            "status": "active",
            "providerSubscriptionId": None,
            "cancelAtPeriodEnd": False,
            "currentPeriodEnd": None,
            "renewalReminderSentAt": None,
            "creditsRenewedAt": now.isoformat(),
        },
    )
    send_notification(record.user_id, "subscription_ended", {"plan": record.plan})
    return "ended"
