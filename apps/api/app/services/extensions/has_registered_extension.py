from appwrite.query import Query

from app.core.config import settings
from app.schemas.extension_row import ExtensionRow
from app.services.appwrite.get_tables_db import get_tables_db


def has_registered_extension(user_id: str) -> bool:
    result = get_tables_db().list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_extensions_table_id,
        queries=[Query.equal("userId", user_id), Query.limit(1)],
        model_type=ExtensionRow,
    )
    return bool(result.rows)
