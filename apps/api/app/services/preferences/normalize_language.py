from app.constants.languages import DEFAULT_LANGUAGE
from app.services.preferences.find_language import find_language


def normalize_language(value: object) -> str:
    """The language code if it is one we list, otherwise English."""
    language = find_language(value)
    return language.code if language else DEFAULT_LANGUAGE
