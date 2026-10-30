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
    appwrite_cv_bucket_id: str = ""

    cors_origins: str = ""


settings = Settings()
