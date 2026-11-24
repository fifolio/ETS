import base64
import hashlib
import hmac
import json
from collections.abc import Mapping
from typing import Any

from app.constants.whop import WEBHOOK_TOLERANCE_SECONDS
from app.exceptions.webhook_verification_error import WebhookVerificationError


def verify_webhook_signature(
    headers: Mapping[str, str], body: bytes, secret: str, now_seconds: float
) -> dict[str, Any]:
    """Check a Standard Webhooks signature and return the event. Raises WebhookVerificationError."""
    lowered = {name.lower(): value for name, value in headers.items()}
    message_id = lowered.get("webhook-id")
    timestamp = lowered.get("webhook-timestamp")
    signature = lowered.get("webhook-signature")
    if not message_id or not timestamp or not signature:
        raise WebhookVerificationError("Missing webhook headers")
    try:
        sent_at = int(timestamp)
    except ValueError as exc:
        raise WebhookVerificationError("Unreadable timestamp") from exc
    if abs(now_seconds - sent_at) > WEBHOOK_TOLERANCE_SECONDS:
        raise WebhookVerificationError("Timestamp too far from now")

    signed = f"{message_id}.{timestamp}.".encode() + body
    digest = hmac.new(secret.encode("utf-8"), signed, hashlib.sha256).digest()
    expected = base64.b64encode(digest)
    # The header can carry several signatures ("v1,abc v1,def"): one valid one is enough.
    candidates = [part.split(",", 1)[1] for part in signature.split() if part.startswith("v1,")]
    if not any(hmac.compare_digest(expected, candidate.encode()) for candidate in candidates):
        raise WebhookVerificationError("Signature does not match")

    try:
        event = json.loads(body)
    except ValueError as exc:
        raise WebhookVerificationError("Body is not JSON") from exc
    if not isinstance(event, dict):
        raise WebhookVerificationError("Body is not an event")
    return event
