from app.services.payments.get_expected_cents import get_expected_cents
from app.types.payment_notice import PaymentNotice
from app.types.payment_record import PaymentRecord
from app.types.payment_verdict import PaymentVerdict


def judge_payment(notice: PaymentNotice, template: PaymentRecord | None) -> PaymentVerdict:
    """Decide whether a confirmed payment may be applied, without touching anything."""
    if notice.currency != "usd":
        return PaymentVerdict("unsupported_currency", "failed", 0)
    if notice.paid_cents is None:
        return PaymentVerdict("unverifiable", "failed", 0)
    if template is not None and (template.user_id != notice.user_id or template.sku != notice.sku):
        return PaymentVerdict("mismatch", "failed", 0)
    expected = get_expected_cents(notice, template)
    if expected is None:
        return PaymentVerdict("invalid_amount", "failed", 0)
    if notice.paid_cents < expected:
        return PaymentVerdict("underpaid", "underpaid", expected)
    return PaymentVerdict("ok", "completed", expected)
