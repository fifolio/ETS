from datetime import datetime, timedelta

from app.core.config import settings


def is_trial_over(registered_at: datetime | None, now: datetime) -> bool:
    if registered_at is None:
        return False
    return now >= registered_at + timedelta(days=settings.feedback_min_days)
