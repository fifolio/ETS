import logging
from datetime import datetime
from typing import Any

from app.services.payments.apply_membership_update import apply_membership_update
from app.services.payments.apply_refund import apply_refund
from app.services.payments.whop.handle_whop_payment_event import handle_whop_payment_event
from app.services.payments.whop.parse_whop_membership import parse_whop_membership
from app.services.payments.whop.parse_whop_refund import parse_whop_refund

logger = logging.getLogger(__name__)


def handle_whop_event(event: dict[str, Any], environment: str, now: datetime) -> str:
    """Act on a verified Whop event. Returns what happened (for the logs and the response)."""
    event_type = event.get("type")
    data = event.get("data")
    if not isinstance(data, dict):
        return "ignored"

    if event_type in ("payment.succeeded", "payment.failed"):
        outcome = handle_whop_payment_event(event_type, data, environment, now)
    elif event_type == "membership.updated":
        membership = parse_whop_membership(data)
        outcome = apply_membership_update(membership, now) if membership else "ignored"
    elif event_type in ("refund.created", "refund.updated"):
        refund = parse_whop_refund(data)
        outcome = apply_refund(refund, now) if refund else "ignored"
    else:
        return "ignored"
    logger.info("Whop %s %s: %s", event_type, data.get("id"), outcome)
    return outcome
