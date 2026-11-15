from typing import Any

from app.schemas.preferences_out import PreferencesOut
from app.services.preferences.effective_language import effective_language
from app.services.preferences.normalize_language import normalize_language
from app.services.preferences.normalize_theme import normalize_theme


def build_preferences(prefs: dict[str, Any]) -> PreferencesOut:
    """The user's theme and language, cleaned of anything unexpected."""
    language = normalize_language(prefs.get("language"))
    shown = effective_language(language)
    return PreferencesOut(
        theme=normalize_theme(prefs.get("theme")),
        language=language,
        effective_language=shown.code,
        direction=shown.direction,
    )
