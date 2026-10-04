# CEML Programme Status

**Authoritative current phase:** R2 — ALGORITHM / IMPLEMENTATION AUDIT  
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
| R1 | **PASS — 2026-10-04** | docs/LITERATURE_AUDIT.md records the source-level state-of-the-art audit, evidence confidence, implementation landscape, performance conditions, caveats and unresolved R2 questions. |
| R2 | **OPEN — CURRENT GATE** | Algorithm and implementation audit may proceed. No production implementation is authorized. |
| R3 | NOT ENTERED | Reproducibility/validation semantics remain unfrozen. |
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
- public current implementations suitable for R2 source audit, including DRMacIver/collatz-eval and Boutoukoat/Collatz-steps-on-large-numbers;
- independent public output agreement for selected large exact Mersenne starts;
- explicit separation of standard, shortcut and odd-only step conventions;
- separation of isolated-start computation from contiguous verification;
- performance evidence with missing conditions preserved as missing;
- correctness, portability, checkpoint/restart and provenance gaps to be resolved in later gates.

R1 did **not** choose a CEML production architecture or backend.

## Current R2 boundary

R2 is research and source/algorithm audit only. It may inspect mathematics, public source code, licenses, tests, interfaces and bounded deterministic examples needed to understand correctness.

R2 may not:

- implement the CEML production engine;
- generate the scientific master seed;
- freeze the magnitude ladder;
- run a giant or scientific trajectory;
- launch the local Codex implementation;
- infer or record unmeasured local hardware;
- select machine-specific compiler flags, backend thresholds, macro/super-block sizes, thread counts, RAM ceilings or checkpoint cadence;
- convert an author benchmark into a local performance prediction;
- call an implementation audited without documenting the audit scope.

## Non-substitution rule

Passing a later-looking activity does not waive an earlier gate. A benchmark is not validation. Validation is not a scientific run. A scientific anomaly is not divergence. A long runtime is not a counterexample.

## Change-control rule

A material change after scientific execution begins requires a new protocol/build/profile version as applicable. There is no silent recalibration, backend swap, compiler-flag change, macro-block change, map change, checkpoint semantic change, seed rule change, or rung substitution.

## State transitions

A future session that believes a gate is complete must update this file in the same reviewed repository snapshot that records the evidence and acceptance decision. Until that happens, the prior authorization state remains controlling.
