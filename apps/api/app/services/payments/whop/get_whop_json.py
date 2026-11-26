import logging
from typing import Any

import httpx

from app.constants.whop import WHOP_TIMEOUT_SECONDS
from app.exceptions.payment_provider_error import PaymentProviderError
from app.types.whop_settings import WhopSettings

logger = logging.getLogger(__name__)


def get_whop_json(whop: WhopSettings, path: str) -> dict[str, Any]:
    """Read something from the Whop API. Raises PaymentProviderError when it can't."""
    try:
        response = httpx.get(
            f"{whop.api_base}{path}",
            headers={"Authorization": f"Bearer {whop.api_key}"},
            timeout=WHOP_TIMEOUT_SECONDS,
        )
    except httpx.HTTPError as exc:
        logger.error("Could not reach Whop: %s", exc)
        raise PaymentProviderError("Could not reach the payment service") from exc
    if response.status_code >= 400:
        logger.error("Whop refused the request: %s %s", response.status_code, response.text[:500])
        raise PaymentProviderError("The payment service refused the request")
    try:
        data = response.json()
    except ValueError as exc:
        raise PaymentProviderError("The payment service sent an unreadable answer") from exc
    return data if isinstance(data, dict) else {}
