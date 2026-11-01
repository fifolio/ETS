from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db


def delete_cv_row(row_id: str) -> None:
    get_tables_db().delete_row(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_cvs_table_id,
        row_id=row_id,
    )
