import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING

from retail_demand.data.generation import (
    GENERATOR_VERSION,
    DemoDataParameters,
    generate_demo_data,
)
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

if TYPE_CHECKING:
    import pandas as pd

CONTRACTS = (STORES, PRODUCTS, DAILY_PRICES, PROMOTIONS, DAILY_SALES, DAILY_INVENTORY, CALENDAR)


@dataclass(frozen=True, slots=True)
class GenerationSummary:
    output: Path
    row_counts: dict[str, int]


def generate_and_save_demo_data(
    parameters: DemoDataParameters,
    output: Path,
) -> GenerationSummary:
    generated = generate_demo_data(parameters)
    frames = generated.as_mapping()
    output.parent.mkdir(parents=True, exist_ok=True)

    with TemporaryDirectory(prefix="retail-demand-", dir=output.parent) as temporary:
        staging = Path(temporary)
        for contract in CONTRACTS:
            frames[contract.name].to_parquet(staging / contract.filename, index=False)

        load_retail_datasets(staging)
        manifest = _build_manifest(parameters, staging, frames)
        (staging / "manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        output.mkdir(parents=True, exist_ok=True)
        for contract in CONTRACTS:
            (staging / contract.filename).replace(output / contract.filename)
        (staging / "manifest.json").replace(output / "manifest.json")

    return GenerationSummary(
        output=output,
        row_counts={name: len(frame) for name, frame in frames.items()},
    )


def _build_manifest(
    parameters: DemoDataParameters,
    staging: Path,
    frames: dict[str, "pd.DataFrame"],
) -> dict[str, object]:
    files: dict[str, dict[str, object]] = {}
    for contract in CONTRACTS:
        path = staging / contract.filename
        files[contract.name] = {
            "filename": contract.filename,
            "rows": len(frames[contract.name]),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }

    return {
        "synthetic": True,
        "generator_version": GENERATOR_VERSION,
        "generated_at": datetime.now(UTC).isoformat(),
        "seed": parameters.seed,
        "parameters": parameters.model_dump(),
        "files": files,
    }
