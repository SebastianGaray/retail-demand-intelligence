from pathlib import Path

import pandas as pd

from retail_demand.application.generate_demo import generate_and_save_demo_data
from retail_demand.application.train import (
    evaluate_forecasters,
    save_champion_predictions,
    train_forecasters,
)
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
    assert load_model(first_artifact / "model.pkl")
