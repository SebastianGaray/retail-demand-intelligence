from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: Literal["local", "test"] = "local"
    data_directory: Path = Path("data")
    artifact_directory: Path = Path("demo_artifacts/v1.0.1")
    random_seed: int = Field(default=42, ge=0)
    forecast_horizon_days: int = Field(default=28, ge=1, le=365)
    default_locale: Literal["en", "es"] = "en"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="RETAIL_DEMAND_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
