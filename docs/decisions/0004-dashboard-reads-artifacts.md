# ADR 0004: Dashboard reads artifacts directly

## Context

The dashboard must run locally or deploy independently without requiring an API process.

## Decision

The Streamlit dashboard calls the read-only application service over the configured artifact
directory. FastAPI uses the same service but is not in the dashboard request path.

## Consequences

Dashboard deployment includes a validated artifact run. Artifact compatibility is enforced once
in application code instead of separately in both interfaces.
