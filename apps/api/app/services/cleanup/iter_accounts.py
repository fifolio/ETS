from collections.abc import Iterator

from appwrite.query import Query

from app.constants.paging import PAGE_SIZE
from app.services.appwrite.get_users import get_users
from app.services.cleanup.to_account_summary import to_account_summary
from app.types.account_summary import AccountSummary


def iter_accounts() -> Iterator[AccountSummary]:
    """Walk through every user, one page at a time. Read-only."""
    users = get_users()
    last_id = None
    while True:
        queries = [Query.limit(PAGE_SIZE)]
        if last_id:
            queries.append(Query.cursor_after(last_id))
        page = users.list(queries=queries).users
        for user in page:
            yield to_account_summary(user)
        if len(page) < PAGE_SIZE:
            return
        last_id = page[-1].id
