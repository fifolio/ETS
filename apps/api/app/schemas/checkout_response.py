from pydantic import BaseModel, Field


class CheckoutResponse(BaseModel):
    provider: str
    environment: str = Field(description="sandbox or production")
    checkout_id: str
    plan_id: str = Field(description="The provider's plan being bought, for the embedded checkout")
    checkout_url: str = Field(description="The provider's hosted payment page")
    amount_cents: int = Field(description="What the payment will charge, decided by the server")
    credits: int = Field(
        description="The credits it adds (a top-up, or the plan's monthly allowance)"
    )
