from dataclasses import dataclass


@dataclass(frozen=True)
class WhopSettings:
    environment: str
    api_base: str
    checkout_host: str
    api_key: str
    plan_ids: dict[str, str]  # sku -> Whop plan ID
    topup_product_id: str
    webhook_secret: str = ""
