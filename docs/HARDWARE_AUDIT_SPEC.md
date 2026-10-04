# CEML-R4 Hardware Audit Specification

Status: **FROZEN HARDWARE-AUDIT CONTRACT — CEML-R4 PASS**

Decision date: **2026-10-04**  
Authoritative input baseline: **cfdffd21093ab576c0f9a827fff9fb9417eeea19**  
Scientific protocol: **CEML-SCI-1 — unchanged**  
Checkpoint format: **CEML-CKPT-1 — unchanged**  
Scientific execution: **NOT AUTHORIZED**  
Scientific master-seed generation: **NOT AUTHORIZED**  
Production implementation: **NOT AUTHORIZED BY R4**

## 1. Purpose and authority

This document freezes what the later CEML-C1 local hardware audit is allowed and required to inspect, measure, sanitize, test and decide before a production build/profile can be frozen.

R4 does **not** perform that audit. It records no fact about the user's actual machine, chooses no machine-specific parameter, installs no dependency, implements no production engine, generates no scientific seed, freezes no final magnitude-ladder values and executes no scientific or giant trajectory.

The repository remains the sole authoritative CEML state. C1 may characterize the dedicated local machine only after I1 supplies the approved implementation/audit interfaces and bounded benchmark suite required by this contract.

The controlling rule is:

> a hardware-dependent engineering choice is justified only by privacy-safe, machine-local, bounded, reproducible evidence collected under this contract; missing evidence remains missing.

No hardware observation or benchmark may weaken, reinterpret or override CEML-SCI-1.

## 2. R4/C1/I1/V1 boundary

R4 freezes the audit contract. I1 must translate this contract and the already frozen scientific contract into executable interfaces, record formats, bounded benchmark-suite definitions and implementation acceptance tests. C1 may then inspect the actual machine, run the authorized bounded calibration, make hardware-dependent engineering choices from the resulting evidence, implement/build the engine, and freeze the sanitized local machine/build profile.

V1 remains a separate validation gate. C1 benchmark success is not V1 evidence. Performance agreement is not correctness validation. A benchmark checksum is necessary benchmark evidence, but it cannot replace the CEML-V1-SUITE-1 independence architecture.

C1 may stop or refuse. It may not guess.

## 3. Frozen evidence classes

Every C1 machine/audit record must be classified as exactly one of the following.

### 3.1 OBSERVED_FACT

A directly observed property of the audited machine or its active environment, obtained from an identified command, API, file, library query or other local measurement source.

Examples include the reported operating-system release, active kernel, compiler version, available instruction-set feature, installed RAM, active filesystem type, or tool/library version.

An OBSERVED_FACT must record:

- the sanitized fact;
- collection method or source;
- collection time or audit-run identifier where timing matters;
- whether the source reports static capability, active configuration or momentary state;
- any relevant uncertainty or ambiguity;
- sanitization performed.

A vendor/model name is an observation only when exposed by a reliable local source. C1 must not infer a microarchitecture, cache size, feature set, drive technology or other property merely from a marketing family name when the local source does not establish it.

### 3.2 CALIBRATION_MEASUREMENT

A result from an authorized bounded deterministic benchmark or storage/durability test performed on the audited machine/build.

A CALIBRATION_MEASUREMENT must bind the benchmark protocol, deterministic input identity, build identity, activated route, correctness digest/checksum, resource observations, timing methodology and repeat/variability information required by this document.

A benchmark result belongs only to the audited machine, operating state and build/configuration represented by its evidence. It is not a universal performance claim.

### 3.3 ENGINEERING_DECISION

A C1 choice derived from one or more OBSERVED_FACT or CALIBRATION_MEASUREMENT records.

Examples include selected language/toolchain, arithmetic backend, block size, representation, allocation strategy, permitted thread count, checkpoint write strategy or compiler mode.

Every ENGINEERING_DECISION must record:

- the question being decided;
- candidate alternatives actually considered;
- evidence record identifiers used;
- correctness/reproducibility constraints that eliminated any candidate;
- the selected choice or explicit refusal to select;
- the decision rule/rationale;
- remaining limitations;
- whether the choice is frozen into the local machine/build profile.

An engineering decision without traceable local evidence is invalid.

### 3.4 UNAVAILABLE_OR_UNSUPPORTED

A fact, facility, tool, feature or measurement that could not be obtained safely and reliably.

This class must record:

- what was unavailable or unsupported;
- the attempted non-destructive observation method, if any;
- the reason measurement was unavailable, denied, unsafe, ambiguous or unsupported;
- which downstream decisions are blocked or constrained.

