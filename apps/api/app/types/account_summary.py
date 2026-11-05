from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AccountSummary:
    id: str
    registered_at: datetime
    email_verified: bool
    labels: list[str]
