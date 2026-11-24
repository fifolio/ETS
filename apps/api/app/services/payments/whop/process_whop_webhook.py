import time
from collections.abc import Mapping
from datetime import UTC, datetime

from app.exceptions.configuration_error import ConfigurationError
from app.services.payments.whop.get_whop_settings import get_whop_settings
from app.services.payments.whop.handle_whop_event import handle_whop_event
from app.services.payments.whop.verify_webhook_signature import verify_webhook_signature


def process_whop_webhook(headers: Mapping[str, str], body: bytes) -> str:
    whop = get_whop_settings()
    if not whop.webhook_secret:
        raise ConfigurationError(f"WHOP_{whop.environment.upper()}_WEBHOOK_SECRET is not set")
    event = verify_webhook_signature(headers, body, whop.webhook_secret, time.time())
    return handle_whop_event(event, whop.environment, datetime.now(UTC))
