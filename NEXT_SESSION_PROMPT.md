# Next Session Prompt — CEML-R2

Use this prompt to begin the next research session.

---

CEML-R2 — ALGORITHM AND IMPLEMENTATION AUDIT

Repository:

https://github.com/jfairfaxball-348/CEML

Begin by inspecting the current main branch and treat the repository as the sole authoritative state for CEML.

Read, in this order:

1. PROGRAM_STATUS.md
2. START_HERE.md
3. PROJECT_CHARTER.md
4. ROADMAP.md
5. AGENTS.md
6. docs/RESEARCH_PROTOCOL.md
7. docs/LITERATURE_AUDIT.md
8. docs/ALGORITHM_AUDIT.md
9. docs/CLAIM_POLICY.md
10. docs/HARDWARE_AUDIT_SPEC.md
11. NEXT_SESSION_PROMPT.md

CEML-R1 is complete. The current phase is R2 research only.

Do not import architecture, terminology, assumptions, reports, conclusions, or research state from any previous Collatz repository unless a specific fact is independently relevant, independently re-audited, and explicitly cited.

Do not:

- implement the CEML production engine;
- generate the scientific master seed;
- freeze the magnitude ladder;
- run giant Collatz trajectories or any scientific rung;
- launch the local Codex implementation;
- invent or assume local hardware specifications;
- select machine-specific compiler flags, arithmetic backend thresholds, macro/super-block sizes, thread counts, checkpoint cadence, RAM ceilings, storage limits, or similar local engineering parameters;
- treat any public implementation as correct merely because it is published or passes examples;
- treat ANTS review, public source availability, OEIS agreement, or a benchmark as a substitute for source-level correctness analysis;
- conflate standard-map, shortcut-map, and odd-only step counts;
- conflate contiguous Collatz verification with isolated-start extreme-magnitude evaluation;
- advance to R3 unless every R2 exit criterion is genuinely satisfied.

The purpose of this session is CEML-R2 only:

Compare the exact algorithm families and serious public implementations identified by R1, reconstruct their mathematical invariants, source-audit the strongest candidates, and document a defensible shortlist of architecture families for later validation and machine-local benchmarking.

R1 evidence that must be treated with its recorded caveats includes:

- Andreas-Stephan Elsenhans, ANTS XVII 2026, standard-polynomial / affine binary-splitting macro steps;
- the linked Elsenhans code/data archive, which R1 located but did not unpack and audit;
- DRMacIver/collatz-eval, Rust v0.1.0, with Dense/Sparse representations, optional GMP super-batching, optional FLINT routing, oracle scaffolding, and an explicit warning that human auditing is limited;
- Boutoukoat/Collatz-steps-on-large-numbers, C++/GMP, with Gerbicz-attributed acceleration and independently matching outputs for some large Mersenne starts, but incomplete benchmark provenance and a primary-method gap;
- Wei Ren's bit/file-backed C implementations as an independent algorithmic lineage and convention cross-check;
- Bařina's contiguous verifier only as a non-equivalent comparator.

Investigate at minimum:

1. Exact semantic normalization

Define, implementation-independently:

- standard map C;
- shortcut map T;
- any odd-only map U considered;
- stopping time versus total stopping time;
- exact conversion of step counts between conventions;
- the exact meaning of “reaches 1” when a macro block could cross the first occurrence of 1;
- the state variables an engine must preserve to make results and checkpoints unambiguous.

Do not freeze R3 scientific protocol fields prematurely, but identify every semantic choice R3 will have to freeze.

2. Elsenhans mathematical audit

Reconstruct the method from the primary paper:

- standard polynomial / affine triple representation;
- dependence on the low k bits;
- exact composition identity;
- direct base-block construction;
- recursive binary splitting;
- coefficient and denominator bounds;
- macro-step selection logic;
- exact step accounting;
- terminal-block boundary;
- conditional complexity theorem and its G_c hypothesis.

For each formula, state the invariant that an implementation must preserve and identify plausible transcription/overflow/order/boundary failures.

3. Elsenhans artifact audit

Attempt to obtain the linked collatz_2026.tar.gz research archive from the author/institutional source.

If accessible:

- record a cryptographic hash of the downloaded archive;
- inventory the files;
- identify Magma and C/GMP implementations;
- record license information if present;
- map source functions to the paper's formulas;
- identify build/compiler/GMP requirements;
- inspect tests and assertions;
- determine whether exact 10-billion- or 20-billion-digit inputs/results/digests are preserved;
- record any discrepancies with the paper.

If the archive cannot be obtained or inspected, preserve that as an explicit unresolved evidence gap rather than substituting a mirror silently.

4. DRMacIver/collatz-eval audit

Inspect the current pinned revision rather than only the README.

Audit:

- Dense and Sparse state representations;
- BlockTable/fused-step logic;
- super-batch affine representation and recursion;
- GMP/rug interface;
- optional FLINT multiplication path;
- low-limb/shift/carry handling;
- terminal behavior;
- step-count API;
- debug/audit overflow checks;
- property-based tests and oracle independence;
- feature-specific tests;
- any issue/PR history relevant to correctness;
- license and dependency implications.

