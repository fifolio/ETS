from appwrite.exception import AppwriteException

from app.constants.credits import CREDIT_COLUMNS
from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db


def decrement_balance(user_id: str, kind: str, amount: int) -> bool:
    """Take credits from one column. False when it doesn't have enough: it never goes below 0."""
    try:
        get_tables_db().decrement_row_column(
            database_id=settings.appwrite_database_id,
            table_id=settings.appwrite_credit_balances_table_id,
            row_id=user_id,
            column=CREDIT_COLUMNS[kind],
            value=amount,
            min=0,
        )
    except AppwriteException as exc:
        if exc.code in (400, 409):  # the minimum was refused, or a concurrent change
            return False
        raise
    return True
