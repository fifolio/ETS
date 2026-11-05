from collections.abc import Callable, Iterable
from datetime import datetime

from app.services.cleanup.is_setup_expired import is_setup_expired
from app.types.account_summary import AccountSummary


def find_expired_accounts(
    accounts: Iterable[AccountSummary], now: datetime, has_cv: Callable[[str], bool]
) -> list[str]:
    return [account.id for account in accounts if is_setup_expired(account, now, has_cv)]
