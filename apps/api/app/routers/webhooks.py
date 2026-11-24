from fastapi import APIRouter, HTTPException, Request
from starlette.concurrency import run_in_threadpool

from app.exceptions.webhook_verification_error import WebhookVerificationError
from app.services.payments.whop.process_whop_webhook import process_whop_webhook

# Called by Whop, not by browsers: hidden from the public docs.
router = APIRouter(prefix="/webhooks", tags=["webhooks"], include_in_schema=False)


@router.post("/whop")
async def whop_webhook(request: Request) -> dict[str, str]:
    body = await request.body()  # the raw bytes: the signature covers exactly these
    try:
        result = await run_in_threadpool(process_whop_webhook, dict(request.headers), body)
    except WebhookVerificationError as exc:
        raise HTTPException(status_code=400, detail="Invalid webhook.") from exc
    return {"result": result}  # any other failure is a 500, so Whop retries
