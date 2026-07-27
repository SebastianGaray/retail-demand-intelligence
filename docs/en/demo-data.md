# Synthetic demo data

The generator creates related Parquet datasets for stores, products, prices, promotions, sales,
inventory, and calendar dates. Names and values are synthetic and do not represent a company.

```bash
uv run retail-demand generate-data \
  --stores 5 \
  --products 50 \
  --days 730 \
  --seed 42 \
  --output data/processed/demo
```

`make sample-data` runs the same command. The output directory is ignored by Git.

## Demand assumptions

Each product receives a stable base demand, base price, annual trend, and price elasticity. Each
store receives a demand multiplier. Daily expected demand combines those values with:

- lower weekday and higher weekend demand;
- gradual positive or negative product trends;
- lower demand when price rises relative to the product base price;
- extra demand during promotions;
- seeded daily noise.

Promotions last 5 to 10 days, discount prices by 10% to 25%, and add a moderate demand uplift.
Promotion periods do not overlap for the same store and product.

Inventory starts with a few days of demand. Replenishment is attempted every seven days, with
small variation and occasional missed deliveries. Sales are the lower of simulated demand and
available stock. `on_hand_quantity` is the end-of-day balance; `inbound_quantity` is supply
received before that day's sales.

## Output

The seven Parquet files follow the [dataset contracts](datasets.md). Generation reloads and
validates every file before publishing it to the output directory.

`manifest.json` marks the data as synthetic and records:

- generator version and UTC generation time;
- seed, store count, product count, and history length;
- filename, row count, and SHA-256 checksum for each dataset.

The seed makes dataset values reproducible. The manifest timestamp reflects the current run.

## Known simplifications

- All products are sold as individual units and all prices use USD.
- Stores and products are active for the complete generated period.
- Price trends are smooth; promotions are the only temporary discounts.
- Replenishment uses a weekly cadence rather than purchase orders and supplier constraints.
- Lost demand during stockouts is not observed as sales and is not saved separately.
- Holidays include only two synthetic calendar effects and do not change demand yet.
