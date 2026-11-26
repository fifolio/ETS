import httpx
import pytest

import app.services.payments.whop.post_cancel_membership as module
from app.exceptions.payment_provider_error import PaymentProviderError
from app.types.whop_settings import WhopSettings

WHOP = WhopSettings(
    "sandbox", "https://sandbox-api.whop.com/api/v1", "https://x", "secret-key", {}, ""
)


class FakeResponse:
    def __init__(self, status_code=200):
        self.status_code = status_code
        self.text = ""


def install(monkeypatch, response=None, error=None):
    calls = []

    def fake_post(url, json, headers, timeout):
        calls.append((url, json, headers))
        if error:
            raise error
        return response

    monkeypatch.setattr(module.httpx, "post", fake_post)
    return calls


def test_cancels_the_membership_immediately(monkeypatch):
    calls = install(monkeypatch, FakeResponse(200))

    module.post_cancel_membership(WHOP, "mem_1")

    url, body, headers = calls[0]
    assert url == "https://sandbox-api.whop.com/api/v1/memberships/mem_1/cancel"
    assert body == {"cancel_at_period_end": False}
    assert headers["Authorization"] == "Bearer secret-key"


def test_a_refused_cancellation_is_a_provider_error(monkeypatch):
    install(monkeypatch, FakeResponse(403))

    with pytest.raises(PaymentProviderError):
        module.post_cancel_membership(WHOP, "mem_1")


def test_a_network_failure_is_a_provider_error(monkeypatch):
    install(monkeypatch, error=httpx.ConnectError("offline"))

    with pytest.raises(PaymentProviderError):
        module.post_cancel_membership(WHOP, "mem_1")
