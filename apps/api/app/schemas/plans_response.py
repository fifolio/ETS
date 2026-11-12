from pydantic import BaseModel, Field

from app.schemas.plan_out import PlanOut


class PlansResponse(BaseModel):
    plans: list[PlanOut]
    payments_enabled: bool = Field(
        description="Whether payments are enabled for the current environment. \
            If false, all plans are free."
    )
