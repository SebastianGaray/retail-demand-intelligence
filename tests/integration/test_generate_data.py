import json
from pathlib import Path
from typing import cast

import pytest

from retail_demand.cli import main
from retail_demand.data.validation import load_retail_datasets


def test_generate_data_command_writes_valid_parquet_and_manifest(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    output = tmp_path / "demo"

    main(
        [
            "generate-data",
            "--stores",
            "2",
            "--products",
            "3",
            "--days",
            "30",
            "--seed",
            "42",
            "--output",
            str(output),
        ]
    )

    datasets = load_retail_datasets(output)
    manifest = cast(
        dict[str, object],
        json.loads((output / "manifest.json").read_text(encoding="utf-8")),
    )

    assert len(datasets.stores) == 2
    assert len(datasets.products) == 3
    assert len(datasets.daily_sales) == 180
    assert manifest["synthetic"] is True
    assert manifest["seed"] == 42
    assert manifest["generator_version"] == "1"
    assert "Synthetic data written" in capsys.readouterr().out
