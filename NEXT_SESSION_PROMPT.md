# Next Session Prompt — CEML-I1

CEML-I1 — HARDWARE-ADAPTIVE IMPLEMENTATION SPECIFICATION

Repository:

https://github.com/jfairfaxball-348/CEML

Authoritative R4-PASS baseline:

Use the current main commit containing this prompt. Before changing files, resolve and report its exact commit SHA and verify that PROGRAM_STATUS.md says R4 PASS / I1 CURRENT.

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
18. schemas/run_manifest.schema.json
19. schemas/checkpoint_metadata.schema.json
20. schemas/result.schema.json
21. schemas/validation_evidence.schema.json
22. docs/CODEX_HANDOFF.md
23. NEXT_SESSION_PROMPT.md

CEML-R1, CEML-R2, CEML-R3 and CEML-R4 have passed. CEML-SCI-1, CEML-CKPT-1 and the R4 hardware-audit contract are frozen. The current phase is CEML-I1 specification synthesis only.

Do not implement the production engine, launch the local Codex/C1 implementation, inspect or infer the user's actual machine as though C1 had started, install or change local dependencies, generate the scientific master seed, freeze the final executable ladder values, execute a giant or scientific trajectory, claim V1 has passed, or choose machine-specific engineering winners.

Do not change any frozen CEML-SCI-1 or CEML-CKPT-1 scientific rule. Do not weaken the R4 audit/privacy/evidence requirements for implementation convenience.

PURPOSE

Complete and approve docs/CODEX_HANDOFF.md as a self-contained implementation specification that a later C1 local automated agent can execute in the required order:

hardware audit -> bounded deterministic calibration -> measured engineering decisions -> implementation -> build -> frozen sanitized local machine/build profile

I1 must define the interfaces, record formats, benchmark protocols, invariants, tests and decision machinery needed by that sequence without performing the sequence itself.

At minimum:

1. Freeze implementation architecture boundaries.

Define a machine-neutral component/interface decomposition for:

- direct elementary C/T definition oracle;
- exact production trajectory engine;
- small affine/table blocks;
- hierarchical/binary-split affine batching;
- optional odd-only/direct terminal path where useful;
- exact counter/state accounting;
- first-1 terminal-safe handoff;
- route-selection instrumentation;
- checkpoint serialization/promotion/recovery;
- canonical JCS/UENC/digest handling;
- manifest/result/validation-evidence handling;
- hardware-audit collection;
- bounded calibration;
- build/profile generation;
- validation runner.

Do not choose machine-specific block sizes, backends, representations, flags or thread counts.

2. Freeze exact mathematical implementation invariants.

Carry forward the R2/R3 rules, including:

- standard C is the mathematical reference;
- exact shortcut T semantics;
- first occurrence of 1 is terminal;
- standard_steps = shortcut_steps + odd_steps;
- odd-only valuation conversion;
- affine invariant 2^k T^k(n) = 3^i n + B;
- low k bits determine k shortcut parities;
- composition order is non-commutative and must be P2 after P1;
- odd split lengths are supported;
- affine divisibility canaries are checks, not proofs;
- macro blocks may not hide first 1;
- exact arbitrary-precision arithmetic is required.

Express these as code-level preconditions/postconditions/assertions and test obligations.

3. Freeze supported candidate families without selecting the local winner.

I1 must define how C1 can measure and select among, where supported:

- direct stepping;
- small affine/table blocks;
- hierarchical/binary-split batching;
- viable Dense/Sparse or analogous state representations;
- supported GMP route;
- optional supported FLINT route;
- value-threaded versus explicit-coefficient forms if retained;
- allocation reuse/in-place versus copying;
- compiler/optimization modes;
- single-thread versus permitted auxiliary parallelism;
- checkpoint buffering/write strategies;
- terminal handoff options;
- audit/canary modes.

A candidate that I1 rejects for correctness, unsupported/private API, maintainability, licensing/provenance or reproducibility reasons must be explicitly marked rejected so C1 does not benchmark it.

4. Freeze the local hardware-audit interface.

Translate docs/HARDWARE_AUDIT_SPEC.md into exact C1-facing interfaces and record structures for:

- OBSERVED_FACT;
- CALIBRATION_MEASUREMENT;
- ENGINEERING_DECISION;
- UNAVAILABLE_OR_UNSUPPORTED.

Define platform adapters/queries for the authorized observation categories, but do not run them in I1.

Define sanitization/minimization behavior so prohibited identifiers are filtered before persistence where practical.

Define a deterministic sensitive-data scan that must pass before any C1 report/profile commit.

5. Freeze machine-readable C1 artifact formats.

Define concrete versioned schemas/formats and paths for at least:

