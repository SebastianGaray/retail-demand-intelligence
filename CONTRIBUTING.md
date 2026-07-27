# Contributing

## Development

1. Install Python 3.12 or later and `uv`.
2. Run `make install`.
3. Keep changes focused and add tests for changed behavior.
4. Run `make check` before opening a pull request.

Use English for source code, identifiers, and technical documentation. Spanish is reserved for
translated user-facing content under `docs/es/` and the future dashboard.

Do not commit `.env`, local datasets, generated artifacts, or credentials. Update `uv.lock` when
dependencies change.

Pull requests should explain the change, its validation, and any data or model compatibility
impact. Link related issues when applicable.
