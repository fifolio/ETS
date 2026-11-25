from typing import Any

from app.services.appwrite.parse_appwrite_datetime import parse_appwrite_datetime
from app.services.payments.whop.net_paid_cents import net_paid_cents
from app.types.payment_notice import PaymentNotice


def parse_whop_payment(
    data: dict[str, Any], environment: str, owner: tuple[str, str] | None = None
) -> PaymentNotice | None:
    """A neutral notice from a Whop payment, or None when it isn't one of our checkouts.

    `owner` is (user_id, sku) found another way (a renewal is matched through its membership).
    """
    metadata = data.get("metadata")
    metadata = metadata if isinstance(metadata, dict) else {}
    user_id = metadata.get("ets_user_id")
    sku = metadata.get("ets_sku")
    if not (isinstance(user_id, str) and user_id and isinstance(sku, str) and sku) and owner:
        user_id, sku = owner
    payment_id = data.get("id")
    if not all(isinstance(value, str) and value for value in (user_id, sku, payment_id)):
        return None

    paid_at = None
    paid_at_text = data.get("paid_at")
    if isinstance(paid_at_text, str) and paid_at_text:
        try:
            paid_at = parse_appwrite_datetime(paid_at_text)
        except ValueError:
            paid_at = None
    return PaymentNotice(
        provider="whop",
        environment=environment,
        payment_id=payment_id,
        checkout_id=str(data.get("checkout_configuration_id") or ""),
        user_id=user_id,
        sku=sku,
        paid_cents=net_paid_cents(data),
        currency=str(data.get("currency") or "").lower(),
        membership_id=data.get("membership_id") or None,
        customer_id=data.get("member_id") or None,
        paid_at=paid_at,
    )
