from app.schemas.payment_row import PaymentRow
from app.types.payment_record import PaymentRecord


def to_payment_record(row_id: str, row: PaymentRow) -> PaymentRecord:
    return PaymentRecord(
        row_id=row_id,
        user_id=row.userId,
        sku=row.sku,
        checkout_id=row.providerCheckoutId or "",
        payment_id=row.providerPaymentId or None,
        amount_cents=row.amountCents,
        credits=row.credits,
        status=row.status,
        applied=bool(row.appliedAt),
    )
