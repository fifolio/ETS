from typing import Annotated

from fastapi import APIRouter, HTTPException, Path

from app.routers.extensions.options import EXTENSIONS_ROUTER_OPTIONS
from app.schemas.error_response import ErrorResponse
from app.services.extensions.delete_extension import delete_extension
from app.types.verified_user import VerifiedUserId

router = APIRouter(**EXTENSIONS_ROUTER_OPTIONS)


@router.delete(
    "/{extension_id}",
    status_code=204,
    summary="Remove an extension install",
    description=(
        "After this, the API refuses analysis requests from that install, so the extension has "
        "to log in again."
    ),
    responses={404: {"model": ErrorResponse, "description": "Extension not found."}},
)
def revoke_extension(
    extension_id: Annotated[str, Path(min_length=1, max_length=64)], user_id: VerifiedUserId
) -> None:
    if not delete_extension(user_id, extension_id):
        raise HTTPException(status_code=404, detail="Extension not found.")
