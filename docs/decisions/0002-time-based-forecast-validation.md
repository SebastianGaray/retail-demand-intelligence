# ADR 0002: Time-based forecast validation

## Context

Random splits leak future demand patterns and do not represent forecast use.

## Decision

Use rolling forecast origins. Each fold trains only on rows before its origin and evaluates the
same configured horizon. Features use shifted target history or values known at prediction time.

## Consequences

Evaluation costs more than one random split but produces relevant comparisons. Tests must cover
cutoff boundaries and reject features that depend on observed future values.
