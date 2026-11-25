from dataclasses import dataclass


@dataclass(frozen=True)
class RefundNotice:
    provider: str
    refund_id: str
    payment_id: str
    membership_id: str | None
    amount_cents: int | None
    status: str
