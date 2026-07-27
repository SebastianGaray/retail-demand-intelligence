from datetime import date
from typing import cast

import pandas as pd
import pytest
from pydantic import ValidationError

from retail_demand.data.generation import DemoDataParameters, generate_demo_data


def test_generation_is_deterministic() -> None:
    parameters = DemoDataParameters(stores=2, products=3, days=60, seed=42)

    first = generate_demo_data(parameters)
    second = generate_demo_data(parameters)

    for dataset, frame in first.as_mapping().items():
        pd.testing.assert_frame_equal(frame, second.as_mapping()[dataset])


def test_sales_do_not_exceed_available_inventory() -> None:
    generated = generate_demo_data(DemoDataParameters(stores=2, products=3, days=90, seed=7))
    merged = generated.daily_sales.merge(
        generated.daily_inventory,
        on=["store_id", "product_id", "date"],
        validate="one_to_one",
    )

    for _, rows in merged.groupby(["store_id", "product_id"], sort=False):
        ordered = rows.sort_values("date").reset_index(drop=True)
        available = ordered["on_hand_quantity"].shift(1) + ordered["inbound_quantity"]
        assert (ordered.loc[1:, "quantity"] <= available.loc[1:]).all()
        assert (ordered["on_hand_quantity"] >= 0).all()

    stockout_rate = (generated.daily_inventory["on_hand_quantity"] == 0).mean()
    assert 0 < stockout_rate < 0.25


def test_promotions_reduce_price() -> None:
    generated = generate_demo_data(DemoDataParameters(stores=2, products=4, days=180, seed=42))
    promotion = cast(dict[str, object], generated.promotions.iloc[0].to_dict())
    promoted_prices = generated.daily_prices[
        (generated.daily_prices["store_id"] == promotion["store_id"])
        & (generated.daily_prices["product_id"] == promotion["product_id"])
        & (generated.daily_prices["date"] >= cast(date, promotion["start_date"]))
        & (generated.daily_prices["date"] <= cast(date, promotion["end_date"]))
    ]

    assert not promoted_prices.empty
    assert (promoted_prices["price"] < promoted_prices["regular_price"]).all()


def test_generation_parameters_reject_undersized_history() -> None:
    with pytest.raises(ValidationError):
        DemoDataParameters(stores=1, products=1, days=13, seed=0)
