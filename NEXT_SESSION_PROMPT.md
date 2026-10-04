# Next Session Prompt — CEML-R3

Use this prompt to begin the next research session.

---

CEML-R3 — REPRODUCIBILITY AND VALIDATION AUDIT

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
9. docs/RANDOMNESS_AND_REPRODUCIBILITY.md
10. docs/EXPERIMENT_PROTOCOL.md
11. docs/CHECKPOINT_SPEC.md
12. docs/RESULT_SCHEMA.md
13. docs/VALIDATION_PLAN.md
14. docs/SECURITY_AND_INTEGRITY.md
15. docs/CLAIM_POLICY.md
16. docs/HARDWARE_AUDIT_SPEC.md
17. schemas/run_manifest.schema.json
18. schemas/checkpoint_metadata.schema.json
19. schemas/result.schema.json
20. NEXT_SESSION_PROMPT.md

CEML-R1 and CEML-R2 have passed. The current phase is CEML-R3 research and protocol design only.

Do not import architecture, terminology, assumptions, reports, conclusions, or research state from previous Collatz repositories unless a specific fact is independently relevant, independently re-audited, and explicitly cited.

Do not:

- implement the CEML production engine;
- generate the scientific master seed;
- execute a giant Collatz trajectory or any scientific rung;
- launch the local Codex implementation;
- invent or assume local hardware specifications;
- select machine-specific compiler flags, arithmetic-backend thresholds, macro/super-block sizes, thread counts, checkpoint cadence, RAM ceilings, storage ceilings, or similar local engineering parameters;
- silently convert an R2 architecture shortlist into a production winner;
- treat a hash, published output, benchmark, or successful test as a substitute for independent correctness validation;
- treat multiple checks derived from the same affine recurrence as independent oracles;
- conflate shortcut, standard and odd-only step counts;
- allow a macro block to obscure the first occurrence of 1;
- generate or inspect scientific starts before the generator/seed/rung protocol is frozen;
- freeze the final executable ladder or generate its seed during R3;
- advance to R4 unless every R3 exit criterion is genuinely satisfied.

PURPOSE

Freeze the scientific semantics and reproducibility/validation contract that every later CEML implementation, checkpoint, manifest and result must obey.

R2 evidence must be inherited with its caveats, especially:

- exact shortcut affine blocks satisfy 2^k T^k(n) = 3^i n + B;
- the low k bits determine k exact shortcut steps;
- affine composition order is non-commutative;
- exact standard-map count equals shortcut-map count plus the number of odd shortcut steps;
- odd-only stepping must accumulate valuations to convert counts exactly;
- total-stopping semantics require the first occurrence of 1 and terminal-safe macro handling;
- direct elementary stepping is a definition-level oracle for affine batching;
- several collatz-eval audit paths share the affine recurrence and are not mathematically independent;
- Boutoukoat/Gerbicz is an independent implementation lineage but algebraically the same affine family;
- Dense/Sparse, value-threaded recursion, FLINT routing, macro sizes, allocation strategies and parallelism remain later benchmark hypotheses;
- durable checkpoint semantics are not supplied by external implementations;
- the Elsenhans collatz_2026.tar.gz artifact and the cited Gerbicz primary forum post remain unresolved external evidence gaps.

AUDIT AND FREEZE AT MINIMUM

A. Scientific map and count semantics.

Freeze, implementation-independently:

- the canonical CEML map used for trajectory accounting;
- whether standard-map, shortcut-map and odd-only counts are stored/reported and which is primary;
- exact conversion formulas;
- first-occurrence-of-1 semantics;
- total stopping time terminology;
- maximum/minimum magnitude metrics, if any, with exact definitions;
- the rule for macro blocks near terminal state;
- integer and counter domains, including how unbounded counts are serialized.

The protocol must make it impossible for two conforming implementations to disagree merely because they used different internal maps.

B. Magnitude/rung definition.

Freeze the mathematical definition of a rung, not the final ladder values.

Determine whether a rung is defined by:

- exact decimal-digit count;
- exact bit length;
- or another explicit magnitude interval.

For the chosen definition specify the exact set of permitted positive odd integers, boundary inclusion, leading-bit/digit rules, and conversion/reporting rules.

