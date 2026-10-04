# Start Here

## Programme identity

CEML means **Collatz Extreme Magnitude Ladder**. It is a standalone empirical programme that will eventually evaluate exactly one predetermined random positive odd integer at each frozen decimal-digit magnitude rung using exact arithmetic and auditable provenance.

## Current gate

**CEML-R3 passed on 2026-10-04. The authoritative current gate is CEML-R4 — hardware-audit specification.**

R1 established the external evidence base. R2 established algorithmic invariants, implementation findings and a correctness threat model. R3 froze CEML-SCI-1: scientific map/count semantics, decimal-digit rung semantics, deterministic start generation/seed policy, canonical encodings/digests, checkpoint/restart semantics, result statuses, validation architecture and V1 acceptance criteria.

No scientific execution, scientific seed generation, final ladder freeze, production implementation or local hardware audit is authorized yet.

## Read order

1. `PROGRAM_STATUS.md` — authoritative authorization boundary.
2. `PROJECT_CHARTER.md` — programme purpose and exclusions.
3. `ROADMAP.md` — mandatory gates.
4. `AGENTS.md` — repository rules.
5. `docs/RESEARCH_PROTOCOL.md` — research discipline.
6. `docs/LITERATURE_AUDIT.md` — R1 evidence.
7. `docs/ALGORITHM_AUDIT.md` — R2 algorithm/source audit.
8. `docs/REPRODUCIBILITY_VALIDATION_AUDIT.md` — R3 decision/evidence record.
9. `docs/RANDOMNESS_AND_REPRODUCIBILITY.md`.
10. `docs/EXPERIMENT_PROTOCOL.md`.
11. `docs/CHECKPOINT_SPEC.md`.
12. `docs/RESULT_SCHEMA.md`.
13. `docs/VALIDATION_PLAN.md`.
14. `docs/SECURITY_AND_INTEGRITY.md`.
15. `schemas/run_manifest.schema.json`, `schemas/checkpoint_metadata.schema.json`, `schemas/result.schema.json`, `schemas/validation_evidence.schema.json`.
16. `docs/CLAIM_POLICY.md`.
17. `docs/HARDWARE_AUDIT_SPEC.md` — current R4 target.
18. `NEXT_SESSION_PROMPT.md`.

## Frozen R3 essentials

- Reference map: standard C; exact implementations may use T/odd-only/affine batching.
- Terminal condition: first occurrence of 1.
- Mandatory exact counters: standard, shortcut and odd, with `standard=shortcut+odd`.
- Rung: all positive odd integers with exactly D decimal digits.
- Start generator: `ceml-start-v1`, SHAKE256, unbiased rejection sampling, one 32-byte future master seed.
- Integrity: SHA3-256 + RFC 8785 JCS + frozen domain labels.
- Checkpoint: `CEML-CKPT-1`; derived caches disposable; restart must be mathematically equivalent.
- Validation: direct elementary stepping is the independence anchor; zero unexplained disagreements for V1.
- Non-completion statuses never imply divergence.

## Current prohibitions

Do not generate the scientific master seed, freeze the final ladder, run a scientific/giant start, implement the production engine, launch local Codex, assume unmeasured hardware, choose machine-specific tuning, or claim V1/E1 completion.

R4 is allowed only to freeze what a later local hardware audit may inspect, sanitize, benchmark and decide.
