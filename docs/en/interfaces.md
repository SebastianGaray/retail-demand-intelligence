# Local interfaces

FastAPI and Streamlit read the same saved artifact run. Neither interface trains a model.

## Prepare artifacts

```bash
make sample-data
make train
make evaluate
make predictions
```

`make demo` runs those commands and starts Streamlit. Generated data and artifacts remain outside
Git.

## FastAPI

```bash
make api
```

Open `http://127.0.0.1:8000/docs` for the local OpenAPI interface.

| Endpoint | Purpose |
|---|---|
| `GET /health` | Report whether a complete artifact run is available. |
| `GET /metadata` | Return project and artifact metadata. |
| `GET /stores` | List stores. |
| `GET /products` | List products. |
| `GET /forecast` | Return history and holdout predictions for one store-product pair. |
| `GET /inventory-risk` | Return coverage-based stockout and excess indicators. |
| `GET /performance` | Return overall, store, and product metrics. |

Missing artifacts return HTTP 503 with an `artifacts_unavailable` code. Unknown store or product
identifiers return HTTP 404 with a `selection_not_found` code.

## Streamlit

```bash
make app
```

Open `http://localhost:8501`. The dashboard reads Parquet and JSON artifacts directly; FastAPI
does not need to be running. If artifacts are absent or incomplete, the app starts with a clear
setup message.

The five pages cover summary metadata, forecast inspection, inventory coverage, model metrics,
and project context. English and Spanish use the same stable translation keys.

## Manual dashboard smoke test

- Start `make app` without `artifacts/runs/demo`; confirm the setup message and About content.
- Prepare artifacts and restart the app; confirm the Overview counts and periods match metadata.
- Switch between English and Spanish on every page; confirm labels fit without truncation.
- Select a store and product; confirm history, predictions, errors, promotions, and stockouts
  update together.
- Change both inventory thresholds; confirm risk counts and table flags update.
- Compare overall, store, and product metrics; confirm MAE, WAPE, and MASE explanations remain
  visible.
- Open all repository and documentation links on the About page.
- Refresh the browser; confirm the dashboard does not start training or require FastAPI.
