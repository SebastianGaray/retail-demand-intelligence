# pyright: reportUnusedFunction=false

from pathlib import Path
from typing import Annotated, cast

import pandas as pd
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse

from retail_demand import __version__
from retail_demand.api.schemas import (
    EntityOption,
    ErrorResponse,
    ForecastPoint,
    ForecastResponse,
    HealthResponse,
    InventoryRiskItem,
    PerformanceMetric,
    ProjectMetadataResponse,
)
from retail_demand.application.read_results import (
    ArtifactsUnavailableError,
    ResultReader,
    SelectionNotFoundError,
)
from retail_demand.configuration.settings import get_settings

ERROR_RESPONSES: dict[int | str, dict[str, object]] = {
    404: {"model": ErrorResponse},
    422: {"model": ErrorResponse},
    503: {"model": ErrorResponse},
}


def create_app(artifact_directory: Path | None = None) -> FastAPI:
    app = FastAPI(
        title="Retail Demand Intelligence",
        version=__version__,
        description="Local read-only interface for saved retail forecasting artifacts.",
    )
    reader = ResultReader(artifact_directory or get_settings().artifact_directory)

    @app.exception_handler(ArtifactsUnavailableError)
    async def unavailable_handler(
        _: Request,
        error: ArtifactsUnavailableError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=503,
            content=ErrorResponse(
                code="artifacts_unavailable",
                message=str(error),
            ).model_dump(),
        )

    @app.exception_handler(SelectionNotFoundError)
    async def selection_handler(
        _: Request,
        error: SelectionNotFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content=ErrorResponse(
                code="selection_not_found",
                message=str(error),
            ).model_dump(),
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(_: Request, error: ValueError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                code="invalid_request",
                message=str(error),
            ).model_dump(),
        )

    @app.get("/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        available = reader.available()
        return HealthResponse(
            status="ready" if available else "artifacts_missing",
            artifact_available=available,
        )

    @app.get("/metadata", response_model=ProjectMetadataResponse)
    async def project_metadata() -> ProjectMetadataResponse:
        if not reader.available():
            return ProjectMetadataResponse(
                name="Retail Demand Intelligence",
                project_version=__version__,
                artifact_available=False,
            )
        metadata = reader.metadata()
        overview = reader.overview()
        return ProjectMetadataResponse(
            name="Retail Demand Intelligence",
            project_version=__version__,
            artifact_available=True,
            artifact_version=metadata.schema_version,
            current_model=metadata.champion_model,
            created_at=metadata.created_at,
            synthetic_data=bool(overview["synthetic"]),
        )

    @app.get("/stores", response_model=list[EntityOption], responses=ERROR_RESPONSES)
    async def stores() -> list[EntityOption]:
        return [EntityOption.model_validate(item) for item in reader.stores()]

    @app.get("/products", response_model=list[EntityOption], responses=ERROR_RESPONSES)
    async def products() -> list[EntityOption]:
        return [EntityOption.model_validate(item) for item in reader.products()]

    @app.get("/forecast", response_model=ForecastResponse, responses=ERROR_RESPONSES)
    async def forecast(
        store_id: Annotated[str, Query(min_length=1)],
        product_id: Annotated[str, Query(min_length=1)],
    ) -> ForecastResponse:
        model, frame = reader.forecast(store_id, product_id)
        return ForecastResponse(
            store_id=store_id,
            product_id=product_id,
            model=model,
            points=[
                ForecastPoint(
                    date=pd.Timestamp(cast(str, row.date)).date(),
                    historical_demand=float(cast(float, row.quantity)),
                    actual=_optional_float(row.actual),
                    prediction=_optional_float(row.prediction),
                    error=_optional_float(row.error),
                    price=float(cast(float, row.price)),
                    promotion=bool(row.promotion),
                    stockout=bool(row.stockout),
                )
                for row in frame.itertuples()
            ],
        )

    @app.get(
        "/inventory-risk",
        response_model=list[InventoryRiskItem],
        responses=ERROR_RESPONSES,
    )
    async def inventory_risk(
        stockout_coverage_days: Annotated[float, Query(ge=0)] = 7,
        excess_coverage_days: Annotated[float, Query(gt=0)] = 45,
        store_id: str | None = None,
        product_id: str | None = None,
    ) -> list[InventoryRiskItem]:
        frame = reader.inventory_risk(
            stockout_coverage_days,
            excess_coverage_days,
            store_id,
            product_id,
        )
        return [
            InventoryRiskItem(
                store_id=str(row.store_id),
                product_id=str(row.product_id),
                expected_demand=float(cast(float, row.expected_demand)),
                current_inventory=float(cast(float, row.current_inventory)),
                estimated_coverage_days=_optional_float(row.estimated_coverage_days),
                stockout_risk=bool(row.stockout_risk),
                excess_inventory=bool(row.excess_inventory),
            )
            for row in frame.itertuples()
        ]

    @app.get(
        "/performance",
        response_model=list[PerformanceMetric],
        responses=ERROR_RESPONSES,
    )
    async def performance(
        scope: Annotated[str | None, Query(pattern="^(overall|store|product)$")] = None,
        identifier: str | None = None,
    ) -> list[PerformanceMetric]:
        return [
            PerformanceMetric.model_validate(item)
            for item in _records(reader.performance(scope, identifier))
        ]

    return app


def _optional_float(value: object) -> float | None:
    numeric = cast(float | None, value)
    return None if numeric is None or pd.isna(numeric) else float(numeric)


def _records(frame: pd.DataFrame) -> list[dict[str, object]]:
    return [
        {str(key): value for key, value in record.items()}
        for record in frame.to_dict(orient="records")
    ]


app = create_app()
