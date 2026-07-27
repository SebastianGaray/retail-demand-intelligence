# Repository Guidelines

## Project structure

- `src/retail_demand/` is the installable package. Keep domain rules independent from FastAPI
  and Streamlit; interfaces call workflows in `application/`.
- `tests/unit/` contains isolated checks, `tests/integration/` contains boundary checks, and
  `tests/fixtures/` holds reusable test data.
- `data/` is for ignored local datasets. Generated models and reports belong in ignored
  `artifacts/`.
- `docs/architecture/` describes boundaries, `docs/decisions/` records decisions, and
  `docs/en/` and `docs/es/` contain language-specific documentation.
- `scripts/` contains reproducible entry points; reusable logic stays under `src/`.

## Development commands

- `make install`: sync development dependencies and install pre-commit hooks.
- `make sync`: synchronize the environment from `uv.lock`.
- `make format`: apply Ruff formatting and safe lint fixes.
- `make check`: validate formatting, lint, types, and all tests.
- `make test-unit` / `make test-integration`: run one test category.
- `make clean`: remove local Python and test artifacts.

Run commands through `uv`; do not maintain a separate requirements file.

## Code and tests

- Target Python 3.12, use four-space indentation, complete public type annotations, and
  descriptive `snake_case` names.
- Ruff owns formatting and linting. Pyright runs in strict mode.
- Name tests `test_*.py` and place them according to the boundary they exercise.
- Add the smallest test that fails without the behavior under change.
- Use English for code, identifiers, and technical documentation. Spanish is for translated
  user-facing content.

## Changes and pull requests

There is no commit history from which to infer a commit convention. Keep commits and pull
requests focused. Complete the pull request template and run `make check`.

Never commit `.env`, datasets, credentials, or generated artifacts. Commit `uv.lock` whenever
`pyproject.toml` dependencies change.

## Agent instructions

Prefer focused changes and existing package boundaries. Do not add abstractions or dependencies
for hypothetical use. Keep forecasting and inventory logic out of API and dashboard modules.
Do not edit the configured Git remote, commit, or push unless explicitly requested.
