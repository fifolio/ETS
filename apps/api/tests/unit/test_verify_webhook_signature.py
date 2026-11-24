import base64
import hashlib
import hmac
import json

import pytest
from app.exceptions.webhook_verification_error import WebhookVerificationError

from app.services.payments.whop.verify_webhook_signature import verify_webhook_signature

SECRET = "ws_" + "ab" * 32
NOW = 1_800_000_000
BODY = json.dumps({"type": "payment.succeeded", "data": {"id": "pay_1"}}).encode()


def sign(secret, message_id, timestamp, body):
    digest = hmac.new(
        secret.encode(), f"{message_id}.{timestamp}.".encode() + body, hashlib.sha256
    ).digest()
    return "v1," + base64.b64encode(digest).decode()


def headers_for(body=BODY, secret=SECRET, timestamp=NOW):
    return {
        "webhook-id": "msg_1",
        "webhook-timestamp": str(timestamp),
        "webhook-signature": sign(secret, "msg_1", timestamp, body),
    }


def test_a_correctly_signed_event_is_returned():
    event = verify_webhook_signature(headers_for(), BODY, SECRET, NOW)

    assert event["type"] == "payment.succeeded"


def test_header_names_are_case_insensitive():
    headers = {name.title(): value for name, value in headers_for().items()}

    assert verify_webhook_signature(headers, BODY, SECRET, NOW)["data"]["id"] == "pay_1"


def test_one_valid_signature_among_several_is_enough():
    headers = headers_for()
    headers["webhook-signature"] = "v1,AAAA " + headers["webhook-signature"]

    assert verify_webhook_signature(headers, BODY, SECRET, NOW)


def test_a_wrong_secret_is_refused():
    with pytest.raises(WebhookVerificationError):
        verify_webhook_signature(headers_for(secret="ws_other"), BODY, SECRET, NOW)


def test_a_changed_body_is_refused():
    with pytest.raises(WebhookVerificationError):
        verify_webhook_signature(headers_for(), BODY + b" ", SECRET, NOW)


def test_an_old_timestamp_is_refused():
    with pytest.raises(WebhookVerificationError):
        verify_webhook_signature(headers_for(timestamp=NOW - 301), BODY, SECRET, NOW)


def test_a_future_timestamp_is_refused():
    with pytest.raises(WebhookVerificationError):
        verify_webhook_signature(headers_for(timestamp=NOW + 301), BODY, SECRET, NOW)


def test_missing_headers_are_refused():
    with pytest.raises(WebhookVerificationError):
        verify_webhook_signature({}, BODY, SECRET, NOW)


def test_a_signed_body_that_is_not_json_is_refused():
    body = b"not json"

    with pytest.raises(WebhookVerificationError):
        verify_webhook_signature(headers_for(body=body), body, SECRET, NOW)
