from datetime import datetime
from typing import Any


def read_created_at(row: Any) -> str | None:
    """The row's creation time as ISO text, whichever way the SDK names it."""
    value = getattr(row, "created_at", None) or getattr(row, "createdAt", None)
    if isinstance(value, datetime):
        return value.isoformat()
    return value if isinstance(value, str) else None
