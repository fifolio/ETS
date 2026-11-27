from app.constants.billing import HISTORY_PAGE_SIZE
from app.core.config import settings
from app.schemas.payment_entry_out import PaymentEntryOut
from app.schemas.payment_history_page import PaymentHistoryPage
from app.schemas.payment_row import PaymentRow
from app.services.appwrite.get_tables_db import get_tables_db
from app.services.appwrite.read_created_at import read_created_at
from app.services.pagination.build_page_info import build_page_info
from app.services.payments.build_payment_history_queries import build_payment_history_queries
from app.types.history_filters import PaymentProductFilter, PaymentStatusFilter


def list_payment_history(
    user_id: str, page: int, status: PaymentStatusFilter, product: PaymentProductFilter
) -> PaymentHistoryPage:
    result = get_tables_db().list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_payments_table_id,
        queries=build_payment_history_queries(user_id, page, status, product),
        model_type=PaymentRow,
    )
    items = [
        PaymentEntryOut(
            sku=row.data.sku,
            amount_cents=row.data.amountCents,
            credits=row.data.credits,
            status=row.data.status,
            paid_at=row.data.appliedAt or read_created_at(row),
        )
        for row in result.rows
    ]
    info = build_page_info(page, HISTORY_PAGE_SIZE, result.total)
    return PaymentHistoryPage(items=items, **info.model_dump())
