# CEML Roadmap

This roadmap is gate-based. Dates are intentionally absent; evidence, not schedule pressure, controls progression.

## BOOTSTRAP — governance and planning

Deliver repository scaffold, charter, research protocol, claim boundaries, hardware-audit framework, schemas, integrity rules, and a gate model. No production implementation or scientific computation.

## CEML-R1 — state-of-the-art and literature audit — PASS

Research the current literature, implementations, reproductions, performance evidence and correctness caveats.

**Exit evidence:** docs/LITERATURE_AUDIT.md.

## CEML-R2 — algorithm and implementation audit — PASS

Compare viable exact evaluation families and reconstruct invariants, correctness risks and local benchmark questions without choosing machine-specific parameters.

**Exit evidence:** docs/ALGORITHM_AUDIT.md.

## CEML-R3 — reproducibility and validation audit — PASS

Freeze magnitude/rung definition; deterministic start generation and seed handling; exact map/count semantics; canonical manifests/digests; checkpoint/restart semantics; independent validation architecture; fixtures; V1 acceptance; anomaly/freeze rules; and result certification.

**Exit evidence:** docs/REPRODUCIBILITY_VALIDATION_AUDIT.md, CEML-SCI-1 protocol documents and R3-frozen schemas. The scientific master seed remains ungenerated and final ladder values remain unfrozen.

## CEML-R4 — hardware-audit specification — PASS

Freeze what a later C1 local audit may inspect, sanitize, benchmark and optimize, with privacy exclusions, deterministic bounded-work rules, route-activation requirements, checkpoint-filesystem validation, evidence classes, refusal rules and explicit separation from V1/scientific execution.

**Exit evidence:** docs/HARDWARE_AUDIT_SPEC.md. R4 records no local machine facts and selects no hardware-dependent winner.

## CEML-I1 — hardware-adaptive implementation specification — CURRENT

Produce the self-contained implementation/Codex brief. It must map frozen CEML-SCI-1 and R4 requirements into interfaces, record formats, deterministic bounded benchmark suites, audit adapters, route-activation mechanisms, local profile/digest rules and acceptance tests while leaving measured hardware choices to C1.

**Exit evidence:** docs/CODEX_HANDOFF.md APPROVED in the same reviewed repository state that authorizes C1.

## CEML-C1 — local hardware audit and implementation

On the dedicated local machine: inspect/sanitize the environment, establish resource-safety limits, run bounded deterministic calibration, prove candidate route activation, validate the intended checkpoint filesystem, select engineering choices from measurements, build the system, freeze the local machine/build profile and document every choice.

**Prohibition:** no scientific rung and no scientific seed generation.

## CEML-V1 — local implementation validation

Execute the R3-frozen layered validation contract, including independent direct-oracle checks, deterministic differential testing, restart equivalence, fault injection, canonicalization/digest agreement and feature-route coverage.

**Exit evidence:** schema-valid V1-PASS evidence with zero unexplained disagreements.

## CEML-E1 — scientific ladder

Only after V1 may the final executable ladder values be frozen and the already specified scientific seed event be authorized. Generate exactly one master seed under CEML-SCI-1, commit its commitment, precommit all starts, disclose/regenerate, then evaluate one predetermined start per rung with no rerolls.

An anomaly freezes progression and enters a separate audit/certification state. A resource stop or failure to finish is not divergence.
