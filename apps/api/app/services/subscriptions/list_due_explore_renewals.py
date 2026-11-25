from datetime import datetime, timedelta

from appwrite.query import Query

from app.constants.subscriptions import EXPLORE_RENEWAL_DAYS
from app.services.subscriptions.list_subscription_records import list_subscription_records
from app.types.subscription_record import SubscriptionRecord


def list_due_explore_renewals(now: datetime) -> list[SubscriptionRecord]:
    cutoff = now - timedelta(days=EXPLORE_RENEWAL_DAYS)
    return list_subscription_records(
        [Query.equal("plan", "explore"), Query.less_than("creditsRenewedAt", cutoff.isoformat())]
    )
