from collections.abc import Callable
from datetime import datetime, timedelta

from app.constants.account import CV_DONE_LABEL, KEEP_LABEL
from app.core.config import settings
from app.types.account_summary import AccountSummary


def is_setup_expired(account: AccountSummary, now: datetime, has_cv: Callable[[str], bool]) -> bool:
    """True when the account is past the deadline without a verified email and a CV."""
    if KEEP_LABEL in account.labels:
        return False
    if now - account.registered_at < timedelta(hours=settings.setup_deadline_hours):
        return False
    if not account.email_verified:
        return True
    if CV_DONE_LABEL in account.labels:
        return False
    # Accounts from before the label existed: keep them if a CV is stored right now.
    return not has_cv(account.id)
