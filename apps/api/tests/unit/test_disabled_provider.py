import pytest

from app.exceptions.payments_unavailable_error import PaymentsUnavailableError
from app.services.payments.disabled_provider import DisabledProvider
from app.types.checkout_order import CheckoutOrder


def test_it_cannot_start_a_checkout():
    with pytest.raises(PaymentsUnavailableError):
        DisabledProvider().create_checkout(
            CheckoutOrder("user-1", "jane@example.com", "plan_nextmove", 700)
        )


def test_it_reports_no_provider_and_no_environment():
    provider = DisabledProvider()

    assert (provider.name, provider.environment) == ("none", "none")


def test_it_cannot_cancel_a_subscription():
    with pytest.raises(PaymentsUnavailableError):
        DisabledProvider().cancel_subscription("mem_1")
