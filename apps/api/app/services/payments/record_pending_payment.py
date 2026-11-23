import logging

from app.services.payments.create_payment_row import create_payment_row
from app.types.checkout_order import CheckoutOrder
from app.types.checkout_session import CheckoutSession

logger = logging.getLogger(__name__)


def record_pending_payment(
    order: CheckoutOrder, session: CheckoutSession, provider: str, environment: str
) -> None:
    """Remember the checkout as pending. Never raises: the user must still be able to pay."""
    try:
        create_payment_row(
            {
                "userId": order.user_id,
                "provider": provider,
                "environment": environment,
                "sku": order.sku,
                "providerCheckoutId": session.checkout_id,
                "amountCents": order.amount_cents,
                "currency": "usd",
                "status": "pending",
                "credits": order.credits,
            }
        )
    except Exception:
        logger.exception("Could not record the pending payment")
