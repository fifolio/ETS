from typing import Any

from app.services.appwrite.parse_appwrite_datetime import parse_appwrite_datetime
from app.types.account_summary import AccountSummary


def to_account_summary(user: Any) -> AccountSummary:
    return AccountSummary(
        id=user.id,
        registered_at=parse_appwrite_datetime(user.registration),
        email_verified=bool(user.emailverification),
        labels=list(user.labels),
    )
