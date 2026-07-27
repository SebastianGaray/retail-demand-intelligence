from dataclasses import dataclass
from datetime import date
from itertools import pairwise
from pathlib import Path

from retail_demand.data.loading import load_parquet
from retail_demand.data.schemas import (
    CALENDAR,
    DAILY_INVENTORY,
    DAILY_PRICES,
    DAILY_SALES,
    PRODUCTS,
    PROMOTIONS,
    STORES,
)
from retail_demand.domain.errors import DatasetValidationError, DatasetValidationIssue
from retail_demand.domain.models import (
    CalendarDay,
    DailyInventory,
    DailyPrice,
    DailySale,
    Product,
    Promotion,
    Store,
)


@dataclass(frozen=True, slots=True)
class RetailDatasets:
    stores: tuple[Store, ...]
    products: tuple[Product, ...]
    daily_sales: tuple[DailySale, ...]
    daily_prices: tuple[DailyPrice, ...]
    promotions: tuple[Promotion, ...]
    daily_inventory: tuple[DailyInventory, ...]
    calendar: tuple[CalendarDay, ...]


def load_retail_datasets(directory: Path) -> RetailDatasets:
    datasets = RetailDatasets(
        stores=load_parquet(directory / STORES.filename, STORES),
        products=load_parquet(directory / PRODUCTS.filename, PRODUCTS),
        daily_sales=load_parquet(directory / DAILY_SALES.filename, DAILY_SALES),
        daily_prices=load_parquet(directory / DAILY_PRICES.filename, DAILY_PRICES),
        promotions=load_parquet(directory / PROMOTIONS.filename, PROMOTIONS),
        daily_inventory=load_parquet(
            directory / DAILY_INVENTORY.filename,
            DAILY_INVENTORY,
        ),
        calendar=load_parquet(directory / CALENDAR.filename, CALENDAR),
    )
    validate_relationships(datasets)
    return datasets


def validate_relationships(datasets: RetailDatasets) -> None:
    stores = {store.store_id: store for store in datasets.stores}
    products = {product.product_id: product for product in datasets.products}
    calendar_dates = {day.date for day in datasets.calendar}
    issues: list[DatasetValidationIssue] = []

    for dataset_name, rows in (
        ("daily_sales", datasets.daily_sales),
        ("daily_prices", datasets.daily_prices),
        ("daily_inventory", datasets.daily_inventory),
    ):
        for row_number, row in enumerate(rows):
            _validate_daily_relationships(
                dataset_name,
                row_number,
                row.store_id,
                row.product_id,
                row.date,
                stores,
                products,
                calendar_dates,
                issues,
            )

    for row_number, promotion in enumerate(datasets.promotions):
        _validate_period_relationships(
            row_number,
            promotion,
            stores,
            products,
            calendar_dates,
            issues,
        )

    _validate_promotion_overlaps(datasets.promotions, issues)

    if issues:
        raise DatasetValidationError(issues)


def _validate_daily_relationships(
    dataset: str,
    row: int,
    store_id: str,
    product_id: str,
    record_date: date,
    stores: dict[str, Store],
    products: dict[str, Product],
    calendar_dates: set[date],
    issues: list[DatasetValidationIssue],
) -> None:
    store = stores.get(store_id)
    product = products.get(product_id)

    if store is None:
        issues.append(DatasetValidationIssue(dataset, "store_id", "unknown store", row))
    elif record_date < store.opening_date or (
        store.closing_date is not None and record_date > store.closing_date
    ):
        issues.append(
            DatasetValidationIssue(dataset, "date", "outside the store active period", row)
        )

    if product is None:
        issues.append(DatasetValidationIssue(dataset, "product_id", "unknown product", row))
    elif record_date < product.active_from or (
        product.active_to is not None and record_date > product.active_to
    ):
        issues.append(
            DatasetValidationIssue(dataset, "date", "outside the product active period", row)
        )

    if record_date not in calendar_dates:
        issues.append(DatasetValidationIssue(dataset, "date", "missing from calendar", row))


def _validate_period_relationships(
    row: int,
    promotion: Promotion,
    stores: dict[str, Store],
    products: dict[str, Product],
    calendar_dates: set[date],
    issues: list[DatasetValidationIssue],
) -> None:
    store = stores.get(promotion.store_id)
    product = products.get(promotion.product_id)

    if store is None:
        issues.append(DatasetValidationIssue("promotions", "store_id", "unknown store", row))
    elif promotion.start_date < store.opening_date or (
        store.closing_date is not None and promotion.end_date > store.closing_date
    ):
        issues.append(
            DatasetValidationIssue(
                "promotions",
                "start_date, end_date",
                "period is outside the store active period",
                row,
            )
        )

    if product is None:
        issues.append(DatasetValidationIssue("promotions", "product_id", "unknown product", row))
    elif promotion.start_date < product.active_from or (
        product.active_to is not None and promotion.end_date > product.active_to
    ):
        issues.append(
            DatasetValidationIssue(
                "promotions",
                "start_date, end_date",
                "period is outside the product active period",
                row,
            )
        )

    missing_dates = (
        boundary
        for boundary in (promotion.start_date, promotion.end_date)
        if boundary not in calendar_dates
    )
    for missing_date in missing_dates:
        issues.append(
            DatasetValidationIssue(
                "promotions",
                "start_date, end_date",
                f"{missing_date.isoformat()} is missing from calendar",
                row,
            )
        )


def _validate_promotion_overlaps(
    promotions: tuple[Promotion, ...],
    issues: list[DatasetValidationIssue],
) -> None:
    by_item: dict[tuple[str, str], list[tuple[int, Promotion]]] = {}
    for row, promotion in enumerate(promotions):
        by_item.setdefault((promotion.store_id, promotion.product_id), []).append((row, promotion))

    for grouped_promotions in by_item.values():
        ordered = sorted(grouped_promotions, key=lambda item: item[1].start_date)
        for previous, current in pairwise(ordered):
            if current[1].start_date <= previous[1].end_date:
                issues.append(
                    DatasetValidationIssue(
                        "promotions",
                        "start_date, end_date",
                        f"overlaps promotion '{previous[1].promotion_id}'",
                        current[0],
                    )
                )
