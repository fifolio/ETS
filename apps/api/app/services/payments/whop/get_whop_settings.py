from app.constants.whop import WHOP_ENVIRONMENTS, WHOP_SKUS
from app.core.config import settings
from app.exceptions.configuration_error import ConfigurationError
from app.types.whop_settings import WhopSettings


def get_whop_settings() -> WhopSettings:
    """The Whop values of the environment chosen by WHOP_ENVIRONMENT (never a mix of both)."""
    environment = settings.whop_environment
    urls = WHOP_ENVIRONMENTS.get(environment)
    if urls is None:
        raise ConfigurationError(f"Unknown WHOP_ENVIRONMENT: {environment}")
    api_key = getattr(settings, f"whop_{environment}_api_key")
    if not api_key:
        raise ConfigurationError(f"WHOP_{environment.upper()}_API_KEY is not set")
    plan_ids = {
        sku: getattr(settings, f"whop_{environment}_plan_{sku.removeprefix('plan_')}")
        for sku in WHOP_SKUS
    }
    return WhopSettings(
        environment=environment,
        api_base=urls[0],
        checkout_host=urls[1],
        api_key=api_key,
        plan_ids=plan_ids,
        topup_product_id=getattr(settings, f"whop_{environment}_product_topup"),
    )
