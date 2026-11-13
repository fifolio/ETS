from fastapi import APIRouter, Response

from app.schemas.plans_response import PlansResponse
from app.services.job_boards.list_active_job_boards import list_active_job_boards
from app.services.payments.are_payments_enabled import are_payments_enabled
from app.services.plans.list_public_plans import list_public_plans

router = APIRouter(tags=["plans"])


@router.get(
    "/plans",
    response_model=PlansResponse,
    summary="The plans, how many job boards each includes, and whether upgrading is possible",
    description="Public. Used by the Settings page and the landing page.",
)
def plans(response: Response) -> PlansResponse:
    response.headers["Cache-Control"] = "public, max-age=60"
    return PlansResponse(
        plans=list_public_plans(list_active_job_boards()),
        payments_enabled=are_payments_enabled(),
    )
