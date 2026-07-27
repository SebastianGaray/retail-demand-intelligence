# ADR 0003: Parquet artifact contract

## Context

Training, the API, and the dashboard need a stable local exchange format without a database.

## Decision

Persist tabular data as Parquet and describe each immutable run in a versioned JSON manifest.
Include input fingerprints and file checksums. Store trained scikit-learn and LightGBM objects
with joblib only for trusted local artifacts.

## Consequences

Interfaces can read one run without starting another process. Readers must validate manifest
versions and checksums, and must never load model files from untrusted sources.
