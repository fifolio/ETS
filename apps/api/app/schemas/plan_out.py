from pydantic import BaseModel, Field


class PlanOut(BaseModel):
    id: str
    name: str
    job_board_count: int = Field(description="How many job boards the plan includes right now")
    price_usd_per_month: float | None = Field(
        description="Price in USD per month, or null if the plan is not for sale"
    )
