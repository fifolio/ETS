from fastapi import APIRouter

from app.schemas.error_response import ErrorResponse
from app.services.account.delete_user_account import delete_user_account
from app.types.current_user import CurrentUserId

router = APIRouter(
    tags=["account"],
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid token."},
        502: {"model": ErrorResponse, "description": "The storage service failed."},
        503: {"model": ErrorResponse, "description": "The service is not configured."},
    },
)


@router.delete(
    "/account",
    status_code=204,
    summary="Delete your account and all your data",
    description=(
        "Deletes your CV, scans, and usage totals, then the account itself. "
        "Testimonials you already sent are kept. This can't be undone."
    ),
)
def remove_account(user_id: CurrentUserId) -> None:
    delete_user_account(user_id)
