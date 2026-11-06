from appwrite.query import Query

from app.core.config import settings
from app.schemas.usage_row import UsageRow
from app.services.appwrite.get_tables_db import get_tables_db
from app.types.usage_stats import UsageStats


def get_usage_stats(user_id: str) -> UsageStats:
    """The user's running totals. A user who never scanned has zeros."""
    result = get_tables_db().list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_usage_table_id,
        queries=[Query.equal("$id", user_id), Query.limit(1)],
        model_type=UsageRow,
    )
    if not result.rows:
        return UsageStats(scans=0, words=0)
    row = result.rows[0].data
    return UsageStats(scans=row.scanCount, words=row.wordsTotal)
