from pathlib import Path

import pytest
from pydantic import ValidationError

from retail_demand.configuration.settings import Settings


def test_settings_read_typed_environment_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("RETAIL_DEMAND_DATA_DIRECTORY", "/tmp/retail-data")
    monkeypatch.setenv("RETAIL_DEMAND_FORECAST_HORIZON_DAYS", "14")
    monkeypatch.setenv("RETAIL_DEMAND_DEFAULT_LOCALE", "es")

    settings = Settings()

    assert settings.data_directory == Path("/tmp/retail-data")
    assert settings.forecast_horizon_days == 14
    assert settings.default_locale == "es"


def test_settings_reject_invalid_forecast_horizon() -> None:
    with pytest.raises(ValidationError):
        Settings(forecast_horizon_days=0)


def test_settings_use_the_tracked_demo_bundle_by_default() -> None:
    assert Settings().artifact_directory == Path("demo_artifacts/v0.1.0")
