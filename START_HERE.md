# Start Here

## Programme identity

CEML means **Collatz Extreme Magnitude Ladder**. It is an empirical experiment that will eventually evaluate one predetermined random positive odd integer at each successively larger magnitude using exact arithmetic and auditable provenance.

It is independent of every previous Collatz research repository.

## Current gate

**CEML-R1 passed on 2026-10-04. The authoritative current gate is CEML-R2 — algorithm and implementation audit.**

R1 established the external evidence base in docs/LITERATURE_AUDIT.md. Its PASS does not certify any external implementation and does not authorize production implementation or scientific execution.

R2 must compare and source-audit viable exact algorithm families and implementation lineages. Machine-specific choices remain deferred until the later local hardware gate.

## Read order

1. PROGRAM_STATUS.md — what is currently authorized.
2. PROJECT_CHARTER.md — purpose, exclusions, success criterion.
3. ROADMAP.md — mandatory gates R1–R4, I1, C1, V1, E1.
4. AGENTS.md — repository rules for agents.
5. docs/RESEARCH_PROTOCOL.md — how repository-driven research is conducted.
6. docs/LITERATURE_AUDIT.md — completed R1 evidence base and R2 open questions.
7. docs/ALGORITHM_AUDIT.md — current R2 work product.
8. docs/CLAIM_POLICY.md — statements CEML may and may not make.
9. docs/HARDWARE_AUDIT_SPEC.md — framework for the later local Codex run.
10. The remaining audit/specification documents relevant to the current gate.

## Current prohibitions

Not authorized:

- production engine implementation;
- scientific seed generation;
- frozen magnitude ladder;
- giant-number scientific trajectory evaluation;
- local Codex implementation;
- machine-specific tuning before the machine is inspected;
- scientific claims from calibration workloads;
- interpreting failure to finish as divergence.

## R1 facts carried forward, with caveats

R2 may rely on the evidence classifications in docs/LITERATURE_AUDIT.md, including:

- Elsenhans's exact affine/standard-polynomial binary-splitting method is the primary current extreme isolated-start method identified by R1;
- the reported 20-billion-decimal-digit run is an author-reported computation, not an independent CEML reproduction;
- public implementations exist but none was certified as audited by R1;
- step conventions differ materially across sources and must be normalized explicitly;
- contiguous verification above 2^71 is not the same problem as one extreme arbitrary-precision start.

These are evidence conclusions, not production design decisions.

## Stage vocabulary

**Research** evaluates evidence and freezes scientific requirements.

**Hardware characterization** measures the actual dedicated machine and records only reproducibility-relevant, sanitized properties.

**Implementation** builds the exact engine under frozen scientific invariants.

**Validation** tests the implementation without executing a scientific rung.

**Scientific execution** evaluates the single precommitted start for a frozen rung.

**Anomaly investigation** begins only after an anomaly trigger freezes the scientific run.

**Proof/certification** is a separate programme if a genuine counterexample candidate ever appears.

No stage may silently impersonate another.
