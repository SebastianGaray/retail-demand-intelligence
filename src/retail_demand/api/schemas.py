from datetime import date, datetime

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    code: str
    message: str


class HealthResponse(BaseModel):
    status: str
    artifact_available: bool


class ProjectMetadataResponse(BaseModel):
    name: str
    project_version: str
    artifact_available: bool
    artifact_version: str | None = None
    current_model: str | None = None
    created_at: datetime | None = None
    synthetic_data: bool | None = None


class EntityOption(BaseModel):
    id: str
    name: str


class ForecastPoint(BaseModel):
    date: date
    historical_demand: float
    actual: float | None
    prediction: float | None
    error: float | None
    price: float
    promotion: bool
    stockout: bool


class ForecastResponse(BaseModel):
    store_id: str
    product_id: str
    model: str
    points: list[ForecastPoint]


class InventoryRiskItem(BaseModel):
    store_id: str
    product_id: str
    expected_demand: float
    current_inventory: float
    estimated_coverage_days: float | None
    stockout_risk: bool
    excess_inventory: bool


class PerformanceMetric(BaseModel):
    scope: str
    identifier: str
    model: str
    mae: float
    wape: float | None
    mase: float | None
    observations: int