A missing measurement stays missing. C1 must not replace it with a generic internet specification, another machine's benchmark, an inferred model specification, a guessed default or a silently substituted component.

## 4. Authorized machine-observation scope

C1 may inspect only information relevant to correctness, reproducibility, bounded performance calibration, resource safety, build provenance or checkpoint durability.

Where safely and reliably exposed, the authorized categories are as follows.

### 4.1 Operating system and execution environment

C1 may observe:

- operating-system family, release and relevant build/revision;
- kernel family/release;
- machine architecture and ABI/target information;
- active process architecture where it may differ from machine architecture;
- virtualization/container status where it can materially affect measurement or timing and can be observed without collecting identifiers;
- scheduler or affinity facilities relevant to benchmark reproducibility;
- power/sleep/hibernation settings relevant to long-running local work;
- active timezone only if required for interpreting timestamps, without treating location as a hardware fact.

C1 must not inventory unrelated services, user applications, accounts or system history.

### 4.2 CPU

C1 may observe, where reliably exposed:

- architecture;
- vendor and model string;
- microarchitecture only when a trustworthy local facility identifies it;
- physical core count;
- logical processor/thread count;
- topology relevant to benchmarking, including NUMA topology where applicable;
- available instruction-set extensions/capabilities;
- cache hierarchy and sizes;
- nominal/base/max or currently reported frequency information;
- active frequency observations during bounded calibration;
- observable throttling indicators;
- permitted hardware performance-counter facilities.

The existence of a CPU feature does not prove that a compiled route used it. Route activation requires separate evidence under Section 11.

### 4.3 Memory

C1 may observe:

- installed physical RAM;
- currently available RAM;
- memory-page information relevant to allocation behaviour;
- NUMA memory topology where applicable;
- swap/pagefile presence, configured capacity and current pressure;
- bounded memory-bandwidth observations when useful to a candidate implementation decision;
- memory-pressure indicators available without privileged invasive tooling.

Momentary free/available-memory values must be labelled as time-dependent observations, not permanent capacity.

### 4.4 Storage and filesystem

For the intended run/checkpoint artifact location, C1 may observe:

- storage device class when reliably exposed, such as SSD/HDD/NVMe or equivalent;
- filesystem type and version/features where available;
- mount properties relevant to correctness or durability;
- local versus network/remote semantics;
- capacity and free-space/headroom information needed for bounded engineering work;
- block/allocation information relevant to checkpoint files;
- supported flush/synchronization and atomic rename/promotion primitives;
- directory metadata durability requirements documented by the platform/filesystem;
- bounded sequential write, serialization, flush and promotion behaviour.

Do not collect unrelated partition, volume or filesystem inventories. Stable device IDs, filesystem UUIDs, serial numbers and unrelated mount paths are prohibited.

### 4.5 Toolchains and exact-arithmetic dependencies

C1 may determine availability, exact version and relevant build/runtime configuration for tools actually being considered under I1, including as applicable:

- C compiler;
- C++ compiler;
- Rust toolchain and package manager;
- Python runtime;
- build-system tools;
- linker;
- assembler when materially relevant;
- GMP;
- FLINT;
- rug or another approved wrapper;
- other exact-arithmetic libraries explicitly permitted by I1;
- sanitizer/checker tooling required by V1 preparation;
- utilities needed for bounded timing, memory or filesystem measurement.

C1 must not produce a general installed-software inventory.

### 4.6 Thermal and power observations

Where non-invasive userspace facilities expose them, C1 may record:

- temperature observations during bounded calibration;
- thermal-limit or throttling flags;
- frequency reduction correlated with sustained work;
- power-source state where relevant to reproducibility/safety;
- sleep/hibernation risk;
- other platform indicators needed to decide whether a measurement is stable enough to use.

If thermal/power information is unavailable, it is recorded as UNAVAILABLE_OR_UNSUPPORTED. C1 may still benchmark only if other safety observations are sufficient; it may not fabricate a thermal conclusion.

## 5. Privacy, minimization and sanitization

Privacy minimization is mandatory, not optional report polishing.

### 5.1 Prohibited persisted/committed identifiers

C1 must not persist in repository history, machine-readable committed summaries or human-readable committed reports any unnecessary:

- usernames or home-directory names;
- hostnames/device names;
- serial numbers;
- motherboard, CPU, storage or firmware serial identifiers;
- MAC addresses;
- IP addresses;
- Wi-Fi/network identifiers;
- account IDs;
- cloud/tenant IDs;
- credentials, tokens or cookies;
- private keys or key material;
- environment-variable secrets;
- stable hardware/device UUIDs;
- filesystem/partition UUIDs;
- unrelated filesystem paths;
- unrelated process lists;
- unrelated software inventories;
- unrelated network configuration;
- other stable personal or machine identifiers.

