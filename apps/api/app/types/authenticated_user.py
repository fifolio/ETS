from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.constants.account import DEFAULT_SUBSCRIPTION


@dataclass(frozen=True)
class AuthenticatedUser:
    id: str
    name: str
    email: str
    email_verified: bool = False
    prefs: dict[str, Any] = field(default_factory=dict)
    labels: list[str] = field(default_factory=list)
    subscription: str = DEFAULT_SUBSCRIPTION
    registered_at: datetime | None = None
