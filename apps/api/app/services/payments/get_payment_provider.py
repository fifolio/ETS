from app.core.config import settings
from app.exceptions.configuration_error import ConfigurationError
from app.services.payments.disabled_provider import DisabledProvider
from app.types.payment_provider import PaymentProvider

PROVIDERS: dict[str, type[PaymentProvider]] = {
    "none": DisabledProvider,
}


def get_payment_provider() -> PaymentProvider:
    provider_class = PROVIDERS.get(settings.payment_provider)
    if provider_class is None:
        raise ConfigurationError(f"Unknown PAYMENT_PROVIDER: {settings.payment_provider}")
    return provider_class()
