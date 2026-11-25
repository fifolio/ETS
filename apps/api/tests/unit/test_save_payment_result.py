from datetime import UTC, datetime

import app.services.payments.save_payment_result as module
from app.types.payment_result import PaymentResult
from tests.conftest import make_notice, make_record

NOW = datetime(2026, 12, 1, 12, 0, tzinfo=UTC)


def install(monkeypatch):
    updated, created = [], []
    monkeypatch.setattr(
        module, "update_payment_row", lambda row_id, data: updated.append((row_id, data))
    )
    monkeypatch.setattr(module, "create_payment_row", created.append)
    return updated, created


def test_an_existing_row_is_updated_with_the_payment_id_status_and_applied_date(monkeypatch):
    updated, created = install(monkeypatch)

    module.save_payment_result(
        make_record(), make_notice(), PaymentResult(500, 40, "completed", True), NOW
    )

    assert updated == [
        (
            "row-1",
            {"providerPaymentId": "pay_1", "status": "completed", "appliedAt": NOW.isoformat()},
        )
    ]
    assert created == []


def test_a_payment_without_a_row_gets_a_complete_new_row(monkeypatch):
    updated, created = install(monkeypatch)

    module.save_payment_result(None, make_notice(), PaymentResult(500, 40, "completed", True), NOW)

    row = created[0]
    assert (row["userId"], row["sku"], row["amountCents"], row["credits"]) == (
        "user-1",
        "topup",
        500,
        40,
    )
    assert (row["providerPaymentId"], row["status"], row["appliedAt"]) == (
        "pay_1",
        "completed",
        NOW.isoformat(),
    )
    assert updated == []


def test_a_payment_without_a_checkout_id_stores_none_so_the_unique_index_isnt_violated(monkeypatch):
    _, created = install(monkeypatch)

    module.save_payment_result(
        None, make_notice(checkout_id=""), PaymentResult(0, 0, "failed", False), NOW
    )

    assert created[0]["providerCheckoutId"] is None and "appliedAt" not in created[0]
