# ADR 0006: Baseline-first forecasting

## Context

A learned model is useful only when it improves on understandable forecasts under the same
chronological evaluation.

## Decision

Evaluate a recent 28-day average first, then a weekly seasonal-naive forecast. Train LightGBM
after both baselines using the same periods and prediction-time-safe features. LightGBM becomes
the champion only when validation WAPE is at least 2% lower than the best baseline.

## Consequences

Every run keeps all three forecasts and metrics. A baseline remains the published model when the
extra complexity has no material validation benefit. More tuning is justified only after stable
improvement across additional time origins or meaningful product and store segments.
