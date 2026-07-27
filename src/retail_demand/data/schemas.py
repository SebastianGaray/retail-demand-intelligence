from dataclasses import dataclass

from pydantic import BaseModel

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
class DatasetContract[RecordT: BaseModel]:
    name: str
    filename: str
    model: type[RecordT]
    key: tuple[str, ...]


STORES = DatasetContract("stores", "stores.parquet", Store, ("store_id",))
PRODUCTS = DatasetContract("products", "products.parquet", Product, ("product_id",))
DAILY_SALES = DatasetContract(
    "daily_sales",
    "daily_sales.parquet",
    DailySale,
    ("store_id", "product_id", "date"),
)
DAILY_PRICES = DatasetContract(
    "daily_prices",
    "daily_prices.parquet",
    DailyPrice,
    ("store_id", "product_id", "date"),
)
PROMOTIONS = DatasetContract(
    "promotions",
    "promotions.parquet",
    Promotion,
    ("promotion_id",),
)
DAILY_INVENTORY = DatasetContract(
    "daily_inventory",
    "daily_inventory.parquet",
    DailyInventory,
    ("store_id", "product_id", "date"),
)
CALENDAR = DatasetContract("calendar", "calendar.parquet", CalendarDay, ("date",))
