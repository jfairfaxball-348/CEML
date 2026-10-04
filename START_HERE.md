# Start Here

## Programme identity

CEML means **Collatz Extreme Magnitude Ladder**. It is a standalone empirical programme that will eventually evaluate exactly one predetermined random positive odd integer at each frozen decimal-digit magnitude rung using exact arithmetic and auditable provenance.

## Current gate

**CEML-I1 passed on 2026-10-04. The authoritative current gate is CEML-C1 — local hardware audit and implementation.**

R1 established the external evidence base. R2 established algorithmic invariants and the correctness threat model. R3 froze CEML-SCI-1 and CEML-CKPT-1. R4 froze privacy-safe local evidence and bounded-calibration rules. I1 now supplies the exact implementation/audit handoff and CEML-CAL-1.

C1 is the first gate permitted to inspect the actual dedicated machine and implement the production engine, but only in the required order:

`hardware audit -> resource ceilings -> bounded calibration -> evidence-backed decisions -> implementation -> build -> checkpoint-filesystem proof -> frozen sanitized profile`

C1 must stop before V1 and before any scientific seed/start/trajectory.

## Read order for C1

1. PROGRAM_STATUS.md
2. PROJECT_CHARTER.md
3. ROADMAP.md
4. AGENTS.md
5. docs/RESEARCH_PROTOCOL.md
6. docs/LITERATURE_AUDIT.md
7. docs/ALGORITHM_AUDIT.md
8. docs/REPRODUCIBILITY_VALIDATION_AUDIT.md
9. docs/RANDOMNESS_AND_REPRODUCIBILITY.md
10. docs/EXPERIMENT_PROTOCOL.md
11. docs/CHECKPOINT_SPEC.md
12. docs/RESULT_SCHEMA.md
13. docs/VALIDATION_PLAN.md
14. docs/SECURITY_AND_INTEGRITY.md
15. docs/CLAIM_POLICY.md
16. docs/HARDWARE_AUDIT_SPEC.md
17. docs/CODEX_HANDOFF.md
18. config/calibration_suite_v1.json
19. schemas/c1_evidence.schema.json
20. schemas/hardware_profile.schema.json
21. schemas/run_manifest.schema.json
22. schemas/checkpoint_metadata.schema.json
23. schemas/result.schema.json
24. schemas/validation_evidence.schema.json
25. NEXT_SESSION_PROMPT.md

## Frozen scientific essentials

- Reference map: standard C; exact implementations may use T/odd-only/affine batching.
- Terminal condition: first occurrence of 1.
- Mandatory exact counters: standard, shortcut and odd, with `standard = shortcut + odd`.
- Rung: all positive odd integers with exactly D decimal digits.
- Start generator: ceml-start-v1, SHAKE256, unbiased rejection sampling, one later 32-byte scientific master seed.
- Integrity: SHA3-256 + RFC 8785 JCS + frozen scientific domain labels.
- Checkpoint: CEML-CKPT-1; derived caches are disposable; restart must be mathematically equivalent.
- Validation: direct elementary stepping is the independence anchor; V1 permits zero unexplained disagreements.
- Non-completion statuses never imply divergence.

## Frozen C1 engineering essentials

- Evidence classes remain distinct: OBSERVED_FACT, CALIBRATION_MEASUREMENT, ENGINEERING_DECISION and UNAVAILABLE_OR_UNSUPPORTED.
- Missing facts remain missing; no guesses, generic internet specifications or other-machine benchmarks substitute.
- Sensitive identifiers are filtered before persistence where practical and must pass the I1 deterministic scan before commit.
- CEML-CAL-1 uses only public engineering inputs under `CEML-CALIBRATION-RANDOM-V1\0`, capped far below scientific scale.
- A performance record is usable only with exact correctness agreement and positive route-activation proof.
- C1 selects language/backend/representation/flags/threading/block/checkpoint choices only from eligible locally measured candidates.
- Checkpoint durability must be established on the actual intended filesystem/mount class.
- Scientific build/run must be pinned and offline-capable.
- Native-tuned builds are explicitly non-portable and receive distinct build/profile identities.
- Calibration does not satisfy V1.

## Current prohibitions

Do not generate the scientific master seed, freeze the final ladder, derive/evaluate a scientific start, run a giant/scientific trajectory, claim V1/E1 completion, exceed CEML-CAL-1, guess unavailable machine facts or weaken a frozen scientific/audit rule.
