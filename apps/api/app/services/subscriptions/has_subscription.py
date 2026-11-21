from appwrite.query import Query

from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db


def has_subscription(user_id: str) -> bool:
    result = get_tables_db().list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_subscriptions_table_id,
        queries=[Query.equal("$id", user_id), Query.limit(1)],
    )
    return bool(result.rows)
