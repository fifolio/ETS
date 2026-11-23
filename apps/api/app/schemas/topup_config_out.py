from pydantic import BaseModel


class TopupConfigOut(BaseModel):
    min_usd: float
    max_usd: float
    step_usd: float
    credits_per_step: int
    credits_per_usd: int
