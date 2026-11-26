from fastapi import APIRouter

from app.schemas.error_response import ErrorResponse
from app.schemas.payment_entry_out import PaymentEntryOut
from app.services.payments.list_payment_history import list_payment_history
from app.types.verified_user import VerifiedUserId

router = APIRouter(
    tags=["payments"],
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid token."},
        403: {"model": ErrorResponse, "description": "The user's email isn't verified yet."},
    },
)


@router.get("/payments", response_model=list[PaymentEntryOut], summary="Your latest payments")
def payments(user_id: VerifiedUserId) -> list[PaymentEntryOut]:
    return list_payment_history(user_id)
