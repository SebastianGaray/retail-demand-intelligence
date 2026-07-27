# Release notes

## 0.1.0

First public project release.

### Included

- Deterministic synthetic retail data generation and validated Parquet contracts.
- Recent-average, seasonal-naive, and LightGBM forecasting.
- Chronological validation with leakage-safe temporal features.
- MAE, WAPE, and MASE overall, by store, and by product.
- Checksummed model, prediction, metric, and metadata artifacts.
- Local FastAPI endpoints and a bilingual Streamlit dashboard.
- Automated formatting, linting, typing, tests, pre-commit hooks, and CI.
- English and Spanish user documentation plus architecture decisions.

### Known limitations

- Evaluation uses a single validation and test block.
- Forecasts do not include uncertainty intervals.
- Inventory risk is a coverage indicator, not replenishment optimization.
- Generated datasets and artifacts are local and excluded from Git.
- The live dashboard remains blocked until a validated synthetic artifact bundle is available to
  the deployment.
