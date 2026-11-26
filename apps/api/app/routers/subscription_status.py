from fastapi import APIRouter, HTTPException

from app.exceptions.payment_provider_error import PaymentProviderError
from app.exceptions.payments_unavailable_error import PaymentsUnavailableError
from app.exceptions.subscription_action_error import SubscriptionActionError
from app.schemas.error_response import ErrorResponse
from app.schemas.manage_url_out import ManageUrlOut
from app.schemas.subscription_out import SubscriptionOut
from app.services.subscriptions.cancel_user_subscription import cancel_user_subscription
from app.services.subscriptions.get_subscription_status import get_subscription_status
from app.services.subscriptions.get_user_manage_url import get_user_manage_url
from app.types.verified_user import VerifiedUser

router = APIRouter(
    prefix="/subscription",
    tags=["subscription"],
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid token."},
        403: {"model": ErrorResponse, "description": "The user's email isn't verified yet."},
        502: {"model": ErrorResponse, "description": "The payment service failed."},
        503: {"model": ErrorResponse, "description": "Payments are not available."},
    },
)


@router.get("", response_model=SubscriptionOut, summary="The user's plan and renewal state")
def subscription_status(user: VerifiedUser) -> SubscriptionOut:
    return get_subscription_status(user)


@router.post(
    "/cancel",
    response_model=SubscriptionOut,
    summary="Cancel the subscription immediately",
    responses={400: {"model": ErrorResponse, "description": "There is no paid subscription."}},
)
def cancel_subscription(user: VerifiedUser) -> SubscriptionOut:
    try:
        return cancel_user_subscription(user)
    except SubscriptionActionError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
    except PaymentsUnavailableError as exc:
        raise HTTPException(status_code=503, detail="Payments are not available yet.") from exc
    except PaymentProviderError as exc:
        raise HTTPException(
            status_code=502, detail="The payment service failed. Please try again."
        ) from exc


@router.get(
    "/manage-url",
    response_model=ManageUrlOut,
    summary="The provider's billing page for the subscription",
    responses={404: {"model": ErrorResponse, "description": "There is no billing page."}},
)
def manage_url(user: VerifiedUser) -> ManageUrlOut:
    try:
        return ManageUrlOut(url=get_user_manage_url(user))
    except SubscriptionActionError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
    except PaymentsUnavailableError as exc:
        raise HTTPException(status_code=503, detail="Payments are not available yet.") from exc
    except PaymentProviderError as exc:
        raise HTTPException(
            status_code=502, detail="The payment service failed. Please try again."
        ) from exc
