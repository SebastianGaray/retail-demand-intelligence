import json
from pathlib import Path, PurePosixPath
from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator

from retail_demand.artifacts.metadata import DataPeriod
from retail_demand.artifacts.store import load_metadata, sha256
from retail_demand.data.loading import read_parquet_frame
from retail_demand.data.schemas import (
    CALENDAR,
    DAILY_INVENTORY,
    DAILY_PRICES,
    DAILY_SALES,
    PRODUCTS,
    PROMOTIONS,
    STORES,
)
from retail_demand.data.validation import load_retail_datasets

BUNDLE_MANIFEST = "manifest.json"
DATA_FILES = tuple(
    f"data/{contract.filename}"
    for contract in (
        STORES,
        PRODUCTS,
        DAILY_PRICES,
        PROMOTIONS,
        DAILY_SALES,
        DAILY_INVENTORY,
        CALENDAR,
    )
)
REQUIRED_FILES = ("metadata.json", "predictions.parquet", *DATA_FILES)


class DemoArtifactManifest(BaseModel):
    bundle_version: str
    schema_version: Literal["1"] = "1"
    date_range: DataPeriod
    store_count: int
    product_count: int
    row_counts: dict[str, int]
    source_artifact_version: str
    files: dict[str, str]
    synthetic: Literal[True] = True

    model_config = ConfigDict(frozen=True)

    @field_validator("files", "row_counts")
    @classmethod
    def paths_are_relative(cls, values: dict[str, object]) -> dict[str, object]:
        for value in values:
            path = PurePosixPath(value)
            if path.is_absolute() or ".." in path.parts or str(path) != value:
                raise ValueError(f"bundle path must be relative: {value}")
        return values


def load_bundle_manifest(directory: Path) -> DemoArtifactManifest:
    path = directory / BUNDLE_MANIFEST
    try:
        return DemoArtifactManifest.model_validate_json(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"bundle manifest was not found: {path}") from error


def validate_demo_artifact_bundle(directory: Path) -> DemoArtifactManifest:
    manifest = validate_bundle_files(directory)
    datasets = load_retail_datasets(directory / "data")
    metadata = load_metadata(directory / "metadata.json")
    predictions = read_parquet_frame(directory / "predictions.parquet")
    actual_rows = {
        relative_path: len(read_parquet_frame(directory / relative_path))
        for relative_path in (*DATA_FILES, "predictions.parquet")
    }
    if manifest.row_counts != actual_rows:
        raise ValueError("bundle row counts do not match its files")
    if manifest.store_count != len(datasets.stores):
        raise ValueError("bundle store count does not match stores.parquet")
    if manifest.product_count != len(datasets.products):
        raise ValueError("bundle product count does not match products.parquet")

    sales_dates = [row.date for row in datasets.daily_sales]
    if manifest.date_range != DataPeriod(start=min(sales_dates), end=max(sales_dates)):
        raise ValueError("bundle date range does not match daily_sales.parquet")
    if metadata.data_directory != "data":
        raise ValueError("public artifact metadata must use the relative data directory")
    if metadata.files != {"predictions.parquet": manifest.files["predictions.parquet"]}:
        raise ValueError("public artifact metadata contains unsupported files")
    if metadata.schema_version != manifest.source_artifact_version:
        raise ValueError("source artifact version does not match metadata")
    if not metadata.test_metrics:
        raise ValueError("public artifact metadata does not contain evaluation metrics")
    if predictions.empty:
        raise ValueError("public predictions are empty")
    required_prediction_columns = {
        "store_id",
        "product_id",
        "date",
        "actual",
        "model",
        "prediction",
        "split",
    }
    if not required_prediction_columns.issubset(predictions.columns):
        raise ValueError("public predictions do not contain the required columns")
    return manifest


def validate_bundle_files(directory: Path) -> DemoArtifactManifest:
    manifest = load_bundle_manifest(directory)
    expected = set(REQUIRED_FILES)
    if set(manifest.files) != expected:
        missing = sorted(expected - manifest.files.keys())
        extra = sorted(manifest.files.keys() - expected)
        raise ValueError(f"bundle file list is invalid: missing={missing}, extra={extra}")

    for relative_path, expected_checksum in manifest.files.items():
        path = directory / relative_path
        if not path.is_file():
            raise ValueError(f"bundle file was not found: {relative_path}")
        if sha256(path) != expected_checksum:
            raise ValueError(f"bundle checksum does not match: {relative_path}")
    return manifest


def manifest_json(manifest: DemoArtifactManifest) -> str:
    content = json.loads(manifest.model_dump_json())
    return json.dumps(content, indent=2, sort_keys=True) + "\n"
