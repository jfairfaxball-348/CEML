# Collatz Extreme Magnitude Ladder (CEML)

CEML is a standalone empirical research programme for exact Collatz evaluation at extreme starting magnitudes.

Its narrow purpose is:

> Choose exactly one reproducibly random positive odd integer at each successively larger magnitude, evaluate its Collatz trajectory exactly using a validated high-magnitude implementation, and preserve enough provenance to reproduce and independently verify every result.

CEML is **not** a proof-oriented divergence search, a contiguous verification project, a high-throughput search, an anomaly-ranking project, or a continuation of any previous Collatz repository. No other repository is authoritative for CEML.

## Current authorization state

**CEML-I1 HAS PASSED. THE CURRENT GATE IS CEML-C1 — LOCAL HARDWARE AUDIT AND IMPLEMENTATION. SCIENTIFIC COMPUTATION, SCIENTIFIC SEED GENERATION, FINAL LADDER FREEZE AND V1 CLAIMS ARE NOT AUTHORIZED.**

C1 may inspect the dedicated local machine and implement the production engine only under the approved sequence in `docs/CODEX_HANDOFF.md`: privacy-minimized hardware audit, measured resource ceilings, bounded CEML-CAL-1, evidence-backed engineering decisions, implementation/build, target-filesystem checkpoint proof, then sanitized build/profile freeze.

Required gates:

`BOOTSTRAP -> R1 -> R2 -> R3 -> R4 -> I1 -> C1 -> V1 -> E1`

See `PROGRAM_STATUS.md` for the authoritative boundary.

## Frozen scientific invariants

Hardware-specific engineering may not alter:

- standard-map/shortcut-map exact semantics and first-1 termination;
- exact standard/shortcut/odd step accounting;
- decimal-digit rung definition;
- deterministic precommitted `ceml-start-v1` generation with no behavioural rerolls;
- exact arithmetic;
- SHA3-256/JCS integrity rules and provenance binding;
- CEML-CKPT-1 checkpoint/restart equivalence;
- result status semantics;
- independent validation and anomaly/freeze rules.

## C1 engineering contract

I1 additionally freezes:

- machine-neutral component interfaces and exact code-level invariants;
- eligible/rejected candidate families;
- public-API route policy and activation proof;
- privacy-safe platform audit adapters;
- C1 evidence/profile schemas;
- CEML-CAL-1 deterministic bounded calibration;
- decision sufficiency/tie/refusal rules;
- offline dependency/build provenance;
- checkpoint filesystem/fault-injection contract;
- V1 implementation hooks.

Machine-specific winners remain unselected until C1 measures them.

## Repository map

Start with `START_HERE.md`. R1–R4 evidence and the I1 handoff live under `docs/`. Scientific and C1 machine-readable contracts live under `schemas/`. `config/calibration_suite_v1.json` contains only public engineering constants; `config/local_machine_profile.json` does not exist until C1. `src/` contains no production engine before C1 implementation begins. `local/` is ignored local-only evidence storage.

## Authority

This repository's Git history is the sole authoritative CEML state. A claim, parameter, seed, rung value, implementation choice or result is not part of CEML merely because it exists elsewhere.
