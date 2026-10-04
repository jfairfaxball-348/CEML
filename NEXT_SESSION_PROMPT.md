# Next Session Prompt — CEML-C1

CEML-C1 — LOCAL HARDWARE AUDIT, BOUNDED CALIBRATION AND IMPLEMENTATION

Repository:

https://github.com/jfairfaxball-348/CEML

Authoritative I1-PASS baseline:

Use the current `main` commit containing this prompt. Before changing files, resolve and report its exact commit SHA and verify that `PROGRAM_STATUS.md` says I1 PASS / C1 CURRENT.

Treat this repository as the sole authoritative state for CEML.

Read, in this order:

1. PROGRAM_STATUS.md
2. START_HERE.md
3. PROJECT_CHARTER.md
4. ROADMAP.md
5. AGENTS.md
6. docs/RESEARCH_PROTOCOL.md
7. docs/LITERATURE_AUDIT.md
8. docs/ALGORITHM_AUDIT.md
9. docs/REPRODUCIBILITY_VALIDATION_AUDIT.md
10. docs/RANDOMNESS_AND_REPRODUCIBILITY.md
11. docs/EXPERIMENT_PROTOCOL.md
12. docs/CHECKPOINT_SPEC.md
13. docs/RESULT_SCHEMA.md
14. docs/VALIDATION_PLAN.md
15. docs/SECURITY_AND_INTEGRITY.md
16. docs/CLAIM_POLICY.md
17. docs/HARDWARE_AUDIT_SPEC.md
18. docs/CODEX_HANDOFF.md
19. config/calibration_suite_v1.json
20. schemas/c1_evidence.schema.json
21. schemas/hardware_profile.schema.json
22. schemas/run_manifest.schema.json
23. schemas/checkpoint_metadata.schema.json
24. schemas/result.schema.json
25. schemas/validation_evidence.schema.json
26. NEXT_SESSION_PROMPT.md

CEML-R1, R2, R3, R4 and I1 have passed. CEML-SCI-1, CEML-CKPT-1, the R4 hardware-audit contract and the I1 implementation/calibration specification are frozen.

The current phase is CEML-C1 only.

## Hard boundaries

Do not generate, request, disclose or use the scientific master seed.

Do not derive, inspect or evaluate a scientific start.

Do not freeze the final executable ladder.

Do not run a giant/scientific trajectory.

Do not enter or claim CEML-V1, and do not enter E1 automatically.

Do not alter a frozen CEML-SCI-1/CEML-CKPT-1 rule.

Do not weaken R4 privacy/evidence/refusal rules or I1 calibration/activation/decision rules.

Do not silently install, upgrade, fetch, replace or enable a dependency/toolchain/backend. Missing components remain missing until an explicit authorized operator action.

Do not guess unavailable hardware facts, substitute internet specifications, reuse another machine's benchmark or choose unmeasured tuning.

Do not use private/internal GMP/FLINT interfaces rejected by I1.

Do not exceed CEML-CAL-1 or stricter measured local safety ceilings.

## Required order

Execute exactly this sequence:

1. authorization/baseline verification;
2. privacy-minimized hardware/environment audit;
3. local resource-safety ceilings;
4. candidate tool/dependency availability;
5. bounded CEML-CAL-1 reference/calibration harnesses only;
6. deterministic calibration and route-activation evidence;
7. CEML-CKPT-1 target-filesystem durability/interruption tests;
8. evidence-backed engineering decisions/refusals;
9. production implementation using only selected eligible choices;
10. offline-capable pinned build and provenance capture;
11. rerun any calibration invalidated by the final implementation/build;
12. freeze sanitized BUILD_MANIFEST and local machine profile;
13. run deterministic sensitive-data scan and review staged C1 artifacts;
14. commit C1 evidence/implementation/profile;
15. stop before V1.

Do not reverse the order by implementing a presumed production architecture before the measurements needed to select it.

## Phase 1 — baseline and audit

Verify the I1-PASS main commit and all frozen protocol identifiers.

Collect only the authorized R4/I1 observation categories using narrow platform adapters. Emit OBSERVED_FACT and UNAVAILABLE_OR_UNSUPPORTED records rather than broad raw inventories. Filter prohibited identifiers before persistence wherever practical.

Before non-trivial calibration, establish conservative local ceilings for memory headroom, storage headroom, swap/pagefile pressure, process/thread count, thermal/throttling stop conditions where observable, per-case work/time and power/sleep preconditions. Do not silently change global machine policy.

Record availability and exact versions/configuration only for tools/dependencies actually eligible under I1. An absent GMP/FLINT/compiler/runtime remains unavailable; do not install it silently.

## Phase 2 — bounded deterministic CEML-CAL-1

Use `config/calibration_suite_v1.json` and the exact generator/framing/digest rules in `docs/CODEX_HANDOFF.md`.

The public calibration seed and `CEML-CALIBRATION-RANDOM-V1\0` domain are engineering-only. Never touch `ceml-start-v1` or the scientific seed.

Respect both I1 hard maxima and stricter local limits.

For every decision-relevant applicable comparison, record exact correctness/reference state digests, timing methodology, repeats/variability, peak memory/resource observations and route activation. A requested optimized route must have positive activation and zero silent fallback. Incorrect output or failed activation invalidates the performance datum.

