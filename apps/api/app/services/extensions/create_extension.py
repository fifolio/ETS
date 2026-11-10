from appwrite.id import ID

from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db
from app.types.extension_row_data import ExtensionRowData


def create_extension(data: ExtensionRowData) -> None:
    get_tables_db().create_row(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_extensions_table_id,
        row_id=ID.unique(),
        data=data,
    )
