from typing import Any

from app.services.payments.whop.parse_whop_payment import parse_whop_payment
from app.services.subscriptions.find_subscription_row import find_subscription_row
from app.types.payment_notice import PaymentNotice


def resolve_renewal_notice(data: dict[str, Any], environment: str) -> PaymentNotice | None:
    """A payment of a membership we know (a renewal) has no checkout metadata: find the owner."""
    membership_id = data.get("membership_id")
    if not isinstance(membership_id, str) or not membership_id:
        return None
    record = find_subscription_row("providerSubscriptionId", membership_id)
    if record is None or record.plan == "explore":
        return None
    return parse_whop_payment(data, environment, owner=(record.user_id, f"plan_{record.plan}"))
