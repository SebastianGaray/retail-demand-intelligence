from pathlib import Path

import pandas as pd
import pytest

from retail_demand.application.demo_artifacts import build_demo_artifacts
from retail_demand.application.generate_demo import generate_and_save_demo_data
from retail_demand.application.read_results import ResultReader
from retail_demand.application.train import (
    evaluate_forecasters,
    save_champion_predictions,
    train_forecasters,
)
from retail_demand.artifacts.demo_bundle import validate_demo_artifact_bundle
from retail_demand.artifacts.metadata import ForecastConfiguration
from retail_demand.artifacts.store import load_metadata, load_model
from retail_demand.data.generation import DemoDataParameters


def test_training_pipeline_saves_reproducible_artifacts(tmp_path: Path) -> None:
    data = tmp_path / "data"
    first_artifact = tmp_path / "first"
    second_artifact = tmp_path / "second"
    generate_and_save_demo_data(
        DemoDataParameters(stores=2, products=3, days=120, seed=42),
        data,
    )
    configuration = ForecastConfiguration(horizon=14, seed=42)

    first = train_forecasters(data, first_artifact, configuration)
    train_forecasters(data, second_artifact, configuration)
    metrics = evaluate_forecasters(data, first_artifact)
    predictions_path = save_champion_predictions(first_artifact)

    pd.testing.assert_frame_equal(
        pd.read_parquet(first_artifact / "validation_predictions.parquet"),
        pd.read_parquet(second_artifact / "validation_predictions.parquet"),
    )
    predictions = pd.read_parquet(predictions_path)
    metadata = load_metadata(first_artifact / "metadata.json")

    assert first.train_period.end < first.validation_period.start
    assert first.validation_period.end < first.test_period.start
    assert set(metrics["scope"]) == {"overall", "store", "product"}
    assert set(metrics["model"]) == {"recent_average", "seasonal_naive", "lightgbm"}
    assert predictions["model"].unique().tolist() == [metadata.champion_model]
    assert (predictions["prediction"] >= 0).all()
    assert metadata.schema_version == "1"
    assert metadata.test_metrics
    assert metadata.data_manifest_sha256
    assert load_model(first_artifact / "model.pkl", metadata.files["model.pkl"])

    model_path = tmp_path / "untrusted-model.pkl"
    model_path.write_bytes(b"untrusted model payload")
    with pytest.raises(ValueError, match="checksum mismatch"):
        load_model(model_path, metadata.files["model.pkl"])

    first_bundle = tmp_path / "v1.0.0"
    second_bundle = tmp_path / "second" / "v1.0.0"
    first_manifest = build_demo_artifacts(first_artifact, first_bundle)
    build_demo_artifacts(first_artifact, second_bundle)

    assert first_manifest.store_count == 2
    assert first_manifest.product_count == 3
    assert set(first_manifest.files) == {
        "metadata.json",
        "predictions.parquet",
        "data/stores.parquet",
        "data/products.parquet",
        "data/daily_prices.parquet",
        "data/promotions.parquet",
        "data/daily_sales.parquet",
        "data/daily_inventory.parquet",
        "data/calendar.parquet",
    }
    assert ResultReader(first_bundle).available()
    assert {
        path.relative_to(first_bundle): path.read_bytes()
        for path in first_bundle.rglob("*")
        if path.is_file()
    } == {
        path.relative_to(second_bundle): path.read_bytes()
        for path in second_bundle.rglob("*")
        if path.is_file()
    }

    (first_bundle / "predictions.parquet").write_bytes(b"changed")
    with pytest.raises(ValueError, match="checksum"):
        validate_demo_artifact_bundle(first_bundle)
