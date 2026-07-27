# Repository Guidelines

## Purpose and layout

Retail Demand Intelligence demonstrates reproducible demand forecasting and inventory-risk
analysis with local FastAPI and bilingual Streamlit interfaces.

- `src/retail_demand/`: installable package. `domain/` owns business rules. `application/`
  coordinates use cases. `data/`, `features/`, `modeling/`, and `artifacts/` implement workflows.
  `api/` and `dashboard/` are delivery layers.
- `tests/unit/`, `tests/integration/`, and `tests/fixtures/`: behavior checks and small synthetic
  inputs.
- `docs/architecture/`, `docs/decisions/`, `docs/en/`, and `docs/es/`: design, ADRs, and
  language-specific user documentation.
- `scripts/`: reproducible entry points. Reusable logic belongs under `src/`.

Dependencies point inward: delivery and infrastructure modules may use `application` and
`domain`. `domain` and `application` must not import FastAPI or Streamlit. API and dashboard code
call application services. Notebooks are exploration-only and application code must not import
them.

## Engineering rules

- Inspect existing code and callers before editing. Start broad changes with a short plan.
- Use English for code, identifiers, comments, and technical documentation.
- Use Spanish only for translated user documentation and dashboard content. Keep English and
  Spanish user-facing content aligned.
- Target Python 3.12. Ruff owns formatting and linting. Pyright runs in strict mode. Type public
  functions, class attributes, return values, and trust-boundary data.
- Add dependencies only for a clear current use. Update and commit `uv.lock` with dependency
  changes.
- Keep comments for intent or non-obvious constraints. Record meaningful architectural choices
  as short ADRs under `docs/decisions/`.

## Data and forecasting

- Never add real or confidential company data. Keep generated datasets and model artifacts out
  of Git unless they are small test fixtures.
- Validate schemas and business rules at load boundaries. Preserve source, cutoff, seed, schema
  version, and code/model metadata with generated artifacts.
- Evaluate forecasts with time-based splits. Random train/test splits are invalid for temporal
  demand data.
- Features may use only information available at prediction time. Lag and rolling features must
  stop before the forecast origin. Future inputs must be known in advance.

## Tests and validation

Name tests `test_*.py`. Put pure behavior tests in `tests/unit/` and filesystem, artifact, API,
or end-to-end boundaries in `tests/integration/`. Prefer deterministic fixtures and the smallest
test that proves changed behavior. Bug fixes require a regression test.

```bash
make format
make check
make test-unit
make test-integration
```

`make check` validates formatting, linting, strict typing, and all tests. Run it before completion.

## Git and definition of done

Keep changes focused and complete the pull request template. Do not commit, push, or change
remotes without explicit instructions.

Work is done when behavior and boundaries match the request, tests cover meaningful changes,
documentation and translations are current, `make check` passes, generated data stays outside
Git, and the final summary reports validation and remaining limitations.
