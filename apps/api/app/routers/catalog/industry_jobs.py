from typing import Annotated

from fastapi import APIRouter, Path, Response

from app.schemas.public_job import PublicJob
from app.services.catalog.list_industry_jobs import list_industry_jobs

router = APIRouter(tags=["catalog"])


@router.get(
    "/industries/{industry_id}/jobs",
    response_model=list[PublicJob],
    summary="The jobs of one industry, with their hourly rates",
    description="Public. An unknown industry returns an empty list.",
)
def industry_jobs(
    industry_id: Annotated[str, Path(min_length=1, max_length=64)], response: Response
) -> list[PublicJob]:
    response.headers["Cache-Control"] = "public, max-age=300"
    return list_industry_jobs(industry_id)
