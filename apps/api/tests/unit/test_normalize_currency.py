from app.services.preferences.normalize_currency import normalize_currency

CODES = {"usd", "eur", "tnd"}


def test_a_known_code_is_kept():
    assert normalize_currency("eur", CODES) == "eur"


def test_an_unknown_code_becomes_usd():
    assert normalize_currency("xyz", CODES) == "usd"


def test_none_becomes_usd():
    assert normalize_currency(None, CODES) == "usd"
