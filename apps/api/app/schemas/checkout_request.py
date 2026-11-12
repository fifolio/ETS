from pydantic import BaseModel, Field


class CheckoutRequest(BaseModel):
    plan: str = Field(max_length=20, description="The plan to upgrade to: nextmove or urgent")
