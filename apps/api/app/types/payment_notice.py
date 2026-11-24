from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PaymentNotice:
    """A payment as reported by a provider, in provider-neutral terms."""

    provider: str
    environment: str
    payment_id: str
    checkout_id: str  # empty when the provider didn't say
    user_id: str
    sku: str
    paid_cents: int | None  # what was paid for the product, without added tax. None if unreadable
    currency: str
    membership_id: str | None
    customer_id: str | None
    paid_at: datetime | None
