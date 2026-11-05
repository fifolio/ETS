from fastapi import APIRouter

from app.schemas.error_response import ErrorResponse
from app.schemas.onboarding_status import OnboardingStatus
from app.services.cv.get_cv import get_cv
from app.services.onboarding.build_onboarding_status import build_onboarding_status
from app.types.current_user import CurrentUser

router = APIRouter(
    tags=["onboarding"],
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid token."},
        502: {"model": ErrorResponse, "description": "The storage service failed."},
        503: {"model": ErrorResponse, "description": "The service is not configured."},
    },
)


@router.get(
    "/onboarding/status",
    response_model=OnboardingStatus,
    summary="Where the user is in the account setup",
    description="Works before the email is verified, so the setup screen can show the first step.",
)
def onboarding_status(user: CurrentUser) -> OnboardingStatus:
    has_cv = user.email_verified and get_cv(user.id) is not None
    return build_onboarding_status(user, has_cv)
