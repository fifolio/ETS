from datetime import datetime

from app.services.payments.resolve_payment_rows import resolve_payment_rows
from app.services.payments.save_payment_result import save_payment_result
from app.types.payment_notice import PaymentNotice
from app.types.payment_result import PaymentResult


def mark_payment_failed(notice: PaymentNotice, now: datetime) -> str:
    """Record a failed payment. It never changes the plan or the credits."""
    row = resolve_payment_rows(notice).row
    if row is not None and row.applied:
        return "ignored"  # a late failure notice for a payment that was already applied
    amounts = PaymentResult(
        row.amount_cents if row else 0, row.credits if row else 0, "failed", False
    )
    save_payment_result(row, notice, amounts, now)
    return "failed"
