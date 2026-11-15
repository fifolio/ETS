from app.constants.languages import LANGUAGES
from app.schemas.language_out import LanguageOut
from app.services.preferences.to_language_out import to_language_out


def list_languages() -> list[LanguageOut]:
    return [to_language_out(language) for language in LANGUAGES]
