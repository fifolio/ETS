from datetime import datetime

from appwrite.exception import AppwriteException

from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db


def create_subscription_row(user_id: str, plan: str, now: datetime) -> None:
    """The row ID is the user ID. An existing row is left as it is."""
    try:
        get_tables_db().create_row(
            database_id=settings.appwrite_database_id,
            table_id=settings.appwrite_subscriptions_table_id,
            row_id=user_id,
            data={
                "userId": user_id,
                "plan": plan,
                "status": "active",
                "startedAt": now.isoformat(),
                "creditsRenewedAt": now.isoformat(),
            },
        )
    except AppwriteException as exc:
        if exc.code != 409:
            raise
