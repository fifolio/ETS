from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db
from app.types.cv_row_data import CVRowData


def update_cv_row(row_id: str, data: CVRowData) -> None:
    get_tables_db().update_row(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_cvs_table_id,
        row_id=row_id,
        data=data,
    )
