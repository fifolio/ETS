from app.constants.languages import LANGUAGES
from app.services.preferences.list_languages import list_languages


def test_lists_every_language_in_the_catalog_order():
    assert [item.code for item in list_languages()] == [language.code for language in LANGUAGES]


def test_a_language_is_mapped_field_by_field():
    arabic = next(item for item in list_languages() if item.code == "ar")

    assert arabic.model_dump() == {
        "code": "ar",
        "name": "Arabic",
        "native_name": "العربية",
        "direction": "rtl",
        "translated": False,
    }
