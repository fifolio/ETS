from app.constants.billing import HISTORY_PAGE_SIZE
from app.core.config import settings
from app.schemas.credit_entry_out import CreditEntryOut
from app.schemas.credit_history_page import CreditHistoryPage
from app.schemas.ledger_row import LedgerRow
from app.services.appwrite.get_tables_db import get_tables_db
from app.services.appwrite.read_created_at import read_created_at
from app.services.credits.build_credit_history_queries import build_credit_history_queries
from app.services.pagination.build_page_info import build_page_info
from app.types.history_filters import CreditChangeFilter, CreditKindFilter


def list_credit_history(
    user_id: str, page: int, kind: CreditKindFilter, change: CreditChangeFilter
) -> CreditHistoryPage:
    result = get_tables_db().list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_credit_ledger_table_id,
        queries=build_credit_history_queries(user_id, page, kind, change),
        model_type=LedgerRow,
    )
    items = [
        CreditEntryOut(
            amount=row.data.amount,
            kind=row.data.kind,
            reason=row.data.reason,
            created_at=read_created_at(row),
        )
        for row in result.rows
    ]
    info = build_page_info(page, HISTORY_PAGE_SIZE, result.total)
    return CreditHistoryPage(items=items, **info.model_dump())
