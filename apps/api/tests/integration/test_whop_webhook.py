import base64
import hashlib
import hmac
import json
import time

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.types.whop_settings import WhopSettings

client = TestClient(app)
failing_client = TestClient(app, raise_server_exceptions=False)
SECRET = "ws_testsecret"
BODY = json.dumps({"type": "payment.succeeded", "data": {"id": "pay_1"}}).encode()
MODULE = "app.services.payments.whop.process_whop_webhook"


def signed_headers(body=BODY, secret=SECRET, timestamp=None):
    timestamp = str(int(time.time()) if timestamp is None else timestamp)
    digest = hmac.new(
        secret.encode(), f"msg_1.{timestamp}.".encode() + body, hashlib.sha256
    ).digest()
    return {
        "webhook-id": "msg_1",
        "webhook-timestamp": timestamp,
        "webhook-signature": "v1," + base64.b64encode(digest).decode(),
    }


def whop(secret=SECRET):
    return WhopSettings("sandbox", "https://api", "https://sandbox.whop.com", "key", {}, "", secret)


@pytest.fixture
def handled(monkeypatch):
    calls = []
    monkeypatch.setattr(f"{MODULE}.get_whop_settings", lambda: whop())
    monkeypatch.setattr(
        f"{MODULE}.handle_whop_event",
        lambda event, environment, now: calls.append((event["type"], environment)) or "applied",
    )
    return calls


def test_a_correctly_signed_event_is_handled_and_acknowledged(handled):
    response = client.post("/webhooks/whop", content=BODY, headers=signed_headers())

    assert response.status_code == 200
    assert response.json() == {"result": "applied"}
    assert handled == [("payment.succeeded", "sandbox")]


def test_a_wrong_signature_is_rejected_and_nothing_is_handled(handled):
    response = client.post(
        "/webhooks/whop", content=BODY, headers=signed_headers(secret="ws_other")
    )

    assert response.status_code == 400
    assert handled == []


def test_a_request_without_signature_headers_is_rejected(handled):
    assert client.post("/webhooks/whop", content=BODY).status_code == 400
    assert handled == []


def test_an_old_signed_request_is_rejected_as_a_replay(handled):
    headers = signed_headers(timestamp=int(time.time()) - 3600)

    assert client.post("/webhooks/whop", content=BODY, headers=headers).status_code == 400
    assert handled == []


def test_a_signed_body_that_is_not_json_is_rejected(handled):
    body = b"not json"

    assert (
        client.post("/webhooks/whop", content=body, headers=signed_headers(body=body)).status_code
        == 400
    )


def test_the_endpoint_is_unavailable_until_the_webhook_secret_is_configured(monkeypatch):
    monkeypatch.setattr(f"{MODULE}.get_whop_settings", lambda: whop(secret=""))

    assert client.post("/webhooks/whop", content=BODY, headers=signed_headers()).status_code == 503


def test_a_processing_failure_returns_500_so_whop_retries(monkeypatch):
    def fail(event, environment, now):
        raise RuntimeError("table down")

    monkeypatch.setattr(f"{MODULE}.get_whop_settings", lambda: whop())
    monkeypatch.setattr(f"{MODULE}.handle_whop_event", fail)

    assert (
        failing_client.post("/webhooks/whop", content=BODY, headers=signed_headers()).status_code
        == 500
    )


def test_the_endpoint_is_hidden_from_the_public_docs():
    assert "/webhooks/whop" not in client.get("/openapi.json").json()["paths"]