Hashing a prohibited stable identifier does not make it acceptable. Do not retain a digest of a hostname, serial number, MAC address or analogous identifier merely to create a pseudonymous machine fingerprint.

### 5.2 Collection minimization

Prefer narrow commands/APIs that return only the needed field over broad inventory commands.

If a tool can select specific properties, C1 must request only those properties. If a broad command is the only practical source, raw output must be treated as sensitive until sanitized.

C1 must never collect credentials or secrets for the purpose of proving that they were later removed.

### 5.3 Sanitization-before-persistence rule

When raw command output mixes useful and sensitive fields:

1. collect it through a pipeline that extracts/filters the permitted fields before writing a persistent audit artifact whenever practical;
2. if temporary raw capture is unavoidable, keep it local in a restricted temporary location, do not add it to Git, sanitize it immediately, and delete it after the sanitized record has been checked;
3. persist only the minimized sanitized representation needed to support the observation;
4. record that sanitization occurred and which prohibited field classes were removed, without recording the removed values.

Raw sensitive inventories must never be committed for convenience.

### 5.4 Paths

Committed reports should use semantic path labels such as "checkpoint filesystem", "benchmark scratch area" or repository-relative paths. Absolute user-specific paths are prohibited unless an exact path is genuinely necessary for correctness and can be sanitized without retaining identity; in normal C1 reporting it should not be necessary.

### 5.5 Human review gate

Before any C1 hardware/profile artifact enters repository history, C1 must run an explicit sensitive-data scan defined by I1 and present the sanitized diff/artifact set for review. Discovery of a prohibited identifier blocks commit until removed and the affected artifact is regenerated.

## 6. Bounded deterministic calibration

Calibration exists only to choose engineering parameters for the audited machine/build. It is not scientific execution and not V1.

### 6.1 Scientific separation

Calibration must:

- use only the domain label CEML-CALIBRATION-RANDOM-V1 plus its terminating NUL for deterministic pseudo-random engineering inputs;
- use only public, non-secret calibration seeds/input descriptors committed or frozen by the I1 benchmark-suite definition;
- never read, request, derive, load or reuse the scientific master seed;
- never derive any ceml-start-v1 scientific start;
- never evaluate a precommitted or candidate scientific rung start;
- never use trajectory behaviour to select, reroll or retain a scientific start;
- remain materially below scientific magnitude.

A calibration artifact must be visibly labelled non-scientific.

### 6.2 Deterministic input identity

Every benchmark case must be reproducible from a versioned case specification. The specification must identify, as applicable:

- benchmark-suite/protocol version;
- public calibration seed or exact formula-defined input;
- domain label;
- generator/version;
- operand/input size class;
- case index;
- route/candidate configuration;
- exact input digest;
- any generated auxiliary artifact digest.

I1 must define the deterministic calibration generator and canonical input/artifact digest procedure before C1. R4 does not generate any calibration inputs.

### 6.3 Maximum-work principle

Every benchmark suite and individual case must have an explicit finite bound on work before execution, expressed in the dimensions that matter to the case: input size, iteration/block count, repeat count, scratch/storage allowance, process count/thread count and/or wall-time safety limit.

R4 does not invent machine-specific numerical ceilings. I1 must define suite-level non-scientific maxima; C1 must set stricter local safety limits from observed machine headroom before running the case. C1 may reduce or abort work for safety, but may not silently enlarge the authorized suite.

Calibration must stay far below the smallest contemplated scientific scale and must not become a disguised giant-trajectory run.

### 6.4 Warm-up and repeated measurements

For timing-sensitive choices:

- distinguish warm-up runs from measured repetitions;
- use at least one warm-up when initialization, allocator state, dynamic frequency, JIT/runtime startup, cache population or library initialization can materially affect the measurement;
- use multiple measured repetitions for a timing-based comparison;
- keep benchmark inputs/configuration identical across repetitions unless the suite explicitly defines a deterministic case sequence;
- report the repeat count and variability summary;
- do not discard slow or fast repetitions merely because they are inconvenient;
- if an environmental disturbance invalidates a repetition, mark it invalid with a reason rather than silently removing it.

Cold-start and warmed-state measurements may both be useful, but they must be separately labelled and never pooled without explanation.

### 6.5 Correctness prerequisite

A performance datum is admissible only when the case's exact final state/checksum/digest agrees with its required reference.

A faster incorrect result is not calibration evidence.

## 7. Required hardware-dependent questions

C1 must answer the following with measured local evidence where the candidate is applicable and supported. R4 does not choose the winner.

