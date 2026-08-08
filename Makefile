.PHONY: install sync sample-data train evaluate predictions demo-artifacts api app demo format format-check lint typecheck test test-unit test-integration coverage audit check clean

install:
	uv sync --dev
	uv run pre-commit install

sync:
	uv sync --dev

sample-data:
	uv run retail-demand generate-data --stores 5 --products 50 --days 730 --seed 42 --output data/processed/demo

train:
	uv run retail-demand train --data data/processed/demo --output artifacts/runs/demo --horizon 28 --seed 42

evaluate:
	uv run retail-demand evaluate --data data/processed/demo --artifact artifacts/runs/demo

predictions:
	uv run retail-demand predictions --artifact artifacts/runs/demo

demo-artifacts:
	$(MAKE) sample-data
	$(MAKE) train
	$(MAKE) evaluate
	$(MAKE) predictions
	uv run retail-demand build-demo-artifacts \
		--source artifacts/runs/demo \
		--output demo_artifacts/v0.1.0

api:
	RETAIL_DEMAND_ARTIFACT_DIRECTORY=artifacts/runs/demo uv run uvicorn retail_demand.api.main:app --reload

app:
	RETAIL_DEMAND_ARTIFACT_DIRECTORY=artifacts/runs/demo uv run streamlit run src/retail_demand/dashboard/app.py

demo:
	$(MAKE) sample-data
	$(MAKE) train
	$(MAKE) evaluate
	$(MAKE) predictions
	$(MAKE) app

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

coverage:
	uv run pytest --cov=retail_demand --cov-report=term-missing --cov-report=xml --cov-fail-under=75

audit:
	uv run pip-audit

check: format-check lint typecheck coverage audit

clean:
	rm -rf .pytest_cache .pyright .ruff_cache .coverage htmlcov build dist
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f -name '*.py[co]' -delete
