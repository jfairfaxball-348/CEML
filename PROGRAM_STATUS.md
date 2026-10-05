# CEML Programme Status

**Authoritative current phase:** C1 — COMPLETE, STOPPED FOR OPERATOR REVIEW (V1 NOT ENTERED)  
**Scientific execution authorization:** DENIED  
**Production implementation authorization:** AUTHORIZED ONLY UNDER THE APPROVED C1 HANDOFF AND REQUIRED AUDIT/CALIBRATION ORDER  
**Scientific master-seed generation:** DENIED  
**Magnitude-rung semantics:** FROZEN as decimal-digits-v1  
**Final executable ladder values:** PROVISIONAL / NOT FROZEN  
**Local machine profile:** MEASURED AND FROZEN — `config/local_machine_profile.json`, digest `fed3d3c38d5ec932e0f0c311344e19c15190dcfca77d9c026bcb82a178116a9e`  
**Scientific protocol version:** CEML-SCI-1  
**Checkpoint format:** CEML-CKPT-1  
**Hardware-audit contract:** R4 FROZEN  
**Implementation specification:** I1 FROZEN / APPROVED  
**Calibration suite:** CEML-CAL-1 FROZEN  
**Last status update:** 2026-10-05

## Gate decisions

| Gate | Status | Evidence / consequence |
|---|---|---|
| BOOTSTRAP | COMPLETE | Governance and scaffold committed before R1. |
| R1 | **PASS — 2026-10-04** | `docs/LITERATURE_AUDIT.md` records the state-of-the-art evidence base and caveats. |
| R2 | **PASS — 2026-10-04** | `docs/ALGORITHM_AUDIT.md` freezes algorithmic invariants, threat model, validation implications and a machine-neutral shortlist. |
| R3 | **PASS — 2026-10-04** | `docs/REPRODUCIBILITY_VALIDATION_AUDIT.md` plus CEML-SCI-1 documents/schemas freeze scientific semantics, deterministic start generation, canonical integrity, checkpoint/restart, V1 and anomaly rules. |
| R4 | **PASS — 2026-10-04** | `docs/HARDWARE_AUDIT_SPEC.md` freezes privacy-safe observation, bounded calibration, route activation, resource safety, filesystem-durability testing and evidence/refusal rules. |
| I1 | **PASS — 2026-10-04** | `docs/CODEX_HANDOFF.md`, `config/calibration_suite_v1.json`, `schemas/c1_evidence.schema.json` and `schemas/hardware_profile.schema.json` provide an executable C1 specification without machine guessing or production implementation. |
| C1 | **PASS — 2026-10-05 (agent-assessed; operator review required)** | `docs/C1_COMPLETION.md`, the sanitized `local_reports/` artifacts, `local_reports/BUILD_MANIFEST.json` (build digest `14f2811832f052c84cadd83759e6d23e14f657cbf7c9d6cc0fa7f24dceaa312b`, engine commit `5c354aadc85d7e80372d3c49547b1c73bc2d449f`) and `config/local_machine_profile.json`. Limitations are listed in the completion record. C1 has stopped. |
| V1 | NOT ENTERED | Not authorized by C1 completion. Requires operator review of the C1 package and a separate reviewed status transition. |
| E1 | NOT ENTERED | Scientific ladder execution, final ladder freeze and scientific seed event remain unauthorized. |

## I1 acceptance summary

I1 freezes, without inspecting the actual machine or selecting a local performance winner:

- definition-oracle, production-engine, affine-block, hierarchical batching, terminal-safety, counter, route, checkpoint, canonicalization, audit, calibration, build/profile and validation interfaces;
- code-level C/T/U, affine, split/composition, exact-count, first-1 and arbitrary-precision invariants;
- the terminal-safe macro rule: for nonterminal `n`, a macro is definition-level safe only when `k <= bit_length(n)-1`, otherwise exact direct/odd-only handoff/decomposition is required;
- a public-API candidate baseline and explicit rejection of private GMP/FLINT internals, raw limb serialization and other unsupported/high-risk baselines;
- stable route IDs and fail-closed REQUIRE activation evidence;
- versioned C1 artifact paths and schemas;
- CEML-CAL-1 deterministic engineering input generation, case ordering, benchmark matrix and hard suite maxima;
- evidence sufficiency, variability/tie-break and refusal rules;
- Linux/macOS/Windows privacy-minimized audit adapters plus a deterministic sensitive-data gate;
- an offline-capable two-layer dependency lock/pin strategy;
- CEML-CKPT-1 platform adapter, interruption/recovery and fresh-process restart requirements;
- engineering-only build/profile digest domains that do not modify any CEML-SCI-1 digest rule;
- required CLI authorization boundaries and all twelve V1 implementation hooks.

## Current C1 boundary

C1 may now inspect the dedicated local machine only within the R4/I1 observation scope, establish conservative local safety ceilings, run the bounded deterministic CEML-CAL-1 suite, make only evidence-backed engineering selections, implement the selected exact engine, build it, test the intended checkpoint filesystem and freeze sanitized build/profile artifacts.

C1 may not:

- generate, request or use the scientific master seed;
- derive or evaluate a scientific start;
- freeze the final executable ladder;
- exceed CEML-CAL-1 or stricter local safety bounds;
- guess unavailable machine facts or import another machine's measurements;
- silently install, upgrade or substitute dependencies;
- select private/unsupported backend routes;
- accept a benchmark without exact correctness agreement and activation proof;
- weaken CEML-SCI-1, CEML-CKPT-1, R4 privacy or V1 requirements;
- claim V1 or proceed to E1 automatically.

C1 completion requires the sanitized reports, benchmark summary/bundle index, engineering decision log, exact build manifest, offline lock/pin evidence, target-filesystem checkpoint durability evidence, sensitive-data-scan PASS and `config/local_machine_profile.json`. C1 then stops for review.

## C1 result

C1 produced its required package and stopped. Scientific execution, scientific master-seed generation, final ladder freeze, V1 and E1 remain exactly as stated above. The engine executable refuses `validate`, `prepare` and `run` under this status. A rejection of any recorded C1 interpretation or decision on review reopens C1 through additive history; it is never patched silently.

## Non-substitution rule

A hardware observation is not a benchmark. A benchmark is not V1 validation. Validation is not scientific execution. A resource stop, failed restart, corrupt artifact or long runtime is not divergence. A suspected counterexample is an anomaly requiring separate certification.

## Change control

Any material change to CEML-SCI-1 map/count, rung, start-generation, integrity, checkpoint, result or anomaly semantics requires an explicit new scientific protocol/schema version and reviewed repository history.

Any relaxation of the R4 privacy/evidence/refusal contract requires an explicit reviewed R4 contract revision. Any material change to the CEML-I1 implementation/calibration/profile contract requires a reviewed I1 engineering-specification revision before affected C1 evidence is accepted.
