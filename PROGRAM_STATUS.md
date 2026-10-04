# CEML Programme Status

**Authoritative current phase:** I1 — HARDWARE-ADAPTIVE IMPLEMENTATION SPECIFICATION  
**Scientific execution authorization:** DENIED  
**Production implementation authorization:** DENIED  
**Scientific master-seed generation:** DENIED  
**Magnitude-rung semantics:** FROZEN as decimal-digits-v1  
**Final executable ladder values:** PROVISIONAL / NOT FROZEN  
**Local machine profile:** NOT MEASURED  
**Scientific protocol version:** CEML-SCI-1  
**Checkpoint format:** CEML-CKPT-1  
**Hardware-audit contract:** R4 FROZEN  
**Last status update:** 2026-10-04

## Gate decisions

| Gate | Status | Evidence / consequence |
|---|---|---|
| BOOTSTRAP | COMPLETE | Governance and scaffold committed before R1. |
| R1 | **PASS — 2026-10-04** | docs/LITERATURE_AUDIT.md records the state-of-the-art evidence base and caveats. |
| R2 | **PASS — 2026-10-04** | docs/ALGORITHM_AUDIT.md freezes algorithmic invariants, threat model, validation implications and a machine-neutral shortlist without choosing machine parameters. |
| R3 | **PASS — 2026-10-04** | docs/REPRODUCIBILITY_VALIDATION_AUDIT.md plus the CEML-SCI-1 protocol documents/schemas freeze scientific semantics, deterministic start generation, canonical integrity rules, checkpoint/restart semantics, validation architecture, V1 acceptance and anomaly handling. |
| R4 | **PASS — 2026-10-04** | docs/HARDWARE_AUDIT_SPEC.md freezes privacy-safe observation scope, evidence classes, bounded deterministic calibration, route-activation proof, resource safety, dependency/build provenance, checkpoint-filesystem testing and refusal rules without measuring a machine. |
| I1 | **OPEN — CURRENT GATE** | Complete and approve docs/CODEX_HANDOFF.md. No production implementation or local audit is authorized merely by entering I1. |
| C1 | NOT ENTERED | Local hardware audit/calibration/implementation not authorized. |
| V1 | NOT ENTERED | Production validation not authorized. |
| E1 | NOT ENTERED | Scientific ladder execution not authorized. |

## R4 acceptance summary

R4 froze, without inspecting the user's machine or choosing any local engineering winner:

- an authorized observation scope covering OS/kernel, CPU/topology/features/cache/frequency, memory/swap/bandwidth, intended checkpoint storage/filesystem, toolchains/exact-arithmetic dependencies, permitted counters and accessible thermal/power information;
- mandatory privacy minimization and sanitization, including prohibition on persisting usernames, hostnames, serial/MAC/IP/account identifiers, secrets, unrelated paths/software inventories and stable identifier hashes;
- four distinct C1 evidence classes: OBSERVED_FACT, CALIBRATION_MEASUREMENT, ENGINEERING_DECISION and UNAVAILABLE_OR_UNSUPPORTED;
- a rule that missing measurements remain missing and cannot be replaced by inference, external-machine results or generic specifications;
- deterministic, public-seed/domain-separated, far-below-scientific bounded calibration that never uses the scientific seed or a scientific start;
- required benchmark evidence for build/toolchain/configuration, wall/CPU methodology, memory/storage/thermal observations, repeats/variability, correctness digests and route activation;
- measured C1 comparison requirements for direct/small-block/hierarchical batching, block sizes, GMP/optional FLINT, multiplication crossovers, representations, allocation strategies, compiler modes, parallelism, checkpoint I/O, terminal handoff, canary costs and memory scaling;
- explicit provenance/non-portability treatment for native compiler tuning;
- pinned/offline-capable dependency/build requirements;
- target-filesystem tests for CEML-CKPT-1 durable writes, atomic promotion, directory metadata, A/B retention/recovery and interrupted bounded writes;
- local resource-safety and abort rules with no invented R4 numeric ceilings;
- route-activation proof as a prerequisite for any optimized-route benchmark claim;
- required sanitized C1 hardware reports, benchmark summaries/digests, decision log and frozen local machine/build profile;
- refusal rules for unsafe/unavailable/unmeasured hardware-dependent choices;
- preservation of direct elementary stepping as the V1 independence anchor and explicit non-substitution of calibration for V1.

## Current I1 boundary

I1 is specification synthesis only. It may define implementation interfaces, record schemas, deterministic calibration suites, route-activation hooks, profile/build digest procedures, checkpoint adapters, resource-safety machinery and validation hooks.

I1 may not:

- inspect or infer the user's actual machine as if C1 had begun;
- launch local Codex/C1 or implement the production engine;
- install or modify local toolchains/dependencies;
- generate the scientific master seed;
- freeze the final ladder values;
- run a scientific or giant trajectory;
- choose machine-specific compiler flags, backends, block sizes, representations, thread counts, checkpoint cadence or resource ceilings;
- weaken R4 privacy/evidence requirements;
- alter any CEML-SCI-1 scientific rule for implementation convenience;
- claim C1 or V1 has passed.

## Non-substitution rule

A hardware observation is not a benchmark. A benchmark is not V1 validation. Validation is not scientific execution. A resource stop, failed restart, corrupt artifact or long runtime is not divergence. A suspected counterexample is an anomaly requiring separate certification.

## Change control

Any material change to CEML-SCI-1 map/count, rung, start-generation, integrity, checkpoint, result or anomaly semantics requires an explicit new protocol/schema version and reviewed repository history.

Any relaxation of the R4 privacy/evidence/refusal contract requires an explicit reviewed R4 contract revision; C1 may not make ad hoc exceptions.
