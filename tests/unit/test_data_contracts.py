import json
from collections.abc import Mapping
from pathlib import Path
from typing import cast

import pandas as pd
import pytest
from pydantic import ValidationError

from retail_demand.data.loading import validate_records
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
from retail_demand.domain.errors import DatasetValidationError
from retail_demand.domain.models import CalendarDay, DailyPrice, Promotion

type DatasetRows = dict[str, list[dict[str, object]]]
FIXTURES = Path(__file__).parents[1] / "fixtures"
CONTRACTS = (STORES, PRODUCTS, DAILY_SALES, DAILY_PRICES, PROMOTIONS, DAILY_INVENTORY, CALENDAR)


def load_fixture(name: str) -> DatasetRows:
    raw = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
    return cast(DatasetRows, raw)


def write_parquet_bundle(directory: Path, rows: DatasetRows) -> None:
    for contract in CONTRACTS:
        pd.DataFrame(rows[contract.name]).to_parquet(directory / contract.filename, index=False)


def test_valid_parquet_bundle_loads_as_domain_records(tmp_path: Path) -> None:
    write_parquet_bundle(tmp_path, load_fixture("valid_datasets.json"))

    datasets = load_retail_datasets(tmp_path)

    assert datasets.stores[0].store_id == "STORE_001"
    assert datasets.daily_sales[1].quantity == 10
    assert datasets.promotions[0].promotion_id == "PROMO_001"


def test_record_error_identifies_dataset_field_and_problem() -> None:
    invalid = load_fixture("invalid_datasets.json")

    with pytest.raises(DatasetValidationError) as captured:
        validate_records(invalid["negative_price"], DAILY_PRICES)

    issue = captured.value.issues[0]
    assert issue.dataset == "daily_prices"
    assert issue.field == "price"
    assert "greater than 0" in issue.problem


def test_duplicate_composite_key_is_rejected() -> None:
    invalid = load_fixture("invalid_datasets.json")

    with pytest.raises(DatasetValidationError, match="duplicate key"):
        validate_records(invalid["duplicate_sales"], DAILY_SALES)


def test_unknown_relationship_is_rejected(tmp_path: Path) -> None:
    valid = load_fixture("valid_datasets.json")
    invalid = load_fixture("invalid_datasets.json")
    valid["daily_inventory"] = invalid["unknown_product_inventory"]
    write_parquet_bundle(tmp_path, valid)

    with pytest.raises(DatasetValidationError) as captured:
        load_retail_datasets(tmp_path)

    assert any(
        issue.dataset == "daily_inventory"
        and issue.field == "product_id"
        and issue.problem == "unknown product"
        for issue in captured.value.issues
    )


def test_overlapping_promotions_are_rejected(tmp_path: Path) -> None:
    valid = load_fixture("valid_datasets.json")
    invalid = load_fixture("invalid_datasets.json")
    valid["promotions"] = invalid["overlapping_promotions"]
    write_parquet_bundle(tmp_path, valid)

    with pytest.raises(DatasetValidationError, match="overlaps promotion"):
        load_retail_datasets(tmp_path)


@pytest.mark.parametrize(
    ("model", "record", "field"),
    [
        (
            DailyPrice,
            {
                "store_id": "STORE_001",
                "product_id": "SKU_001",
                "date": "2024-01-01",
                "price": 11,
                "regular_price": 10,
            },
            "regular_price",
        ),
        (
            Promotion,
            {
                "promotion_id": "PROMO_001",
                "store_id": "STORE_001",
                "product_id": "SKU_001",
                "start_date": "2024-01-02",
                "end_date": "2024-01-01",
                "discount_percent": 10,
            },
            "end_date",
        ),
        (
            CalendarDay,
            {
                "date": "2024-01-01",
                "day_of_week": 6,
                "is_weekend": True,
            },
            "day_of_week",
        ),
    ],
)
def test_business_rules_reject_invalid_rows(
    model: type[DailyPrice] | type[Promotion] | type[CalendarDay],
    record: Mapping[str, object],
    field: str,
) -> None:
    with pytest.raises(ValidationError) as captured:
        model.model_validate(record)

    assert captured.value.errors()[0]["loc"] == (field,)
