from fastapi import APIRouter, Query

from app.schemas.credit_history_page import CreditHistoryPage
from app.schemas.error_response import ErrorResponse
from app.services.credits.list_credit_history import list_credit_history
from app.types.history_filters import CreditChangeFilter, CreditKindFilter
from app.types.verified_user import VerifiedUserId

router = APIRouter(
    tags=["credits"],
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid token."},
        403: {"model": ErrorResponse, "description": "The user's email isn't verified yet."},
    },
)


@router.get(
    "/credits/history",
    response_model=CreditHistoryPage,
    summary="Your credit changes, newest first, 10 per page",
)
def credit_history(
    user_id: VerifiedUserId,
    page: int = Query(1, ge=1, le=1000),
    kind: CreditKindFilter = "all",
    change: CreditChangeFilter = "all",
) -> CreditHistoryPage:
    return list_credit_history(user_id, page, kind, change)
