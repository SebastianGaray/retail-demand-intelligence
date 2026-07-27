from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = "local"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="RETAIL_DEMAND_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