Do not freeze the final ladder during R3; E1 retains final ladder authorization.

C. Deterministic random-start generation.

Audit suitable deterministic cryptographic primitives and standard references.

Specify:

- primitive and exact version/standard;
- seed bitstring interpretation;
- domain separation;
- rung/index encoding;
- deterministic expansion;
- unbiased mapping into the chosen finite set of odd starts;
- rejection-sampling rules where required;
- retry/counter semantics;
- canonical generated-start encoding;
- start digest;
- test vectors sufficient for independent implementations.

Candidates already noted in the repository include SHAKE256 and ChaCha20-based streams, but R3 must choose only after auditing their standards and suitability. Do not generate the actual scientific master seed.

D. Seed policy and precommitment.

Freeze the protocol for:

- seed generation event requirements at the later authorized gate;
- whether the seed is published immediately, committed then revealed, or handled another reproducible way;
- commitment algorithm and canonical bytes;
- prevention/detection of candidate selection or rerolling;
- loss/recovery policy;
- domain separation between scientific starts and all validation/calibration randomness.

The scientific master seed must remain nonexistent after R3.

E. Canonical encodings and cryptographic digests.

Select and specify stable algorithms and canonicalization for:

- start value;
- checkpoint body and metadata;
- run manifest;
- result record;
- build/profile references where scientifically required.

Research relevant standards for cryptographic hashes and canonical JSON or choose a simpler unambiguous canonical binary/text encoding.

Define exactly:

- byte encoding;
- integer encoding;
- field order/canonicalization;
- Unicode/text restrictions if applicable;
- digest algorithm;
- digest rendering;
- domain-separation prefixes;
- versioning;
- how self-referential digest fields are excluded or normalized.

Hashes identify bytes; they are not correctness proofs.

F. Run manifest.

Substantially complete and scientifically freeze schemas/run_manifest.schema.json plus prose requirements.

The manifest must distinguish:

- scientific protocol identity;
- repository/protocol commit;
- rung definition;
- generator/seed reference and start commitment/digest;
- exact map/count convention;
- engine/build identity placeholders to be populated later;
- machine-profile identity placeholders;
- checkpoint format;
- authorization gate;
- timestamps only where scientifically meaningful.

R3 may define required fields even when later gates supply their values.

G. Checkpoint/restart semantics.

Substantially complete docs/CHECKPOINT_SPEC.md and schemas/checkpoint_metadata.schema.json.

Freeze logical and canonical semantics for:

- current exact n;
- exact step counters needed by the map conventions;
- first-1 safety;
- required run/start/protocol/build/profile identities;
- maximum or other trajectory statistics if scientifically retained;
- checkpoint body encoding;
- metadata/digest binding;
- crash consistency;
- atomic promotion;
- corruption/version refusal;
- resumption validation;
- restart equivalence with uninterrupted execution;
- treatment of caches/derived batching state;
- failure categories.

Do not freeze checkpoint cadence; that remains C1 engineering.

H. Result semantics and certification.

Substantially complete docs/RESULT_SCHEMA.md and schemas/result.schema.json.

Freeze:

- status enum and exact meaning of each status;
- completed-run condition;
- resource stop versus anomaly versus validation/integrity failure;
- map/count fields;
- final value;
- trajectory statistics retained;
- start/build/profile/protocol provenance;
- timing definitions if they remain in scientific records;
- result digest and canonicalization;
- required certification/validation references.

A non-completed status must never imply divergence.

I. Independent validation architecture.

Substantially complete docs/VALIDATION_PLAN.md.

Freeze which validation paths count as genuinely independent.

At minimum specify:

- direct elementary reference stepping;
- affine-block versus k direct T-step differential checks;
- standard/shortcut/odd-only conversion tests;
- exhaustive small-residue/base-table tests;
- randomized bounded differential tests from a validation-only deterministic seed/domain;
- adversarial low-bit and limb-boundary patterns;
- odd split lengths;
- powers of two and terminal overshoot fixtures;
- serialization round trips;
- checkpoint stop/resume equivalence;
- fault injection;
- backend/feature-route activation tests;
- selected exact Mersenne fixtures inherited from R2;
- implementation diversity where practical.

