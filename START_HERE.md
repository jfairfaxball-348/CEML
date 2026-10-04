# Start Here

## Programme identity

CEML means **Collatz Extreme Magnitude Ladder**. It is a standalone empirical programme that will eventually evaluate exactly one predetermined random positive odd integer at each frozen decimal-digit magnitude rung using exact arithmetic and auditable provenance.

## Current gate

**CEML-R4 passed on 2026-10-04. The authoritative current gate is CEML-I1 — hardware-adaptive implementation specification.**

R1 established the external evidence base. R2 established algorithmic invariants, implementation findings and a correctness threat model. R3 froze CEML-SCI-1 and CEML-CKPT-1. R4 froze the privacy-safe, evidence-driven hardware-audit and bounded-calibration contract that C1 must later execute on the real dedicated machine.

I1 must now turn the frozen scientific and hardware-audit contracts into one self-contained implementation/Codex handoff. I1 may define code interfaces, local audit adapters, bounded benchmark suites, record schemas, route-activation hooks, build/profile digest procedures and acceptance tests. It may not inspect the actual machine as if C1 had begun, choose machine-specific winners, implement the production engine, generate the scientific seed, freeze the final ladder, run a scientific/giant trajectory or claim V1.

## Read order

1. PROGRAM_STATUS.md — authoritative authorization boundary.
2. PROJECT_CHARTER.md — programme purpose and exclusions.
3. ROADMAP.md — mandatory gates.
4. AGENTS.md — repository rules.
5. docs/RESEARCH_PROTOCOL.md — research discipline.
6. docs/LITERATURE_AUDIT.md — R1 evidence.
7. docs/ALGORITHM_AUDIT.md — R2 algorithm/source audit.
8. docs/REPRODUCIBILITY_VALIDATION_AUDIT.md — R3 decision/evidence record.
9. docs/RANDOMNESS_AND_REPRODUCIBILITY.md.
10. docs/EXPERIMENT_PROTOCOL.md.
11. docs/CHECKPOINT_SPEC.md.
12. docs/RESULT_SCHEMA.md.
13. docs/VALIDATION_PLAN.md.
14. docs/SECURITY_AND_INTEGRITY.md.
15. docs/CLAIM_POLICY.md.
16. docs/HARDWARE_AUDIT_SPEC.md — R4 frozen audit contract.
17. schemas/run_manifest.schema.json, schemas/checkpoint_metadata.schema.json, schemas/result.schema.json, schemas/validation_evidence.schema.json.
18. docs/CODEX_HANDOFF.md — current I1 target.
19. NEXT_SESSION_PROMPT.md.

## Frozen R3 scientific essentials

- Reference map: standard C; exact implementations may use T/odd-only/affine batching.
- Terminal condition: first occurrence of 1.
- Mandatory exact counters: standard, shortcut and odd, with standard = shortcut + odd.
- Rung: all positive odd integers with exactly D decimal digits.
- Start generator: ceml-start-v1, SHAKE256, unbiased rejection sampling, one later 32-byte scientific master seed.
- Integrity: SHA3-256 + RFC 8785 JCS + frozen domain labels.
- Checkpoint: CEML-CKPT-1; derived caches disposable; restart must be mathematically equivalent.
- Validation: direct elementary stepping is the independence anchor; zero unexplained disagreements for V1.
- Non-completion statuses never imply divergence.

## Frozen R4 audit essentials

- C1 records OBSERVED_FACT, CALIBRATION_MEASUREMENT, ENGINEERING_DECISION and UNAVAILABLE_OR_UNSUPPORTED separately.
- Missing machine facts remain missing; no guesses, generic benchmarks or inferred specifications may substitute.
- Sensitive identifiers are minimized and sanitized before persistence or commit.
- Calibration is bounded, deterministic, public-seed/domain-separated and non-scientific.
- A benchmark is usable only with correctness agreement and proof that the intended optimized route actually activated.
- Compiler/native tuning, backend, block size, representation, threading and resource ceilings remain C1 measured choices.
- CEML-CKPT-1 storage durability must be established on the target filesystem through documented semantics and bounded interruption/recovery tests.
- Sanitized hardware reports, benchmark summary/digests, decision log and local machine/build profile are required C1 artifacts.
- Calibration cannot satisfy V1 and no hardware result can alter CEML-SCI-1.

## Current prohibitions

Do not generate the scientific master seed, freeze the final ladder, run a scientific/giant start, implement the production engine, launch local Codex/C1 work, assume unmeasured hardware, choose machine-specific tuning, or claim V1/E1 completion.

I1 is specification synthesis only.
