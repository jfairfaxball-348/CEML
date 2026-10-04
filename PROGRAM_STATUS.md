# CEML Programme Status

**Authoritative current phase:** R4 — HARDWARE-AUDIT SPECIFICATION  
**Scientific execution authorization:** DENIED  
**Production implementation authorization:** DENIED  
**Scientific master-seed generation:** DENIED  
**Magnitude-rung semantics:** FROZEN as `decimal-digits-v1`  
**Final executable ladder values:** PROVISIONAL / NOT FROZEN  
**Local machine profile:** NOT MEASURED  
**Scientific protocol version:** CEML-SCI-1  
**Checkpoint format:** CEML-CKPT-1  
**Last status update:** 2026-10-04

## Gate decisions

| Gate | Status | Evidence / consequence |
|---|---|---|
| BOOTSTRAP | COMPLETE | Governance and scaffold committed before R1. |
| R1 | **PASS — 2026-10-04** | `docs/LITERATURE_AUDIT.md` records the state-of-the-art evidence base and caveats. |
| R2 | **PASS — 2026-10-04** | `docs/ALGORITHM_AUDIT.md` freezes algorithmic invariants, threat model, validation implications and a machine-neutral shortlist without choosing machine parameters. |
| R3 | **PASS — 2026-10-04** | `docs/REPRODUCIBILITY_VALIDATION_AUDIT.md` plus the CEML-SCI-1 protocol documents/schemas freeze scientific semantics, deterministic start generation, canonical integrity rules, checkpoint/restart semantics, validation architecture, V1 acceptance and anomaly handling. |
| R4 | **OPEN — CURRENT GATE** | Complete/freeze the local hardware-audit specification. No local audit is authorized merely by entering R4. |
| I1 | NOT ENTERED | Codex implementation brief not approved. |
| C1 | NOT ENTERED | Local audit/build not authorized. |
| V1 | NOT ENTERED | Production validation not authorized. |
| E1 | NOT ENTERED | Scientific ladder execution not authorized. |

## R3 acceptance summary

R3 froze, without generating a scientific seed or implementing production code:

- standard Collatz map C as the mathematical reference, shortcut map T as an exact permitted representation, and first occurrence of 1 as the terminal boundary;
- exact unbounded `standard_steps`, `shortcut_steps`, and `odd_steps` with invariant `standard = shortcut + odd`;
- decimal-digit rung semantics `R_D` as all positive odd D-digit integers, while leaving the actual ladder values unfrozen;
- `ceml-start-v1`: SHAKE256/FIPS-202 deterministic expansion, U64-length-framed integer encoding, uniform rejection sampling, rung/index/retry binding and independent test vectors;
- one-time later seed generation, commitment, full-ladder start precommitment and disclosure/regeneration policy, with scientific randomness separated from validation/calibration randomness;
- SHA3-256/FIPS-202 digests, RFC 8785 JCS canonical JSON, lowercase-hex rendering, domain labels and self-digest omission rules;
- `CEML-CKPT-1` canonical checkpoint body/metadata semantics, crash-consistent promotion requirements, corruption/version refusal and exact restart equivalence;
- result statuses in which only `completed` denotes first-1 completion and every non-completed status is explicitly non-divergence evidence;
- a diverse validation architecture anchored by direct elementary stepping rather than shared affine recurrences;
- objective V1 zero-unexplained-disagreement acceptance criteria and machine-readable validation evidence;
- anomaly/failure rules that stop automatic progression and preserve evidence.

CEML-SCI-1 deliberately does not freeze peak/minimum trajectory metrics, because R2 did not establish a common exact observation contract under batched implementations. Adding such a scientific metric requires a later protocol/schema version.

## Current R4 boundary

R4 is research/specification only. It may refine `docs/HARDWARE_AUDIT_SPEC.md` so a later C1 local audit can inspect and sanitize the real machine, execute bounded deterministic calibration, and record evidence needed for hardware-dependent engineering choices.

R4 may not:

- inspect or infer the user's local machine as if C1 had begun;
- launch local Codex or implement the production engine;
- generate the scientific master seed;
- freeze the final ladder values;
- run a scientific or giant trajectory;
- choose machine-specific compiler flags, backends, block sizes, thread counts, checkpoint cadence or resource ceilings without measured C1 evidence;
- weaken or replace any CEML-SCI-1 scientific rule for performance reasons;
- claim V1 has passed.

## Non-substitution rule

A benchmark is not validation. Validation is not scientific execution. A resource stop, failed restart, corrupt artifact or long runtime is not divergence. A suspected counterexample is an anomaly requiring separate certification.

## Change control

Any material change to CEML-SCI-1 map/count, rung, start-generation, integrity, checkpoint, result or anomaly semantics requires an explicit new protocol/schema version and reviewed repository history. No later hardware decision may silently alter them.
