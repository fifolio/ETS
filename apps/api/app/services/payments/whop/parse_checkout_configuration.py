from typing import Any

from app.exceptions.payment_provider_error import PaymentProviderError
from app.types.whop_settings import WhopSettings


def parse_checkout_configuration(
    data: dict[str, Any], whop: WhopSettings, plan_id: str | None
) -> tuple[str, str, str]:
    """The checkout ID, the hosted payment page address, and the plan ID from Whop's answer."""
    checkout_id = data.get("id")
    if not isinstance(checkout_id, str) or not checkout_id:
        raise PaymentProviderError("The payment service didn't return a checkout ID")
    variant = data.get("variant")
    variant_id = variant.get("id") if isinstance(variant, dict) else None
    resolved = variant_id if isinstance(variant_id, str) and variant_id else plan_id
    if not resolved:
        raise PaymentProviderError("The payment service didn't return a plan ID")
    url = data.get("purchase_url")
    if not isinstance(url, str) or not url:
        url = f"{whop.checkout_host}/checkout/{resolved}/?session={checkout_id}"
    return checkout_id, url, resolved
