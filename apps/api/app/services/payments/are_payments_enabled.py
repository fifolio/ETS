from app.core.config import settings


def are_payments_enabled() -> bool:
    return settings.payment_provider != "none"