- local_reports/HARDWARE_REPORT.json;
- local_reports/HARDWARE_REPORT.md generation/reconciliation;
- sanitized raw bounded benchmark records;
- benchmark summary;
- engineering decision log;
- config/local_machine_profile.toml or equivalent;
- retained local-only benchmark bundle digest/index.

Specify required/optional fields, versioning, canonicalization/digest rules where artifacts are bound by digest, and cross-references among evidence records.

Do not fabricate any machine values.

6. Freeze deterministic bounded calibration generation.

Define a calibration-suite version and deterministic input generator using the already reserved CEML-CALIBRATION-RANDOM-V1 domain.

Specify:

- public non-secret calibration seed(s) or formula-defined inputs;
- unambiguous byte framing;
- input/case identifiers;
- exact input digest procedure;
- deterministic case ordering;
- size classes;
- suite-level maximum work bounds that remain far below scientific scale;
- warm-up rules;
- repeated-run rules;
- variability summary;
- correctness reference/checksum/state digest;
- abort/invalid-run semantics.

Never use the scientific master seed and never derive/evaluate a scientific start.

7. Freeze benchmark case matrix and decision rules.

For each hardware-dependent question required by R4, define the bounded case matrix C1 must run where applicable:

- direct versus small block versus hierarchical batching crossover;
- block/macro-size sweep;
- GMP versus supported optional FLINT;
- multiplication/backend crossover;
- Dense/Sparse or analogous representations;
- allocation reuse/in-place versus copying;
- permitted compiler modes;
- single-thread versus auxiliary parallelism;
- checkpoint serialization/write/flush/promotion;
- terminal handoff;
- audit/canary costs;
- memory scaling/simultaneous buffers.

Define when evidence is sufficient to choose a winner, when a tie-break toward simpler/portable/lower-risk code is permitted, and when C1 must refuse to decide.

Do not encode a machine-specific winner in I1.

8. Freeze route-activation instrumentation.

Every optimized route must expose a deterministic bounded way to prove it actually executed.

Define:

- route IDs;
- force/request mechanism;
- route counters/traces/assertions or equivalent evidence;
- fallback detection;
- benchmark evidence field linking activation proof;
- V1 feature-route coverage hooks.

A route that silently falls back is not benchmark evidence for the requested route.

9. Freeze compiler/build provenance.

Define exact provenance capture for:

- compiler/linker/toolchain versions;
- target triple/ABI;
- relevant flags;
- native tuning such as -march=native or equivalents;
- dependency versions and build configuration;
- GMP/FLINT/wrapper linkage;
- enabled features;
- build digest;
- source/engine commit.

Define how native-tuned builds are marked non-portable and why a build/profile/V1 record from one machine cannot be silently transferred to another.

Do not select flags in I1.

10. Freeze offline-capable dependency strategy.

Choose and specify an offline-capable reproducibly pinned build strategy consistent with docs/SECURITY_AND_INTEGRITY.md.

Define:

- lock/pin files;
- dependency/source artifact digest expectations;
- vendoring or approved local-cache behavior;
- network prohibition for scientific execution;
- build/rebuild commands at a specification level;
- dependency-change invalidation rules.

Do not fetch/install dependencies on the user's machine during I1.

11. Freeze checkpoint implementation mapping.

Map CEML-CKPT-1 into implementation interfaces without changing its semantics.

Define:

- canonical state.bin encoder/decoder;
- metadata generation/validation;
- A/B or equivalent slot abstraction;
- write/flush/re-read/verify/promotion sequence;
- platform filesystem adapter contract;
- directory metadata durability adapter;
- recovery selection/refusal;
- previous-valid-slot retention;
- interruption/fault injection hooks;
- fresh-process restart path;
- serialization memory accounting.

C1 must later test the actual target filesystem; I1 must not assume it is durable.

12. Freeze resource-safety machinery.

Define how C1 supplies measured local ceilings for:

- memory headroom;
- storage headroom;
- swap pressure;
- process/thread limits;
- thermal/throttling stops;
- maximum calibration work/time;
- sleep/power considerations.

Define preflight checks, mid-case abort checks and cleanup behavior.

I1 must not invent actual local ceiling values.

13. Freeze command/subcommand semantic surface.

Specify the later implementation's required operational capabilities, such as semantic equivalents of:

- hardware-report;
- calibrate;
- build/profile;
- self-test;
- validate;
- prepare scientific manifest/start verification;
- run;
- status;
- checkpoint/resume;
- verify result/artifacts.

Exact CLI spelling may be chosen in I1, but the separation of responsibilities and authorization checks must be explicit.

Scientific run/prepare commands must refuse before E1/V1 prerequisites exist.

14. Freeze error/status mapping.

Define implementation-level errors and how they map to the already frozen scientific statuses where a scientific run is authorized later.

