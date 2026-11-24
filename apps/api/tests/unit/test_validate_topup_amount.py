import pytest

from app.exceptions.checkout_refused_error import CheckoutRefusedError
from app.services.topups.validate_topup_amount import validate_topup_amount


@pytest.mark.parametrize(("amount", "cents"), [(3.0, 300), (5.25, 525), (50.0, 5000)])
def test_a_valid_amount_becomes_cents(amount, cents):
    assert validate_topup_amount(amount) == cents


@pytest.mark.parametrize("amount", [None, 0, 2.75, 50.25, 5.1, -5, float("nan")])
def test_an_amount_outside_the_range_or_the_steps_is_refused(amount):
    with pytest.raises(CheckoutRefusedError):
        validate_topup_amount(amount)
