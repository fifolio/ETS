from datetime import datetime, timedelta

from appwrite.query import Query

from app.constants.subscriptions import REMINDER_LEAD_HOURS
from app.services.subscriptions.list_subscription_records import list_subscription_records
from app.types.subscription_record import SubscriptionRecord


def list_renewal_reminders(now: datetime) -> list[SubscriptionRecord]:
    """Paid plans whose period ends within the lead time and that weren't reminded yet."""
    soon = now + timedelta(hours=REMINDER_LEAD_HOURS)
    records = list_subscription_records(
        [
            Query.equal("status", "active"),
            Query.greater_than("currentPeriodEnd", now.isoformat()),
            Query.less_than("currentPeriodEnd", soon.isoformat()),
        ]
    )
    return [r for r in records if r.plan != "explore" and r.reminder_sent_at is None]
