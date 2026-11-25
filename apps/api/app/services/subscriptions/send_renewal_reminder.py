from datetime import datetime

from app.services.notifications.send_notification import send_notification
from app.services.subscriptions.update_subscription_row import update_subscription_row
from app.types.subscription_record import SubscriptionRecord


def send_renewal_reminder(record: SubscriptionRecord, now: datetime) -> None:
    kind = "subscription_ending" if record.cancel_at_period_end else "subscription_renewing"
    ends = record.period_end.isoformat() if record.period_end else None
    send_notification(record.user_id, kind, {"plan": record.plan, "period_end": ends})
    update_subscription_row(record.user_id, {"renewalReminderSentAt": now.isoformat()})
