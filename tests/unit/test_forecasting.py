from datetime import date, timedelta

import pandas as pd
import pytest

from retail_demand.features.temporal import TARGET_DERIVED_FEATURES, add_temporal_features
from retail_demand.modeling.baselines import recent_average, seasonal_naive
from retail_demand.modeling.evaluation import mae, mase, wape


def make_history(days: int = 100) -> pd.DataFrame:
    start = date(2024, 1, 1)
    return pd.DataFrame(
        {
            "store_id": ["STORE_001"] * days,
            "product_id": ["SKU_001"] * days,
            "date": [start + timedelta(days=offset) for offset in range(days)],
            "quantity": [float(offset) for offset in range(days)],
            "on_hand_quantity": [100.0 - offset / 2 for offset in range(days)],
            "inbound_quantity": [10.0 if offset % 7 == 0 else 0.0 for offset in range(days)],
        }
    )


def test_target_features_are_unchanged_when_forecast_period_targets_change() -> None:
    horizon = 28
    original = make_history()
    changed = original.copy()
    changed.loc[changed.index[-horizon:], "quantity"] = 1_000_000
    changed.loc[changed.index[-horizon:], "on_hand_quantity"] = 0

    original_features = add_temporal_features(original, horizon).tail(horizon)
    changed_features = add_temporal_features(changed, horizon).tail(horizon)

    pd.testing.assert_frame_equal(
        original_features[TARGET_DERIVED_FEATURES].reset_index(drop=True),
        changed_features[TARGET_DERIVED_FEATURES].reset_index(drop=True),
    )


def test_rolling_features_end_before_the_forecast_horizon() -> None:
    horizon = 28
    features = add_temporal_features(make_history(), horizon)

    assert features.loc[horizon + 6, "demand_rolling_7"] == pytest.approx(3.0)
    assert features.loc[horizon + 27, "demand_rolling_28"] == pytest.approx(13.5)


def test_baselines_use_only_history() -> None:
    history = make_history(35)
    targets = make_history(42).tail(7).copy()

    assert recent_average(history, targets).tolist() == pytest.approx([20.5] * 7)
    assert seasonal_naive(history, targets).tolist() == pytest.approx(
        history.tail(7)["quantity"].tolist()
    )


def test_forecast_metrics_have_expected_values() -> None:
    assert mae([1.0, 2.0], [2.0, 2.0]) == pytest.approx(0.5)
    assert wape([1.0, 2.0], [2.0, 2.0]) == pytest.approx(1 / 3)
    assert mase(
        [8.0, 9.0],
        [7.0, 10.0],
        [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
        seasonality=1,
    ) == pytest.approx(1.0)
