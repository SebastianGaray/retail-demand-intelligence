# ADR 0001: Layered package boundaries

## Context

Forecasting logic must be reusable from scripts, FastAPI, and Streamlit without coupling it to a
delivery framework.

## Decision

Keep business rules in `domain`, orchestration in `application`, and framework code in `api` and
`dashboard`. Delivery modules call application services. Domain and application modules do not
import FastAPI or Streamlit.

## Consequences

The same workflows serve both interfaces. Some data conversion remains at delivery boundaries,
but no general repository or service interfaces are added until a second implementation exists.
