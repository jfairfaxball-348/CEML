# Start Here

## Programme identity

CEML means **Collatz Extreme Magnitude Ladder**. It is an empirical experiment that will eventually evaluate one predetermined random positive odd integer at each successively larger magnitude using exact arithmetic and auditable provenance.

It is independent of every previous Collatz research repository.

## Read order

1. `PROGRAM_STATUS.md` — what is currently authorized.
2. `PROJECT_CHARTER.md` — purpose, exclusions, success criterion.
3. `ROADMAP.md` — mandatory gates R1–R4, I1, C1, V1, E1.
4. `docs/RESEARCH_PROTOCOL.md` — how repository-driven research is conducted.
5. `docs/CLAIM_POLICY.md` — statements CEML may and may not make.
6. `docs/HARDWARE_AUDIT_SPEC.md` — what the later local Codex run must inspect.
7. The remaining audit/specification documents relevant to the current gate.

## Bootstrap status

This commit establishes governance and planning only.

Not authorized:

- production engine implementation;
- scientific seed generation;
- frozen magnitude ladder;
- giant-number trajectory evaluation;
- machine-specific tuning before the machine is inspected;
- scientific claims from calibration workloads;
- interpreting failure to finish as divergence.

## Stage vocabulary

**Research** evaluates evidence and freezes scientific requirements.

**Hardware characterization** measures the actual dedicated machine and records only reproducibility-relevant, sanitized properties.

**Implementation** builds the exact engine under frozen scientific invariants.

**Validation** tests the implementation without executing a scientific rung.

**Scientific execution** evaluates the single precommitted start for a frozen rung.

**Anomaly investigation** begins only after an anomaly trigger freezes the scientific run.

**Proof/certification** is a separate programme if a genuine counterexample candidate ever appears.

No stage may silently impersonate another.
