from app.constants.languages import LANGUAGES
from app.types.language_definition import LanguageDefinition


def find_language(code: object) -> LanguageDefinition | None:
    if not isinstance(code, str):
        return None
    return next((language for language in LANGUAGES if language.code == code), None)
