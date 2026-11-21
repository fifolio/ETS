from appwrite.exception import AppwriteException

from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db


def delete_row_by_id(table_id: str, row_id: str) -> None:
    """Delete a row by its ID. A row that doesn't exist is fine."""
    try:
        get_tables_db().delete_row(
            database_id=settings.appwrite_database_id, table_id=table_id, row_id=row_id
        )
    except AppwriteException as exc:
        if exc.code != 404:
            raise
