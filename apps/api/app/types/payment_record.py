from dataclasses import dataclass


@dataclass(frozen=True)
class PaymentRecord:
    row_id: str
    user_id: str
    sku: str
    checkout_id: str
    payment_id: str | None
    amount_cents: int
    credits: int
    status: str
    applied: bool