Run the applicable matrix for:

- direct vs small affine vs hierarchical crossover;
- small-block widths;
- hierarchical divisor/k-cap candidates;
- public GMP vs supported public FLINT and multiplication shapes;
- dense/sparse or analogous representations;
- copy vs safe reuse/in-place allocation;
- checked/portable-release/native-release build modes where supported;
- single-thread vs permitted auxiliary parallelism;
- checkpoint serialization/write/flush/promotion;
- terminal handoff;
- audit/canary modes;
- memory/simultaneous-buffer scaling.

Use the I1 decision thresholds and tie-break order exactly. If evidence is insufficient/noisy/unsupported, record refusal or no justified winner rather than inventing one.

## Phase 3 — checkpoint filesystem

On the same filesystem/mount class intended for later scientific checkpoints, execute the bounded synthetic CEML-CKPT-1 durability contract:

- complete write and durable flush;
- close/reopen and exact digest verification;
- atomic A/B or equivalent promotion;
- required directory/pointer durability operation;
- previous-valid-slot retention;
- recovery without trusting a latest pointer;
- forced process interruption before/after each materially distinct write/flush/promotion/cleanup phase;
- fresh-process recovery.

Do not perform destructive power-cut testing unless a later explicit authorization exists. If documented semantics plus safe interruption tests cannot justify CKPT-1, mark the storage target unsupported.

## Phase 4 — engineering decisions and implementation

Create ENGINEERING_DECISION records for every hardware-dependent choice/refusal. Each selected choice must trace to valid observations/calibration and satisfy the I1 correctness/support/activation/resource/provenance rules.

Only after those decisions may you implement the production engine.

Preserve all I1 interfaces and invariants, including:

- separate direct C/T definition oracle;
- exact T-boundary canonical state;
- centralized unbounded counter accounting;
- affine invariant `2^k T^k(n)=3^i n+B`;
- P2-after-P1 composition;
- odd split support;
- divisibility canaries as checks, not proofs;
- first-1 macro safety `k <= bit_length(n)-1` or exact terminal handoff;
- public documented arbitrary-precision APIs;
- fail-closed route activation instrumentation;
- canonical JCS/UENC/SHA3/SHAKE handling;
- exact CEML-CKPT-1 checkpoint codec/store;
- all twelve V1 hooks, without running/claiming V1.

## Phase 5 — build/profile freeze

Build using the I1 two-layer offline strategy:

- ecosystem-native exact lock/pin;
- committed CEML dependency/source digest manifest;
- vendored or approved content-addressed local cache for required build inputs;
- no mutable network content;
- offline rebuild recipe that fails if network fetch would be required.

Capture source commit, exact compiler/linker/toolchain versions, target triple/ABI, complete relevant flags, native-target request/features, dependency versions/digests/options/linkage, enabled routes/features, lock identities and executable/library byte digests.

Native tuning, if selected from evidence, must set non-portable=true. A different machine/build is a new profile event and does not inherit V1 evidence.

Generate:

- local_reports/HARDWARE_REPORT.json
- local_reports/HARDWARE_REPORT.md
- local_reports/BENCHMARK_SUMMARY.json
- local_reports/ENGINEERING_DECISIONS.json
- local_reports/BENCHMARK_BUNDLES.json
- local_reports/BUILD_MANIFEST.json
- config/local_machine_profile.json
- exact lock/pin/dependency provenance files required by the selected stack.

Raw large records remain under ignored `local/c1/` paths by default and are bound by the committed bundle index/digests.

Run the deterministic I1 sensitive-data scan on the staged committed C1 artifacts. Any prohibited identifier blocks commit; hashing it is not sanitization.

## C1 completion standard

CEML-C1 passes only if:

- every local machine fact used by a decision is directly observed and sanitized;
- every unavailable fact is recorded as unavailable rather than guessed;
- local resource ceilings exist before non-trivial calibration;
- every selected optimized route has correctness agreement and activation proof;
- every hardware-dependent selected choice is evidence-backed under the I1 decision rules;
- the intended checkpoint filesystem has the required CKPT-1 durability/recovery evidence;
- the production engine was implemented only after its prerequisite engineering decisions;
- the final selected build is pinned, offline-capable and fully provenance-bound;
- any final-build change that invalidated calibration caused the affected evidence to be rerun;
- all required sanitized reports/build/profile artifacts are schema-valid;
- build_digest and machine_profile_digest reproduce exactly from the committed sanitized artifacts;
- the sensitive-data scan passes;
- no scientific seed/start/rung was used;
- V1 and E1 remain unentered.

At the end:

1. commit all C1 repository updates;
2. report the authoritative commit SHA;
3. summarize observed local capabilities without prohibited identifiers;
4. summarize measured engineering choices and evidence;
5. summarize unavailable/unsupported items and refusals;
6. summarize the implemented architecture/build/profile;
7. summarize checkpoint-filesystem evidence and remaining risks;
8. state explicitly either **“CEML-C1 PASS”** or **“CEML-C1 REMAINS OPEN”**;
9. if C1 passes, provide a self-contained CEML-V1 prompt that executes only the frozen validation suite and does not enter E1;
10. if C1 remains open, provide the exact continuation task required to finish C1.

The C1 standard is local evidence before implementation, exactness before speed, privacy before persistence, and a hard stop before validation/science.
