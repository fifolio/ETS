from pydantic import BaseModel, Field


class PaymentEntryOut(BaseModel):
    sku: str = Field(description="plan_nextmove, plan_urgent, or topup")
    amount_cents: int
    credits: int
    status: str = Field(description="completed, failed, underpaid, or refunded")
    paid_at: str | None
