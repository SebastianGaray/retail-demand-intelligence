from dataclasses import dataclass
from datetime import date, timedelta
from random import Random

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field

GENERATOR_VERSION = "1"
START_DATE = date(2023, 1, 1)
WEEKLY_DEMAND = (0.90, 0.95, 1.00, 1.00, 1.10, 1.30, 1.20)


class DemoDataParameters(BaseModel):
    stores: int = Field(ge=1, le=100)
    products: int = Field(ge=1, le=1_000)
    days: int = Field(ge=14, le=3_650)
    seed: int = Field(ge=0)

    model_config = ConfigDict(frozen=True)


@dataclass(frozen=True, slots=True)
class GeneratedDatasets:
    stores: pd.DataFrame
    products: pd.DataFrame
    daily_prices: pd.DataFrame
    promotions: pd.DataFrame
    daily_sales: pd.DataFrame
    daily_inventory: pd.DataFrame
    calendar: pd.DataFrame

    def as_mapping(self) -> dict[str, pd.DataFrame]:
        return {
            "stores": self.stores,
            "products": self.products,
            "daily_prices": self.daily_prices,
            "promotions": self.promotions,
            "daily_sales": self.daily_sales,
            "daily_inventory": self.daily_inventory,
            "calendar": self.calendar,
        }


@dataclass(frozen=True, slots=True)
class ProductBehavior:
    base_demand: float
    base_price: float
    annual_trend: float
    price_elasticity: float


@dataclass(frozen=True, slots=True)
class PromotionEffect:
    discount: float
    uplift: float


def generate_demo_data(parameters: DemoDataParameters) -> GeneratedDatasets:
    rng = Random(parameters.seed)
    dates = [START_DATE + timedelta(days=offset) for offset in range(parameters.days)]
    store_ids = [f"STORE_{number:03d}" for number in range(1, parameters.stores + 1)]
    product_ids = [f"SKU_{number:04d}" for number in range(1, parameters.products + 1)]

    store_factors = {store_id: rng.uniform(0.75, 1.25) for store_id in store_ids}
    product_behavior = {
        product_id: ProductBehavior(
            base_demand=rng.uniform(2.0, 20.0),
            base_price=rng.uniform(2.0, 50.0),
            annual_trend=rng.uniform(-0.10, 0.20),
            price_elasticity=rng.uniform(0.8, 2.0),
        )
        for product_id in product_ids
    }

    stores = _generate_stores(store_ids, dates)
    products = _generate_products(product_ids, dates, rng)
    calendar = _generate_calendar(dates)
    promotions, promotion_effects = _generate_promotions(store_ids, product_ids, dates, rng)
    daily_prices, daily_sales, daily_inventory = _generate_daily_facts(
        store_ids,
        product_ids,
        dates,
        store_factors,
        product_behavior,
        promotion_effects,
        rng,
    )

    return GeneratedDatasets(
        stores=pd.DataFrame(stores),
        products=pd.DataFrame(products),
        daily_prices=pd.DataFrame(daily_prices),
        promotions=pd.DataFrame(
            promotions,
            columns=[
                "promotion_id",
                "store_id",
                "product_id",
                "start_date",
                "end_date",
                "discount_percent",
                "description",
            ],
        ),
        daily_sales=pd.DataFrame(daily_sales),
        daily_inventory=pd.DataFrame(daily_inventory),
        calendar=pd.DataFrame(calendar),
    )


def _generate_stores(store_ids: list[str], dates: list[date]) -> list[dict[str, object]]:
    regions = ("North", "Central", "South")
    return [
        {
            "store_id": store_id,
            "name": f"Synthetic Store {index}",
            "opening_date": dates[0],
            "region": regions[(index - 1) % len(regions)],
        }
        for index, store_id in enumerate(store_ids, start=1)
    ]


def _generate_products(
    product_ids: list[str], dates: list[date], rng: Random
) -> list[dict[str, object]]:
    categories = ("Grocery", "Beverages", "Household", "Personal Care")
    return [
        {
            "product_id": product_id,
            "name": f"Synthetic Product {index}",
            "category": categories[(index - 1) % len(categories)],
            "active_from": dates[0],
            "brand": f"Demo Brand {rng.randint(1, 8)}",
            "unit": "each",
        }
        for index, product_id in enumerate(product_ids, start=1)
    ]