1. What is the crossover among direct elementary stepping, small affine/table blocks and hierarchical/binary-split affine batching for representative bounded operand sizes?
2. How do viable macro/block sizes affect wall time, CPU time, allocation pressure and peak memory?
3. Does a supported GMP route or a supported optional FLINT route perform better for the product shapes actually used, and can each route be proved active?
4. Where are multiplication/backend crossover points for the audited build?
5. Are Dense/Sparse or analogous state representations still viable, and for what deterministic dense/sparse input classes?
6. What are the costs and peak-memory effects of allocation reuse/in-place operations versus copying strategies?
7. How do I1-permitted compiler/optimization modes compare on correctness-identical cases?
8. Does single-thread execution remain preferable, or does permitted auxiliary parallelism improve wall time without violating exactness, resource limits or reproducibility requirements?
9. Which checkpoint serialization/write/flush/promotion approach best satisfies CEML-CKPT-1 on the intended filesystem?
10. What terminal handoff strategy preserves exact first-occurrence-of-1 accounting while avoiding excessive overhead?
11. What is the measured cost of each proposed audit/canary/invariant check?
12. How do peak RSS, live/transient allocation and simultaneous-buffer pressure scale with state size and macro/block choice?
13. What is the effect of checkpoint serialization/deserialization on time, memory and temporary storage?
14. Are any performance conclusions unstable under thermal throttling, frequency changes, swap pressure or other observed sustained-load effects?

If I1 rejects a candidate before C1 for correctness, maintainability, unsupported API or reproducibility reasons, C1 need not benchmark it; the decision log must reference that I1 exclusion.

## 8. Benchmark evidence requirements

Each machine-readable benchmark record must contain enough information to reproduce and interpret the case.

At minimum, as applicable, record:

- benchmark-suite/protocol version;
- benchmark/case identifier;
- deterministic input specification and input digest;
- exact executable/build identity;
- source/engine commit where applicable;
- compiler/toolchain versions;
- dependency/library versions;
- target triple/ABI where applicable;
- relevant compiler/linker flags;
- runtime/build feature configuration;
- backend/feature route requested;
- backend/feature route proved active;
- route-activation evidence identifier;
- process/thread/affinity configuration where relevant;
- warm-up count;
- measured repeat count;
- wall-clock measurement source/methodology;
- per-repeat wall-clock values or lossless local raw record;
- CPU-time source/methodology and values;
- variability summary, at minimum a central value and range;
- peak resident memory;
- live/transient allocation observations when measurable;
- swap/pagefile pressure observations relevant to validity;
- temporary/scratch bytes;
- serialized checkpoint bytes where applicable;
- checkpoint serialization time;
- write time;
- durable flush/sync time;
- rename/promotion/directory-sync time where applicable;
- thermal/throttling/frequency observations when accessible;
- abort/invalid-run flags and reasons;
- exact correctness final-state digest/checksum;
- reference digest/checksum;
- correctness agreement boolean;
- sanitized artifact/log digest(s).

Benchmark timing without correctness agreement is invalid. Benchmark timing without route-activation evidence is invalid for selecting that route.

## 9. Timing and memory methodology

I1 must provide a portable measurement abstraction with platform-specific adapters where needed.

C1 must:

- prefer a monotonic high-resolution wall clock;
- record whether CPU time is process, thread or aggregate child-process time;
- distinguish elapsed wall time from CPU time;
- avoid comparing measurements that use materially different timer definitions without normalization/explanation;
- record process/thread count and affinity/pinning if used;
- capture peak RSS with a documented platform method;
- capture allocator/live/transient bytes where the selected runtime/library exposes them reliably;
- record when a metric is unavailable rather than substituting an estimate;
- avoid treating filesystem cache effects as durable-write time unless the benchmark specifically intends cached-write measurement.

Memory conclusions must account for simultaneous old/new values, affine coefficients, scratch temporaries, serialization buffers, checkpoint A/B copies and other live buffers relevant to the candidate route.

## 10. Compiler and native-tuning policy

R4 selects no compiler and no flag.

If I1 permits machine-specific tuning such as -march=native, target-cpu=native or an equivalent facility, C1 must compare it against an appropriate reproducible portable/reference build where applicable and document:

- exact compiler and linker identity/version;
- complete relevant flags;
- target triple;
- requested CPU target/features;
- observable emitted/activated feature route where practical;
- dependency builds affected by native tuning;
- benchmark and correctness evidence supporting selection;
- portability consequences.

