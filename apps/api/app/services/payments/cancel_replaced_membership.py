import logging

from app.services.payments.get_payment_provider import get_payment_provider

logger = logging.getLogger(__name__)


def cancel_replaced_membership(membership_id: str) -> None:
    """Stop billing a membership the user replaced by an upgrade. Never raises."""
    try:
        get_payment_provider().cancel_subscription(membership_id)
    except Exception:
        logger.exception(
            "Could not cancel the replaced membership %s: the user may be billed twice",
            membership_id,
        )
