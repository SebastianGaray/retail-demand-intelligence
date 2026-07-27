from datetime import date
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    ValidationInfo,
    field_validator,
)

type Identifier = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=64,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9_-]*$",
    ),
]
type StoreId = Identifier
type ProductId = Identifier
type PromotionId = Identifier
type NonNegativeQuantity = Annotated[float, Field(ge=0, allow_inf_nan=False)]
type Money = Annotated[Decimal, Field(gt=0, max_digits=12, decimal_places=2)]


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, validate_default=True)


class Store(ContractModel):
    store_id: StoreId
    name: str = Field(min_length=1, max_length=120)
    opening_date: date
    closing_date: date | None = None
    region: str | None = Field(default=None, min_length=1, max_length=80)

    @field_validator("closing_date")
    @classmethod
    def validate_active_period(cls, value: date | None, info: ValidationInfo) -> date | None:
        opening_date = info.data.get("opening_date")
        if value is not None and isinstance(opening_date, date) and value < opening_date:
            raise ValueError("closing_date must be on or after opening_date")
        return value


class Product(ContractModel):
    product_id: ProductId
    name: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=80)
    active_from: date
    active_to: date | None = None
    brand: str | None = Field(default=None, min_length=1, max_length=80)
    unit: Literal["each", "kg", "liter"] = "each"

    @field_validator("active_to")
    @classmethod
    def validate_active_period(cls, value: date | None, info: ValidationInfo) -> date | None:
        active_from = info.data.get("active_from")
        if value is not None and isinstance(active_from, date) and value < active_from:
            raise ValueError("active_to must be on or after active_from")
        return value


class DailySale(ContractModel):
    store_id: StoreId
    product_id: ProductId
    date: date
    quantity: NonNegativeQuantity
    revenue: Annotated[Decimal, Field(ge=0, max_digits=14, decimal_places=2)] | None = None


class DailyPrice(ContractModel):
    store_id: StoreId
    product_id: ProductId
    date: date
    price: Money
    regular_price: Money | None = None
    currency: Annotated[str, StringConstraints(pattern=r"^[A-Z]{3}$")] = "USD"

    @field_validator("regular_price")
    @classmethod
    def validate_regular_price(cls, value: Money | None, info: ValidationInfo) -> Money | None:
        price = info.data.get("price")
        if value is not None and isinstance(price, Decimal) and price > value:
            raise ValueError("price must not exceed regular_price")
        return value


class Promotion(ContractModel):
    promotion_id: PromotionId
    store_id: StoreId
    product_id: ProductId
    start_date: date
    end_date: date
    discount_percent: Annotated[Decimal, Field(gt=0, le=100, decimal_places=2)] | None = None
    promotional_price: Money | None = None
    description: str | None = Field(default=None, min_length=1, max_length=160)

    @field_validator("end_date")
    @classmethod
    def validate_period(cls, value: date, info: ValidationInfo) -> date:
        start_date = info.data.get("start_date")
        if isinstance(start_date, date) and value < start_date:
            raise ValueError("end_date must be on or after start_date")
        return value

    @field_validator("promotional_price")
    @classmethod
    def validate_discount(cls, value: Money | None, info: ValidationInfo) -> Money | None:
        if info.data.get("discount_percent") is None and value is None:
            raise ValueError("discount_percent or promotional_price is required")
        return value


class DailyInventory(ContractModel):
    store_id: StoreId
    product_id: ProductId
    date: date
    on_hand_quantity: NonNegativeQuantity
    inbound_quantity: NonNegativeQuantity = 0
    lead_time_days: int | None = Field(default=None, ge=0, le=365)


class CalendarDay(ContractModel):
    date: date
    day_of_week: int = Field(ge=0, le=6)
    is_weekend: bool
    is_holiday: bool = False
    holiday_name: str | None = Field(default=None, min_length=1, max_length=120)

    @field_validator("day_of_week")
    @classmethod
    def validate_day_of_week(cls, value: int, info: ValidationInfo) -> int:
        calendar_date = info.data.get("date")
        if isinstance(calendar_date, date) and value != calendar_date.weekday():
            raise ValueError("day_of_week must match date")
        return value

    @field_validator("is_weekend")
    @classmethod
    def validate_weekend(cls, value: bool, info: ValidationInfo) -> bool:
        day_of_week = info.data.get("day_of_week")
        if isinstance(day_of_week, int) and value != (day_of_week >= 5):
            raise ValueError("is_weekend must match day_of_week")
        return value

    @field_validator("holiday_name")
    @classmethod
    def validate_holiday_name(cls, value: str | None, info: ValidationInfo) -> str | None:
        is_holiday = info.data.get("is_holiday")
        if value is not None and is_holiday is False:
            raise ValueError("holiday_name requires is_holiday to be true")
        return value
