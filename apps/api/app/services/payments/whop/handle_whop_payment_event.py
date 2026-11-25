import logging
from datetime import datetime
from typing import Any

from app.services.payments.apply_payment import apply_payment
from app.services.payments.mark_payment_failed import mark_payment_failed
from app.services.payments.whop.parse_whop_payment import parse_whop_payment
from app.services.payments.whop.resolve_renewal_notice import resolve_renewal_notice

logger = logging.getLogger(__name__)


def handle_whop_payment_event(
    event_type: str, data: dict[str, Any], environment: str, now: datetime
) -> str:
    if event_type == "payment.succeeded" and data.get("status") != "paid":
        return "ignored"
    notice = parse_whop_payment(data, environment) or resolve_renewal_notice(data, environment)
    if notice is None:
        logger.info("Whop %s %s is not one of our payments", event_type, data.get("id"))
        return "ignored"
    if event_type == "payment.succeeded":
        return apply_payment(notice, now)
    return mark_payment_failed(notice, now)
