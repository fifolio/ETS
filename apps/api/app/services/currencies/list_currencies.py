import time
from typing import Any

from app.core.config import settings
from app.schemas.currency_out import CurrencyOut
from app.schemas.currency_row import CurrencyRow
from app.services.appwrite.iter_table_rows import iter_table_rows

_cache: dict[str, Any] = {"value": None, "expires_at": 0.0}
CACHE_SECONDS = 2592000  # 30 days


def list_currencies() -> list[CurrencyOut]:
    now = time.monotonic()
    if _cache["value"] is not None and now < _cache["expires_at"]:
        return list(_cache["value"])
    rows = iter_table_rows(settings.appwrite_currencies_table_id, CurrencyRow)
    result = sorted(
        [
            CurrencyOut(
                code=r.id, name=r.data.name, symbol=r.data.symbol, rate_from_usd=r.data.rateFromUsd
            )
            for r in rows
        ],
        key=lambda c: c.code,
    )
    _cache["value"] = result
    _cache["expires_at"] = now + CACHE_SECONDS
    return list(result)
