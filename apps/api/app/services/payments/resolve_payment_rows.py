from app.services.payments.find_payment_row import find_payment_row
from app.types.payment_notice import PaymentNotice
from app.types.payment_rows import PaymentRows


def resolve_payment_rows(notice: PaymentNotice) -> PaymentRows:
    """Find this payment's row, or the checkout's unclaimed pending row, to update.

    One checkout link can be paid twice. The second payment doesn't claim the first one's
    row: it gets a row of its own, with the amounts of the checkout as its template.
    """
    existing = find_payment_row("providerPaymentId", notice.payment_id)
    checkout_row = None
    if existing is None and notice.checkout_id:
        checkout_row = find_payment_row("providerCheckoutId", notice.checkout_id)
    claimable = checkout_row if checkout_row and not checkout_row.payment_id else None
    row = existing or claimable
    return PaymentRows(existing=existing, row=row, template=row or checkout_row)
