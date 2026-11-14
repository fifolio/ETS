from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException

from app.exceptions.suggestion_rejected_error import SuggestionRejectedError
from app.schemas.error_response import ErrorResponse
from app.schemas.job_board_suggestion_request import JobBoardSuggestionRequest
from app.schemas.suggestion_receipt import SuggestionReceipt
from app.services.suggestions.submit_suggestion import submit_suggestion
from app.types.verified_user import VerifiedUser

router = APIRouter(
    prefix="/job-board-suggestions",
    tags=["job-boards"],
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid token."},
        403: {"model": ErrorResponse, "description": "The user's email isn't verified yet."},
        502: {"model": ErrorResponse, "description": "The storage service failed."},
    },
)


@router.post(
    "",
    response_model=SuggestionReceipt,
    status_code=201,
    summary="Suggest a new job board",
    description=(
        "Stored as pending for the admin to review. Refused when the board is already "
        "supported, was already suggested by this user, or the user reached the daily limit."
    ),
    responses={
        409: {"model": ErrorResponse, "description": "Already supported or already suggested."},
        422: {"model": ErrorResponse, "description": "The suggestion is not valid."},
        429: {"model": ErrorResponse, "description": "Too many suggestions."},
    },
)
def suggest_job_board(payload: JobBoardSuggestionRequest, user: VerifiedUser) -> SuggestionReceipt:
    try:
        remaining = submit_suggestion(user.id, payload, datetime.now(UTC))
    except SuggestionRejectedError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
    return SuggestionReceipt(status="pending", remaining_today=remaining)
