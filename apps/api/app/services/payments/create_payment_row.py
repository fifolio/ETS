from appwrite.id import ID

from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db
from app.types.payment_row_data import PaymentRowData


def create_payment_row(data: PaymentRowData) -> None:
    get_tables_db().create_row(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_payments_table_id,
        row_id=ID.unique(),
        data=data,
    )
