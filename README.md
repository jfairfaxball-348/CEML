# Collatz Extreme Magnitude Ladder (CEML)

CEML is a standalone empirical research programme for exact Collatz evaluation at extreme starting magnitudes.

Its narrow purpose is:

> Choose exactly one reproducibly random positive odd integer at each successively larger magnitude, evaluate its Collatz trajectory exactly using a validated high-magnitude implementation, and preserve enough provenance to reproduce and independently verify every result.

CEML is **not** a proof-oriented divergence search, a contiguous verification project, a high-throughput search, an anomaly-ranking project, or a continuation of any previous Collatz repository. No other repository is authoritative for CEML.

## Current authorization state

**CEML-R3 HAS PASSED. THE CURRENT GATE IS CEML-R4 — HARDWARE-AUDIT SPECIFICATION. NO SCIENTIFIC COMPUTATION, SCIENTIFIC SEED GENERATION, PRODUCTION IMPLEMENTATION OR LOCAL HARDWARE AUDIT IS AUTHORIZED YET.**

R3 froze CEML-SCI-1 scientific semantics and the reproducibility/validation contract. The meaning of a decimal-digit rung is frozen, but the final ladder values remain **not frozen**. The actual scientific master seed remains **ungenerated**.

Required gates:

`BOOTSTRAP -> R1 -> R2 -> R3 -> R4 -> I1 -> C1 -> V1 -> E1`

See [PROGRAM_STATUS.md](PROGRAM_STATUS.md) for the authoritative boundary.

## Frozen scientific invariants

Hardware-specific engineering may not alter:

- standard-map/shortcut-map exact semantics and first-1 termination;
- exact standard/shortcut/odd step accounting;
- decimal-digit rung definition;
- deterministic precommitted `ceml-start-v1` generation with no behavioural rerolls;
- exact arithmetic;
- SHA3-256/JCS integrity rules and provenance binding;
- checkpoint/restart equivalence;
- result status semantics;
- independent validation and anomaly/freeze rules.

Engineering parameters may be chosen only from measured local evidence at the later authorized gates.

## Repository map

Start with [START_HERE.md](START_HERE.md). R1/R2/R3 decision records live under `docs/`; frozen machine-readable R3 contracts live under `schemas/`. `src/` intentionally contains no production engine. `local/` is for local-only artifacts that Git must not track.

## Authority

This repository is the sole authoritative state for CEML. A claim, parameter, seed, rung value, implementation choice or result is not part of CEML merely because it exists elsewhere.
