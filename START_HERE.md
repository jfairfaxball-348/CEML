# Start Here

## Programme identity

CEML means **Collatz Extreme Magnitude Ladder**. It is an empirical experiment that will eventually evaluate one predetermined random positive odd integer at each successively larger magnitude using exact arithmetic and auditable provenance.

It is independent of every previous Collatz research repository.

## Current gate

**CEML-R2 passed on 2026-10-04. The authoritative current gate is CEML-R3 — reproducibility and validation audit.**

R1 established the external evidence base in docs/LITERATURE_AUDIT.md. R2 established exact algorithm invariants, source-level implementation findings, the correctness threat model and a machine-neutral architecture shortlist in docs/ALGORITHM_AUDIT.md.

Neither PASS certifies a production implementation or authorizes scientific execution.

R3 must now freeze scientific semantics and reproducibility/validation requirements before any hardware-specific implementation work begins.

## Read order

1. PROGRAM_STATUS.md — what is currently authorized.
2. PROJECT_CHARTER.md — purpose, exclusions, success criterion.
3. ROADMAP.md — mandatory gates R1–R4, I1, C1, V1, E1.
4. AGENTS.md — repository rules for agents.
5. docs/RESEARCH_PROTOCOL.md — how repository-driven research is conducted.
6. docs/LITERATURE_AUDIT.md — completed R1 evidence base.
7. docs/ALGORITHM_AUDIT.md — completed R2 algorithm/source audit.
8. docs/RANDOMNESS_AND_REPRODUCIBILITY.md — R3 randomness and start-generation decisions.
9. docs/EXPERIMENT_PROTOCOL.md — scientific semantic contract to freeze in R3.
10. docs/CHECKPOINT_SPEC.md — checkpoint/restart semantics to freeze in R3.
11. docs/RESULT_SCHEMA.md and schemas/ — result/manifest/checkpoint schemas to freeze scientifically.
12. docs/VALIDATION_PLAN.md — validation architecture and V1 acceptance requirements.
13. docs/SECURITY_AND_INTEGRITY.md — digest, precommitment and provenance requirements.
14. docs/CLAIM_POLICY.md — statements CEML may and may not make.
15. docs/HARDWARE_AUDIT_SPEC.md — framework for the later local Codex run.
16. NEXT_SESSION_PROMPT.md — current handoff.

## Current prohibitions

Not authorized:

- production engine implementation;
- scientific master-seed generation;
- final magnitude-ladder freeze;
- giant-number scientific trajectory evaluation;
- local Codex implementation;
- machine-specific tuning before the machine is inspected;
- scientific claims from calibration workloads;
- interpreting failure to finish as divergence.

R3 may freeze the **definition** of a magnitude rung and the deterministic seed/generator protocol, but the actual scientific master seed and final executable ladder remain later-gate decisions.

## R2 facts carried forward, with caveats

R3 may rely on the evidence classifications in docs/ALGORITHM_AUDIT.md, including:

- exact shortcut affine blocks satisfy 2^k T^k(n) = 3^i n + B;
- the low k bits determine the first k shortcut steps;
- affine composition order is non-commutative and must be validated explicitly;
- total-stopping logic must prevent a macro block from passing the first occurrence of 1;
- direct stepping is the strongest definition-level oracle for affine batching;
- several audits in collatz-eval share the affine recurrence and are not independent oracles;
- the Boutoukoat/Gerbicz implementation is an independent code lineage but algebraically the same affine family;
- public/internal arithmetic optimizations, macro sizes and backend thresholds remain C1 hypotheses;
- canonical checkpoint/restart semantics remain to be frozen;
- the Elsenhans source archive and cited Gerbicz primary forum post remain external evidence gaps.

These are evidence conclusions and R3 design inputs, not production engineering decisions.

## Stage vocabulary

**Research** evaluates evidence and freezes scientific requirements.

**Hardware characterization** measures the actual dedicated machine and records only reproducibility-relevant, sanitized properties.

**Implementation** builds the exact engine under frozen scientific invariants.

**Validation** tests the implementation without executing a scientific rung.

**Scientific execution** evaluates the single precommitted start for a frozen rung.

**Anomaly investigation** begins only after an anomaly trigger freezes the scientific run.

**Proof/certification** is a separate programme if a genuine counterexample candidate ever appears.

No stage may silently impersonate another.
