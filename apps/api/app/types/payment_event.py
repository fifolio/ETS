from dataclasses import dataclass


@dataclass(frozen=True)
class PaymentEvent:
    reference: str
    user_id: str
    plan: str
    paid: bool
