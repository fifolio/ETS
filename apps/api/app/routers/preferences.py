from fastapi import APIRouter

from app.schemas.error_response import ErrorResponse
from app.schemas.preferences_out import PreferencesOut
from app.services.preferences.build_preferences import build_preferences
from app.types.verified_user import VerifiedUser

router = APIRouter(
    tags=["preferences"],
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid token."},
        403: {"model": ErrorResponse, "description": "The user's email isn't verified yet."},
    },
)


@router.get(
    "/preferences",
    response_model=PreferencesOut,
    summary="The logged-in user's theme and language, ready to use",
    description=(
        "For the extension. Unknown values are replaced by the defaults, and a language that "
        "isn't translated yet is reported as English in effective_language."
    ),
)
def read_preferences(user: VerifiedUser) -> PreferencesOut:
    return build_preferences(user.prefs)
