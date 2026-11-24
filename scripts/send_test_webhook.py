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


def main() -> None:
    if len(sys.argv) < 5 or sys.argv[1] not in ("succeeded", "failed"):
        sys.exit(
            "Usage: send_test_webhook.py <succeeded|failed> <user-id> <sku> <amount-usd> "
            "[payment-id] [checkout-id]\n  sku: topup, plan_nextmove, or plan_urgent"
        )
    kind, user_id, sku, amount = sys.argv[1:5]
    payment_id = sys.argv[5] if len(sys.argv) > 5 else f"pay_test_{uuid.uuid4().hex[:12]}"
    checkout_id = sys.argv[6] if len(sys.argv) > 6 else None

    message_id = f"msg_{uuid.uuid4().hex}"
    event = {
        "id": message_id,
        "type": f"payment.{kind}",
        "api_version": "v1",
        "timestamp": datetime.now(UTC).isoformat(),
        "data": {
            "id": payment_id,
            "status": "paid" if kind == "succeeded" else "open",
            "currency": "usd",
            "total": {"amount": f"{float(amount):.2f}", "currency": "usd", "decimals": 2},
            "tax_amount": None,
            "tax_behavior": None,
            "metadata": {"ets_user_id": user_id, "ets_sku": sku},
            "checkout_configuration_id": checkout_id,
            "membership_id": "mem_test" if sku.startswith("plan_") else None,
            "member_id": "mber_test",
            "paid_at": datetime.now(UTC).isoformat(),
        },
    }
    body = json.dumps(event).encode()
    timestamp = str(int(time.time()))
    secret = get_whop_settings().webhook_secret
    signed = f"{message_id}.{timestamp}.".encode() + body
    signature = base64.b64encode(hmac.new(secret.encode(), signed, hashlib.sha256).digest()).decode()

    base = os.environ.get("API_URL", "http://localhost:8000")
    response = httpx.post(
        f"{base}/webhooks/whop",
        content=body,
        headers={
            "content-type": "application/json",
            "webhook-id": message_id,
            "webhook-timestamp": timestamp,
            "webhook-signature": f"v1,{signature}",
        },
    )
    print(response.status_code, response.text, f"(payment {payment_id})")


if __name__ == "__main__":
    main()