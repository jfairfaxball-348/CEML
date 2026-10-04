# Collatz Extreme Magnitude Ladder (CEML)

CEML is a standalone empirical research programme for exact Collatz evaluation at extreme starting magnitudes.

Its narrow purpose is:

> Choose exactly one reproducibly random positive odd integer at each successively larger magnitude, evaluate its Collatz trajectory exactly using a validated high-magnitude implementation, and preserve enough provenance to reproduce and independently verify every result.

CEML is **not** a proof-oriented divergence search, a contiguous verification project, a high-throughput search, an anomaly-ranking project, or a continuation of any previous Collatz repository. This repository is the sole authoritative state for CEML.

## Current authorization state

**BOOTSTRAP / GOVERNANCE ONLY — NO SCIENTIFIC COMPUTATION AUTHORIZED.**

As of 2026-10-04, the repository is being established for protocol design and due diligence. The provisional decimal-digit ladder `10^6, 10^7, 10^8, 10^9, 10^10` is not frozen. No scientific master seed may be generated. No production arithmetic engine may be implemented. No giant Collatz start may be run.

Required gates are:

`BOOTSTRAP -> R1 -> R2 -> R3 -> R4 -> I1 -> C1 -> V1 -> E1`

See [START_HERE.md](START_HERE.md), [PROJECT_CHARTER.md](PROJECT_CHARTER.md), and [ROADMAP.md](ROADMAP.md).

## Scientific invariants

Future hardware-specific engineering choices may not alter the exact Collatz semantics, one-start-per-rung rule, deterministic precommitment, exact arithmetic, exact underlying step accounting, checkpoint integrity, reproducibility, result hashing, or anomaly/freeze rules.

## Authority and provenance

Only files and commits in this repository define CEML state. External papers, software, benchmarks, repositories, and claims are evidence to audit—not authority to inherit.
