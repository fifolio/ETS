from dataclasses import dataclass


@dataclass(frozen=True)
class PaymentVerdict:
    outcome: str  # "ok", or why the payment can't be applied
    status: str  # the status to store on the payment row
    expected_cents: int
