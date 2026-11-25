from appwrite.query import Query

from app.core.config import settings
from app.schemas.subscription_row import SubscriptionRow
from app.services.appwrite.get_tables_db import get_tables_db
from app.services.subscriptions.to_subscription_record import to_subscription_record
from app.types.subscription_record import SubscriptionRecord


def find_subscription_row(column: str, value: str) -> SubscriptionRecord | None:
    """The subscription whose `column` equals `value` ("$id" is the user ID)."""
    result = get_tables_db().list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_subscriptions_table_id,
        queries=[Query.equal(column, value), Query.limit(1)],
        model_type=SubscriptionRow,
    )
    if not result.rows:
        return None
    return to_subscription_record(result.rows[0].id, result.rows[0].data)
