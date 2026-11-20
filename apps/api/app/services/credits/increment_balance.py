from appwrite.exception import AppwriteException

from app.constants.credits import CREDIT_COLUMNS
from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db
from app.services.credits.create_balance_row import create_balance_row


def increment_balance(user_id: str, kind: str, amount: int) -> None:
    """Add credits to one column atomically, creating the user's row on the first grant."""
    tables = get_tables_db()

    def add() -> None:
        tables.increment_row_column(
            database_id=settings.appwrite_database_id,
            table_id=settings.appwrite_credit_balances_table_id,
            row_id=user_id,
            column=CREDIT_COLUMNS[kind],
            value=amount,
        )

    try:
        add()
    except AppwriteException as exc:
        if exc.code != 404:
            raise
        try:
            create_balance_row(user_id, kind, amount)
        except AppwriteException as create_exc:
            if create_exc.code != 409:
                raise
            add()  # another request created the row first
