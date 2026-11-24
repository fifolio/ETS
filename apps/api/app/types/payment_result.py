from dataclasses import dataclass


@dataclass(frozen=True)
class PaymentResult:
    amount_cents: int
    credits: int
    status: str
    applied: bool
