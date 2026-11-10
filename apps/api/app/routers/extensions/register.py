from fastapi import APIRouter, Response

from app.schemas.error_response import ErrorResponse
from app.schemas.extension_receipt import ExtensionReceipt
from app.schemas.extension_registration import ExtensionRegistration
from app.services.extensions.register_extension import register_extension
from app.types.verified_user import VerifiedUser

router = APIRouter(
    prefix="/extensions",
    tags=["extensions"],
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid token."},
        403: {"model": ErrorResponse, "description": "The user's email isn't verified yet."},
        502: {"model": ErrorResponse, "description": "The storage service failed."},
        503: {"model": ErrorResponse, "description": "The service is not configured."},
    },
)


@router.post(
    "",
    response_model=ExtensionReceipt,
    status_code=201,
    summary="Register a browser extension install",
    description=(
        "Called by the extension after the user signs in. Registering links this install to the "
        "account and completes the setup. Calling it again for the same install refreshes it "
        "(status 200). Self-reported: it is not proof that the real extension sent it."
    ),
)
def register(
    registration: ExtensionRegistration, user: VerifiedUser, response: Response
) -> ExtensionReceipt:
    created = register_extension(user.id, registration)
    response.status_code = 201 if created else 200
    return ExtensionReceipt(created=created)
