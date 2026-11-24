from typing import Any

from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db


def update_subscription_row(user_id: str, data: dict[str, Any]) -> None:
    """The subscription row's ID is the user ID."""
    get_tables_db().update_row(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_subscriptions_table_id,
        row_id=user_id,
        data=data,
    )
