# ADR 0005: Deterministic demo data

## Context

The public workflow needs realistic retail behavior without real or confidential company data.

## Decision

Generate synthetic daily demand, pricing, promotions, stock, and inbound supply from an explicit
seed and configuration. Persist the seed and configuration fingerprint with the dataset and run.

## Consequences

Examples and tests are reproducible. The generator demonstrates workflow behavior but is not
evidence of production model performance.
