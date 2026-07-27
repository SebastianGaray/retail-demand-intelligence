# pyright: reportCallIssue=false, reportUnknownMemberType=false, reportUnknownVariableType=false

import json
from datetime import timedelta
from functools import cached_property
from pathlib import Path

import pandas as pd

from retail_demand import __version__
from retail_demand.artifacts.metadata import ArtifactMetadata
from retail_demand.artifacts.store import load_metadata, sha256
from retail_demand.data.validation import RetailDatasets, load_retail_datasets


class ArtifactsUnavailableError(RuntimeError):
    pass


class SelectionNotFoundError(LookupError):
    pass


class ResultReader:
    def __init__(self, artifact_directory: Path) -> None:
        self.artifact_directory = artifact_directory

    def available(self) -> bool:
        try:
            self._load()
        except (ArtifactsUnavailableError, OSError, ValueError):
            return False
        return True

    def overview(self) -> dict[str, object]:
        metadata, datasets = self._load()
        sales = pd.DataFrame(row.model_dump() for row in datasets.daily_sales)
        return {
            "dataset_start": pd.Timestamp(sales["date"].min()).date(),
            "dataset_end": pd.Timestamp(sales["date"].max()).date(),
            "store_count": len(datasets.stores),
            "product_count": len(datasets.products),
            "observation_count": len(datasets.daily_sales),
            "current_model": metadata.champion_model,
            "artifact_version": metadata.schema_version,
            "project_version": __version__,
            "synthetic": self._is_synthetic(metadata),
        }

    def stores(self) -> list[dict[str, str]]:
        _, datasets = self._load()
        return [
            {"id": store.store_id, "name": store.name}
            for store in sorted(datasets.stores, key=lambda item: item.store_id)
        ]

    def products(self) -> list[dict[str, str]]:
        _, datasets = self._load()
        return [
            {"id": product.product_id, "name": product.name}
            for product in sorted(datasets.products, key=lambda item: item.product_id)
        ]

    def forecast(self, store_id: str, product_id: str) -> tuple[str, pd.DataFrame]:
        metadata, datasets = self._load()
        self._require_selection(datasets, store_id, product_id)
        sales = pd.DataFrame(
            row.model_dump()
            for row in datasets.daily_sales
            if row.store_id == store_id and row.product_id == product_id
        )
        prices = pd.DataFrame(
            row.model_dump()
            for row in datasets.daily_prices
            if row.store_id == store_id and row.product_id == product_id
        )
        inventory = pd.DataFrame(
            row.model_dump()
            for row in datasets.daily_inventory
            if row.store_id == store_id and row.product_id == product_id
        )
        predictions = pd.read_parquet(self.artifact_directory / "predictions.parquet")
        predictions = predictions[
            (predictions["store_id"] == store_id) & (predictions["product_id"] == product_id)
        ][["date", "prediction"]]
        for dated_frame in (sales, prices, inventory, predictions):
            dated_frame["date"] = pd.to_datetime(dated_frame["date"])
        frame = (
            sales.merge(prices[["date", "price", "regular_price"]], on="date", how="left")
            .merge(inventory[["date", "on_hand_quantity"]], on="date", how="left")
            .merge(predictions, on="date", how="left")
            .sort_values("date")
        )
        frame["actual"] = frame["quantity"].where(frame["prediction"].notna())
        frame["error"] = frame["actual"] - frame["prediction"]
        frame["stockout"] = frame["on_hand_quantity"] == 0
        frame["promotion"] = (
            self._promotion_dates(datasets, store_id, product_id)
            .reindex(pd.to_datetime(frame["date"]), fill_value=False)
            .to_numpy()
        )
        return metadata.champion_model, frame

    def inventory_risk(
        self,
        stockout_coverage_days: float = 7,
        excess_coverage_days: float = 45,
        store_id: str | None = None,
        product_id: str | None = None,
    ) -> pd.DataFrame:
        if stockout_coverage_days < 0 or excess_coverage_days <= stockout_coverage_days:
            raise ValueError("coverage thresholds must be nonnegative and increasing")

        metadata, datasets = self._load()
        if store_id is not None or product_id is not None:
            self._require_selection(datasets, store_id, product_id)
        predictions = pd.read_parquet(self.artifact_directory / "predictions.parquet")
        inventory = pd.DataFrame(row.model_dump() for row in datasets.daily_inventory)
        result = calculate_inventory_risk(
            predictions,
            inventory,
            metadata,
            stockout_coverage_days,
            excess_coverage_days,
        )
        if store_id is not None:
            result = result[result["store_id"] == store_id]
        if product_id is not None:
            result = result[result["product_id"] == product_id]
        return result.reset_index(drop=True)

    def performance(
        self,
        scope: str | None = None,
        identifier: str | None = None,
    ) -> pd.DataFrame:
        metadata, _ = self._load()
        metrics = pd.DataFrame(metric.model_dump() for metric in metadata.test_metrics)
        if scope is not None:
            metrics = metrics[metrics["scope"] == scope]
        if identifier is not None:
            metrics = metrics[metrics["identifier"] == identifier]
        return metrics.reset_index(drop=True)

    def metadata(self) -> ArtifactMetadata:
        metadata, _ = self._load()
        return metadata

    def _load(self) -> tuple[ArtifactMetadata, RetailDatasets]:
        return self._bundle

    @cached_property
    def _bundle(self) -> tuple[ArtifactMetadata, RetailDatasets]:
        metadata_path = self.artifact_directory / "metadata.json"
        if not metadata_path.exists():
            raise ArtifactsUnavailableError(
                f"forecast artifacts were not found in {self.artifact_directory}"
            )
        metadata = load_metadata(metadata_path)
        required = {"predictions.parquet", "evaluation_predictions.parquet", "metrics.json"}
        missing = required - metadata.files.keys()
        if missing:
            raise ArtifactsUnavailableError(
                f"artifact run is incomplete: missing {', '.join(sorted(missing))}"
            )
        for filename, expected in metadata.files.items():
            path = self.artifact_directory / filename
            if not path.exists() or sha256(path) != expected:
                raise ArtifactsUnavailableError(f"artifact file is missing or changed: {filename}")
        data_directory = Path(metadata.data_directory)
        if not data_directory.exists():
            raise ArtifactsUnavailableError(f"dataset directory was not found: {data_directory}")
        return metadata, load_retail_datasets(data_directory)

    def _require_selection(
        self,
        datasets: RetailDatasets,
        store_id: str | None,
        product_id: str | None,
    ) -> None:
        if store_id is not None and store_id not in {store.store_id for store in datasets.stores}:
            raise SelectionNotFoundError(f"store '{store_id}' was not found")
        if product_id is not None and product_id not in {
            product.product_id for product in datasets.products
        }:
            raise SelectionNotFoundError(f"product '{product_id}' was not found")

    def _promotion_dates(
        self,
        datasets: RetailDatasets,
        store_id: str,
        product_id: str,
    ) -> pd.Series:
        dates: dict[pd.Timestamp, bool] = {}
        for promotion in datasets.promotions:
            if promotion.store_id != store_id or promotion.product_id != product_id:
                continue
            current = promotion.start_date
            while current <= promotion.end_date:
                dates[pd.Timestamp(current)] = True
                current += timedelta(days=1)
        return pd.Series(dates, dtype=bool)

    def _is_synthetic(self, metadata: ArtifactMetadata) -> bool:
        manifest = Path(metadata.data_directory) / "manifest.json"
        if not manifest.exists():
            return False
        content = json.loads(manifest.read_text(encoding="utf-8"))
        return content.get("synthetic") is True


def calculate_inventory_risk(
    predictions: pd.DataFrame,
    inventory: pd.DataFrame,
    metadata: ArtifactMetadata,
    stockout_coverage_days: float,
    excess_coverage_days: float,
) -> pd.DataFrame:
    forecast = (
        predictions.groupby(["store_id", "product_id"], as_index=False)["prediction"]
        .sum()
        .rename(columns={"prediction": "expected_demand"})
    )
    cutoff = pd.Timestamp(metadata.test_period.start)
    current = (
        inventory[pd.to_datetime(inventory["date"]) < cutoff]
        .sort_values("date")
        .groupby(["store_id", "product_id"], as_index=False)
        .tail(1)[["store_id", "product_id", "on_hand_quantity"]]
        .rename(columns={"on_hand_quantity": "current_inventory"})
    )
    result = forecast.merge(current, on=["store_id", "product_id"], validate="one_to_one")
    daily_demand = result["expected_demand"] / metadata.configuration.horizon
    result["estimated_coverage_days"] = result["current_inventory"] / daily_demand.replace(0, pd.NA)
    result["stockout_risk"] = result["estimated_coverage_days"] < stockout_coverage_days
    result["excess_inventory"] = result["estimated_coverage_days"] > excess_coverage_days
    return result
