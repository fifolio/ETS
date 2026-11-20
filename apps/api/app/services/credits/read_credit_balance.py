from appwrite.query import Query

from app.core.config import settings
from app.schemas.credit_balance_row import CreditBalanceRow
from app.services.appwrite.get_tables_db import get_tables_db
from app.types.credit_balance import CreditBalance


def get_credit_balance(user_id: str) -> CreditBalance | None:
    """The user's balances, or None when they have no balance row yet."""
    result = get_tables_db().list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_credit_balances_table_id,
        queries=[Query.equal("$id", user_id), Query.limit(1)],
        model_type=CreditBalanceRow,
    )
    if not result.rows:
        return None
    row = result.rows[0].data
    return CreditBalance(
        subscription=row.subscriptionCredits,
        promotional=row.promotionalCredits,
        purchased=row.purchasedCredits,
    )
