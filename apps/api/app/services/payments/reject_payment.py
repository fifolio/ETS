import logging
from datetime import datetime

from app.services.payments.save_payment_result import save_payment_result
from app.types.payment_notice import PaymentNotice
from app.types.payment_record import PaymentRecord
from app.types.payment_result import PaymentResult
from app.types.payment_verdict import PaymentVerdict

logger = logging.getLogger(__name__)


def reject_payment(
    row: PaymentRecord | None, notice: PaymentNotice, verdict: PaymentVerdict, now: datetime
) -> str:
    """Record a payment that must not be applied. Nothing is granted."""
    logger.warning("Payment %s was not applied: %s", notice.payment_id, verdict.outcome)
    save_payment_result(
        row, notice, PaymentResult(verdict.expected_cents, 0, verdict.status, False), now
    )
    return verdict.outcome
