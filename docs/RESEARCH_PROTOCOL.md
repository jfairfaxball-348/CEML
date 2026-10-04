# CEML Research Protocol

Status: **Bootstrap framework; research findings not yet populated**

## Purpose

Repository-driven research must make scientific and engineering decisions auditable before implementation. A research session is not complete when an answer is written in chat; it is complete when evidence, reasoning, open questions, and any approved decision are committed here.

## Required session sequence

- **R1:** state-of-the-art and literature audit;
- **R2:** algorithm and implementation audit;
- **R3:** reproducibility and validation audit;
- **R4:** local hardware-audit specification;
- **I1:** synthesis into a self-contained Codex implementation brief.

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

## Decision taxonomy

Each conclusion must be marked as one of:

- **OBSERVATION:** evidence collected, no decision;
- **PROVISIONAL:** preferred direction pending a later gate;
- **FROZEN-SCIENTIFIC:** invariant requiring protocol version change to alter;
- **FROZEN-ENGINEERING:** local build/profile choice requiring build/profile version change to alter;
- **REJECTED:** considered and not selected, with reason;
- **OPEN:** unresolved.

## Research-session deliverable

Each R-session must update its principal document with:

1. research questions;
2. search/source strategy;
3. evidence table;
4. findings;
5. contradictions/caveats;
6. decisions and their status;
7. unresolved questions;
8. implications for later gates;
9. repository files changed.

## Independence rule

Other Collatz repositories are not baseline evidence. If a fact from one is useful, locate its primary basis or explicitly cite and assess that repository as an external source. Never import its research state wholesale.

## No-compute boundary

Research sessions may use small deterministic examples needed to understand mathematics or interfaces, but may not perform a scientific rung, generate the scientific seed, or run an input near the intended extreme scale.
