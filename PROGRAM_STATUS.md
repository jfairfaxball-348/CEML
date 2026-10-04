# CEML Programme Status

**Authoritative current phase:** R3 — REPRODUCIBILITY / VALIDATION AUDIT  
**Scientific execution authorization:** DENIED  
**Production implementation authorization:** DENIED  
**Scientific master-seed generation:** DENIED  
**Magnitude ladder:** PROVISIONAL / NOT FROZEN  
**Local machine profile:** NOT MEASURED  
**Protocol version:** BOOTSTRAP-DRAFT / SCIENTIFIC SEMANTICS NOT YET FROZEN  
**Last status update:** 2026-10-04

## Gate decisions

| Gate | Status | Evidence / consequence |
|---|---|---|
| BOOTSTRAP | COMPLETE | Governance and scaffold committed before R1. |
| R1 | **PASS — 2026-10-04** | docs/LITERATURE_AUDIT.md records the state-of-the-art evidence base, source confidence, caveats and implementation landscape. |
| R2 | **PASS — 2026-10-04** | docs/ALGORITHM_AUDIT.md reconstructs exact affine invariants, audits the strongest source lineages, records failure modes, validation implications, checkpoint implications, a viable machine-neutral shortlist and C1 benchmark questions. |
| R3 | **OPEN — CURRENT GATE** | Reproducibility, scientific semantics, manifests, checkpoint/restart semantics and validation acceptance criteria may now be researched and frozen. |
| R4 | NOT ENTERED | Local hardware-audit specification not frozen. |
| I1 | NOT ENTERED | Codex implementation brief not approved. |
| C1 | NOT ENTERED | Local audit/build not authorized. |
| V1 | NOT ENTERED | Production validation not authorized. |
| E1 | NOT ENTERED | Scientific ladder execution not authorized. |

## Gate chain

| Gate | Purpose | Entry condition | Exit condition | Scientific rung allowed? |
|---|---|---|---|---|
| BOOTSTRAP | Governance/scaffold | Empty/new repository | Bootstrap documents committed | No |
| R1 | State of art/literature | Bootstrap complete | Literature evidence and caveats reviewed | No |
| R2 | Algorithm/implementation audit | R1 complete | Viable architecture families documented | No |
| R3 | Reproducibility/validation | R2 complete | Randomness, manifests, validation, hashes, checkpoints frozen scientifically | No |
| R4 | Hardware-audit specification | R3 complete | Local audit/benchmark permissions and criteria frozen | No |
| I1 | Codex implementation brief | R4 complete | Self-contained handoff approved | No |
| C1 | Local audit + calibrated implementation | I1 complete | Sanitized hardware report, bounded benchmarks, built system, frozen local profile | No |
| V1 | Offline validation | C1 complete | All required validation gates pass | No |
| E1 | First scientific ladder | V1 complete and ladder/seed protocol frozen | Execute one precommitted start per rung | Yes |

## R1 acceptance summary

R1 established, without importing authority from another Collatz repository:

- a primary current high-magnitude method: Elsenhans's exact standard-polynomial / affine binary-splitting approach;
- an author-reported 20-billion-decimal-digit computation, explicitly not treated as independently reproduced;
- public current implementations suitable for source audit;
- independent public output agreement for selected large exact Mersenne starts;
- explicit separation of standard, shortcut and odd-only step conventions;
- separation of isolated-start computation from contiguous verification;
- performance evidence with missing conditions preserved as missing.

R1 did **not** choose a CEML production architecture or backend.

## R2 acceptance summary

R2 established, without writing production code or importing machine-specific tuning:

- normalized standard-map, shortcut-map and odd-only semantics and exact count conversions;
- the affine invariant 2^k T^k(n) = 3^i n + B and its non-commutative composition order;
- why the low k bits determine k exact shortcut steps;
- direct-base and binary-split construction invariants, including odd split lengths;
- the first-occurrence-of-1 macro-block hazard and the requirement for terminal-safe scheduling or exact decomposition;
- the scope and hypotheses of Elsenhans's conditional complexity theorem;
- a source-level audit of DRMacIver/collatz-eval at 0f5ad6da40171cdcd68ce167776a0644ceb942dc;
- a source-level audit of Boutoukoat/Collatz-steps-on-large-numbers at ec82c0a7e248add8f3f6d16b07cda0aae4e7ebfd, including mpz_mullo history, standard-step preservation and portability risks;
- explicit separation between direct-step oracles and checks that share the affine recurrence;
- a correctness threat model tied to R3/V1 detection methods;
- machine-neutral viable families: direct arbitrary-precision reference/tail stepping, small affine leaves, and on-demand binary-split/hierarchical affine batching;
- optional Dense/Sparse, value-threaded, FLINT and parallel paths left as later benchmark hypotheses;
- canonical checkpoint/restart requirements identified but not yet scientifically frozen;
- exact local benchmark questions for C1 without choosing values.

R2 also preserved two external evidence gaps:

- the institutional Elsenhans collatz_2026.tar.gz archive could not be acquired as inspectable bytes in the R2 environment and therefore was not hashed or source-audited;
- the cited R. Gerbicz primary forum post could not be retrieved directly, so the current Boutoukoat recurrence was audited from source without promoting its approximate complexity description into a theorem.

These gaps do not certify the external artifacts and remain recorded in docs/ALGORITHM_AUDIT.md. They do not block the R2 exit condition, which requires viable architecture families, invariants, correctness risks and benchmark requirements to be documented.

## Current R3 boundary

R3 is research and protocol design only. It may define and freeze the scientific and validation semantics that later implementation must obey.

R3 may research and decide:

- the canonical reported map/count semantics and first-1 definition;
- deterministic start-generation and scientific master-seed protocol without generating the actual scientific master seed;
- what magnitude-ladder properties must be frozen later, without executing a rung;
- canonical integer, result, manifest and checkpoint encodings;
- hash/digest requirements and domain separation;
- build/run/provenance manifest requirements;
- checkpoint crash consistency and restart equivalence rules;
- independent oracle diversity requirements;
- bounded fixture suites, adversarial tests, differential tests and fault-injection expectations;
- acceptance criteria for V1;
- anomaly handling and evidence-preservation triggers.

R3 may not:

- implement the CEML production engine;
- generate the scientific master seed;
- freeze or execute the scientific magnitude ladder unless the roadmap explicitly assigns that freeze to R3 and the required protocol evidence is complete;
- run a giant or scientific trajectory;
- launch the local Codex implementation;
- infer or record unmeasured local hardware;
- select machine-specific compiler flags, backend thresholds, macro/super-block sizes, thread counts, RAM ceilings, storage ceilings or checkpoint cadence;
- convert an author benchmark into a local performance prediction;
- call an implementation validated before V1 actually passes.

## Non-substitution rule

Passing a later-looking activity does not waive an earlier gate. A benchmark is not validation. Validation is not a scientific run. A scientific anomaly is not divergence. A long runtime is not a counterexample.

## Change-control rule

A material change after scientific execution begins requires a new protocol/build/profile version as applicable. There is no silent recalibration, backend swap, compiler-flag change, macro-block change, map change, checkpoint semantic change, seed rule change, or rung substitution.

## State transitions

A future session that believes a gate is complete must update this file in the same reviewed repository snapshot that records the evidence and acceptance decision. Until that happens, the prior authorization state remains controlling.
