# Release notes

## 1.0.2 - 2026-08-09

- Prevented the portfolio footer from failing while Streamlit Cloud refreshes cached translation modules.
- Added safe bilingual footer copy for mixed-version deployment transitions.

## 1.0.1 - 2026-08-09

### Fixed

- Normalized tracked demo JSON artifacts to LF so checksums remain stable across platforms.
- Corrected the hosted dashboard bundle checksum and added regression coverage for the tracked bundle.

## 1.0.0 - 2026-08-09

First stable release of the forecasting demo.

### Included

- Versioned `v1.0.0` synthetic dashboard bundle with schema and checksum validation.
- Leakage-safe temporal forecasting, baseline comparison, and inventory-risk presentation.
- Local FastAPI and bilingual Streamlit delivery surfaces.
- Integrity verification before model deserialization.
- Strict formatting, typing, tests, dependency auditing, container build, and CodeQL checks.

### Known limitations

- Evaluation uses one chronological validation block and one test block.
- Forecasts do not include calibrated uncertainty intervals.
- Inventory risk is a coverage indicator rather than replenishment optimization.
- The hosted Streamlit application may sleep when inactive.

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
