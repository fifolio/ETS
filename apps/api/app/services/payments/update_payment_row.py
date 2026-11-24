from typing import Any

from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db


def update_payment_row(row_id: str, data: dict[str, Any]) -> None:
    get_tables_db().update_row(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_payments_table_id,
        row_id=row_id,
        data=data,
    )
