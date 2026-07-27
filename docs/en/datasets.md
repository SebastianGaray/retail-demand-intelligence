# Dataset contracts

All datasets use Parquet. Identifiers contain letters, numbers, `_`, or `-`, start with a letter
or number, and are at most 64 characters. Dates use ISO format in examples.

## Stores

Key: `store_id`.

| Field | Required | Rule |
|---|---|---|
| `store_id` | Yes | Unique store identifier. |
| `name` | Yes | Non-empty display name. |
| `opening_date` | Yes | First active date. |
| `closing_date` | No | On or after `opening_date`. |
| `region` | No | Non-empty when provided. |

## Products

Key: `product_id`.

| Field | Required | Rule |
|---|---|---|
| `product_id` | Yes | Unique product identifier. |
| `name` | Yes | Non-empty display name. |
| `category` | Yes | Non-empty category. |
| `active_from` | Yes | First active date. |
| `active_to` | No | On or after `active_from`. |
| `brand` | No | Non-empty when provided. |
| `unit` | No | `each`, `kg`, or `liter`; defaults to `each`. |

## Daily sales

Key: `store_id`, `product_id`, `date`. Store and product identifiers must exist, the date must
fall within both active periods, and the date must exist in the calendar.

| Field | Required | Rule |
|---|---|---|
| `store_id` | Yes | References stores. |
| `product_id` | Yes | References products. |
| `date` | Yes | Business date. |
| `quantity` | Yes | Finite and at least zero. |
| `revenue` | No | At least zero, with two decimal places. |

## Daily prices

Key and relationships match daily sales.

| Field | Required | Rule |
|---|---|---|
| `store_id`, `product_id`, `date` | Yes | Store-product-date key. |
| `price` | Yes | Greater than zero, with at most two decimal places. |
| `regular_price` | No | At least `price`. |
| `currency` | No | Three uppercase letters; defaults to `USD`. |

## Promotions

Key: `promotion_id`. Promotions reference one store and product. Their boundaries must be in the
calendar and within both active periods. Periods for the same store and product cannot overlap.

| Field | Required | Rule |
|---|---|---|
| `promotion_id` | Yes | Unique promotion identifier. |
| `store_id`, `product_id` | Yes | Existing store and product. |
| `start_date`, `end_date` | Yes | Inclusive period; end is not before start. |
| `discount_percent` | Conditional | Greater than zero and at most 100. |
| `promotional_price` | Conditional | Greater than zero. |
| `description` | No | Non-empty when provided. |

At least one of `discount_percent` or `promotional_price` is required.

## Daily inventory

Key and relationships match daily sales.

| Field | Required | Rule |
|---|---|---|
| `store_id`, `product_id`, `date` | Yes | Store-product-date key. |
| `on_hand_quantity` | Yes | Finite and at least zero. |
| `inbound_quantity` | No | Finite and at least zero; defaults to zero. |
| `lead_time_days` | No | Integer from 0 through 365. |

Inventory is an end-of-day snapshot. `inbound_quantity` is supply planned to arrive on that date;
it is not included in `on_hand_quantity`.

## Calendar

Key: `date`.

| Field | Required | Rule |
|---|---|---|
| `date` | Yes | Unique calendar date. |
| `day_of_week` | Yes | Monday is 0 and Sunday is 6; must match `date`. |
| `is_weekend` | Yes | True for Saturday and Sunday. |
| `is_holiday` | No | Defaults to false. |
| `holiday_name` | No | Requires `is_holiday` to be true. |

## Example

```json
{
  "store_id": "STORE_001",
  "product_id": "SKU_001",
  "date": "2024-01-02",
  "quantity": 10,
  "revenue": 90.00
}
```

Validation errors identify the dataset, row, field, and problem. Small synthetic fixtures live in
`tests/fixtures/`; generated and real datasets stay outside Git.
