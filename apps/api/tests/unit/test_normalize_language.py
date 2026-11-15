import pytest

from app.services.preferences.normalize_language import normalize_language


@pytest.mark.parametrize(
    ("value", "expected"),
    [("en", "en"), ("ar", "ar"), ("xx", "en"), ("", "en"), (None, "en"), (5, "en")],
)
def test_a_listed_language_is_kept_and_anything_else_becomes_english(value, expected):
    assert normalize_language(value) == expected
