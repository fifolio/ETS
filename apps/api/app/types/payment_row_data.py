from typing import TypedDict


class PaymentRowData(TypedDict):
    userId: str
    provider: str
    environment: str
    sku: str
    providerCheckoutId: str
    amountCents: int
    currency: str
    status: str
    credits: int
