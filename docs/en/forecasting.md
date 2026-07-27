# Forecasting workflow

The workflow compares two baselines with LightGBM on synthetic or contract-compatible Parquet
data. Results are offline estimates, not evidence of production performance.

## Run

```bash
make sample-data
make train
make evaluate
make predictions
```

`make train` uses `data/processed/demo` and writes an ignored run to `artifacts/runs/demo`.
`make evaluate` calculates holdout metrics. `make predictions` exports the champion's holdout
predictions for later API and dashboard work.

## Periods and features

The default horizon is 28 days. The last 28 days form the test period, the preceding 28 days form
validation, and earlier eligible rows form training. No dates are shuffled.

Target lags, rolling demand, prior inventory, and inbound supply are shifted by the full forecast
horizon. Therefore, changing demand or inventory inside validation or test cannot alter features
for that same period. Calendar fields, listed prices, and scheduled promotions are treated as
known before prediction. The categorical encoder is fitted on training only; the final test model
is refitted on training plus validation.

The feature set contains:

- store and product identifiers;
- weekday, day of month, month, weekend, and holiday fields;
- price, regular price, promotion status, and discount;
- horizon-safe demand lags and shifted 7-day and 28-day averages;
- horizon-shifted end-of-day inventory and inbound quantities.

## Models and selection

The recent-average baseline repeats each store-product's last 28-day mean. Seasonal naive repeats
the latest observed value for each weekday. LightGBM uses a fixed small configuration and one CPU
thread for reproducible local runs.

Validation WAPE selects the champion. LightGBM must improve the best baseline by at least 2%;
otherwise the baseline remains champion. This rule avoids claiming value from a marginal metric
change.

## Metrics

- MAE is the average absolute unit error.
- WAPE divides total absolute error by total observed demand. It is unavailable when total demand
  is zero.
- MASE divides MAE by the training period's weekly seasonal-naive error. It is unavailable when
  that scale is zero.

Metrics are saved overall, by store, and by product. Segment metrics help locate uneven errors;
they do not replace a longer backtest.

## Artifacts

Each run contains:

```text
metadata.json
model.pkl
validation_predictions.parquet
evaluation_predictions.parquet
metrics.json
predictions.parquet
```

Metadata stores schema and feature versions, seed, horizon, train/validation/test dates,
validation and test metrics, model parameters, the data-manifest checksum, champion name, and
artifact checksums. Model files use Python pickle and must only be loaded from trusted runs.

This first workflow uses one validation and one test block. Multiple rolling origins, tuning, and
probabilistic forecasts should be added only when the single-block workflow is stable.
