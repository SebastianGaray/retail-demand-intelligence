from datetime import timedelta

import pandas as pd

from retail_demand.data.validation import RetailDatasets

FEATURE_SCHEMA_VERSION = "1"
CATEGORICAL_FEATURES = ["store_id", "product_id"]
KNOWN_FEATURES = [
    "day_of_week",
    "day_of_month",
    "month",
    "is_weekend",
    "is_holiday",
    "price",
    "regular_price",
    "is_promotion",
    "discount_percent",
]
TARGET_DERIVED_FEATURES = [
    "demand_lag_horizon",
    "demand_lag_horizon_plus_7",
    "demand_lag_horizon_plus_28",
    "demand_rolling_7",
    "demand_rolling_28",
    "inventory_lag_horizon",
    "inbound_lag_horizon",
]
FEATURE_COLUMNS = CATEGORICAL_FEATURES + KNOWN_FEATURES + TARGET_DERIVED_FEATURES


def build_feature_table(datasets: RetailDatasets, horizon: int) -> pd.DataFrame:
    sales = pd.DataFrame(row.model_dump() for row in datasets.daily_sales)
    prices = pd.DataFrame(row.model_dump() for row in datasets.daily_prices)
    inventory = pd.DataFrame(row.model_dump() for row in datasets.daily_inventory)
    calendar = pd.DataFrame(row.model_dump() for row in datasets.calendar)
    promotions = _expand_promotions(datasets)

    frame = (
        sales.merge(
            prices,
            on=["store_id", "product_id", "date"],
            how="left",
            validate="one_to_one",
        )
        .merge(
            inventory,
            on=["store_id", "product_id", "date"],
            how="left",
            validate="one_to_one",
        )
        .merge(calendar, on="date", how="left", validate="many_to_one")
        .merge(
            promotions,
            on=["store_id", "product_id", "date"],
            how="left",
            validate="one_to_one",
        )
    )
    frame["is_promotion"] = frame["is_promotion"].fillna(False).astype(bool)
    frame["discount_percent"] = frame["discount_percent"].fillna(0.0).astype(float)
    return add_temporal_features(frame, horizon)


def add_temporal_features(frame: pd.DataFrame, horizon: int) -> pd.DataFrame:
    if horizon < 1:
        raise ValueError("horizon must be at least 1")

    featured = frame.sort_values(["store_id", "product_id", "date"]).copy()
    featured["date"] = pd.to_datetime(featured["date"])
    featured["day_of_month"] = featured["date"].dt.day
    featured["month"] = featured["date"].dt.month
    groups = featured.groupby(["store_id", "product_id"], sort=False)
    demand = groups["quantity"]

    featured["demand_lag_horizon"] = demand.shift(horizon)
    featured["demand_lag_horizon_plus_7"] = demand.shift(horizon + 7)
    featured["demand_lag_horizon_plus_28"] = demand.shift(horizon + 28)
    featured["demand_rolling_7"] = demand.transform(
        lambda values: values.shift(horizon).rolling(7, min_periods=7).mean()
    )
    featured["demand_rolling_28"] = demand.transform(
        lambda values: values.shift(horizon).rolling(28, min_periods=28).mean()
    )
    featured["inventory_lag_horizon"] = groups["on_hand_quantity"].shift(horizon)
    featured["inbound_lag_horizon"] = groups["inbound_quantity"].shift(horizon)
    return featured


def eligible_feature_rows(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.dropna(subset=[*FEATURE_COLUMNS, "quantity"]).reset_index(drop=True)


def _expand_promotions(datasets: RetailDatasets) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for promotion in datasets.promotions:
        current = promotion.start_date
        while current <= promotion.end_date:
            rows.append(
                {
                    "store_id": promotion.store_id,
                    "product_id": promotion.product_id,
                    "date": current,
                    "is_promotion": True,
                    "discount_percent": float(promotion.discount_percent or 0),
                }
            )
            current += timedelta(days=1)
    return pd.DataFrame(
        rows,
        columns=[
            "store_id",
            "product_id",
            "date",
            "is_promotion",
            "discount_percent",
        ],
    )
