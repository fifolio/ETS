from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env", extra="ignore")
    groq_api_key: str = ""
    groq_model: str = ""
    groq_fallback_model: str = ""

    appwrite_endpoint: str = ""
    appwrite_project_id: str = ""
    appwrite_api_key: str = ""
    appwrite_database_id: str = ""
    appwrite_cvs_table_id: str = ""
    appwrite_scans_table_id: str = ""
    appwrite_testimonials_table_id: str = ""
    appwrite_usage_table_id: str = ""
    appwrite_industries_table_id: str = ""
    appwrite_jobs_table_id: str = ""
    appwrite_extensions_table_id: str = ""
    appwrite_job_boards_table_id: str = ""
    appwrite_suggestions_table_id: str = ""
    appwrite_currencies_table_id: str = ""
    appwrite_subscriptions_table_id: str = ""
    appwrite_credit_balances_table_id: str = ""
    appwrite_credit_ledger_table_id: str = ""
    appwrite_payments_table_id: str = ""

    cors_origins: str = ""

    cleanup_token: str = ""  # shared secret for the scheduled cleanup; empty disables it
    setup_deadline_hours: int = 48

    feedback_min_days: int = 7
    feedback_min_scans: int = 15

    payment_provider: str = ""

    payment_success_url: str = ""
    whop_environment: str = ""  # sandbox or production
    whop_sandbox_api_key: str = ""
    whop_sandbox_webhook_secret: str = ""
    whop_sandbox_plan_nextmove: str = ""
    whop_sandbox_plan_urgent: str = ""
    whop_sandbox_product_topup: str = ""
    whop_production_api_key: str = ""
    whop_production_webhook_secret: str = ""
    whop_production_plan_nextmove: str = ""
    whop_production_plan_urgent: str = ""
    whop_production_product_topup: str = ""


settings = Settings()
