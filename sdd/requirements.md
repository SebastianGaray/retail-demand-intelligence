# Requirements

## Data and forecasting

- Generate deterministic synthetic retail datasets with explicit schemas and referential integrity.
- Preserve chronology across training, validation, and test windows.
- Compare transparent baselines with LightGBM and retain weak results without embellishment.
- Produce versioned Parquet artifacts, metadata, metrics, predictions, and checksums.
- Calculate inventory coverage indicators without presenting replenishment or production claims.

## Interfaces

- Provide a bilingual Streamlit dashboard for overview, forecasts, inventory risk, and model metrics.
- Provide a typed, read-only FastAPI interface over saved artifacts.
- Return explicit unavailable-artifact and invalid-selection states.
- Support local execution without paid services or external customer data.

## Quality and delivery

- Enforce Ruff, formatting, strict Pyright, unit tests, integration tests, and coverage thresholds.
- Verify the container can build and import the installed package.
- Audit Python dependencies and scan source with CodeQL.
- Keep source, identifiers, comments, and technical documentation in English.
