from app.schemas.language_out import LanguageOut
from app.types.language_definition import LanguageDefinition


def to_language_out(language: LanguageDefinition) -> LanguageOut:
    return LanguageOut(
        code=language.code,
        name=language.name,
        native_name=language.native_name,
        direction=language.direction,
        translated=language.translated,
    )