If a native-tuned build is selected, the local profile must state that the build is machine-specific. Rebuilding on a different machine is a **new build/profile event**, not reproduction of the same binary identity. The different machine must be re-audited and any hardware-dependent decisions re-justified before scientific use. V1 evidence for the original build/profile does not automatically transfer.

Binary reproducibility and source-level reproducibility must not be conflated. C1 must preserve enough provenance to rebuild the selected configuration, but a rebuild on different hardware may legitimately produce a different build digest and require new validation.

## 11. Route-activation evidence

Every optimized feature/backend considered for selection must have a bounded case that proves the intended route actually executed.

Acceptable route-activation evidence can include an I1-designed deterministic route counter, explicit trace/event, backend callback, diagnostic build hook, symbol/path assertion or another mechanism that cannot be satisfied by silently remaining on a fallback path.

For each tested route:

1. request or force the route;
2. run a deterministic correctness-known bounded case;
3. prove activation with the route evidence mechanism;
4. record the activation evidence;
5. verify exact output/state digest against the required reference;
6. record fallback/refusal explicitly if activation cannot be achieved.

A benchmark that silently stays on a fallback path is **not evidence** about the intended feature, even if its output is correct and fast.

Route instrumentation used for calibration may be excluded from final production performance builds only if I1 defines how the selected route remains identifiable in build/profile provenance and V1 can force/verify it independently.

## 12. Dependency and toolchain capture

For every tool/dependency actually used to build, calibrate or validate a candidate that may enter the scientific build/profile, C1 must record as applicable:

- component name;
- exact version;
- source/distribution channel;
- source or package digest where available/relevant;
- build configuration/options;
- link mode and ABI-relevant details;
- enabled/disabled features;
- wrapper/binding version;
- compiler used to build the dependency when relevant;
- runtime library identity where relevant;
- license/provenance note where already required by I1.

Missing GMP, FLINT, Rust, C/C++, Python or other optional tooling remains missing until an explicitly authorized installation step occurs. C1 must not silently install, upgrade, enable or substitute a component.

An installation or toolchain change that can affect measurements invalidates affected prior calibration evidence unless the decision log explicitly demonstrates non-impact. Normally the relevant observations/benchmarks must be rerun.

## 13. Offline-capable and pinned build/run requirement

The eventual scientific build/run must be reproducibly pinned and offline-capable, consistent with docs/SECURITY_AND_INTEGRITY.md.

I1/C1 must ensure that:

- dependency versions are locked/pinned;
- required source/package artifacts or an approved reproducible local cache are available before scientific execution;
- integrity digests are retained for fetched/vendored build inputs where practical;
- scientific execution does not fetch code or dependencies from the network;
- build scripts do not depend on mutable network content;
- generated code/build metadata needed for reproduction is retained;
- network availability is not required to resume or verify a scientific checkpoint.

R4 does not mandate vendoring versus another pinned offline-capable method; I1/C1 must choose and document one.

## 14. CEML-CKPT-1 storage/filesystem validation

The scientific checkpoint semantics in docs/CHECKPOINT_SPEC.md are already frozen. C1 may determine whether the intended target storage can satisfy them; it may not weaken them.

C1 must run bounded non-scientific storage tests on the **same filesystem/mount class intended for checkpoints** and establish evidence for:

### 14.1 Complete file durability

Demonstrate the required platform sequence for writing a complete candidate state.bin and metadata.json, flushing file data/metadata as required, closing/reopening and verifying exact bytes/digests.

### 14.2 Atomic promotion

Demonstrate that the selected rename/replace/promotion primitive has the atomicity semantics required by the A/B or equivalent checkpoint design on the target filesystem.

If the platform/filesystem does not provide the required atomic operation, that storage approach is unsupported.

### 14.3 Directory/pointer metadata durability

Establish the platform-specific operation required to make directory entries, renamed slots and any latest pointer durable after promotion. Do not assume a file flush automatically makes directory metadata durable.

Where the platform exposes no meaningful directory-sync primitive, C1 must rely on documented platform semantics plus bounded recovery tests and record the limitation. If CEML-CKPT-1 durability cannot be justified, the filesystem is unsupported for scientific checkpoints.

### 14.4 A/B slot retention and recovery

Demonstrate that promotion never destroys the sole valid prior checkpoint and that recovery can choose a unique latest valid slot using slot contents/digests rather than an untrusted pointer alone.

### 14.5 Interrupted-write matrix

Using bounded synthetic checkpoint artifacts only, deliberately interrupt the writer at each materially distinct phase defined by I1, including at least:

- before body completion;
- between body and metadata completion;
- before durable file flush;
- after file flush but before promotion;
- during/around pointer or slot promotion to the extent safely testable;
- after promotion but before directory/pointer durability step;
- during cleanup/retirement of the older slot.

