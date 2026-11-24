from dataclasses import dataclass

from app.types.payment_record import PaymentRecord


@dataclass(frozen=True)
class PaymentRows:
    existing: PaymentRecord | None  # this payment's own row
    row: PaymentRecord | None  # the row to update: its own, or the unclaimed checkout row
    template: PaymentRecord | None  # where the expected amounts come from
