from app.core.config import settings
from app.services.payments.are_payments_enabled import are_payments_enabled


def test_payments_are_off_without_a_provider(monkeypatch):
    monkeypatch.setattr(settings, "payment_provider", "none")

    assert are_payments_enabled() is False


def test_payments_are_on_when_a_provider_is_set(monkeypatch):
    monkeypatch.setattr(settings, "payment_provider", "konnect")

    assert are_payments_enabled() is True
