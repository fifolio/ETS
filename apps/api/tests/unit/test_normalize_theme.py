import pytest

from app.services.preferences.normalize_theme import normalize_theme


@pytest.mark.parametrize(
    ("value", "expected"),
    [("light", "light"), ("dark", "dark"), ("neon", "light"), (None, "light")],
)
def test_light_and_dark_are_kept_and_anything_else_becomes_light(value, expected):
    assert normalize_theme(value) == expected
