from appwrite.query import Query

from app.constants.billing import CREDIT_HISTORY_LIMIT
from app.core.config import settings
from app.schemas.credit_entry_out import CreditEntryOut
from app.schemas.ledger_row import LedgerRow
from app.services.appwrite.get_tables_db import get_tables_db
from app.services.appwrite.read_created_at import read_created_at


def list_credit_history(user_id: str, limit: int = CREDIT_HISTORY_LIMIT) -> list[CreditEntryOut]:
    """The user's latest credit changes, newest first."""
    result = get_tables_db().list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_credit_ledger_table_id,
        queries=[
            Query.equal("userId", user_id),
            Query.order_desc("$createdAt"),
            Query.limit(limit),
        ],
        model_type=LedgerRow,
    )
    return [
        CreditEntryOut(
            amount=row.data.amount,
            kind=row.data.kind,
            reason=row.data.reason,
            created_at=read_created_at(row),
        )
        for row in result.rows
    ]
