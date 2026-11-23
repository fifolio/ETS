from pydantic import BaseModel, Field


class CheckoutRequest(BaseModel):
    product: str = Field(max_length=20, description="nextmove, urgent, or topup")
    amount_usd: float | None = Field(
        default=None, description="Only for topup: dollars, from $1 to $50 in $0.25 steps"
    )
