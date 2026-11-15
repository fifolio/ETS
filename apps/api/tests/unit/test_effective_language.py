import app.services.preferences.find_language as find_module

from app.services.preferences.effective_language import effective_language
from app.types.language_definition import LanguageDefinition

EN = LanguageDefinition("en", "English", "English", "ltr", True)
FR_COMING = LanguageDefinition("fr", "French", "Français", "ltr", False)
FR_READY = LanguageDefinition("fr", "French", "Français", "ltr", True)


def test_a_language_without_a_translation_shows_english(monkeypatch):
    monkeypatch.setattr(find_module, "LANGUAGES", (EN, FR_COMING))

    assert effective_language("fr").code == "en"


def test_a_translated_language_is_shown(monkeypatch):
    monkeypatch.setattr(find_module, "LANGUAGES", (EN, FR_READY))

    assert effective_language("fr").code == "fr"


def test_an_unknown_language_shows_english():
    assert effective_language("xx").code == "en"
