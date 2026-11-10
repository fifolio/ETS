import time
from typing import Any

from app.constants.stats import SITE_TOTALS_CACHE_SECONDS
from app.schemas.site_totals import SiteTotals
from app.services.stats.compute_site_totals import compute_site_totals

_cache: dict[str, Any] = {"value": None, "expires_at": 0.0}


def get_site_totals() -> SiteTotals:
    """The public totals, recomputed at most once every few minutes."""
    now = time.monotonic()
    cached = _cache["value"]
    if cached is not None and now < _cache["expires_at"]:
        return cached
    totals = compute_site_totals()
    _cache["value"] = totals
    _cache["expires_at"] = now + SITE_TOTALS_CACHE_SECONDS
    return totals
