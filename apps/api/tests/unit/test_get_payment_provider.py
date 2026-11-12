import pytest

from app.core.config import settings
from app.exceptions.configuration_error import ConfigurationError
from app.services.payments.disabled_provider import DisabledProvider
from app.services.payments.get_payment_provider import get_payment_provider


def test_none_gives_the_disabled_provider(monkeypatch):
    monkeypatch.setattr(settings, "payment_provider", "none")

    assert isinstance(get_payment_provider(), DisabledProvider)


def test_an_unknown_provider_is_a_configuration_error(monkeypatch):
    monkeypatch.setattr(settings, "payment_provider", "paypal")

    with pytest.raises(ConfigurationError):
        get_payment_provider()
