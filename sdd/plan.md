# Implementation plan

## Architecture

The package separates domain models, data loading and validation, deterministic generation, temporal
features, model implementations, application use cases, artifact storage, API presentation, and the
Streamlit dashboard. Interfaces depend on saved artifacts instead of retraining at request time.

## Data flow

Synthetic tables are validated before temporal features are calculated. Training compares baselines
and LightGBM using chronological windows, writes a versioned run, and derives a compact demo bundle.
The API and dashboard read that immutable bundle through shared application services.

## Verification

Unit tests cover invariants, metrics, leakage boundaries, configuration, and presentation logic.
Integration tests exercise Parquet generation, training, artifact persistence, API responses, and
dashboard reruns. CI adds 75% minimum coverage, dependency auditing, a container smoke test, CodeQL,
pinned actions, and weekly dependency maintenance.

## Repository presentation

The README presents English and Spanish in one rendered document. Both languages follow the same
sequence from product behavior and data through setup, verification, limitations, and licensing.

## Engineering process page

The Streamlit sidebar exposes a dedicated bilingual process page. It presents four connected stages:
specification, AI assistance, human decisions, and validation evidence. The copy uses concrete project
examples such as chronological splits, leakage checks, artifact contracts, and test coverage. Links
open the versioned SDD documents in GitHub. The page remains available when model artifacts are not.
