import pytest

from app.constants.topups import TOPUP_MAX_CENTS, TOPUP_STEP_CENTS
from app.services.topups.credits_for_cents import credits_for_cents


@pytest.mark.parametrize(
    ("cents", "credits"),
    [(100, 8), (125, 10), (200, 16), (500, 40), (1000, 80), (2000, 160), (5000, 400)],
)
def test_the_credits_follow_the_8_per_dollar_rate(cents, credits):
    assert credits_for_cents(cents) == credits


def test_every_step_from_the_minimum_to_the_maximum_follows_the_same_rate():
    for cents in range(300, TOPUP_MAX_CENTS + 1, TOPUP_STEP_CENTS):
        assert credits_for_cents(cents) * 12.5 == cents