The recovery test must verify that no partially written or digest-invalid checkpoint is accepted and that the previous validated slot remains recoverable whenever the CEML-CKPT-1 protocol promises it.

Forced process termination/fault injection is required. Destructive power-cut testing is not automatically authorized by R4; if documented platform guarantees plus process-interruption tests are insufficient to justify the needed durability semantics, C1 must mark the storage path unsupported rather than perform unsafe hardware actions.

### 14.6 Serialization and flush performance

After correctness/durability semantics are established, C1 may benchmark serialization, write, flush, promotion and recovery costs. A faster method that does not satisfy all checkpoint semantics is ineligible.

## 15. Resource-safety rules

C1 calibration must protect the dedicated machine and preserve the distinction between engineering aborts and scientific outcomes.

Before any non-trivial bounded case, C1 must establish local safety limits from observed conditions for:

- memory headroom;
- storage headroom;
- temporary/scratch space;
- swap/pagefile pressure;
- sustained CPU load;
- thermal/throttling behaviour where observable;
- permitted process/thread count;
- sleep/hibernation/power-loss risk;
- maximum case duration/work.

R4 intentionally freezes no machine-specific numeric values.

### 15.1 Memory

Calibration must reserve enough headroom for the operating system, audit tooling, simultaneous big-integer buffers, checkpoint A/B copies and failure handling. C1 must abort before memory pressure threatens system stability or risks uncontrolled OOM behaviour.

Swap activity that materially distorts or endangers a benchmark must cause the case to be marked invalid/aborted according to the I1 rules. C1 must not disable swap or alter global memory policy silently.

### 15.2 Storage

Before a storage-heavy case, verify sufficient free-space headroom for the benchmark, temporary artifacts, retained prior checkpoint slot and cleanup margin. Abort before exhausting the filesystem.

### 15.3 Thermal/throttling

If sustained thermal throttling or frequency collapse makes a performance comparison unstable, stop or invalidate the affected measurement and record the observation. Do not defeat platform thermal protections.

### 15.4 Power and sleep

Longer calibration cases require an explicitly observed power/sleep state suitable for uninterrupted local work. C1 may recommend/record an operator-approved temporary configuration change, but it must not silently change global power policy.

### 15.5 Abort semantics

A calibration abort is an engineering event only. It is never a CEML scientific result, never evidence of divergence, and never permission to infer the outcome of a larger case.

Abort reasons must be recorded in the benchmark evidence and may justify reducing a later case size. They may not justify increasing limits.

### 15.6 Cleanup

Temporary calibration artifacts must be isolated from scientific run directories, named/marked as non-scientific, and removed after required digests/summaries are retained. Cleanup must never delete the only evidence needed to reproduce an accepted engineering decision.

## 16. Decision rules for hardware-dependent choices

A C1 choice may be frozen only when:

1. all correctness eligibility constraints from CEML-SCI-1, R2, R3 and I1 are satisfied;
2. the candidate is supported on the observed machine/toolchain;
3. required route activation has been proved;
4. deterministic bounded correctness output agrees with the required reference;
5. measurements needed for the decision are available and valid;
6. resource-safety constraints are satisfied;
7. the decision log links the selected choice to the evidence.

When two candidates are indistinguishable within observed variability, C1 must not manufacture a performance winner. It may select the simpler/more portable/lower-risk eligible route only if I1 explicitly permits that tie-break rule and the decision log states it.

A choice may be "unsupported", "not measurable safely" or "no justified winner". Refusal is preferable to unmeasured tuning.

## 17. Required C1 artifacts

C1 must produce sanitized equivalents of at least the following.

### 17.1 local_reports/HARDWARE_REPORT.json

Machine-readable sanitized observations with evidence-class tags, collection-source descriptors, availability status and uncertainty notes. It must contain only authorized/minimized hardware/environment facts.

### 17.2 local_reports/HARDWARE_REPORT.md

Human-readable summary generated from or reconciled with the JSON report, clearly distinguishing observed facts, unavailable information and conclusions. It must not add unrecorded machine facts.

### 17.3 Machine-readable bounded benchmark records

I1 must define the concrete format/location. The records must include all Section 8 fields applicable to each case.

Sanitized raw per-repeat benchmark records may remain local when they are large, provided repository history contains:

- suite/version identity;
- summary;
- aggregate artifact digest(s);
- retained local locator expressed without prohibited private path detail;
- decision references sufficient to audit the choice.

If the sanitized raw records are small and contain no prohibited information, they may be committed.

### 17.4 Benchmark summary

