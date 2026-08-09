# Release readiness for 1.0.0

## Checklist

- [x] Package and demo bundle versions are `1.0.0`; the compatible artifact schema remains `1`.
- [x] README commands match the Makefile and CLI.
- [x] Runtime and development dependencies are separated and locked.
- [x] Synthetic data is clearly identified.
- [x] Generated data, artifacts, credentials, and local caches are ignored.
- [x] English and Spanish documentation is linked.
- [x] Contribution, security, license, issue, and pull request files exist.
- [x] CI runs formatting, linting, strict typing, and tests.
- [x] Local API and dashboard handle missing artifacts.
- [x] Add a real dashboard screenshot.
- [x] Publish a validated synthetic artifact bundle for the hosted dashboard.
- [x] Deploy the dashboard and replace the live-demo placeholder.
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

The release can proceed after the final diff, local validation, and required CI checks pass. The
tracked synthetic bundle, dashboard screenshot, and public Streamlit URL are present; the dashboard
continues to avoid training at startup.
