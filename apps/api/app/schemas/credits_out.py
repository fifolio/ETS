from pydantic import BaseModel, Field


class CreditsOut(BaseModel):
    subscription: int = Field(description="The monthly allowance left")
    promotional: int = Field(description="Bonus credits left")
    purchased: int = Field(description="Top-up credits left")
    total: int
    credits_per_scan: int
