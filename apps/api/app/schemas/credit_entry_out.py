from pydantic import BaseModel, Field


class CreditEntryOut(BaseModel):
    amount: int = Field(
        description="Positive when credits were added, negative when they were used"
    )
    kind: str = Field(description="subscription, promotional, or purchased")
    reason: str
    created_at: str | None
