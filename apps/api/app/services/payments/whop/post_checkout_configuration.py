import logging
from typing import Any

import httpx

from app.constants.whop import WHOP_TIMEOUT_SECONDS
from app.exceptions.payment_provider_error import PaymentProviderError
from app.types.whop_settings import WhopSettings

logger = logging.getLogger(__name__)


def post_checkout_configuration(whop: WhopSettings, body: dict[str, Any]) -> dict[str, Any]:
    """Create a Whop checkout configuration. Raises PaymentProviderError when it can't."""
    try:
        response = httpx.post(
            f"{whop.api_base}/checkout_configurations",
            json=body,
            headers={"Authorization": f"Bearer {whop.api_key}"},
            timeout=WHOP_TIMEOUT_SECONDS,
        )
    except httpx.HTTPError as exc:
        logger.error("Could not reach Whop: %s", exc)
        raise PaymentProviderError("Could not reach the payment service") from exc
    if response.status_code >= 400:
        logger.error("Whop refused the checkout: %s %s", response.status_code, response.text[:500])
        raise PaymentProviderError("The payment service refused the request")
    try:
        return response.json()
    except ValueError as exc:
        raise PaymentProviderError("The payment service sent an unreadable answer") from exc
