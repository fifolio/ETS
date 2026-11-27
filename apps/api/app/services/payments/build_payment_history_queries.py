from appwrite.query import Query

from app.constants.billing import HISTORY_PAGE_SIZE
from app.constants.plans import PLANS
from app.constants.topups import TOPUP_SKU
from app.types.history_filters import PaymentProductFilter, PaymentStatusFilter

PLAN_SKUS = [f"plan_{plan.id}" for plan in PLANS if plan.price_usd_per_month > 0]


def build_payment_history_queries(
    user_id: str, page: int, status: PaymentStatusFilter, product: PaymentProductFilter
) -> list[str]:
    """This user's payments, newest first, one page. Abandoned checkouts only show on request."""
    queries = [
        Query.equal("userId", user_id),
        Query.order_desc("$createdAt"),
        Query.limit(HISTORY_PAGE_SIZE),
        Query.offset((page - 1) * HISTORY_PAGE_SIZE),
    ]
    if status == "all":
        queries.append(Query.not_equal("status", "pending"))
    else:
        queries.append(Query.equal("status", status))
    if product == "plan":
        queries.append(Query.equal("sku", PLAN_SKUS))
    elif product == "topup":
        queries.append(Query.equal("sku", TOPUP_SKU))
    return queries
