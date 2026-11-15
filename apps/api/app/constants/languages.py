from app.types.language_definition import LanguageDefinition

DEFAULT_LANGUAGE = "en"

# `translated` says whether the web app and the extension have real text for the language.
# Until it is True, people who pick the language see English. Flip it here when a translation ships.
LANGUAGES = (
    LanguageDefinition("en", "English", "English", "ltr", True),
    LanguageDefinition("ar", "Arabic", "العربية", "rtl", False),
    LanguageDefinition("fr", "French", "Français", "ltr", False),
    LanguageDefinition("es", "Spanish", "Español", "ltr", False),
    LanguageDefinition("de", "German", "Deutsch", "ltr", False),
    LanguageDefinition("pt", "Portuguese", "Português", "ltr", False),
    LanguageDefinition("it", "Italian", "Italiano", "ltr", False),
    LanguageDefinition("nl", "Dutch", "Nederlands", "ltr", False),
    LanguageDefinition("tr", "Turkish", "Türkçe", "ltr", False),
    LanguageDefinition("ru", "Russian", "Русский", "ltr", False),
    LanguageDefinition("uk", "Ukrainian", "Українська", "ltr", False),
    LanguageDefinition("pl", "Polish", "Polski", "ltr", False),
    LanguageDefinition("hi", "Hindi", "हिन्दी", "ltr", False),
    LanguageDefinition("bn", "Bengali", "বাংলা", "ltr", False),
    LanguageDefinition("ur", "Urdu", "اردو", "rtl", False),
    LanguageDefinition("fa", "Persian", "فارسی", "rtl", False),
    LanguageDefinition("he", "Hebrew", "עברית", "rtl", False),
    LanguageDefinition("id", "Indonesian", "Bahasa Indonesia", "ltr", False),
    LanguageDefinition("vi", "Vietnamese", "Tiếng Việt", "ltr", False),
    LanguageDefinition("th", "Thai", "ไทย", "ltr", False),
    LanguageDefinition("zh", "Chinese", "中文", "ltr", False),
    LanguageDefinition("ja", "Japanese", "日本語", "ltr", False),
    LanguageDefinition("ko", "Korean", "한국어", "ltr", False),
)
