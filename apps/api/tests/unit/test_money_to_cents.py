import pytest

from app.services.payments.whop.money_to_cents import money_to_cents


@pytest.mark.parametrize(
    ("value", "cents"),
    [({"amount": "5.25"}, 525), ({"amount": "0.30"}, 30), ({"amount": "10"}, 1000)],
)
def test_dollars_become_cents(value, cents):
    assert money_to_cents(value) == cents


@pytest.mark.parametrize("value", [None, {}, {"amount": "abc"}])
def test_anything_unreadable_gives_none(value):
    assert money_to_cents(value) is None
