# Collatz Extreme Magnitude Ladder (CEML)

CEML is a standalone empirical research programme for exact Collatz evaluation at extreme starting magnitudes.

Its narrow purpose is:

> Choose exactly one reproducibly random positive odd integer at each successively larger magnitude, evaluate its Collatz trajectory exactly using a validated high-magnitude implementation, and preserve enough provenance to reproduce and independently verify every result.

CEML is **not** a proof-oriented divergence search, a contiguous verification project, a high-throughput search, an anomaly-ranking project, or a continuation of any previous Collatz repository. No other repository is authoritative for CEML. External work is evidence to audit and cite, not state to inherit.

## Current authorization state

**BOOTSTRAP / GOVERNANCE ONLY — NO SCIENTIFIC COMPUTATION AUTHORIZED.**

The provisional magnitude ladder is `10^6, 10^7, 10^8, 10^9, 10^10` decimal digits. It is deliberately **not frozen**. No scientific master seed may be generated. No production arithmetic engine may be implemented. No giant Collatz start may be run.

Required gates:

`BOOTSTRAP -> R1 -> R2 -> R3 -> R4 -> I1 -> C1 -> V1 -> E1`

See [PROGRAM_STATUS.md](PROGRAM_STATUS.md) for the authoritative authorization boundary.

## Scientific invariants

Future hardware-specific engineering choices may not alter:

- exact Collatz map semantics once frozen;
- deterministic precommitted start generation;
- exactly one start per frozen rung;
- no rerolling for trajectory behaviour;
- exact arithmetic for candidate-affecting operations;
- exact underlying step accounting;
- checkpoint integrity and restartability;
- provenance and result hashing;
- anomaly/freeze rules.

Engineering parameters may be chosen from measured local hardware only after the hardware-audit gate.

## Repository map

Start with [START_HERE.md](START_HERE.md), then read [PROJECT_CHARTER.md](PROJECT_CHARTER.md), [ROADMAP.md](ROADMAP.md), and [docs/RESEARCH_PROTOCOL.md](docs/RESEARCH_PROTOCOL.md).

The `docs/` directory contains bootstrap-stage research and protocol specifications. `schemas/` contains draft machine-readable schemas. `src/` intentionally contains no production engine. `local/` documents local-only artifacts that Git must not track.

## Authority

This repository becomes the sole authoritative state for CEML. A claim, parameter, seed, rung, implementation choice, or result is not part of CEML merely because it exists elsewhere.
