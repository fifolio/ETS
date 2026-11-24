from pydantic import BaseModel


class PaymentRow(BaseModel):
    """Shape of a row in the payments table, used by the Appwrite SDK for typed access."""

    userId: str = ""
    sku: str = ""
    providerCheckoutId: str | None = None
    providerPaymentId: str | None = None
    amountCents: int = 0
    credits: int = 0
    status: str = "pending"
    appliedAt: str | None = None
