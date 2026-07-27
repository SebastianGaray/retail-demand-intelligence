from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ForecastConfiguration(BaseModel):
    horizon: int = Field(default=28, ge=7, le=90)
    seed: int = Field(default=42, ge=0)
    recent_average_window: int = Field(default=28, ge=7, le=90)
    model_improvement_threshold: float = Field(default=0.02, ge=0, le=1)

    model_config = ConfigDict(frozen=True)


class DataPeriod(BaseModel):
    start: date
    end: date


class MetricResult(BaseModel):
    scope: Literal["overall", "store", "product"]
    identifier: str
    model: str
    mae: float
    wape: float | None
    mase: float | None
    observations: int


class ArtifactMetadata(BaseModel):
    schema_version: Literal["1"] = "1"
    created_at: datetime
    data_directory: str
    data_manifest_sha256: str | None
    configuration: ForecastConfiguration
    feature_schema_version: str
    feature_columns: list[str]
    train_period: DataPeriod
    validation_period: DataPeriod
    test_period: DataPeriod
    champion_model: str
    validation_metrics: list[MetricResult]
    test_metrics: list[MetricResult] = []
    model_parameters: dict[str, int | float | str]
    files: dict[str, str]
