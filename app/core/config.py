"""Central configuration. All settings come from environment variables / .env file."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Adaptive RAG Platform"
    environment: str = "dev"
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """Cached so the .env file is read only once."""
    return Settings()
