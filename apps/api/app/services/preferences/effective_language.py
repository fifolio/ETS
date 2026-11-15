from app.constants.languages import DEFAULT_LANGUAGE, LANGUAGES
from app.services.preferences.find_language import find_language
from app.types.language_definition import LanguageDefinition


def effective_language(code: str) -> LanguageDefinition:
    """The language to display: the chosen one when it is translated, otherwise English."""
    chosen = find_language(code)
    if chosen is not None and chosen.translated:
        return chosen
    return find_language(DEFAULT_LANGUAGE) or LANGUAGES[0]
