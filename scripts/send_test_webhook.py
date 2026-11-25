import base64
import hashlib
import hmac
import json
import os
import sys
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.services.payments.whop.get_whop_settings import get_whop_settings  # noqa: E402

USAGE = """Usage: send_test_webhook.py <kind> <args>
  succeeded  <user-id> <sku> <amount-usd> [payment-id] [checkout-id] [membership-id]
  failed     <user-id> <sku> <amount-usd> [payment-id] [checkout-id] [membership-id]
  renewal    <membership-id> <amount-usd> [payment-id]
  membership <membership-id> <status> [cancel_at_period_end true|false] [period-end-iso]
  refund     <payment-id> <amount-usd> [status] [membership-id]
sku: topup, plan_nextmove, or plan_urgent"""


def payment(payment_id, amount, metadata, checkout_id, membership_id):
    return {
        "id": payment_id,
        "status": "paid",
        "currency": "usd",
        "total": {"amount": f"{float(amount):.2f}", "currency": "usd", "decimals": 2},
        "tax_amount": None,
        "tax_behavior": None,
        "metadata": metadata,
        "checkout_configuration_id": checkout_id,
        "membership_id": membership_id,
        "member_id": "mber_test",
        "paid_at": datetime.now(UTC).isoformat(),
    }


def build(kind: str, a: list[str]) -> tuple[str, dict]:
    pay_id = f"pay_test_{uuid.uuid4().hex[:12]}"
    if kind in ("succeeded", "failed") and len(a) >= 3:
        user_id, sku, amount = a[:3]
        membership = (a[5] if len(a) > 5 else "mem_test") if sku.startswith("plan_") else None
        data = payment(
            a[3] if len(a) > 3 else pay_id,
            amount,
            {"ets_user_id": user_id, "ets_sku": sku},
            a[4] if len(a) > 4 else None,
            membership,
        )
        return f"payment.{kind}", data
    if kind == "renewal" and len(a) >= 2:
        return "payment.succeeded", payment(a[2] if len(a) > 2 else pay_id, a[1], {}, None, a[0])
    if kind == "membership" and len(a) >= 2:
        data = {
            "id": a[0],
            "status": a[1],
            "cancel_at_period_end": (a[2] == "true") if len(a) > 2 else False,
        }
        if len(a) > 3:
            data["current_period_end"] = a[3]
        return "membership.updated", data
    if kind == "refund" and len(a) >= 2:
        data = {
            "id": f"rf_test_{uuid.uuid4().hex[:10]}",
            "amount": float(a[1]),
            "status": a[2] if len(a) > 2 else "succeeded",
            "payment": {"id": a[0], "membership": {"id": a[3]} if len(a) > 3 else None},
        }
        return "refund.created", data
    sys.exit(USAGE)


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(USAGE)
    event_type, data = build(sys.argv[1], sys.argv[2:])
    message_id = f"msg_{uuid.uuid4().hex}"
    body = json.dumps(
        {
            "id": message_id,
            "type": event_type,
            "api_version": "v1",
            "data": data,
            "timestamp": datetime.now(UTC).isoformat(),
        }
    ).encode()
    timestamp = str(int(time.time()))
    secret = get_whop_settings().webhook_secret
    signed = f"{message_id}.{timestamp}.".encode() + body
    signature = base64.b64encode(
        hmac.new(secret.encode(), signed, hashlib.sha256).digest()
    ).decode()
    response = httpx.post(
        f"{os.environ.get('API_URL', 'http://localhost:8000')}/webhooks/whop",
        content=body,
        headers={
            "content-type": "application/json",
            "webhook-id": message_id,
            "webhook-timestamp": timestamp,
            "webhook-signature": f"v1,{signature}",
        },
    )
    print(response.status_code, response.text, f"({event_type}: {data.get('id')})")


if __name__ == "__main__":
    main()
