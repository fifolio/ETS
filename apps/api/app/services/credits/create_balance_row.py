from app.constants.credits import CREDIT_COLUMNS
from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db


def create_balance_row(user_id: str, kind: str, amount: int) -> None:
    """The row ID is the user ID. The other columns start at 0 (their default)."""
    get_tables_db().create_row(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_credit_balances_table_id,
        row_id=user_id,
        data={CREDIT_COLUMNS[kind]: amount},
    )
