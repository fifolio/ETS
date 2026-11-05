from datetime import datetime

from app.schemas.cleanup_result import CleanupResult
from app.services.cleanup.delete_account import delete_account
from app.services.cleanup.find_expired_accounts import find_expired_accounts
from app.services.cleanup.iter_accounts import iter_accounts
from app.services.cv.get_cv import get_cv


def run_cleanup(now: datetime, dry_run: bool) -> CleanupResult:
    # Collect first, delete afterwards, so deleting never disturbs the paging.
    accounts = list(iter_accounts())
    expired = find_expired_accounts(accounts, now, lambda user_id: get_cv(user_id) is not None)

    if not dry_run:
        for user_id in expired:
            delete_account(user_id)

    return CleanupResult(
        checked=len(accounts),
        expired=len(expired),
        deleted=0 if dry_run else len(expired),
        dry_run=dry_run,
    )
