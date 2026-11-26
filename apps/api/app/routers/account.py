from fastapi import APIRouter, HTTPException

from app.schemas.error_response import ErrorResponse
from app.services.account.delete_user_account import delete_user_account
from app.services.subscriptions.get_subscription_status import get_subscription_status
from app.types.current_user import CurrentUser

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
        "Deletes your CV, scans, credits, usage totals, and extensions, then the account itself. "
        "Testimonials and payment records are kept. A paid subscription that is still set to "
        "renew must be cancelled first. This can't be undone."
    ),
    responses={
        409: {"model": ErrorResponse, "description": "A paid subscription is still renewing."}
    },
)
def remove_account(user: CurrentUser) -> None:
    if get_subscription_status(user).can_cancel:
        raise HTTPException(
            status_code=409,
            detail="Cancel your subscription before deleting your account"
            "or it would keep renewing.",
        )
    delete_user_account(user.id)
