import pytest

from app.services.usage.minutes_to_cash import minutes_to_cash


@pytest.mark.parametrize(
    ("minutes", "rate", "cash"),
    [(5.0, 50.0, 4.1667), (1.0, 60.0, 1.0), (0.0, 50.0, 0.0), (5.0, 0.0, 0.0)],
)
def test_cash_is_the_hourly_rate_divided_by_60_times_the_minutes(minutes, rate, cash):
    assert minutes_to_cash(minutes, rate) == cash
