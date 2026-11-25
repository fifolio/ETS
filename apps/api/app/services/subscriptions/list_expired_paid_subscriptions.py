from datetime import datetime, timedelta

from appwrite.query import Query

from app.constants.subscriptions import PAID_GRACE_DAYS
from app.services.subscriptions.list_subscription_records import list_subscription_records
from app.types.subscription_record import SubscriptionRecord


def list_expired_paid_subscriptions(now: datetime) -> list[SubscriptionRecord]:
    """Safety net: paid plans whose period ended long ago with no renewal event."""
    cutoff = now - timedelta(days=PAID_GRACE_DAYS)
    records = list_subscription_records(
        [Query.equal("status", "active"), Query.less_than("currentPeriodEnd", cutoff.isoformat())]
    )
    return [record for record in records if record.plan != "explore"]
