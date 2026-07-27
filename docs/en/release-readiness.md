# Release readiness for 0.1.0

## Checklist

- [x] Package and artifact schema versions are `0.1.0` and `1`.
- [x] README commands match the Makefile and CLI.
- [x] Runtime and development dependencies are separated and locked.
- [x] Synthetic data is clearly identified.
- [x] Generated data, artifacts, credentials, and local caches are ignored.
- [x] English and Spanish documentation is linked.
- [x] Contribution, security, license, issue, and pull request files exist.
- [x] CI runs formatting, linting, strict typing, and tests.
- [x] Local API and dashboard handle missing artifacts.
- [ ] Add a real dashboard screenshot.
- [ ] Publish a validated synthetic artifact bundle for the hosted dashboard.
- [ ] Deploy the dashboard and replace the live-demo placeholder.
- [ ] Review the final staged diff before creating the release commit.
- [ ] Confirm CI passes on the release commit.

## Files that remain outside Git

- `.env` and `.streamlit/secrets.toml`.
- `.venv/`, Python bytecode, and tool caches.
- `data/processed/` and every other generated dataset under `data/`.
- `artifacts/`, including models, predictions, metrics, and run metadata.
- Coverage, build, and package output such as `.coverage`, `htmlcov/`, `build/`, and `dist/`.
- Local IDE and operating-system files.
- Notebooks with generated output or local data extracts.

Small synthetic fixtures under `tests/fixtures/` are the only dataset exception.

## Release blockers

The source release can proceed after the final diff and CI checks.

The public dashboard is blocked by the missing deployable artifact bundle, screenshot, and live
URL. The repository deliberately excludes generated artifacts, and the dashboard does not train
at startup. Resolve this by publishing a validated synthetic run through an explicit deployment
mechanism, then complete the Streamlit smoke test.
