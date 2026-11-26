from fastapi import APIRouter

from app.schemas.credit_entry_out import CreditEntryOut
from app.schemas.error_response import ErrorResponse
from app.services.credits.list_credit_history import list_credit_history
from app.types.verified_user import VerifiedUserId

router = APIRouter(
    tags=["credits"],
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid token."},
        403: {"model": ErrorResponse, "description": "The user's email isn't verified yet."},
    },
)


@router.get(
    "/credits/history", response_model=list[CreditEntryOut], summary="Your latest credit changes"
)
def credit_history(user_id: VerifiedUserId) -> list[CreditEntryOut]:
    return list_credit_history(user_id)
