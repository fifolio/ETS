from appwrite.query import Query

from app.core.config import settings
from app.schemas.extension_row import ExtensionRow
from app.services.appwrite.get_tables_db import get_tables_db


def delete_extension(user_id: str, extension_id: str) -> bool:
    """Delete one of the user's installs. Returns False if it isn't theirs or doesn't exist."""
    tables = get_tables_db()
    found = tables.list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_extensions_table_id,
        queries=[
            Query.equal("$id", extension_id),
            Query.equal("userId", user_id),
            Query.limit(1),
        ],
        model_type=ExtensionRow,
    )
    if not found.rows:
        return False
    tables.delete_row(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_extensions_table_id,
        row_id=extension_id,
    )
    return True
