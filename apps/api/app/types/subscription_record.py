from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SubscriptionRecord:
    user_id: str  # the row ID is the user ID
    plan: str
    status: str
    membership_id: str | None
    cancel_at_period_end: bool
    period_end: datetime | None
    credits_renewed_at: datetime | None
    reminder_sent_at: datetime | None
