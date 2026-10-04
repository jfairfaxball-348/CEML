# Next Session Prompt — CEML-R4

CEML-R4 — HARDWARE-AUDIT SPECIFICATION

Repository:

https://github.com/jfairfaxball-348/CEML

Authoritative R3-PASS baseline:

Use the current `main` commit containing this prompt. Before changing files, resolve and report its exact commit SHA and verify that `PROGRAM_STATUS.md` says R3 PASS / R4 OPEN.

Treat this repository as the sole authoritative state for CEML.

Read, in order:

1. PROGRAM_STATUS.md
2. START_HERE.md
3. PROJECT_CHARTER.md
4. ROADMAP.md
5. AGENTS.md
6. docs/RESEARCH_PROTOCOL.md
7. docs/LITERATURE_AUDIT.md
8. docs/ALGORITHM_AUDIT.md
9. docs/REPRODUCIBILITY_VALIDATION_AUDIT.md
10. docs/RANDOMNESS_AND_REPRODUCIBILITY.md
11. docs/EXPERIMENT_PROTOCOL.md
12. docs/CHECKPOINT_SPEC.md
13. docs/RESULT_SCHEMA.md
14. docs/VALIDATION_PLAN.md
15. docs/SECURITY_AND_INTEGRITY.md
16. docs/CLAIM_POLICY.md
17. docs/HARDWARE_AUDIT_SPEC.md
18. schemas/run_manifest.schema.json
19. schemas/checkpoint_metadata.schema.json
20. schemas/result.schema.json
21. schemas/validation_evidence.schema.json
22. NEXT_SESSION_PROMPT.md

R1, R2 and R3 have passed. CEML-SCI-1 is frozen. The current phase is R4 specification/research only.

Do not implement the production engine, launch local Codex, inspect or infer the user's actual machine as if C1 had started, generate the scientific master seed, freeze the final ladder values, execute a scientific/giant trajectory, claim V1, or choose machine-specific parameters without later measured evidence.

PURPOSE

Complete and freeze `docs/HARDWARE_AUDIT_SPEC.md` so a later C1 local automated audit can safely and reproducibly characterize the dedicated machine, sanitize evidence, run bounded deterministic engineering calibration, and make hardware-dependent implementation choices without changing any CEML-SCI-1 scientific rule.

At minimum R4 must freeze:

- exact categories of hardware/OS/filesystem/toolchain information C1 may inspect;
- privacy/sensitive-data exclusions and sanitization requirements;
- command/output handling rules so raw sensitive inventories are not committed;
- what counts as observation, benchmark evidence and an engineering decision;
- bounded deterministic calibration workload rules and explicit scientific/non-scientific separation;
- which candidate architecture/backend/compiler/memory/checkpoint/parallelism questions C1 must measure;
- exact measurements to record for time, memory, storage/flush, route activation and thermal/sustained behaviour where available;
- resource-safety limits for calibration as a specification without inventing local values;
- rules for compiler flags such as native tuning and their reproducibility implications;
- dependency/toolchain version capture and offline-build expectations;
- storage/filesystem tests needed to support CEML-CKPT-1 crash-consistent atomic promotion;
- evidence needed to justify each hardware-dependent choice;
- required sanitized human- and machine-readable hardware reports and local profile artifacts;
- failure/refusal rules when required information cannot be measured safely;
- the boundary between R4 specification, C1 measurement/implementation and V1 validation.

R4 must explicitly preserve CEML-SCI-1: map/count semantics, decimal-digit rung meaning, ceml-start-v1, seed policy, SHA3/JCS integrity rules, CEML-CKPT-1 semantics, result statuses and the R3 validation/V1 contract.

R4 passes only if a later local agent could execute the audit without inventing machine facts, leaking sensitive identifiers, silently running scientific work, or making unmeasured tuning decisions.

At the end:

1. commit all R4 repository updates;
2. report the authoritative commit SHA;
3. summarize the frozen hardware-audit contract;
4. list risks legitimately deferred to I1/C1/V1;
5. state explicitly either “CEML-R4 PASS” or “CEML-R4 REMAINS OPEN”;
6. if R4 passes, provide a self-contained CEML-I1 implementation-specification prompt;
7. if R4 remains open, provide the exact continuation task.

No later hardware or performance consideration may change a frozen CEML-SCI-1 scientific rule without an explicit new protocol version.
