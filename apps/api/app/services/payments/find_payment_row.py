from appwrite.query import Query

from app.core.config import settings
from app.schemas.payment_row import PaymentRow
from app.services.appwrite.get_tables_db import get_tables_db
from app.services.payments.to_payment_record import to_payment_record
from app.types.payment_record import PaymentRecord


def find_payment_row(column: str, value: str) -> PaymentRecord | None:
    """The oldest payment row whose `column` equals `value`."""
    result = get_tables_db().list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_payments_table_id,
        queries=[Query.equal(column, value), Query.order_asc("$createdAt"), Query.limit(1)],
        model_type=PaymentRow,
    )
    if not result.rows:
        return None
    return to_payment_record(result.rows[0].id, result.rows[0].data)
