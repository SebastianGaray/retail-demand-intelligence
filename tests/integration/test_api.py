# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false, reportUnknownVariableType=false

from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from pytest import TempPathFactory
from streamlit.testing.v1 import AppTest

from retail_demand.api.main import create_app
from retail_demand.application.generate_demo import generate_and_save_demo_data
from retail_demand.application.train import (
    evaluate_forecasters,
    save_champion_predictions,
    train_forecasters,
)
from retail_demand.artifacts.metadata import ForecastConfiguration
from retail_demand.configuration.settings import get_settings
from retail_demand.data.generation import DemoDataParameters


def prepare_artifacts(root: Path) -> Path:
    data = root / "data"
    artifacts = root / "artifacts"
    generate_and_save_demo_data(
        DemoDataParameters(stores=2, products=3, days=120, seed=42),
        data,
    )
    train_forecasters(data, artifacts, ForecastConfiguration(horizon=14, seed=42))
    evaluate_forecasters(data, artifacts)
    save_champion_predictions(artifacts)
    return artifacts


@pytest.fixture(scope="module")
def artifact_directory(tmp_path_factory: TempPathFactory) -> Path:
    return prepare_artifacts(tmp_path_factory.mktemp("api"))


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_api_exposes_saved_results(artifact_directory: Path) -> None:
    transport = ASGITransport(app=create_app(artifact_directory))
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        assert (await client.get("/health")).json() == {
            "status": "ready",
            "artifact_available": True,
        }
        metadata = await client.get("/metadata")
        assert metadata.status_code == 200
        assert metadata.json()["synthetic_data"] is True
        assert len((await client.get("/stores")).json()) == 2
        assert len((await client.get("/products")).json()) == 3

        forecast = await client.get(
            "/forecast",
            params={"store_id": "STORE_001", "product_id": "SKU_0001"},
        )
        assert forecast.status_code == 200, forecast.json()
        assert any(point["prediction"] is not None for point in forecast.json()["points"])

        risk = await client.get("/inventory-risk")
        assert risk.status_code == 200
        assert len(risk.json()) == 6

        performance = await client.get("/performance")
        assert performance.status_code == 200
        assert {metric["scope"] for metric in performance.json()} == {
            "overall",
            "store",
            "product",
        }


@pytest.mark.anyio
async def test_api_returns_clear_selection_and_artifact_errors(
    artifact_directory: Path,
    tmp_path: Path,
) -> None:
    ready_transport = ASGITransport(app=create_app(artifact_directory))
    missing_transport = ASGITransport(app=create_app(tmp_path / "missing"))
    async with (
        AsyncClient(transport=ready_transport, base_url="http://test") as ready,
        AsyncClient(transport=missing_transport, base_url="http://test") as missing,
    ):
        not_found = await ready.get(
            "/forecast",
            params={"store_id": "UNKNOWN", "product_id": "SKU_0001"},
        )
        assert not_found.status_code == 404
        assert not_found.json()["code"] == "selection_not_found"

        unavailable = await missing.get("/stores")
        assert unavailable.status_code == 503
        assert unavailable.json()["code"] == "artifacts_unavailable"
        assert (await missing.get("/health")).json()["status"] == "artifacts_missing"


def test_dashboard_survives_reruns(
    artifact_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("RETAIL_DEMAND_ARTIFACT_DIRECTORY", str(artifact_directory))
    get_settings.cache_clear()
    dashboard = AppTest.from_file("src/retail_demand/dashboard/app.py", default_timeout=60).run()

    assert not dashboard.exception
    dashboard.selectbox[0].set_value("es").run()
    assert not dashboard.exception
    assert dashboard.selectbox[0].value == "es"
    for page, page_id in (
        ("Explorador de Pronósticos", "forecast"),
        ("Riesgo de Inventario", "inventory"),
        ("Rendimiento del Modelo", "performance"),
        ("Acerca del Proyecto", "about"),
        ("Resumen", "overview"),
    ):
        next(button for button in dashboard.button if button.label == page).click().run()
        assert not dashboard.exception
        assert dashboard.session_state["dashboard_page"] == page_id
        if page_id == "about":
            assert any(page in element.value for element in dashboard.markdown)
        else:
            assert dashboard.title[0].value == page
    get_settings.cache_clear()
