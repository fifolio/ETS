from fastapi import APIRouter, Query

from app.schemas.error_response import ErrorResponse
from app.schemas.payment_history_page import PaymentHistoryPage
from app.services.payments.list_payment_history import list_payment_history
from app.types.history_filters import PaymentProductFilter, PaymentStatusFilter
from app.types.verified_user import VerifiedUserId

router = APIRouter(
    tags=["payments"],
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid token."},
        403: {"model": ErrorResponse, "description": "The user's email isn't verified yet."},
    },
)


@router.get(
    "/payments",
    response_model=PaymentHistoryPage,
    summary="Your payments, newest first, 10 per page",
    description="Abandoned checkouts (pending) are only listed when you filter for them.",
)
def payments(
    user_id: VerifiedUserId,
    page: int = Query(1, ge=1, le=1000),
    status: PaymentStatusFilter = "all",
    product: PaymentProductFilter = "all",
) -> PaymentHistoryPage:
    return list_payment_history(user_id, page, status, product)
