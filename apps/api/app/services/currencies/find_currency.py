from app.schemas.currency_out import CurrencyOut

from app.services.currencies.list_currencies import list_currencies


def find_currency(code: str) -> CurrencyOut | None:
    return next((c for c in list_currencies() if c.code == code), None)
