import pytest

from app.services.usage.words_to_minutes import words_to_minutes


@pytest.mark.parametrize(("words", "minutes"), [(900, 4.0), (450, 2.0), (0, 0.0), (100, 0.4444)])
def test_words_become_minutes_at_225_words_per_minute(words, minutes):
    assert words_to_minutes(words) == minutes
