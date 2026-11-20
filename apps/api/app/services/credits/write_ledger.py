from appwrite.exception import AppwriteException
from appwrite.id import ID

from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db


def write_ledger(
    user_id: str,
    amount: int,
    kind: str,
    reason: str,
    ref_id: str | None = None,
    idempotency_key: str | None = None,
) -> str | None:
    """Add a row to the credit history. Returns its ID, or None when the key was already used."""
    row_id = ID.unique()
    try:
        get_tables_db().create_row(
            database_id=settings.appwrite_database_id,
            table_id=settings.appwrite_credit_ledger_table_id,
            row_id=row_id,
            data={
                "userId": user_id,
                "amount": amount,
                "kind": kind,
                "reason": reason,
                "refId": ref_id,
                "idempotencyKey": idempotency_key,
            },
        )
    except AppwriteException as exc:
        if exc.code == 409:  # the unique index on idempotencyKey
            return None
        raise
    return row_id
