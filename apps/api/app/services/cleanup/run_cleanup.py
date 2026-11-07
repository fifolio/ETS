from datetime import datetime

from app.schemas.cleanup_result import CleanupResult
from app.services.account.delete_user_account import delete_user_account
from app.services.account.delete_user_data import delete_user_data
from app.services.cleanup.apply_to_each import apply_to_each
from app.services.cleanup.find_data_owner_ids import find_data_owner_ids
from app.services.cleanup.find_expired_accounts import find_expired_accounts
from app.services.cleanup.find_orphan_user_ids import find_orphan_user_ids
from app.services.cleanup.iter_accounts import iter_accounts
from app.services.cv.get_cv import get_cv


def run_cleanup(now: datetime, dry_run: bool) -> CleanupResult:
    # Collect first, delete afterwards, so deleting never disturbs the paging.
    accounts = list(iter_accounts())
    expired = find_expired_accounts(accounts, now, lambda user_id: get_cv(user_id) is not None)

    # Data left behind by accounts deleted some other way, for example in the Appwrite console.
    # Never sweep when no accounts were found at all: that would look like everyone left.
    orphans = (
        find_orphan_user_ids({account.id for account in accounts}, find_data_owner_ids())
        if accounts
        else []
    )

    deleted = cleaned = failed = 0
    if not dry_run:
        deleted, failed_accounts = apply_to_each(expired, delete_user_account)
        cleaned, failed_orphans = apply_to_each(orphans, delete_user_data)
        failed = failed_accounts + failed_orphans

    return CleanupResult(
        checked=len(accounts),
        expired=len(expired),
        deleted=deleted,
        orphaned=len(orphans),
        orphans_cleaned=cleaned,
        failed=failed,
        dry_run=dry_run,
    )
