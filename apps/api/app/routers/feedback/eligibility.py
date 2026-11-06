from datetime import UTC, datetime

from fastapi import APIRouter

from app.routers.feedback.options import FEEDBACK_ROUTER_OPTIONS
from app.schemas.feedback_eligibility import FeedbackEligibility
from app.services.feedback.get_feedback_eligibility import get_feedback_eligibility
from app.types.verified_user import VerifiedUser

router = APIRouter(**FEEDBACK_ROUTER_OPTIONS)


@router.get(
    "/eligibility",
    response_model=FeedbackEligibility,
    summary="Should the feedback form be shown to this user?",
)
def feedback_eligibility(user: VerifiedUser) -> FeedbackEligibility:
    return get_feedback_eligibility(user, datetime.now(UTC))