A sanitized committed machine-readable summary must identify all candidate comparisons used in decisions, valid/invalid/aborted cases, variability summaries, correctness agreement and route activation.

### 17.5 Decision log

A committed decision log must map every hardware-dependent selection or refusal to its supporting observation/calibration record IDs and record alternatives considered.

No decision may exist only in chat, shell history or an uncommitted notebook.

### 17.6 config/local_machine_profile.toml or equivalent

A frozen sanitized local machine/build profile must bind the engineering selections required to reproduce the selected build on the audited machine. At minimum it must identify, directly or by digest/reference:

- profile format/version;
- sanitized relevant hardware capability summary;
- OS/kernel/ABI class needed for build/run interpretation;
- selected toolchain/dependency versions;
- selected compiler/linker configuration;
- selected backend/feature routes;
- block/macro/representation/allocation/thread choices;
- checkpoint storage/durability strategy;
- resource-safety ceilings selected in C1;
- build identity/digest linkage;
- evidence/decision-log linkage;
- non-portability markers such as native tuning;
- unavailable capabilities that constrain the build.

I1 must freeze the exact profile serialization and digest construction before C1 so the machine_profile_digest required by the R3 schemas is deterministic. R4 does not introduce or alter a CEML-SCI-1 digest domain label.

## 18. Commit versus local-only artifact policy

The following **sanitized** artifacts must enter repository history at C1:

- local_reports/HARDWARE_REPORT.json;
- local_reports/HARDWARE_REPORT.md;
- benchmark summary;
- decision log;
- frozen local machine/build profile;
- hashes/digests of any decision-relevant sanitized raw benchmark bundles kept outside Git;
- exact audit/benchmark protocol versions and build/profile identifiers.

The following may remain local and must not be committed when sensitive or unnecessarily large:

- unsanitized raw command output;
- temporary sensitive captures;
- large per-repeat benchmark logs whose sanitized digest/summary is committed;
- temporary benchmark inputs reproducible from the frozen deterministic generator;
- scratch files;
- intermediate build products not required for provenance.

A local-only artifact used to justify a frozen decision must have a committed cryptographic digest and a stable non-sensitive logical identifier, and must be retained according to the C1 evidence policy. If it is lost before its decision can be independently audited, the affected decision must be treated as unsupported and regenerated.

## 19. Refusal and failure rules

C1 must refuse a hardware-dependent decision when required evidence cannot be obtained safely, reliably and reproducibly.

Specifically:

- unsupported instruction sets remain unsupported;
- missing compilers/libraries remain missing;
- inaccessible performance counters remain unavailable;
- inaccessible thermal data remains unavailable;
- ambiguous CPU/storage properties remain ambiguous;
- failed route activation means the route is not benchmark-proven;
- unverified filesystem durability means the storage target is unsupported for CEML-CKPT-1;
- a benchmark with incorrect digest/checksum is invalid;
- a benchmark under uncontrolled resource pressure is invalid;
- an unsafe privileged probe must not be run merely to fill a field.

C1 must not silently:

- install or upgrade dependencies;
- enable kernel/system features;
- change BIOS/firmware settings;
- change global power/thermal policy;
- substitute a different library/backend;
- infer a missing specification from a product database;
- reuse another machine's benchmark;
- interpolate an unmeasured crossover as though observed.

If an explicitly authorized operator action changes the environment, C1 must record it and repeat any observations/benchmarks invalidated by the change.

## 20. Preservation of V1 validation independence

Hardware calibration cannot satisfy CEML-V1.

The following R3 requirements remain unchanged:

- direct elementary C/T stepping is the definition-level independence anchor;
- affine production routes must be compared against independent direct stepping;
- all CEML-V1-SUITE-1 required classes must execute;
- restart equivalence must be tested;
- required fault injection must be detected;
- canonicalization/digest agreement must be established;
- every enabled optimized route must be forced/covered;
- checked/sanitized build requirements must be met;
- V1 requires zero unexplained disagreements.

Calibration may use the direct oracle or other checks to reject a bad performance candidate, but those calibration runs do not become V1-PASS evidence.

## 21. Preservation of CEML-SCI-1

No R4, I1 or C1 hardware/performance finding may alter any of the following frozen scientific rules:

- standard Collatz map semantics;
- shortcut map semantics;
- first-occurrence-of-1 termination;
- exact standard/shortcut/odd count conversion and invariant;
- decimal-digit rung semantics decimal-digits-v1;
- ceml-start-v1;
- scientific seed commitment/disclosure/precommitment policy;
- SHA3-256/FIPS-202 digest rules;
- SHAKE256/FIPS-202 start generation;
- RFC 8785 JCS canonicalization;
- U64-framed integer encoding;
- CEML-CKPT-1 mathematical/restart semantics;
- result status meanings;
- anomaly/freeze rules;
- V1 zero-unexplained-disagreement acceptance standard.

