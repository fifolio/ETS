from fastapi import APIRouter, HTTPException

from app.exceptions.checkout_refused_error import CheckoutRefusedError
from app.exceptions.payment_provider_error import PaymentProviderError
from app.exceptions.payments_unavailable_error import PaymentsUnavailableError
from app.schemas.checkout_request import CheckoutRequest
from app.schemas.checkout_response import CheckoutResponse
from app.schemas.error_response import ErrorResponse
from app.services.payments.build_checkout_order import build_checkout_order
from app.services.payments.get_payment_provider import get_payment_provider
from app.services.payments.record_pending_payment import record_pending_payment
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


@router.post(
    "/checkout",
    response_model=CheckoutResponse,
    summary="Start paying for a plan upgrade or a credit top-up",
    description=(
        "Creates a checkout with the payment provider. The plan and credits change only after "
        "the payment is confirmed by the provider's webhook, never because this was called."
    ),
    responses={400: {"model": ErrorResponse, "description": "That purchase isn't allowed."}},
)
def start_checkout(payload: CheckoutRequest, user: VerifiedUser) -> CheckoutResponse:
    try:
        order = build_checkout_order(user, payload.product, payload.amount_usd)
    except CheckoutRefusedError as exc:
        raise HTTPException(status_code=400, detail=exc.message) from exc

    provider = get_payment_provider()
    try:
        session = provider.create_checkout(order)
    except PaymentsUnavailableError as exc:
        raise HTTPException(status_code=503, detail="Payments are not available yet.") from exc
    except PaymentProviderError as exc:
        raise HTTPException(
            status_code=502, detail="The payment service failed. Please try again."
        ) from exc

    record_pending_payment(order, session, provider.name, provider.environment)
    return CheckoutResponse(
        provider=provider.name,
        environment=provider.environment,
        checkout_id=session.checkout_id,
        plan_id=session.plan_id,
        checkout_url=session.url,
        amount_cents=order.amount_cents,
        credits=order.credits,
    )
