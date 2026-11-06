from app.services.text.count_words import count_words


def test_counts_words_separated_by_any_whitespace():
    assert count_words("Senior  engineer\nwanted for\tour team") == 6


def test_an_empty_text_has_no_words():
    assert count_words("") == 0
