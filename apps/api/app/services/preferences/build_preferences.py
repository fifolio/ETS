from typing import Any

from app.schemas.preferences_out import PreferencesOut
from app.services.currencies.find_currency import find_currency
from app.services.currencies.list_currencies import list_currencies
from app.services.preferences.effective_language import effective_language
from app.services.preferences.normalize_currency import normalize_currency
from app.services.preferences.normalize_language import normalize_language
from app.services.preferences.normalize_theme import normalize_theme

DEFAULT_CURRENCY_SYMBOL = "$"


def build_preferences(prefs: dict[str, Any]) -> PreferencesOut:
    language = normalize_language(prefs.get("language"))
    shown = effective_language(language)
    codes = {c.code for c in list_currencies()}
    currency_code = normalize_currency(prefs.get("currency"), codes)
    currency = find_currency(currency_code)
    return PreferencesOut(
        theme=normalize_theme(prefs.get("theme")),
        language=language,
        effective_language=shown.code,
        direction=shown.direction,
        currency=currency_code,
        currency_symbol=currency.symbol if currency else DEFAULT_CURRENCY_SYMBOL,
    )
