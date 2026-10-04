# CEML Research Protocol

Status: **R1–R4 COMPLETE; CEML-I1 SPECIFICATION SYNTHESIS CURRENT**

## Purpose

Repository-driven research and specification work must make scientific and engineering decisions auditable before implementation. A session is not complete when an answer is written in chat; it is complete when evidence, reasoning, open questions and any approved decision are committed here.

## Required sequence

- **R1:** state-of-the-art and literature audit — PASS;
- **R2:** algorithm and implementation audit — PASS;
- **R3:** reproducibility and validation audit — PASS;
- **R4:** hardware-audit specification — PASS;
- **I1:** synthesis into a self-contained Codex implementation brief — CURRENT;
- **C1:** local hardware audit, bounded calibration, implementation/build/profile freeze;
- **V1:** frozen validation suite;
- **E1:** scientific ladder.

The sequence is mandatory because later decisions depend on earlier evidence.

## Evidence rules

For every material external claim record:

- source and stable locator;
- author/publisher;
- publication or version date where available;
- date accessed;
- whether the source is primary, peer-reviewed, preprint, code, documentation, benchmark report, or secondary discussion;
- the exact proposition CEML uses it to support;
- relevant experimental conditions;
- known caveats or conflicts;
- whether CEML independently reproduced the claim.

Do not equate a source's availability with correctness. Do not call an implementation audited unless the nature and scope of that audit are documented.

For local hardware work, docs/HARDWARE_AUDIT_SPEC.md additionally controls evidence classes, privacy, measurement, sanitization, route activation, bounded calibration and decision provenance.

## Decision taxonomy

Each conclusion must be marked as one of:

- **OBSERVATION:** evidence collected, no decision;
- **PROVISIONAL:** preferred direction pending a later gate;
- **FROZEN-SCIENTIFIC:** invariant requiring protocol version change to alter;
- **FROZEN-AUDIT:** R4 hardware-audit contract requirement;
- **FROZEN-ENGINEERING:** local build/profile choice requiring build/profile version change to alter;
- **REJECTED:** considered and not selected, with reason;
- **OPEN:** unresolved.

During C1, machine evidence additionally uses the R4 record classes OBSERVED_FACT, CALIBRATION_MEASUREMENT, ENGINEERING_DECISION and UNAVAILABLE_OR_UNSUPPORTED.

## Research/specification deliverable

Each R-session must update its principal document with:

1. research questions;
2. search/source strategy;
3. evidence table where external evidence is used;
4. findings;
5. contradictions/caveats;
6. decisions and their status;
7. unresolved questions;
8. implications for later gates;
9. repository files changed.

I1 must instead produce a complete executable specification in docs/CODEX_HANDOFF.md that is sufficient for C1 without inventing local measurements.

## Independence rule

Other Collatz repositories are not baseline evidence. If a fact from one is useful, locate its primary basis or explicitly cite and assess that repository as an external source. Never import its research state wholesale.

## No-compute boundary before C1

Research and I1 specification sessions may use small deterministic examples needed to understand mathematics or interfaces, but may not perform a scientific rung, generate the scientific seed, inspect the real local machine as a C1 audit, or run an input near the intended extreme scale.

## C1 non-substitution rule

When C1 is authorized, a missing local observation remains missing. Calibration is engineering evidence only. It cannot substitute for V1, and neither calibration nor V1 is scientific execution.
