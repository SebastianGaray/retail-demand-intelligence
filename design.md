# Dashboard design

## Direction

Retail Demand Intelligence uses a restrained analytical interface for reviewing synthetic demand,
forecast errors, and inventory coverage. Information density and legibility take priority over
decoration.

The implementation follows the supplied Stitch desktop and mobile references while using native
Streamlit controls. It does not reproduce controls that have no application behavior.

## Visual system

| Token | Value | Use |
|---|---|---|
| Background | `#f7f8f9` | Application canvas |
| Surface | `#ffffff` | Charts, tables, and grouped controls |
| Primary | `#062b3a` | Navigation, headings, active controls |
| Secondary | `#496173` | Supporting text |
| Border | `#d9dee2` | Dividers and surface boundaries |
| Risk | `#ba1a1a` | Stockout risk and destructive states |
| Warning | `#b56b16` | Attention states |
| Success | `#08775b` | Available and normal states |
| Forecast | `#76a5bb` | Predicted demand |

Use Hanken Grotesk for headings when available and Inter for interface text, with system sans-serif
fallbacks. Use a monospaced font for identifiers and numerical table values.

Spacing follows an 8 px grid. Controls have at least 44 px height. Borders are 1 px, radii are
4–8 px, and shadows are reserved for floating Streamlit elements.

## Layout

Desktop uses Streamlit's expanded sidebar and a fluid main canvas up to 1440 px. Mobile uses the
native collapsible sidebar and stacked content. Labels wrap instead of truncating so Spanish text
can expand.

Each page contains:

1. A short title and one line of scope.
2. Controls, when the page supports them.
3. A compact metric strip.
4. One dominant chart or table.
5. Secondary detail.

## Screens

### Overview

Show dataset period, stores, products, observations, champion model, and artifact version. Follow
with aggregate demand, inventory-risk counts, and overall model metrics. Keep the synthetic-data
notice visible.

### Forecast Explorer

Filter by an existing store and product. Show actual and predicted demand on the same timeline,
then evaluated rows and promotion or stockout dates. The dashboard displays saved holdout
predictions. It does not retrain or update forecasts.

### Inventory Risk

Support store, product, stockout-coverage, and excess-coverage filters. Show risk counts, expected
demand, current inventory, average coverage, and a detailed table. Indicators are coverage-based,
not replenishment recommendations.

### Model Performance

Show champion holdout MAE, WAPE, MASE, and observation count. Compare the implemented
recent-average, seasonal-naive, and LightGBM models. Allow selection of one comparison metric and
show results overall, by store, and by product.

### About

Explain purpose, implemented boundaries, synthetic data, limitations, architecture flow,
repository, documentation, and MIT license. Keep paragraphs short.

## States

- Artifact loading: “Reading forecast artifacts…” / “Leyendo artefactos de pronóstico…”
- Forecast loading: “Preparing demand history…” / “Preparando el historial de demanda…”
- Inventory loading: “Calculating inventory coverage…” / “Calculando la cobertura…”
- Metrics loading: “Loading model metrics…” / “Cargando métricas del modelo…”
- Missing artifacts: show `make demo` and state that startup never trains models.
- Empty selection: keep filters visible and explain that no saved rows match.
- Unexpected errors: show a short message without a stack trace.

Loading feedback belongs to the affected workspace. A language or page change must not trigger
training or require FastAPI.

## Internationalization and accessibility

Translations live in `dashboard/translations.py` and use stable keys. English and Spanish have
identical key sets. Controls retain visible labels, keyboard focus remains visible, and risk is
communicated by text as well as color.

## Excluded Stitch concepts

The current application does not include authentication, user profiles, notifications, global
search, regional analytics, store deep-dives, downloadable reports, CSV export, live data,
in-dashboard training, forecast updates, automated recommendations, MAPE, RMSE, bias, XGBoost,
Prophet, or neural networks. These controls are intentionally absent.
