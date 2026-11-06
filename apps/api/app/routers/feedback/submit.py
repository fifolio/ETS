from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.exceptions.feedback_already_submitted_error import FeedbackAlreadySubmittedError
from app.exceptions.feedback_not_available_error import FeedbackNotAvailableError
from app.routers.feedback.options import FEEDBACK_ROUTER_OPTIONS
from app.schemas.error_response import ErrorResponse
from app.schemas.feedback_receipt import FeedbackReceipt
from app.schemas.feedback_request import FeedbackRequest
from app.services.feedback.submit_feedback import submit_feedback
from app.types.verified_user import VerifiedUser

router = APIRouter(**FEEDBACK_ROUTER_OPTIONS)


@router.post(
    "",
    response_model=FeedbackReceipt,
    status_code=201,
    summary="Send a testimonial and private suggestions",
    description="Stored as pending. An admin approves public testimonials in the Appwrite console.",
    responses={409: {"model": ErrorResponse, "description": "Feedback was already sent."}},
)
def send_feedback(payload: FeedbackRequest, user: VerifiedUser) -> FeedbackReceipt:
    try:
        submit_feedback(user, payload, datetime.now(UTC))
    except FeedbackAlreadySubmittedError as exc:
        raise HTTPException(status_code=409, detail="You already sent your feedback.") from exc
    except FeedbackNotAvailableError as exc:
        raise HTTPException(
            status_code=403,
            detail=(
                f"Feedback opens after {settings.feedback_min_days} days "
                f"and {settings.feedback_min_scans} scans."
            ),
        ) from exc
    return FeedbackReceipt(status="pending")
