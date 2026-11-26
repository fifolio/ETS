from pydantic import BaseModel, Field


class SubscriptionOut(BaseModel):
    plan: str
    plan_name: str
    is_paid: bool
    current_period_end: str | None = Field(description="When the current period ends or renews")
    cancel_at_period_end: bool
    can_manage: bool = Field(description="True when a billing page exists for this subscription")
    can_cancel: bool = Field(description="True for a paid, not yet cancelled subscription")
