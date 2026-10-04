# CEML Validation Plan

Status: **Framework — details freeze in R3 and I1**

No extreme result is trusted merely because one implementation returns 1.

## Layer 1 — unit identities

Test all exact arithmetic identities, macro-transform composition rules, parity/valuation handling, count accumulation, serialization identities, and hash/integrity routines.

## Layer 2 — independent reference oracle

For small and medium inputs, compare the compiled engine against a simple independently authored exact iterator, expected initially to be Python integers or a separate GMP reference.

At configured macro boundaries compare exact state equality, not merely final convergence.

## Layer 3 — reproducible randomized differential testing

Generate deterministic moderate-size test inputs and compare implementations across many cases, including edge conditions for batching and checkpoint boundaries.

## Layer 4 — known trajectory fixtures

Maintain small, independently verified fixtures with start, exact convention, exact step count, selected intermediate states, and final value.

## Layer 5 — implementation diversity

Where practical, compare with an independently authored implementation or alternate mathematical formulation. Two modes sharing the same transformation code are not strong implementation diversity.

## Layer 6 — scale-ladder validation

Before accepting a new magnitude class, exercise workloads below it and explain which correctness invariants are size-independent and which resource/representation assumptions require new testing.

A successful small test alone is not certification for arbitrary scale.

## Failure rule

Any arithmetic disagreement, failed invariant, corrupt checkpoint, nondeterministic regeneration, or unexplained count mismatch blocks V1/E1 and is entered in the failure ledger.

## Validation evidence

Record protocol/build/profile versions, deterministic test seeds, commands, exact checksums, pass/fail counts, resource observations, and all deviations.
