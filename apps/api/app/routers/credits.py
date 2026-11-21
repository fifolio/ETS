from fastapi import APIRouter

from app.schemas.credits_out import CreditsOut
from app.schemas.error_response import ErrorResponse
from app.services.credits.read_user_credits import read_user_credits
from app.types.verified_user import VerifiedUserId

router = APIRouter(
    tags=["credits"],
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid token."},
        403: {"model": ErrorResponse, "description": "The user's email isn't verified yet."},
        502: {"model": ErrorResponse, "description": "The storage service failed."},
    },
)


@router.get(
    "/credits",
    response_model=CreditsOut,
    summary="The logged-in user's credit balance",
    description="Bonus credits are used first, then the monthly allowance, then purchased credits.",
)
def credits(user_id: VerifiedUserId) -> CreditsOut:
    return read_user_credits(user_id)
