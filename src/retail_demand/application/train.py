from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import cast

import pandas as pd
from sklearn.pipeline import Pipeline

from retail_demand.artifacts.metadata import (
    ArtifactMetadata,
    DataPeriod,
    ForecastConfiguration,
    MetricResult,
)
from retail_demand.artifacts.store import (
    load_metadata,
    load_model,
    save_metadata,
    save_model,
    sha256,
)
from retail_demand.data.loading import read_parquet_frame
from retail_demand.data.validation import load_retail_datasets
from retail_demand.features.temporal import (
    FEATURE_COLUMNS,
    FEATURE_SCHEMA_VERSION,
    build_feature_table,
    eligible_feature_rows,
)
from retail_demand.modeling.baselines import recent_average, seasonal_naive
from retail_demand.modeling.evaluation import calculate_metrics
from retail_demand.modeling.lightgbm import fit_model, predict

MODEL_NAME = "lightgbm"
RECENT_AVERAGE = "recent_average"
SEASONAL_NAIVE = "seasonal_naive"


def train_forecasters(
    data_directory: Path,
    artifact_directory: Path,
    configuration: ForecastConfiguration,
) -> ArtifactMetadata:
    frame = _load_features(data_directory, configuration.horizon)
    periods = _split_periods(frame, configuration.horizon)
    train = _period(frame, periods.train)
    validation = _period(frame, periods.validation)
    validation_predictions = _predict_all(
        train,
        validation,
        fit_model(train, configuration.seed),
        configuration.recent_average_window,
        "validation",
    )
    validation_metrics = calculate_metrics(validation_predictions, train)
    champion = _select_champion(validation_metrics, configuration.model_improvement_threshold)

    final_training = frame[frame["date"] <= pd.Timestamp(periods.validation.end)]
    final_model = fit_model(final_training, configuration.seed)
    artifact_directory.mkdir(parents=True, exist_ok=True)
    model_path = artifact_directory / "model.pkl"
    model_checksum = save_model(final_model, model_path)
    validation_path = artifact_directory / "validation_predictions.parquet"
    validation_predictions.to_parquet(validation_path, index=False)

    metadata = ArtifactMetadata(
        created_at=datetime.now(UTC),
        data_directory=str(data_directory),
        data_manifest_sha256=_manifest_checksum(data_directory),
        configuration=configuration,
        feature_schema_version=FEATURE_SCHEMA_VERSION,
        feature_columns=FEATURE_COLUMNS,
        train_period=periods.train,
        validation_period=periods.validation,
        test_period=periods.test,
        champion_model=champion,
        validation_metrics=_metric_results(validation_metrics),
        model_parameters={
            "n_estimators": 200,
            "learning_rate": 0.05,
            "num_leaves": 31,
            "random_state": configuration.seed,
            "n_jobs": 1,
        },
        files={
            "model.pkl": model_checksum,
            "validation_predictions.parquet": sha256(validation_path),
        },
    )
    save_metadata(metadata, artifact_directory / "metadata.json")
    return metadata


def evaluate_forecasters(data_directory: Path, artifact_directory: Path) -> pd.DataFrame:
    metadata_path = artifact_directory / "metadata.json"
    metadata = load_metadata(metadata_path)
    frame = _load_features(data_directory, metadata.configuration.horizon)
    history = frame[frame["date"] < pd.Timestamp(metadata.test_period.start)]
    test = _period(frame, metadata.test_period)
    predictions = _predict_all(
        history,
        test,
        load_model(artifact_directory / "model.pkl", metadata.files["model.pkl"]),
        metadata.configuration.recent_average_window,
        "test",
    )
    metrics = calculate_metrics(predictions, history)
    predictions_path = artifact_directory / "evaluation_predictions.parquet"
    metrics_path = artifact_directory / "metrics.json"
    predictions.to_parquet(predictions_path, index=False)
    metrics_path.write_text(
        pd.DataFrame(_metric_dicts(metrics)).to_json(orient="records", indent=2) + "\n",
        encoding="utf-8",
    )
    files = metadata.files | {
        "evaluation_predictions.parquet": sha256(predictions_path),
        "metrics.json": sha256(metrics_path),
    }
    save_metadata(
        metadata.model_copy(update={"test_metrics": _metric_results(metrics), "files": files}),
        metadata_path,
    )
    return metrics


