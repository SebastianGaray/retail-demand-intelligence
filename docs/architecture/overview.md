# Architecture

`retail_demand` uses a layered package:

- `configuration`: environment-backed settings.
- `domain`: retail concepts and business rules without framework dependencies.
- `application`: workflows that coordinate domain and infrastructure code.
- `data`: loading, schema validation, and Parquet access.
- `features`: transformations shared by training and inference.
- `modeling`: model training and evaluation.
- `artifacts`: persistence of trained models, metrics, and metadata.
- `api`: the local FastAPI interface.
- `dashboard`: the bilingual Streamlit interface.

Dependencies should point toward `domain` and `application`. API and dashboard code call
application workflows instead of containing forecasting or inventory logic.
