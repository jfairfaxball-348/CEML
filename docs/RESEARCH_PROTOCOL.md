# CEML Research Protocol

Status: **R1–R4 AND I1 COMPLETE; CEML-C1 CURRENT**

## Purpose

Repository-driven research, specification, implementation and validation must make decisions auditable before scientific execution. A session is not complete when an answer is written in chat; it is complete when its required evidence, reasoning, open questions and approved decisions are committed here.

## Required sequence

- **R1:** state-of-the-art and literature audit — PASS;
- **R2:** algorithm and implementation audit — PASS;
- **R3:** reproducibility and validation audit — PASS;
- **R4:** hardware-audit specification — PASS;
- **I1:** executable implementation/audit specification — PASS;
- **C1:** local hardware audit, bounded calibration, implementation/build/profile freeze — CURRENT;
- **V1:** frozen validation suite execution;
- **E1:** scientific ladder.

The sequence is mandatory because later evidence depends on earlier frozen semantics.

## Evidence rules

For every material external claim record:

- source and stable locator;
- author/publisher;
- publication/version date where available;
- date accessed;
- source class;
- exact proposition CEML uses;
- relevant conditions;
- caveats/conflicts;
- whether CEML independently reproduced it.

For local hardware work, `docs/HARDWARE_AUDIT_SPEC.md` and `docs/CODEX_HANDOFF.md` control evidence classes, privacy, measurement, route activation, bounded calibration, decision sufficiency and provenance.

Do not equate source availability with correctness. Do not call an implementation audited unless the nature/scope of that audit is documented.

## Decision taxonomy

Each repository conclusion is one of:

- **OBSERVATION:** evidence collected, no decision;
- **PROVISIONAL:** preferred direction pending a later gate;
- **FROZEN-SCIENTIFIC:** change requires scientific protocol versioning;
- **FROZEN-AUDIT:** R4 audit-contract requirement;
- **FROZEN-IMPLEMENTATION-SPEC:** I1 implementation/calibration/profile requirement;
- **FROZEN-ENGINEERING:** C1 build/profile choice requiring build/profile version change to alter;
- **REJECTED:** considered and not selected, with reason;
- **OPEN:** unresolved.

C1 machine evidence uses exactly OBSERVED_FACT, CALIBRATION_MEASUREMENT, ENGINEERING_DECISION and UNAVAILABLE_OR_UNSUPPORTED.

## C1 execution discipline

C1 must follow the I1 order:
`authorized audit -> local safety ceilings -> bounded deterministic calibration -> evidence-backed decisions -> implementation -> build -> checkpoint-filesystem proof -> sanitized profile`.

C1 calibration is non-scientific engineering work. It uses only CEML-CAL-1 public inputs, never the scientific master seed or a scientific start, and remains within the I1 suite maxima and stricter measured local ceilings.

No missing local observation may be replaced by inference, an internet specification, another machine's result or an unmeasured default. A performance record is admissible only with exact correctness agreement and required route activation.

## Independence rule

Other Collatz repositories are not baseline evidence. If a fact from one is useful, locate its primary basis or explicitly cite and assess that repository as an external source. Never import its research state wholesale.

## Non-substitution rule

A local observation is not calibration. Calibration is not V1. V1 is not scientific execution. C1 may use direct reference checks to invalidate a performance candidate, but C1 calibration records cannot satisfy CEML-V1-SUITE-1.

## Gate closure

Each gate closes only when its required repository evidence and status transition appear in the same reviewed history state. C1 must stop after committing its sanitized evidence/build/profile package; V1 requires a separate authorization transition.
