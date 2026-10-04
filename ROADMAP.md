# CEML Roadmap

This roadmap is gate-based. Dates are intentionally absent; evidence, not schedule pressure, controls progression.

## BOOTSTRAP — governance and planning — COMPLETE

Deliver repository scaffold, charter, research protocol, claim boundaries, hardware-audit framework, schemas, integrity rules and gate model. No production implementation or scientific computation.

## CEML-R1 — state-of-the-art and literature audit — PASS

Research current literature, implementations, reproductions, performance evidence and correctness caveats.

**Exit evidence:** `docs/LITERATURE_AUDIT.md`.

## CEML-R2 — algorithm and implementation audit — PASS

Compare viable exact evaluation families and reconstruct invariants, correctness risks and local benchmark questions without choosing machine-specific parameters.

**Exit evidence:** `docs/ALGORITHM_AUDIT.md`.

## CEML-R3 — reproducibility and validation audit — PASS

Freeze magnitude/rung definition; deterministic start generation and seed handling; exact map/count semantics; canonical manifests/digests; checkpoint/restart semantics; independent validation architecture; fixtures; V1 acceptance; anomaly handling and result certification.

**Exit evidence:** `docs/REPRODUCIBILITY_VALIDATION_AUDIT.md`, CEML-SCI-1 documents and R3 schemas.

## CEML-R4 — hardware-audit specification — PASS

Freeze what C1 may inspect, sanitize, benchmark and optimize, including privacy exclusions, deterministic bounded-work rules, route-activation requirements, checkpoint-filesystem validation, evidence classes, resource safety and refusal rules.

**Exit evidence:** `docs/HARDWARE_AUDIT_SPEC.md`.

## CEML-I1 — hardware-adaptive implementation specification — PASS

Translate CEML-SCI-1/CEML-CKPT-1/R4 into executable interfaces, code invariants, eligible/rejected candidates, C1 evidence schemas, deterministic CEML-CAL-1 inputs/case matrix, activation instrumentation, build/profile digest rules, checkpoint adapters, offline dependency policy, resource-safety machinery, CLI gates and V1 hooks.

**Exit evidence:** approved `docs/CODEX_HANDOFF.md`, `config/calibration_suite_v1.json`, `schemas/c1_evidence.schema.json` and `schemas/hardware_profile.schema.json`.

## CEML-C1 — local hardware audit and implementation — CURRENT

On the dedicated local machine, in the approved sequence: inspect/sanitize the environment, establish resource ceilings, run bounded CEML-CAL-1, prove route activation, validate the intended checkpoint filesystem, make evidence-backed engineering choices, implement/build the selected exact engine, rerun invalidated calibration when required, and freeze the sanitized build/machine profile.

**Exit evidence:** required sanitized `local_reports/` artifacts, build/dependency provenance, checkpoint-filesystem evidence, sensitive-data-scan PASS and `config/local_machine_profile.json`.

**Prohibition:** no scientific seed/start/rung and no automatic V1 entry.

## CEML-V1 — local implementation validation

After a reviewed C1 PASS, execute CEML-V1-SUITE-1 for the exact engine/build/profile: independent direct-oracle checks, deterministic differential tests, restart equivalence, fault injection, canonicalization/digest agreement, feature-route coverage and checked/sanitized builds.

**Exit evidence:** schema-valid V1-PASS evidence with zero unexplained disagreements.

## CEML-E1 — scientific ladder

Only after V1 may the final executable ladder values and scientific seed event be authorized under the frozen lifecycle. Commit the final ladder, generate exactly one master seed, commit its commitment, precommit all starts, disclose/regenerate, then evaluate one predetermined start per rung with no rerolls.

An anomaly freezes progression and enters separate certification. A resource stop or failure to finish is not divergence.