A hardware-driven exception to any item above is prohibited. A scientifically material change requires an explicit new scientific protocol/schema version and reviewed repository history.

## 22. R4 frozen decisions

| Decision | Status |
|---|---|
| C1 may inspect only the hardware/environment categories in this specification | **FROZEN-AUDIT** |
| Sensitive identifiers are minimized and sanitized before persistence/commit | **FROZEN-AUDIT** |
| Observations, measurements, decisions and unavailable facts are distinct record classes | **FROZEN-AUDIT** |
| Missing evidence may not be guessed or substituted | **FROZEN-AUDIT** |
| Calibration is deterministic, public-seed/domain-separated, bounded and non-scientific | **FROZEN-AUDIT** |
| Scientific master seed and scientific starts are prohibited in calibration | **FROZEN-AUDIT** |
| Timing evidence requires correctness and route-activation evidence | **FROZEN-AUDIT** |
| Machine-specific compiler tuning requires explicit provenance and non-portability treatment | **FROZEN-AUDIT** |
| Dependency/toolchain state used by decisions must be pinned and captured | **FROZEN-AUDIT** |
| Scientific build/run must be offline-capable | **FROZEN-AUDIT** |
| CEML-CKPT-1 storage semantics must be established experimentally/documentarily on the target filesystem | **FROZEN-AUDIT** |
| Resource limits are measured C1 choices; R4 invents no local values | **FROZEN-AUDIT** |
| Unsupported/unmeasurable features remain unsupported/unmeasured | **FROZEN-AUDIT** |
| Calibration does not count as V1 validation | **FROZEN-AUDIT** |
| No hardware finding may weaken CEML-SCI-1 | **FROZEN-AUDIT** |

## 23. Legitimately deferred questions

The following are intentionally deferred without weakening the R4 exit standard.

### I1

I1 must define:

- exact audit command/API adapters by supported platform;
- exact sanitized record schemas;
- deterministic calibration input generator details and public calibration seed(s);
- suite-level bounded case-size/work limits that remain far below scientific scale;
- route-activation instrumentation interfaces;
- benchmark executable/subcommand layout;
- machine-profile serialization and digest procedure;
- exact sensitive-data scan/check;
- code interfaces and build layout that implement the frozen contracts.

I1 must not choose machine-specific winners.

### C1

Only C1 may determine from measured local evidence:

- actual machine facts;
- language/toolchain/backend selected;
- exact compiler flags;
- native-tuning decision;
- macro/block sizes and crossovers;
- Dense/Sparse or analogous representation choice;
- allocation/in-place/copy strategy;
- thread/parallelism policy;
- local memory/storage/thermal safety ceilings;
- checkpoint cadence and buffering;
- actual checkpoint filesystem support;
- terminal handoff implementation choice among I1-eligible exact methods;
- canary/audit level selected for the scientific build.

### V1

V1 must execute the frozen independent correctness/validation suite for the exact C1 engine/build/profile. R4/C1 cannot pre-pass or replace any V1 class.

The unresolved R2 historical evidence gaps concerning the Elsenhans archive and Gerbicz primary source remain historical research gaps and do not block this hardware-audit contract.

## 24. C1 minimum execution sequence

A conforming C1 agent must follow this order:

1. verify repository/I1 authorization and frozen protocol identities;
2. collect only authorized sanitized OBSERVED_FACT records;
3. establish local resource-safety limits before non-trivial calibration;
4. confirm required tool/dependency availability without silent installation;
5. run bounded deterministic correctness-qualified calibration;
6. prove route activation for every optimized route being considered;
7. run checkpoint filesystem/durability tests on the intended storage;
8. record UNAVAILABLE_OR_UNSUPPORTED items without guessing;
9. create ENGINEERING_DECISION records that trace to evidence;
10. implement/build only the selected eligible design under I1;
11. rerun affected calibration if implementation/toolchain changes invalidate evidence;
12. freeze the sanitized local machine/build profile;
13. commit required sanitized reports/summaries/digests/decision log/profile;
14. stop before V1 and before any scientific seed or scientific trajectory.

## 25. R4 exit assessment

A later C1 agent can execute the hardware audit under this contract without inventing machine facts, exposing prohibited identifiers, changing CEML-SCI-1, running scientific work, treating calibration as validation, making unmeasured tuning decisions, accepting an unproven optimized route or assuming checkpoint durability.

No machine-specific fact or engineering winner has been recorded in R4.

**CEML-R4 PASS.**
