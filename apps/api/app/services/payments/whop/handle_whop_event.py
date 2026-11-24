import logging
from datetime import datetime
from typing import Any

from app.services.payments.apply_payment import apply_payment
from app.services.payments.mark_payment_failed import mark_payment_failed
from app.services.payments.whop.parse_whop_payment import parse_whop_payment

logger = logging.getLogger(__name__)


def handle_whop_event(event: dict[str, Any], environment: str, now: datetime) -> str:
    """Act on a verified Whop event. Returns what happened (for the logs and the response)."""
    event_type = event.get("type")
    data = event.get("data")
    if not isinstance(data, dict) or event_type not in ("payment.succeeded", "payment.failed"):
        return "ignored"
    if event_type == "payment.succeeded" and data.get("status") != "paid":
        return "ignored"

    notice = parse_whop_payment(data, environment)
    if notice is None:
        logger.info("Whop %s %s is not one of our checkouts", event_type, data.get("id"))
        return "ignored"
    if event_type == "payment.succeeded":
        outcome = apply_payment(notice, now)
    else:
        outcome = mark_payment_failed(notice, now)
    logger.info("Whop %s %s: %s", event_type, notice.payment_id, outcome)
    return outcome
