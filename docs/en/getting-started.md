# Getting started

Install Python 3.12 and `uv`, then run:

```bash
make install
make check
```

Copy `.env.example` to `.env` only when local overrides are needed.

See [dataset contracts](datasets.md) for the validated Parquet inputs.
See [synthetic demo data](demo-data.md) to generate a local dataset.
See [forecasting](forecasting.md) for training, evaluation, and saved predictions.
See [local interfaces](interfaces.md) for FastAPI, Streamlit, and the smoke-test checklist.
See [Streamlit Community Cloud](streamlit-community-cloud.md) for hosted dashboard constraints.