Calibration/audit failures must remain engineering events and must not emit scientific result statuses as though a rung had been attempted.

Preserve resource_stop, validation_failure, integrity_failure, reproducibility_failure, provenance_failure, unexpected_termination and frozen_anomaly semantics exactly.

15. Freeze validation implementation hooks.

Map every CEML-V1-SUITE-1 class to concrete implementation/test hooks:

- elementary identities;
- exhaustive small residues;
- deterministic randomized differential;
- adversarial patterns;
- odd split lengths;
- terminal/overshoot;
- serialization/digest round trips;
- checkpoint/restart equivalence;
- fault injection;
- feature-route activation;
- formula-defined fixtures;
- checked/sanitized builds.

Direct elementary stepping remains the definition-level independence anchor.

Do not run or claim V1 in I1.

16. Freeze profile and build digest procedure.

Define deterministic serialization/digest rules for the local machine/build profile and build artifact identity needed by the R3 schemas.

The procedure must:

- avoid prohibited stable personal/machine identifiers;
- bind all engineering choices that affect executable behavior;
- distinguish source identity, build identity and machine profile identity;
- be independently reproducible from the sanitized committed artifacts;
- version the profile format;
- avoid changing any already frozen CEML-SCI-1 digest rule or domain label unless an explicit protocol-version review says otherwise.

If an additional engineering-only digest domain is needed, define it as an I1 engineering artifact rule without silently modifying scientific start/checkpoint/result digest semantics.

17. Freeze C1 authorization/refusal rules.

The eventual local agent must refuse to:

- guess missing machine facts;
- silently install/upgrade dependencies;
- enable unsupported/private backend routes;
- select unmeasured tuning;
- accept a route without activation proof;
- use a checkpoint filesystem without required durability evidence;
- exceed bounded calibration scope;
- use the scientific seed/start;
- proceed to V1 or E1 automatically.

Define exactly what artifacts must exist before C1 can be considered complete.

18. Preserve privacy.

I1 must operationalize the R4 prohibited-data list. Broad raw inventories must not be committed. Hashing a prohibited stable identifier does not sanitize it.

Any unavoidable temporary sensitive capture must remain local, restricted, sanitized immediately and deleted after the minimized record is checked.

19. Preserve all CEML-SCI-1 invariants.

No implementation convenience may change:

- standard/shortcut map semantics;
- first-1 termination;
- standard/shortcut/odd count conversion;
- decimal-digit rung semantics;
- ceml-start-v1;
- scientific seed policy;
- SHA3-256/SHAKE256 rules;
- RFC 8785 canonicalization;
- U64-framed integer encoding;
- CEML-CKPT-1 mathematical/restart semantics;
- result status semantics;
- anomaly/freeze rules;
- V1 zero-unexplained-disagreement standard.

A scientifically material change requires an explicit new protocol/schema version, not an I1 implementation exception.

REPOSITORY DELIVERABLES

At minimum:

- substantially complete and approve docs/CODEX_HANDOFF.md;
- add any small machine-readable schemas/config templates needed to make C1 evidence deterministic, provided they contain no fabricated machine data;
- add benchmark/calibration protocol specifications or fixtures only at bounded non-scientific scale;
- update governance/status/read-order documents necessary for consistency;
- record I1 decisions, rejected implementation candidates and legitimate C1/V1 deferrals;
- do not implement the production engine;
- do not launch C1/local Codex;
- do not inspect the actual machine;
- do not generate the scientific seed;
- do not execute a scientific rung.

I1 EXIT STANDARD

CEML-I1 passes only if a later C1 local automated agent can, from docs/CODEX_HANDOFF.md and its referenced repository artifacts, perform the authorized hardware audit and bounded calibration, make only evidence-backed engineering selections, implement/build the engine, and freeze a sanitized local profile without inventing scientific or machine semantics.

The handoff must be sufficiently explicit that C1 does not need to improvise:

- mathematical invariants;
- audit scope;
- privacy rules;
- benchmark inputs/digests;
- route activation;
- decision sufficiency;
- checkpoint durability testing;
- resource safety;
- artifact schemas;
- build/profile provenance;
- V1 hooks;
- gate/refusal behavior.

At the end:

1. commit all I1 repository updates;
2. report the authoritative commit SHA;
3. summarize the approved implementation specification;
4. summarize choices deliberately left to measured C1 evidence;
5. summarize risks legitimately deferred to C1/V1;
6. state explicitly either “CEML-I1 PASS” or “CEML-I1 REMAINS OPEN”;
7. if I1 passes, provide a self-contained CEML-C1 local hardware-audit/implementation prompt;
8. if I1 remains open, provide the exact continuation task required to finish I1.

The standard is executable specificity without premature implementation or machine guessing.
