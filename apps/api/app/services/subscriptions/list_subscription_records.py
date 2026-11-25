from app.core.config import settings
from app.schemas.subscription_row import SubscriptionRow
from app.services.appwrite.iter_table_rows import iter_table_rows
from app.services.subscriptions.to_subscription_record import to_subscription_record
from app.types.subscription_record import SubscriptionRecord


def list_subscription_records(queries: list[str]) -> list[SubscriptionRecord]:
    rows = iter_table_rows(settings.appwrite_subscriptions_table_id, SubscriptionRow, queries)
    return [to_subscription_record(row.id, row.data) for row in rows]
