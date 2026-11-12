import pytest

from app.constants.plans import PLANS
from app.exceptions.payments_unavailable_error import PaymentsUnavailableError
from app.services.payments.disabled_provider import DisabledProvider


def test_it_cannot_start_a_checkout():
    with pytest.raises(PaymentsUnavailableError):
        DisabledProvider().create_checkout("user-1", "jane@example.com", PLANS[1])


def test_it_ignores_webhooks():
    assert DisabledProvider().parse_webhook({}, b"{}") is None
