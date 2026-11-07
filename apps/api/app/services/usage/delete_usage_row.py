from appwrite.exception import AppwriteException

from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db


def delete_usage_row(user_id: str) -> None:
    """Delete the user's usage totals. A user who never scanned has none, which is fine."""
    try:
        get_tables_db().delete_row(
            database_id=settings.appwrite_database_id,
            table_id=settings.appwrite_usage_table_id,
            row_id=user_id,
        )
    except AppwriteException as exc:
        if exc.code != 404:
            raise
