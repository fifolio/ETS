from pydantic import BaseModel


class SubscriptionRow(BaseModel):
    """Shape of a row in the subscriptions table (the row ID is the user ID)."""

    plan: str = "explore"
    status: str = "active"
    cancelAtPeriodEnd: bool = False
    providerSubscriptionId: str | None = None
    currentPeriodEnd: str | None = None
    creditsRenewedAt: str | None = None
    renewalReminderSentAt: str | None = None
