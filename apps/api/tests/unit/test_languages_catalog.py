from app.constants.languages import DEFAULT_LANGUAGE, LANGUAGES


def test_every_language_code_appears_once():
    assert len({language.code for language in LANGUAGES}) == len(LANGUAGES)


def test_english_is_first_translated_and_the_default():
    assert LANGUAGES[0].code == DEFAULT_LANGUAGE == "en"
    assert LANGUAGES[0].translated is True


def test_directions_are_left_to_right_or_right_to_left():
    assert all(language.direction in ("ltr", "rtl") for language in LANGUAGES)


def test_the_right_to_left_languages_are_marked():
    rtl = {language.code for language in LANGUAGES if language.direction == "rtl"}

    assert rtl == {"ar", "ur", "fa", "he"}
