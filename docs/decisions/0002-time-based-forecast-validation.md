# ADR 0002: Time-based forecast validation

## Context

Random splits leak future demand patterns and do not represent forecast use.

## Decision

Use chronological train, validation, and test blocks. Training ends before validation, and
validation ends before the test horizon. Features use shifted target history or values known at
prediction time.

## Consequences

The first release has one validation block and one test block. Tests cover cutoff boundaries and
reject features that depend on observed future values. Rolling origins remain a later extension.
