from pydantic import BaseModel, Field


class PlanOut(BaseModel):
    id: str
    name: str
    max_job_boards: int | None = Field(description="null means every job board")
    price_usd_per_month: float | None = Field(description="null means the price is not set")