R2 bounded fixtures include:

- 27: 111 standard steps and 70 shortcut steps;
- 2^127-1: 1,660 standard steps, 593 odd standard steps, 1,067 shortcut steps;
- 2^44497-1: 598,067 standard steps, 214,150 odd standard steps, 383,917 shortcut steps.

Confirm provenance before freezing fixture files or schemas. Do not execute a scientific rung.

J. V1 acceptance criteria.

Define objective pass/fail criteria for the later V1 gate.

Include requirements for:

- all required test classes;
- zero unexplained arithmetic disagreements;
- deterministic regeneration;
- checkpoint/restart equivalence;
- canonical serialization and digest agreement;
- feature-specific route coverage;
- sanitizer/checked-build expectations where relevant;
- validation evidence manifest;
- handling and logging of any deviation.

Do not claim V1 has passed during R3.

K. Anomaly and freeze rules.

Freeze what later scientific execution must do on:

- unexpected non-1 state behavior;
- arithmetic/oracle disagreement;
- resource exhaustion;
- checkpoint corruption;
- reproducibility mismatch;
- build/profile mismatch;
- unexpected termination;
- suspected counterexample behavior.

Automatic progression must stop. Preserve evidence. A resource stop is not divergence, and a possible counterexample requires a separate certification programme.

L. Machine-readable schema consistency.

Review all R3-relevant schemas together. Required fields, versions and terminology must agree across:

- protocol prose;
- run manifest;
- checkpoint metadata/body specification;
- result schema;
- validation evidence requirements.

Avoid implementation-language-sized integers in schemas. Prefer canonical strings or another explicitly unbounded representation for scientific counters.

M. Research evidence.

Use current primary standards for cryptographic primitives, canonicalization and reproducibility claims. Record exact standard/version/section where material.

Do not select a primitive merely because it is popular. Analyze determinism, unbiased mapping, test vectors, domain separation, availability for independent reproduction, and long-term specification stability.

REPOSITORY DELIVERABLES

Substantially complete, mutually consistent R3 versions of:

- docs/RANDOMNESS_AND_REPRODUCIBILITY.md;
- docs/EXPERIMENT_PROTOCOL.md;
- docs/CHECKPOINT_SPEC.md;
- docs/RESULT_SCHEMA.md;
- docs/VALIDATION_PLAN.md;
- docs/SECURITY_AND_INTEGRITY.md where justified;
- schemas/run_manifest.schema.json;
- schemas/checkpoint_metadata.schema.json;
- schemas/result.schema.json;
- any additional small schema/specification needed to make validation evidence machine-readable.

Update PROGRAM_STATUS.md only if every R3 exit condition is genuinely met.

Do not write production code.
Do not generate the scientific master seed.
Do not execute a scientific rung.
Do not launch local Codex.
Do not choose machine-specific engineering parameters.

R3 EXIT STANDARD

R3 passes only if:

- scientific map/count and first-1 semantics are unambiguous;
- magnitude/rung definition semantics are frozen;
- deterministic random-start generation and seed policy are reproducible and unbiased by construction;
- the actual scientific master seed has not been generated;
- canonical encodings and digest rules are fully specified;
- run/result/checkpoint schemas agree with prose;
- checkpoint restart equivalence is defined;
- independent-oracle diversity is explicit;
- validation fixtures/test classes and fault-injection requirements are frozen;
- V1 objective acceptance criteria are frozen;
- anomaly/freeze rules are explicit;
- no machine-specific tuning or production implementation has occurred.

At the end:

1. commit all R3 repository updates;
2. report the authoritative commit SHA;
3. summarize the scientific semantics frozen;
4. summarize the validation/oracle contract;
5. summarize unresolved risks that are legitimately deferred to R4/I1/C1/V1;
6. state explicitly either "CEML-R3 PASS" or "CEML-R3 REMAINS OPEN";
7. if R3 passes, provide a self-contained CEML-R4 hardware-audit specification prompt;
8. if R3 remains open, provide the exact continuation task required to finish R3.

The standard is reproducibility, independence of validation, unambiguous scientific semantics and auditability. No later performance consideration may silently change a frozen R3 scientific rule.
