import logging
from urllib.parse import quote

import httpx

from app.constants.whop import WHOP_TIMEOUT_SECONDS
from app.exceptions.payment_provider_error import PaymentProviderError
from app.types.whop_settings import WhopSettings

logger = logging.getLogger(__name__)


def post_cancel_membership(whop: WhopSettings, membership_id: str) -> None:
    """Cancel a Whop membership immediately. Raises PaymentProviderError."""
    url = f"{whop.api_base}/memberships/{quote(membership_id, safe='')}/cancel"
    try:
        response = httpx.post(
            url,
            json={"cancel_at_period_end": False},
            headers={"Authorization": f"Bearer {whop.api_key}"},
            timeout=WHOP_TIMEOUT_SECONDS,
        )
    except httpx.HTTPError as exc:
        logger.error("Could not reach Whop: %s", exc)
        raise PaymentProviderError("Could not reach the payment service") from exc
    if response.status_code >= 400:
        logger.error(
            "Whop refused the cancellation: %s %s", response.status_code, response.text[:500]
        )
        raise PaymentProviderError("The payment service refused the cancellation")
