# CEML Programme Status

**Authoritative current phase:** BOOTSTRAP  
**Scientific execution authorization:** DENIED  
**Production implementation authorization:** DENIED  
**Scientific master-seed generation:** DENIED  
**Magnitude ladder:** PROVISIONAL / NOT FROZEN  
**Local machine profile:** NOT MEASURED  
**Protocol version:** BOOTSTRAP-DRAFT  
**Last status update:** 2026-10-04

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

## Non-substitution rule

Passing a later-looking activity does not waive an earlier gate. A benchmark is not validation. Validation is not a scientific run. A scientific anomaly is not divergence. A long runtime is not a counterexample.

## Change-control rule

A material change after scientific execution begins requires a new protocol/build/profile version as applicable. There is no silent recalibration, backend swap, compiler-flag change, macro-block change, map change, checkpoint semantic change, seed rule change, or rung substitution.

## State transitions

A future session that believes a gate is complete must update this file in the same reviewed commit that records the evidence and acceptance decision. Until that happens, the prior authorization state remains controlling.
