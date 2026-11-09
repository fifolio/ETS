from pydantic import BaseModel


class PublicJob(BaseModel):
    id: str
    name: str
    hourly_rate_usd: float
