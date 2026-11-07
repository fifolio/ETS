from appwrite.query import Query

from app.constants.deletion import MAX_DELETE_ROUNDS
from app.core.config import settings
from app.exceptions.data_deletion_error import DataDeletionError
from app.services.appwrite.get_tables_db import get_tables_db


def delete_user_scans(user_id: str) -> None:
    """Delete every scan of the user, repeating until none are left."""
    tables = get_tables_db()
    by_user = Query.equal("userId", user_id)
    for _ in range(MAX_DELETE_ROUNDS):
        tables.delete_rows(
            database_id=settings.appwrite_database_id,
            table_id=settings.appwrite_scans_table_id,
            queries=[by_user],
        )
        remaining = tables.list_rows(
            database_id=settings.appwrite_database_id,
            table_id=settings.appwrite_scans_table_id,
            queries=[by_user, Query.limit(1)],
        )
        if not remaining.rows:
            return
    raise DataDeletionError(f"Could not delete all scans of user {user_id}")
