from appwrite.query import Query

from app.constants.billing import HISTORY_PAGE_SIZE
from app.types.history_filters import CreditChangeFilter, CreditKindFilter


def build_credit_history_queries(
    user_id: str, page: int, kind: CreditKindFilter, change: CreditChangeFilter
) -> list[str]:
    """This user's ledger rows, newest first, one page, with the chosen filters."""
    queries = [
        Query.equal("userId", user_id),
        Query.order_desc("$createdAt"),
        Query.limit(HISTORY_PAGE_SIZE),
        Query.offset((page - 1) * HISTORY_PAGE_SIZE),
    ]
    if kind != "all":
        queries.append(Query.equal("kind", kind))
    if change == "added":
        queries.append(Query.greater_than("amount", 0))
    elif change == "used":
        queries.append(Query.less_than("amount", 0))
    return queries
