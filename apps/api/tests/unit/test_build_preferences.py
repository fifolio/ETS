import app.services.preferences.find_language as find_module

from app.services.preferences.build_preferences import build_preferences
from app.types.language_definition import LanguageDefinition

EN = LanguageDefinition("en", "English", "English", "ltr", True)
AR_COMING = LanguageDefinition("ar", "Arabic", "العربية", "rtl", False)
AR_READY = LanguageDefinition("ar", "Arabic", "العربية", "rtl", True)


def test_empty_preferences_give_the_defaults():
    assert build_preferences({}).model_dump() == {
        "theme": "light",
        "language": "en",
        "effective_language": "en",
        "direction": "ltr",
    }


def test_unexpected_values_are_replaced_by_the_defaults():
    result = build_preferences({"theme": "neon", "language": 42})

    assert (result.theme, result.language) == ("light", "en")


def test_a_language_without_a_translation_keeps_the_choice_but_shows_english(monkeypatch):
    monkeypatch.setattr(find_module, "LANGUAGES", (EN, AR_COMING))

    result = build_preferences({"language": "ar"})

    assert (result.language, result.effective_language, result.direction) == ("ar", "en", "ltr")


def test_a_translated_right_to_left_language_gives_its_direction(monkeypatch):
    monkeypatch.setattr(find_module, "LANGUAGES", (EN, AR_READY))

    result = build_preferences({"language": "ar", "theme": "dark"})

    assert result.model_dump() == {
        "theme": "dark",
        "language": "ar",
        "effective_language": "ar",
        "direction": "rtl",
    }
