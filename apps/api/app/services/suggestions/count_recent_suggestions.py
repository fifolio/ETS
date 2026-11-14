from datetime import datetime, timedelta

from appwrite.query import Query

from app.constants.suggestions import SUGGESTION_WINDOW_HOURS
from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db


def count_recent_suggestions(user_id: str, now: datetime, limit: int) -> int:
    """How many suggestions the user sent in the last day, looking at no more than `limit`."""
    since = now - timedelta(hours=SUGGESTION_WINDOW_HOURS)
    result = get_tables_db().list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_suggestions_table_id,
        queries=[
            Query.equal("userId", user_id),
            Query.greater_than_equal("$createdAt", since.isoformat()),
            Query.limit(limit),
        ],
    )
    return len(result.rows)