Determine what is mathematically independent versus derived from Elsenhans. Do not call its oracle independent if it merely reuses the same recurrence and bug surface.

5. Boutoukoat / Gerbicz lineage audit

Inspect the current pinned Boutoukoat source.

Determine:

- exact recurrence or decomposition used;
- how it differs from Elsenhans;
- the role of GMP internals and mpz_mullo;
- standard-map step preservation;
- tail handling;
- architecture-specific assumptions;
- known size/GMP limits;
- build portability constraints;
- whether the Mersenne outputs can be reproduced by a genuinely independent reference implementation on bounded/appropriate test sizes.

Trace the cited R. Gerbicz primary source if possible. If the source remains inaccessible or informal, reconstruct the algorithm from code and label the provenance honestly. Do not promote the repository's approximate complexity statement into a theorem without evidence.

6. Other exact families

Compare at least:

- direct arbitrary-precision stepping;
- odd-only valuation stepping;
- table-driven affine/composite-polynomial batching;
- on-demand binary-split affine batching;
- hierarchical/super-batching;
- Ren-style bit/file representation;
- any additional exact macro-transform family found during R2.

For each record:

- mathematical state;
- exact transform;
- step accounting;
- correctness argument;
- asymptotic claim and assumptions;
- allocation/copy pressure;
- multiplication requirements;
- memory behavior;
- checkpoint boundary options;
- implementation complexity;
- independent-test strategy;
- maturity.

7. Arithmetic/backend audit

Compare, without selecting machine-specific thresholds:

- GMP;
- GMP plus FLINT;
- Rust wrappers/FFI options;
- direct C;
- C++;
- Rust;
- Python only as orchestration/reference where appropriate.

Record:

- exactness guarantees;
- ABI/dependency/license issues;
- serialization portability;
- low-level APIs relied upon;
- risk from undocumented/internal library functions;
- what later C1 benchmarks must measure.

Do not select a winner based on reputation or another machine's benchmark.

8. Correctness threat model

Build an explicit failure-mode matrix covering at least:

- fixed-width overflow;
- big-integer allocation failure handling;
- carry/borrow errors;
- low-bit extraction errors;
- parity/valuation errors;
- affine composition order;
- denominator/shift errors;
- base-table errors;
- odd block-length split errors;
- final-block overshoot of 1;
- step-count convention mismatch;
- state/result serialization mismatch;
- checkpoint restart drift;
- backend/FFI aliasing or lifetime errors;
- architecture-specific undefined behavior;
- compiler-optimization-sensitive undefined behavior.

For each failure mode identify detection/validation methods appropriate to R3/V1.

9. Validation architecture inputs for R3

R2 should not freeze the R3 protocol, but must identify what an independent oracle needs to be genuinely diverse.

Specify candidate cross-checks such as:

- direct Python or GMP stepping on bounded fixtures;
- standard versus shortcut count conversion;
- randomly generated small/medium differential cases;
- adversarial low-bit patterns;
- known exact large formula-defined starts such as selected Mersenne values;
- comparing affine block application with k direct T steps;
- comparing two implementation lineages that do not share the same batching code.

10. Benchmark plan inputs for C1

Identify what later local benchmarking must compare, without choosing values now:

- direct versus affine/super-batch;
- GMP versus GMP+FLINT where available;
- block/macro-size families;
- allocation/copy strategies;
- single-thread core trajectory versus auxiliary parallel work;
- memory scaling;
- checkpoint serialization cost.

Preserve the rule that R2 produces hypotheses and benchmark requirements, not local tuning decisions.

Repository deliverable:

Substantially complete docs/ALGORITHM_AUDIT.md.

It must include:

- research questions and methodology;
- normalized Collatz semantics relevant to implementations;
- algorithm-family comparison matrix;
- Elsenhans mathematical and artifact audit;
- source-level audits of serious public implementations;
- arithmetic/backend comparison;
- correctness/failure-mode matrix;
- independent-validation implications;
- checkpoint/restart implications;
- performance claims classified as theoretical, author-reported, independently reproduced, or CEML inference;
- viable architecture shortlist, if justified;
- rejected/deferred families with reasons;
- exact local benchmarks C1 will later need;
- unresolved questions;
- explicit R2 exit checklist and decision.

Update other repository files only where justified.

In particular, update PROGRAM_STATUS.md only if every R2 exit criterion has actually been satisfied.

Do not write production code.

Do not authorize scientific execution.

Do not generate a scientific seed.

Do not freeze the magnitude ladder.

Do not select machine-specific engineering parameters.

End-of-session requirements:

1. commit all R2 repository updates;
2. report the new authoritative commit SHA;
3. summarize the strongest algorithm/correctness conclusions;
4. summarize important unresolved risks and implementation disagreements;
5. state explicitly either:
   - “CEML-R2 PASS”, or
   - “CEML-R2 REMAINS OPEN”;
6. if R2 passes, provide a self-contained prompt for CEML-R3 — reproducibility and validation audit;
7. if R2 remains open, provide the exact continuation task required to finish R2.

The standard is source-level correctness, explicit invariants, and auditability. Performance is secondary and must never substitute for correctness.
