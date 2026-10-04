# Next Session Prompt — CEML-R1

Use this prompt to begin the next research session.

---

CEML-R1 — STATE-OF-THE-ART AND LITERATURE AUDIT

Repository:
https://github.com/jfairfaxball-348/CEML

Authoritative bootstrap baseline:
78c6facbb9bd3110105006ed825a9909aa558f2f

Begin by reading, in this order:

1. PROGRAM_STATUS.md
2. START_HERE.md
3. PROJECT_CHARTER.md
4. ROADMAP.md
5. AGENTS.md
6. docs/RESEARCH_PROTOCOL.md
7. docs/LITERATURE_AUDIT.md
8. docs/CLAIM_POLICY.md
9. docs/HARDWARE_AUDIT_SPEC.md

This repository is the sole authoritative state for CEML.

Do not import architecture, terminology, assumptions, reports, conclusions, or research state from any previous Collatz repository unless a specific fact is independently relevant, re-audited, and explicitly cited.

The current phase is research only.

Do not:
- implement the production engine;
- generate the scientific master seed;
- freeze the magnitude ladder;
- run giant Collatz trajectories;
- launch the local Codex implementation;
- invent or assume local hardware specifications;
- select machine-specific compiler flags, macro-block sizes, arithmetic backends, thread counts, checkpoint cadence, or RAM ceilings;
- treat another implementation as correct merely because it is published or public;
- conflate contiguous verification with isolated-start extreme-magnitude computation;
- make performance claims without the relevant hardware/software conditions;
- advance to R2 unless the R1 exit criteria are genuinely satisfied.

The purpose of this session is CEML-R1 only: establish the state of the art for extreme-size isolated-start Collatz trajectory evaluation.

Research with current primary sources wherever possible and update the repository as the authoritative output of the session.

Investigate at minimum:

1. The largest credible isolated-start Collatz computations you can identify.
   - Distinguish starting magnitude, peak magnitude, stopping time, total stopping time, and contiguous verification bounds.
   - Determine exactly what was computed and what was only claimed.
   - Record whether results are reproducible from public information.

2. Elsenhans-style methods.
   - Locate the primary source(s).
   - Explain the mathematical method accurately.
   - Determine publication/peer-review status.
   - Identify exact batching / Collatz-polynomial / affine ideas used.
   - Determine what performance claims were made and under what conditions.
   - Identify any public code, archived code, forks, reproductions, critiques, or correctness discussions.

3. Other credible extreme-size isolated-start algorithms.
   - Exact macro-step methods.
   - Odd-only transformations.
   - Affine batching.
   - Binary splitting.
   - Super-batching or hierarchical composition.
   - Any relevant large-integer techniques specific to Collatz evaluation.

4. Existing implementations.
   For each serious implementation found, record:
   - language;
   - arithmetic library/backend;
   - algorithmic method;
   - source availability;
   - license if relevant;
   - last meaningful maintenance/version;
   - test strategy if visible;
   - audit/review status;
   - known limitations;
   - whether anyone independently reproduced its output or performance.

5. Performance evidence.
   - Separate author-reported benchmarks from independently reproduced measurements.
   - Preserve CPU/model, memory, compiler, library versions, input size, and other conditions when available.
   - Do not extrapolate generic benchmark numbers to the eventual CEML local machine.

6. Correctness caveats.
   Search specifically for:
   - overflow issues;
   - incorrect step-count conventions;
   - bugs in batching formulas;
   - boundary/valuation errors;
   - serialization/checkpoint hazards;
   - discrepancies between implementations;
   - unverifiable claims;
   - code that is fast but insufficiently validated.

7. Known huge-start computations.
   Build a clearly sourced table of credible examples, but do not turn it into a ranking contest. The purpose is to understand demonstrated scale, methods, reproducibility, and evidence quality.

Evidence discipline:

For every material claim, record:
- source;
- author/publisher;
- date/version;
- source type;
- whether primary/secondary;
- exact proposition supported;
- experimental conditions;
- whether independently reproduced;
- caveats/conflicts;
- CEML confidence assessment.

Prefer original papers, authors' technical pages, source repositories, published code, issue trackers, archived technical material, and independent reproductions over unsourced summaries.

When sources disagree, preserve the disagreement instead of forcing consensus.

Repository deliverables for this session:

- substantially complete docs/LITERATURE_AUDIT.md;
- source/evidence table with citations;
- a section on Elsenhans-style methods;
- a section on credible existing implementations;
- a section on known extreme isolated-start computations;
- a section on correctness/audit caveats;
- a section on what is known versus merely claimed;
- explicit unresolved questions for R2;
- any justified improvements to docs/RESEARCH_PROTOCOL.md or ROADMAP.md;
- update PROGRAM_STATUS.md only if every R1 exit condition is genuinely satisfied.

Do not write production code.

Do not authorize scientific execution.

Do not freeze machine-specific engineering decisions.

At the end:

1. commit all R1 repository updates;
2. report the authoritative commit SHA;
3. summarize the strongest evidence found;
4. summarize important uncertainty or conflicting evidence;
5. state explicitly whether R1 passes or remains open;
6. if R1 passes, provide a self-contained prompt for CEML-R2; if it does not pass, provide the exact next R1 continuation task.

The standard is auditability, not speed. A source claim without enough provenance to verify it should remain labeled as such.
