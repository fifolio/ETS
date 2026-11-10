from fastapi import APIRouter, Response

from app.constants.stats import SITE_TOTALS_CACHE_SECONDS
from app.schemas.site_totals import SiteTotals
from app.services.stats.get_site_totals import get_site_totals

router = APIRouter(tags=["stats"])


@router.get(
    "/stats/totals",
    response_model=SiteTotals,
    summary="Public totals for the landing page",
    description="Users, scans, time saved, and cash saved, /"
    "added up over everyone. Public and cached.",
)
def site_totals(response: Response) -> SiteTotals:
    response.headers["Cache-Control"] = f"public, max-age={SITE_TOTALS_CACHE_SECONDS}"
    return get_site_totals()