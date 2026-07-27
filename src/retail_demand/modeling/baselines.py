import pandas as pd


def recent_average(
    history: pd.DataFrame,
    targets: pd.DataFrame,
    window: int = 28,
) -> pd.Series:
    averages = (
        history.sort_values("date")
        .groupby(["store_id", "product_id"], sort=False)
        .tail(window)
        .groupby(["store_id", "product_id"])["quantity"]
        .mean()
    )
    keys = pd.MultiIndex.from_frame(targets[["store_id", "product_id"]])
    return pd.Series(averages.reindex(keys).to_numpy(), index=targets.index).fillna(0.0)


def seasonal_naive(history: pd.DataFrame, targets: pd.DataFrame) -> pd.Series:
    latest_week = (
        history.assign(day_of_week=pd.to_datetime(history["date"]).dt.dayofweek)
        .sort_values("date")
        .groupby(["store_id", "product_id", "day_of_week"], sort=False)
        .tail(1)
        .set_index(["store_id", "product_id", "day_of_week"])["quantity"]
    )
    target_keys = targets[["store_id", "product_id"]].copy()
    target_keys["day_of_week"] = pd.to_datetime(targets["date"]).dt.dayofweek
    keys = pd.MultiIndex.from_frame(target_keys)
    return pd.Series(latest_week.reindex(keys).to_numpy(), index=targets.index).fillna(0.0)
