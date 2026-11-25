from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class MembershipNotice:
    provider: str
    membership_id: str
    status: str
    cancel_at_period_end: bool
    period_end: datetime | None
