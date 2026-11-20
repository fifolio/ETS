import pytest

from app.services.credits.compute_renewal_delta import compute_renewal_delta


@pytest.mark.parametrize(
    ("current", "allowance", "roll_over", "expected"),
    [(40, 150, False, 110), (200, 150, False, -50), (40, 150, True, 150), (0, 150, False, 150)],
)
def test_renewal_resets_to_the_allowance_or_adds_it_on_top(current, allowance, roll_over, expected):
    assert compute_renewal_delta(current, allowance, roll_over) == expected
