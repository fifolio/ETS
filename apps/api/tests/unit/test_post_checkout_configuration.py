import httpx
import pytest

import app.services.payments.whop.post_checkout_configuration as module
from app.exceptions.payment_provider_error import PaymentProviderError
from app.types.whop_settings import WhopSettings

WHOP = WhopSettings(
    "sandbox", "https://sandbox-api.whop.com/api/v1", "https://x", "secret-key", {}, ""
)


class FakeResponse:
    def __init__(self, status_code=200, payload=None, text=""):
        self.status_code = status_code
        self.payload = payload
        self.text = text

    def json(self):
        if self.payload is None:
            raise ValueError("not json")
        return self.payload


def install(monkeypatch, response=None, error=None):
    calls = []

    def fake_post(url, json, headers, timeout):
        calls.append((url, json, headers))
        if error:
            raise error
        return response

    monkeypatch.setattr(module.httpx, "post", fake_post)
    return calls


def test_sends_the_body_with_the_bearer_key_and_returns_the_answer(monkeypatch):
    calls = install(monkeypatch, FakeResponse(200, {"id": "ch_1"}))

    result = module.post_checkout_configuration(WHOP, {"plan_id": "plan_1"})

    assert result == {"id": "ch_1"}
    url, body, headers = calls[0]
    assert url == "https://sandbox-api.whop.com/api/v1/checkout_configurations"
    assert body == {"plan_id": "plan_1"}
    assert headers["Authorization"] == "Bearer secret-key"


def test_a_refused_request_is_a_provider_error(monkeypatch):
    install(monkeypatch, FakeResponse(401, text="unauthorized"))

    with pytest.raises(PaymentProviderError):
        module.post_checkout_configuration(WHOP, {})


def test_a_network_failure_is_a_provider_error(monkeypatch):
    install(monkeypatch, error=httpx.ConnectError("offline"))

    with pytest.raises(PaymentProviderError):
        module.post_checkout_configuration(WHOP, {})


def test_an_unreadable_answer_is_a_provider_error(monkeypatch):
    install(monkeypatch, FakeResponse(200, None))

    with pytest.raises(PaymentProviderError):
        module.post_checkout_configuration(WHOP, {})
