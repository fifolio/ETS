import httpx
import pytest

import app.services.payments.whop.get_whop_json as module
from app.exceptions.payment_provider_error import PaymentProviderError
from app.types.whop_settings import WhopSettings

WHOP = WhopSettings(
    "sandbox", "https://sandbox-api.whop.com/api/v1", "https://x", "secret-key", {}, ""
)


class FakeResponse:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self.payload = payload
        self.text = ""

    def json(self):
        if self.payload is None:
            raise ValueError("not json")
        return self.payload


def install(monkeypatch, response=None, error=None):
    calls = []

    def fake_get(url, headers, timeout):
        calls.append((url, headers))
        if error:
            raise error
        return response

    monkeypatch.setattr(module.httpx, "get", fake_get)
    return calls


def test_reads_the_path_with_the_bearer_key(monkeypatch):
    calls = install(monkeypatch, FakeResponse(200, {"id": "mem_1"}))

    assert module.get_whop_json(WHOP, "/memberships/mem_1") == {"id": "mem_1"}
    assert calls[0][0] == "https://sandbox-api.whop.com/api/v1/memberships/mem_1"
    assert calls[0][1]["Authorization"] == "Bearer secret-key"


def test_a_refused_request_is_a_provider_error(monkeypatch):
    install(monkeypatch, FakeResponse(403, {}))

    with pytest.raises(PaymentProviderError):
        module.get_whop_json(WHOP, "/memberships/mem_1")


def test_a_network_failure_is_a_provider_error(monkeypatch):
    install(monkeypatch, error=httpx.ConnectError("offline"))

    with pytest.raises(PaymentProviderError):
        module.get_whop_json(WHOP, "/memberships/mem_1")
