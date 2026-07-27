import shutil
from datetime import UTC, datetime, time
from pathlib import Path
from tempfile import TemporaryDirectory

from retail_demand.artifacts.demo_bundle import (
    BUNDLE_MANIFEST,
    DATA_FILES,
    DemoArtifactManifest,
    manifest_json,
    validate_demo_artifact_bundle,
)
from retail_demand.artifacts.metadata import ArtifactMetadata, DataPeriod
from retail_demand.artifacts.store import load_metadata, save_metadata, sha256
from retail_demand.data.loading import read_parquet_frame
from retail_demand.data.validation import load_retail_datasets


def build_demo_artifacts(source: Path, output: Path) -> DemoArtifactManifest:
    metadata = _validate_source(source)
    source_data = Path(metadata.data_directory)
    datasets = load_retail_datasets(source_data)
    date_range = DataPeriod(
        start=min(row.date for row in datasets.daily_sales),
        end=max(row.date for row in datasets.daily_sales),
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix="retail-demand-demo-", dir=output.parent) as temporary:
        staging = Path(temporary)
        data_output = staging / "data"
        data_output.mkdir()
        for relative_path in DATA_FILES:
            filename = Path(relative_path).name
            shutil.copyfile(source_data / filename, data_output / filename)
        shutil.copyfile(source / "predictions.parquet", staging / "predictions.parquet")

        public_metadata = metadata.model_copy(
            update={
                "created_at": datetime.combine(date_range.end, time.min, UTC),
                "data_directory": "data",
                "data_manifest_sha256": None,
                "files": {
                    "predictions.parquet": sha256(staging / "predictions.parquet"),
                },
            }
        )
        save_metadata(public_metadata, staging / "metadata.json")

        row_counts = {
            relative_path: len(read_parquet_frame(staging / relative_path))
            for relative_path in (*DATA_FILES, "predictions.parquet")
        }
        files = {
            relative_path: sha256(staging / relative_path)
            for relative_path in sorted(("metadata.json", "predictions.parquet", *DATA_FILES))
        }
        manifest = DemoArtifactManifest(
            bundle_version=output.name,
            date_range=date_range,
            store_count=len(datasets.stores),
            product_count=len(datasets.products),
            row_counts=row_counts,
            source_artifact_version=metadata.schema_version,
            files=files,
        )
        (staging / BUNDLE_MANIFEST).write_text(manifest_json(manifest), encoding="utf-8")
        validate_demo_artifact_bundle(staging)

        if output.exists():
            shutil.rmtree(output)
        staging.replace(output)

    return validate_demo_artifact_bundle(output)


def _validate_source(source: Path) -> ArtifactMetadata:
    metadata_path = source / "metadata.json"
    if not metadata_path.is_file():
        raise ValueError(f"source metadata was not found: {metadata_path}")
    metadata = load_metadata(metadata_path)
    required = {"predictions.parquet", "evaluation_predictions.parquet", "metrics.json"}
    missing = required - metadata.files.keys()
    if missing:
        raise ValueError(f"source artifact is incomplete: {', '.join(sorted(missing))}")
    for filename, expected_checksum in metadata.files.items():
        path = source / filename
        if not path.is_file() or sha256(path) != expected_checksum:
            raise ValueError(f"source artifact file is missing or changed: {filename}")
    data_directory = Path(metadata.data_directory)
    if not data_directory.is_dir():
        raise ValueError(f"source data directory was not found: {data_directory}")
    return metadata
