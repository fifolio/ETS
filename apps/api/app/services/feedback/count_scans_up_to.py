from appwrite.query import Query

from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db


def count_scans_up_to(user_id: str, limit: int) -> int:
    """Count the user's scans, looking at no more than `limit` of them."""
    if limit <= 0:
        return 0
    result = get_tables_db().list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_scans_table_id,
        queries=[Query.equal("userId", user_id), Query.limit(limit)],
    )
    return len(result.rows)
