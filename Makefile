.PHONY: install sync sample-data format format-check lint typecheck test test-unit test-integration check clean

install:
	uv sync --dev
	uv run pre-commit install

sync:
	uv sync --dev

sample-data:
	uv run retail-demand generate-data --stores 5 --products 50 --days 730 --seed 42 --output data/processed/demo

format:
	uv run ruff format .
	uv run ruff check --fix .

format-check:
	uv run ruff format --check .

lint:
	uv run ruff check .

typecheck:
	uv run pyright

test:
	uv run pytest

test-unit:
	uv run pytest tests/unit

test-integration:
	@if test -n "$$(find tests/integration -name 'test_*.py' -print -quit)"; then \
		uv run pytest tests/integration; \
	else \
		echo "No integration tests yet."; \
	fi

check: format-check lint typecheck test

clean:
	rm -rf .pytest_cache .pyright .ruff_cache .coverage htmlcov build dist
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f -name '*.py[co]' -delete
