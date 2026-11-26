from appwrite.query import Query

from app.constants.billing import PAYMENT_HISTORY_LIMIT, PAYMENT_HISTORY_SCAN
from app.core.config import settings
from app.schemas.payment_entry_out import PaymentEntryOut
from app.schemas.payment_row import PaymentRow
from app.services.appwrite.get_tables_db import get_tables_db
from app.services.appwrite.read_created_at import read_created_at


def list_payment_history(user_id: str) -> list[PaymentEntryOut]:
    """The user's latest payments, newest first. Abandoned checkouts (pending) are skipped."""
    result = get_tables_db().list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_payments_table_id,
        queries=[
            Query.equal("userId", user_id),
            Query.order_desc("$createdAt"),
            Query.limit(PAYMENT_HISTORY_SCAN),
        ],
        model_type=PaymentRow,
    )
    entries = [
        PaymentEntryOut(
            sku=row.data.sku,
            amount_cents=row.data.amountCents,
            credits=row.data.credits,
            status=row.data.status,
            paid_at=row.data.appliedAt or read_created_at(row),
        )
        for row in result.rows
        if row.data.status != "pending"
    ]
    return entries[:PAYMENT_HISTORY_LIMIT]
