from app.services.currencies.convert_usd import convert_usd


def test_usd_to_eur():
    assert convert_usd(10.0, 0.92) == 9.2


def test_usd_to_self():
    assert convert_usd(5.0, 1.0) == 5.0


def test_zero_amount():
    assert convert_usd(0.0, 0.92) == 0.0
