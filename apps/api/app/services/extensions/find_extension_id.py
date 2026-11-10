from appwrite.query import Query

from app.core.config import settings
from app.schemas.extension_row import ExtensionRow
from app.services.appwrite.get_tables_db import get_tables_db


def find_extension_id(user_id: str, install_id: str) -> str | None:
    """The row ID of this user's install, or None if it isn't registered."""
    result = get_tables_db().list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_extensions_table_id,
        queries=[
            Query.equal("userId", user_id),
            Query.equal("installId", install_id),
            Query.limit(1),
        ],
        model_type=ExtensionRow,
    )
    return result.rows[0].id if result.rows else None
