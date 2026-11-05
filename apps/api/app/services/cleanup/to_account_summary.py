from datetime import UTC, datetime
from typing import Any

from app.types.account_summary import AccountSummary


def to_account_summary(user: Any) -> AccountSummary:
    registered = datetime.fromisoformat(user.registration)
    if registered.tzinfo is None:
        registered = registered.replace(tzinfo=UTC)
    return AccountSummary(
        id=user.id,
        registered_at=registered,
        email_verified=bool(user.emailverification),
        labels=list(user.labels),
    )
