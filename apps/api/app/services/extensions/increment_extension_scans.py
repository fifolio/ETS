from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db


def increment_extension_scans(row_id: str) -> None:
    get_tables_db().increment_row_column(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_extensions_table_id,
        row_id=row_id,
        column="scanCount",
        value=1,
    )
