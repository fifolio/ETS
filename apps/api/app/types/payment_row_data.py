from typing import NotRequired, TypedDict


class PaymentRowData(TypedDict):
    userId: str
    provider: str
    environment: str
    sku: str
    providerCheckoutId: str | None
    amountCents: int
    currency: str
    credits: int
    status: str
    providerPaymentId: NotRequired[str]
    appliedAt: NotRequired[str]
