from fastapi import APIRouter, HTTPException

from app.exceptions.payments_unavailable_error import PaymentsUnavailableError
from app.schemas.checkout_request import CheckoutRequest
from app.schemas.checkout_response import CheckoutResponse
from app.schemas.error_response import ErrorResponse
from app.services.payments.get_payment_provider import get_payment_provider
from app.services.plans.find_plan import find_plan
from app.services.plans.validate_upgrade import validate_upgrade
from app.types.verified_user import VerifiedUser

router = APIRouter(
    prefix="/subscription",
    tags=["subscription"],
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid token."},
        403: {"model": ErrorResponse, "description": "The user's email isn't verified yet."},
        503: {"model": ErrorResponse, "description": "Payments are not available."},
    },
)


@router.post(
    "/checkout",
    response_model=CheckoutResponse,
    summary="Start paying for a plan upgrade",
    description="Returns the address of the payment page. \
        The plan changes after the payment succeeds.",
    responses={400: {"model": ErrorResponse, "description": "That plan can't be chosen."}},
)
def start_checkout(payload: CheckoutRequest, user: VerifiedUser) -> CheckoutResponse:
    problem = validate_upgrade(user.subscription, payload.plan)
    plan = find_plan(payload.plan)
    if problem or plan is None:
        raise HTTPException(status_code=400, detail=problem or "Unknown plan.")

    provider = get_payment_provider()
    try:
        session = provider.create_checkout(user.id, user.email, plan)
    except PaymentsUnavailableError as exc:
        raise HTTPException(status_code=503, detail="Payments are not available yet.") from exc
    return CheckoutResponse(checkout_url=session.url)
