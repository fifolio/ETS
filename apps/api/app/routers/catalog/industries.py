from fastapi import APIRouter, Response

from app.schemas.public_industry import PublicIndustry
from app.services.catalog.list_industries import list_industries

router = APIRouter(tags=["catalog"])


@router.get(
    "/industries",
    response_model=list[PublicIndustry],
    summary="All industries",
    description="Public. Used by the setup screen to pick an industry.",
)
def industries(response: Response) -> list[PublicIndustry]:
    response.headers["Cache-Control"] = "public, max-age=300"
    return list_industries()
