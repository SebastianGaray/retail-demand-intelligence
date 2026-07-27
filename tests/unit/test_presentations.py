from datetime import UTC, date, datetime
from pathlib import Path

import pandas as pd
import pytest

from retail_demand.application.read_results import ResultReader, calculate_inventory_risk
from retail_demand.artifacts.metadata import (
    ArtifactMetadata,
    DataPeriod,
    ForecastConfiguration,
)
from retail_demand.dashboard.translations import (
    TRANSLATIONS,
    missing_translation_keys,
    translate,
)


def metadata() -> ArtifactMetadata:
    return ArtifactMetadata(
        created_at=datetime.now(UTC),
        data_directory="data",
        data_manifest_sha256=None,
        configuration=ForecastConfiguration(horizon=7),
        feature_schema_version="1",
        feature_columns=[],
        train_period=DataPeriod(start=date(2024, 1, 1), end=date(2024, 1, 31)),
        validation_period=DataPeriod(start=date(2024, 2, 1), end=date(2024, 2, 7)),
        test_period=DataPeriod(start=date(2024, 2, 8), end=date(2024, 2, 14)),
        champion_model="recent_average",
        validation_metrics=[],
        model_parameters={},
        files={},
    )


def test_inventory_risk_uses_pre_forecast_inventory_and_thresholds() -> None:
    predictions = pd.DataFrame(
        {
            "store_id": ["STORE_001"] * 7,
            "product_id": ["SKU_001"] * 7,
            "prediction": [10.0] * 7,
        }
    )
    inventory = pd.DataFrame(
        {
            "store_id": ["STORE_001", "STORE_001"],
            "product_id": ["SKU_001", "SKU_001"],
            "date": [date(2024, 2, 7), date(2024, 2, 8)],
            "on_hand_quantity": [20.0, 100.0],
        }
    )

    result = calculate_inventory_risk(predictions, inventory, metadata(), 3, 10)

    assert result.iloc[0]["expected_demand"] == 70
    assert result.iloc[0]["current_inventory"] == 20
    assert result.iloc[0]["estimated_coverage_days"] == 2
    assert bool(result.iloc[0]["stockout_risk"]) is True
    assert bool(result.iloc[0]["excess_inventory"]) is False


def test_missing_artifacts_are_detected_without_training(tmp_path: Path) -> None:
    assert ResultReader(tmp_path).available() is False


def test_translations_have_matching_nonempty_keys() -> None:
    assert missing_translation_keys() == {"en": set(), "es": set()}
    assert all(
        value.strip() for translations in TRANSLATIONS.values() for value in translations.values()
    )


def test_missing_translation_key_is_explicit() -> None:
    with pytest.raises(KeyError, match="missing translation"):
        translate("es", "missing.key")
