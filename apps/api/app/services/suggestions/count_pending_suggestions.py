from appwrite.query import Query

from app.constants.suggestions import SUGGESTION_STATUS_PENDING
from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db


def count_pending_suggestions(user_id: str, limit: int) -> int:
    """How many of the user's suggestions wait for review, looking at no more than `limit`."""
    result = get_tables_db().list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_suggestions_table_id,
        queries=[
            Query.equal("userId", user_id),
            Query.equal("status", SUGGESTION_STATUS_PENDING),
            Query.limit(limit),
        ],
    )
    return len(result.rows)