def _generate_calendar(dates: list[date]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for calendar_date in dates:
        is_new_year = calendar_date.month == 1 and calendar_date.day == 1
        is_year_end = calendar_date.month == 12 and calendar_date.day == 25
        is_holiday = is_new_year or is_year_end
        holiday_name = (
            "New Year's Day" if is_new_year else "Year-end Holiday" if is_year_end else None
        )
        rows.append(
            {
                "date": calendar_date,
                "day_of_week": calendar_date.weekday(),
                "is_weekend": calendar_date.weekday() >= 5,
                "is_holiday": is_holiday,
                "holiday_name": holiday_name,
            }
        )
    return rows


def _generate_promotions(
    store_ids: list[str],
    product_ids: list[str],
    dates: list[date],
    rng: Random,
) -> tuple[list[dict[str, object]], dict[tuple[str, str, date], PromotionEffect]]:
    rows: list[dict[str, object]] = []
    effects: dict[tuple[str, str, date], PromotionEffect] = {}
    promotion_number = 1

    for store_id in store_ids:
        for product_id in product_ids:
            start_offset = rng.randint(14, 35)
            while start_offset < len(dates):
                if rng.random() < 0.45:
                    duration = rng.randint(5, 10)
                    end_offset = min(start_offset + duration - 1, len(dates) - 1)
                    discount = rng.choice((0.10, 0.15, 0.20, 0.25))
                    promotion_id = f"PROMO_{promotion_number:06d}"
                    rows.append(
                        {
                            "promotion_id": promotion_id,
                            "store_id": store_id,
                            "product_id": product_id,
                            "start_date": dates[start_offset],
                            "end_date": dates[end_offset],
                            "discount_percent": round(discount * 100, 2),
                            "description": "Synthetic promotion",
                        }
                    )
                    uplift = rng.uniform(1.10, 1.40)
                    for offset in range(start_offset, end_offset + 1):
                        effects[(store_id, product_id, dates[offset])] = PromotionEffect(
                            discount,
                            uplift,
                        )
                    promotion_number += 1
                start_offset += rng.randint(56, 98)

    return rows, effects


def _generate_daily_facts(
    store_ids: list[str],
    product_ids: list[str],
    dates: list[date],
    store_factors: dict[str, float],
    product_behavior: dict[str, ProductBehavior],
    promotion_effects: dict[tuple[str, str, date], PromotionEffect],
    rng: Random,
) -> tuple[
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
]:
    prices: list[dict[str, object]] = []
    sales: list[dict[str, object]] = []
    inventory: list[dict[str, object]] = []

    for store_id in store_ids:
        store_factor = store_factors[store_id]
        store_price_factor = rng.uniform(0.95, 1.05)

        for product_id in product_ids:
            behavior = product_behavior[product_id]
            stock = round(behavior.base_demand * store_factor * rng.uniform(6.0, 8.0))
            reorder_quantity = behavior.base_demand * store_factor * 7.4

            for day_number, calendar_date in enumerate(dates):
                year_fraction = day_number / 365
                regular_price = (
                    behavior.base_price * store_price_factor * (1 + 0.03 * year_fraction)
                )
                promotion = promotion_effects.get((store_id, product_id, calendar_date))
                price = regular_price * (1 - promotion.discount) if promotion else regular_price
                price = round(price, 2)
                regular_price = round(regular_price, 2)

                trend = max(0.5, 1 + behavior.annual_trend * year_fraction)
                price_effect = (price / behavior.base_price) ** -behavior.price_elasticity
                promotion_uplift = promotion.uplift if promotion else 1.0
                expected_demand = (
                    behavior.base_demand
                    * store_factor
                    * WEEKLY_DEMAND[calendar_date.weekday()]
                    * trend
                    * price_effect
                    * promotion_uplift
                )
                demand = max(0, round(expected_demand * max(0.2, rng.gauss(1.0, 0.18))))

                inbound = 0
                if day_number > 0 and day_number % 7 == 0 and rng.random() >= 0.03:
                    inbound = max(0, round(reorder_quantity * rng.uniform(0.80, 1.10)))
                available = stock + inbound
                quantity = min(demand, available)
                stock = available - quantity

                prices.append(
                    {
                        "store_id": store_id,
                        "product_id": product_id,
                        "date": calendar_date,
                        "price": price,
                        "regular_price": regular_price,
                        "currency": "USD",
                    }
                )
                sales.append(
                    {
                        "store_id": store_id,
                        "product_id": product_id,
                        "date": calendar_date,
                        "quantity": quantity,
                        "revenue": round(quantity * price, 2),
                    }
                )
                inventory.append(
                    {
                        "store_id": store_id,
                        "product_id": product_id,
                        "date": calendar_date,
                        "on_hand_quantity": stock,
                        "inbound_quantity": inbound,
                        "lead_time_days": 7,
                    }
                )

    return prices, sales, inventory
