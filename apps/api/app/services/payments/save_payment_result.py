from datetime import datetime

from app.services.payments.create_payment_row import create_payment_row
from app.services.payments.update_payment_row import update_payment_row
from app.types.payment_notice import PaymentNotice
from app.types.payment_record import PaymentRecord
from app.types.payment_result import PaymentResult


def save_payment_result(
    row: PaymentRecord | None, notice: PaymentNotice, result: PaymentResult, now: datetime
) -> None:
    """Record what happened to a payment: update its row, or create one."""
    changes = {"providerPaymentId": notice.payment_id, "status": result.status}
    if result.applied:
        changes["appliedAt"] = now.isoformat()
    if row is not None:
        update_payment_row(row.row_id, changes)
        return
    create_payment_row(
        {
            "userId": notice.user_id,
            "provider": notice.provider,
            "environment": notice.environment,
            "sku": notice.sku,
            "providerCheckoutId": notice.checkout_id or None,
            "amountCents": result.amount_cents,
            "currency": notice.currency or "usd",
            "credits": result.credits,
            **changes,
        }
    )