def save_champion_predictions(artifact_directory: Path) -> Path:
    metadata_path = artifact_directory / "metadata.json"
    metadata = load_metadata(metadata_path)
    evaluation_path = artifact_directory / "evaluation_predictions.parquet"
    predictions = read_parquet_frame(evaluation_path)
    champion = predictions[predictions["model"] == metadata.champion_model].copy()
    output = artifact_directory / "predictions.parquet"
    champion.to_parquet(output, index=False)
    files = metadata.files | {"predictions.parquet": sha256(output)}
    save_metadata(metadata.model_copy(update={"files": files}), metadata_path)
    return output


class _Periods:
    def __init__(self, train: DataPeriod, validation: DataPeriod, test: DataPeriod) -> None:
        self.train = train
        self.validation = validation
        self.test = test


def _load_features(data_directory: Path, horizon: int) -> pd.DataFrame:
    datasets = load_retail_datasets(data_directory)
    return eligible_feature_rows(build_feature_table(datasets, horizon))


def _split_periods(frame: pd.DataFrame, horizon: int) -> _Periods:
    minimum = pd.Timestamp(frame["date"].min()).date()
    maximum = pd.Timestamp(frame["date"].max()).date()
    test_start = maximum - timedelta(days=horizon - 1)
    validation_end = test_start - timedelta(days=1)
    validation_start = validation_end - timedelta(days=horizon - 1)
    train_end = validation_start - timedelta(days=1)
    if minimum > train_end:
        raise ValueError("not enough eligible history for train, validation, and test periods")
    return _Periods(
        DataPeriod(start=minimum, end=train_end),
        DataPeriod(start=validation_start, end=validation_end),
        DataPeriod(start=test_start, end=maximum),
    )


def _period(frame: pd.DataFrame, period: DataPeriod) -> pd.DataFrame:
    dates = pd.to_datetime(frame["date"])
    return frame[(dates >= pd.Timestamp(period.start)) & (dates <= pd.Timestamp(period.end))].copy()


def _predict_all(
    history: pd.DataFrame,
    targets: pd.DataFrame,
    model: Pipeline,
    average_window: int,
    split: str,
) -> pd.DataFrame:
    predictions = [
        _prediction_rows(
            targets,
            RECENT_AVERAGE,
            recent_average(history, targets, average_window),
            split,
        ),
        _prediction_rows(targets, SEASONAL_NAIVE, seasonal_naive(history, targets), split),
        _prediction_rows(targets, MODEL_NAME, predict(model, targets), split),
    ]
    return pd.concat(predictions, ignore_index=True)


def _prediction_rows(
    targets: pd.DataFrame,
    model: str,
    values: pd.Series,
    split: str,
) -> pd.DataFrame:
    result = targets[["store_id", "product_id", "date", "quantity"]].rename(
        columns={"quantity": "actual"}
    )
    result["model"] = model
    result["prediction"] = values.to_numpy()
    result["split"] = split
    return result


def _select_champion(metrics: pd.DataFrame, threshold: float) -> str:
    overall = metrics[(metrics["scope"] == "overall") & metrics["wape"].notna()]
    scores = {str(row["model"]): cast(float, row["wape"]) for _, row in overall.iterrows()}
    baseline = min((RECENT_AVERAGE, SEASONAL_NAIVE), key=scores.__getitem__)
    if scores[MODEL_NAME] <= scores[baseline] * (1 - threshold):
        return MODEL_NAME
    return baseline


def _metric_results(metrics: pd.DataFrame) -> list[MetricResult]:
    return [MetricResult.model_validate(row) for row in _metric_dicts(metrics)]


def _metric_dicts(metrics: pd.DataFrame) -> list[dict[str, object]]:
    clean = metrics.astype(object).where(pd.notna(metrics), None)
    return cast(list[dict[str, object]], clean.to_dict(orient="records"))


def _manifest_checksum(data_directory: Path) -> str | None:
    manifest = data_directory / "manifest.json"
    return sha256(manifest) if manifest.exists() else None
