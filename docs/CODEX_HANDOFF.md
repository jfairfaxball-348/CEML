# CEML-I1 Codex Implementation Handoff

Status: **APPROVED — CEML-I1 PASS**

Decision date: **2026-10-04**
Authoritative input baseline: **caca7fa2e5cedfc7caf7b9c925eeda771eabcd8c**
Scientific protocol: **CEML-SCI-1 — unchanged**
Checkpoint format: **CEML-CKPT-1 — unchanged**
Hardware-audit contract: **CEML-R4 — unchanged**
Calibration suite: **CEML-CAL-1**
Production implementation: **AUTHORIZED ONLY INSIDE CEML-C1 AFTER THE REQUIRED AUDIT/CALIBRATION ORDER**
Scientific execution: **DENIED**
Scientific master-seed generation: **DENIED**

## 1. Purpose, authority and mandatory C1 order

This document is the executable specification for CEML-C1. It translates the frozen R2/R3/R4 contracts into code boundaries, engineering evidence formats, bounded calibration, decision rules, checkpoint adapters, build/profile provenance and V1 hooks. It does not perform C1.

C1 must execute in this order:

1. verify repository authorization and frozen protocol identities;
2. collect privacy-minimized local hardware/environment evidence;
3. establish local resource-safety ceilings;
4. confirm candidate tool/dependency availability without silent installation;
5. implement only bounded calibration/reference harnesses needed to compare eligible candidates;
6. run CEML-CAL-1 and checkpoint-filesystem tests;
7. make evidence-backed engineering decisions;
8. implement the selected production engine;
9. build it, rerunning any calibration invalidated by implementation/toolchain changes;
10. freeze the sanitized build manifest and local machine profile;
11. commit the required sanitized C1 artifacts;
12. stop. C1 must not enter V1 or E1 automatically.

C1 may refuse at any point. Missing evidence remains missing. Nothing in I1 authorizes the scientific seed, a scientific start, a giant/scientific trajectory, final ladder freeze or a V1-PASS claim.

## 2. Frozen implementation architecture

The implementation must preserve these machine-neutral boundaries. Concrete language/module names may differ, but responsibilities and independence boundaries may not be collapsed in a way that weakens validation.

### 2.1 Canonical scientific state

Production execution is represented only at exact shortcut-map boundaries by:

- current_n: exact positive arbitrary-precision integer;
- shortcut_steps: exact non-negative unbounded integer;
- odd_steps: exact non-negative unbounded integer;
- standard_steps: exact non-negative unbounded integer;
- terminal_reached: boolean.

Invariant: standard_steps = shortcut_steps + odd_steps.
Invariant: terminal_reached if and only if current_n = 1.
No scientific transition is permitted after terminal_reached becomes true.

Engineering caches, route counters, timers, allocator state, recursion stacks, thread schedules and benchmark data are not scientific state.

### 2.2 DefinitionOracle

The definition oracle has two deliberately simple elementary paths.

C-oracle:
- input n >= 1;
- if n is even, return n/2 and one standard step;
- if n is odd, return 3n+1 and one standard step;
- no affine batching, production low-bit helper, production table or production composition routine may be called.

T-oracle:
- input n >= 1;
- if n is even, return n/2, shortcut increment 1, odd increment 0, standard increment 1;
- if n is odd, return (3n+1)/2, shortcut increment 1, odd increment 1, standard increment 2;
- no affine batching or production route selection may be called.

The direct C oracle is the definition-level independence anchor for V1. A C trace may pass through a state that is not a shortcut-map boundary; scientific checkpoints therefore remain T-boundary states. Comparison code must compare C and T only after the corresponding one-or-two C applications have reached the same T boundary.

### 2.3 OddOnlyOracle / terminal candidate

For odd n, compute v = v2(3n+1) exactly and return (3n+1)/2^v with increments:
shortcut += v, odd += 1, standard += v+1.

This path is eligible as an independent direct family and terminal-handoff candidate. It must retain v exactly. Counting one U application as one shortcut step is prohibited.

### 2.4 AffineBlock

An affine block is the exact tuple (k, i, A, B), where k >= 0, 0 <= i <= k, A = 3^i, and for the residue class selecting the block:

2^k T^k(n) = A*n + B.

Required operations:

- construct a base block directly from elementary T on a bounded residue;
- reconstruct/check a block from its parity word where that representation is used;
- compose two blocks;
- apply a block to an exact integer;
- expose k and i to exact counter accounting;
- expose deterministic route instrumentation.

A block apply must assert exact divisibility of A*n+B by 2^k when the divisibility canary is enabled. The canary is a defect detector, not a proof or independent oracle.

### 2.5 SmallBlockTable

A finite table may contain only blocks generated from the exact T definition. Every enabled entry must be exhaustively regenerated and compared with direct T in V1. Table width is a C1 measurement; I1 freezes only the CEML-CAL-1 sweep and the maximum authorized calibration width.

### 2.6 HierarchicalAffine

Hierarchical/binary-split batching must support every positive k, including odd k.

For k=k1+k2, use k1=floor(k/2), k2=k-k1. The right block is computed from the exact post-left residue, not from unadvanced original bits. If P1 is followed by P2, composition is P2 after P1:

A = A2*A1
B = A2*B1 + B2*2^k1
k = k1+k2
i = i1+i2.

Composition order is non-commutative and may never be reversed for convenience.

Explicit-coefficient and value-threaded recursion are eligible C1 candidates, but value-threading is not an independent mathematical oracle because it shares the same parity/split recurrence.

### 2.7 TerminalSafety

Let b = bit_length(n). For a nonterminal state n>1, a macro block is definition-level terminal-safe when 1 <= k <= b-1. Reaching 1 requires at least b-1 shortcut steps because one T step can reduce bit length by at most one. Thus such a block cannot pass an earlier first 1; it may end exactly at 1.

Every production scheduler must therefore do one of the following:

- clamp the requested macro length to at most b-1; or
- hand off to exact direct/odd-only stepping before an otherwise overlong block.

After every accepted block/elementary transition, current_n==1 immediately sets terminal_reached and execution stops. A route that applies T to 1, or crosses first 1 and later returns to 1/2/4, is invalid.

### 2.8 ExactCounters

Counter updates are centralized. Optimized kernels return represented shortcut length k and exact odd count i; they do not mutate counters privately.

Postcondition for any accepted transition:
new_shortcut = old_shortcut + k
new_odd = old_odd + i
new_standard = old_standard + k + i
new_standard = new_shortcut + new_odd.

Counters use arbitrary precision. Fixed-width counter overflow is not an eligible implementation strategy.

### 2.9 RouteRegistry

Every optimized route has a stable route ID, a support predicate, a request/force mode and an activation counter. Required IDs are listed in Section 6.

Request modes:
- AUTO: implementation may choose among profile-authorized routes;
- REQUIRE(route_id): route must execute at least once or the operation refuses;
- FORBID(route_id): route must not execute;
- TRACE: emit deterministic route evidence in addition to counters.

Fallback from REQUIRE is prohibited. A benchmark with requested_count>0 and activated_count=0, or fallback_count>0, is invalid evidence for that route.

### 2.10 CanonicalCodec

One module owns:
- UENC/MAG integer encoding and rejection of non-minimal forms;
- SHA3-256 digests and SHAKE256 generation;
- RFC 8785 JCS canonicalization;
- frozen CEML-SCI-1 domain labels;
- I1 engineering-only digest labels from Section 12;
- manifest/checkpoint/result/validation-evidence schema validation.

Scientific-domain functions are immutable adapters to R3 rules. Engineering digest functions are separate so I1 does not modify any scientific digest preimage.

### 2.11 CheckpointCodec and CheckpointStore

CheckpointCodec owns exact CEML-CKPT-1 state.bin and metadata.json encoding/validation. CheckpointStore owns A/B (or equivalent two-valid-generation) storage, durable flush, re-read/verify, promotion, directory/pointer durability and recovery. Filesystem operations go through a platform adapter so C1 can prove actual target semantics.

### 2.12 AuditCollector, CalibrationRunner, BuildProfiler, ValidationRunner

AuditCollector emits only C1 evidence records defined in Section 5 and schemas/c1_evidence.schema.json.
CalibrationRunner executes only CEML-CAL-1 bounded engineering cases.
BuildProfiler creates the build manifest and config/local_machine_profile.json after decisions are frozen.
ValidationRunner exposes every CEML-V1-SUITE-1 hook but C1 must not execute/claim V1 unless the programme is explicitly advanced to V1.

## 3. Code-level invariants and mandatory assertions

The following are implementation obligations, not prose guidance.

| Invariant | Preconditions | Required postcondition/assertion | Required test |
|---|---|---|---|
| Standard C | n>=1 | exact C definition | elementary identities |
| Shortcut T | n>=1 | exact T definition and increments | elementary + C/T bridge |
| Terminal | scientific state n>=1 | no transition if n==1 | start-1 and overshoot fixtures |
| Count identity | accepted T-boundary state | standard=shortcut+odd | every transition/checkpoint/result |
| Odd-only | odd n>1 | exact v2 and (v,1,v+1) increments | valuation/adversarial |
| Affine identity | valid block for n mod 2^k | 2^k*T^k(n)=3^i*n+B | direct differential |
| Low-bit sufficiency | k>=0 | selector consumes exactly n mod 2^k | exhaustive/adversarial low bits |
| Composition | consecutive P1,P2 | composed=P2(P1(n)) | order-sensitive + three-way |
| Odd split | k>1 | floor/ceil halves sum exactly to k | all 2m+1 fixture widths |
| Divisibility canary | valid selected block | (A*n+B) mod 2^k = 0 | fault injection proves detection |
| First-1 safety | n>1 | macro k<=bit_length(n)-1 or direct handoff | terminal/overshoot |
| Exact arithmetic | all candidate-affecting values | no truncation/overflow/float conversion | checked/sanitized + boundary |
| Canonical serialization | supported artifact | byte-for-byte canonical decode/encode | independent round trips |
| Restart | accepted checkpoint | resumed deterministic state/result equals uninterrupted | fresh-process restart |
| Route activation | REQUIRE route | activated_count>0 and fallback_count=0 | calibration + V1 feature route |

Floating point may be used only for timing/engineering statistics. It may not alter a start, state, counter, route correctness decision, checkpoint, result or scientific acceptance decision.

## 4. Candidate register

C1 benchmarks only candidates marked ELIGIBLE or OPTIONAL below and only when local support exists.

### 4.1 Eligible algorithm/state candidates

- ELIGIBLE: direct exact T stepping as reference/tail and bounded baseline.
- ELIGIBLE: direct exact C stepping as definition oracle, not giant production hot loop.
- ELIGIBLE: odd-only exact valuation stepping as secondary oracle/terminal candidate.
- ELIGIBLE: small affine/table blocks generated from the definition.
- ELIGIBLE: hierarchical/binary-split affine batching with explicit coefficients.
- OPTIONAL: value-threaded hierarchical form, provided it exposes the same exact counters and activation evidence.
- ELIGIBLE: dense arbitrary-precision representation using documented public library APIs.
- OPTIONAL: sparse/chunked or analogous representation only if canonical low-bit extraction/export and direct differential tests are implemented.
- ELIGIBLE: allocation-copy baseline.
- OPTIONAL: reuse/in-place strategy where aliasing rules are documented and checked.
- ELIGIBLE: single-thread route.
- OPTIONAL: auxiliary parallelism only for deterministic pure arithmetic/block construction or other profile-authorized work; scientific state commits remain serialized and deterministic.

### 4.2 Eligible language/backend families

C1 may use an installed supported toolchain to build bounded candidate harnesses for:
- C17 + documented public GMP mpz API;
- C++20 + documented public GMP interfaces;
- Rust stable + rug/GMP using documented safe/public interfaces.

C1 need not benchmark all three when a toolchain/dependency is unavailable. Language selection must consider correctness surface, offline reproducibility, dependency burden and maintainability as well as measured kernel performance.

OPTIONAL FLINT is eligible only through documented public FLINT APIs with explicit conversion/ownership rules and exact differential testing. The C1 decision log must identify the public API used.

### 4.3 Rejected in I1

C1 must not benchmark or select these without a new reviewed I1 amendment:

- private GMP structure-field access as a correctness or serialization dependency, including direct reliance on _mp_d/_mp_size;
- historical/unpublished/internal mpz_mullo-style APIs;
- private FLINT symbols such as _flint_mpn_mul;
- raw host/GMP/FLINT limb dumps as checkpoint or canonical artifact formats;
- an unmodified external repository as the CEML production baseline;
- a new custom giant-integer limb engine;
- a pure fixed-width giant-state core;
- Python bigint as the scientific giant production core (retained as reference/orchestration only);
- Ren-style file/bit engine as the presumptive production core (retained as an independent-lineage reference option);
- contiguous-verification architecture as the CEML core;
- handwritten architecture-specific assembly as the C1 baseline;
- any backend/feature route that cannot be forced and proved active;
- any scientific parameter or start selected from calibration behaviour.

Compiler-generated native instructions are not rejected; they are handled by the native-build provenance rule.

## 5. C1 evidence records and artifact paths

schemas/c1_evidence.schema.json is normative for the engineering evidence envelopes. schemas/hardware_profile.schema.json is normative for the final profile.

### 5.1 Evidence classes

OBSERVED_FACT requires:
- record_id;
- category and fact_name;
- sanitized value;
- source adapter/method;
- audit_run_id or collection time;
- source_state_kind: static_capability, active_configuration or momentary_state;
- uncertainty/availability note;
- sanitization actions.

CALIBRATION_MEASUREMENT requires:
- record_id, suite/case/input identifiers;
- build identity;
- requested/activated route evidence;
- timing/memory/resource methodology and repeats;
- exact correctness/reference digests and agreement;
- invalid/abort fields;
- artifact/bundle linkage.

ENGINEERING_DECISION requires:
- decision_id and question;
- candidates considered;
- evidence record IDs;
- eliminated candidates and constraints;
- selected choice or explicit refusal;
- deterministic decision rule/rationale;
- limitations and profile binding flag.

UNAVAILABLE_OR_UNSUPPORTED requires:
- record_id;
- requested fact/facility/candidate;
- safe attempted method if any;
- reason;
- downstream blocked/constrained decisions.

### 5.2 Paths

Required committed sanitized C1 artifacts:
- local_reports/HARDWARE_REPORT.json
- local_reports/HARDWARE_REPORT.md
- local_reports/BENCHMARK_SUMMARY.json
- local_reports/ENGINEERING_DECISIONS.json
- local_reports/BENCHMARK_BUNDLES.json
- local_reports/BUILD_MANIFEST.json
- config/local_machine_profile.json
- package-manager/native build lock files selected by C1
- dependency pin/digest manifest selected under Section 9.

Raw per-repeat records default to:
local/c1/benchmark_records/<case_id>/<repeat_id>.json

Decision-relevant raw records are bundled under:
local/c1/benchmark_bundles/<bundle_id>/

The committed BENCHMARK_BUNDLES.json stores the logical bundle ID, member ordering, engineering bundle digest and retention status. Raw bundles remain local by default. A small sanitized subset may be committed under local_reports/benchmark_records/ only if the sensitive-data scan passes.

HARDWARE_REPORT.md must be deterministically generated from or mechanically reconciled against HARDWARE_REPORT.json. It may add explanations, never new observed facts.

## 6. Route IDs and activation proof

Stable route IDs:

- oracle.c.direct
- oracle.t.direct
- oracle.u.odd_only
- engine.direct_t
- engine.small_affine
- engine.hier_affine.explicit
- engine.hier_affine.value_threaded
- state.dense
- state.sparse
- arith.gmp.public
- arith.flint.public
- alloc.copy
- alloc.reuse
- parallel.single
- parallel.aux
- terminal.direct_t
- terminal.odd_only
- audit.divisibility
- audit.modular
- checkpoint.buffered
- checkpoint.streaming

An implementation may add versioned route IDs, but may not reuse an ID for materially different semantics.

Route evidence contains case_id, build_digest or provisional build ID, requested route IDs, per-route invocation counts, fallback/refusal counts and a digest of the deterministic trace/counter record. REQUIRE must fail closed if the route cannot activate.

Compiler modes are build identities rather than runtime route IDs.

## 7. Hardware-audit adapters

C1 must use narrow, field-selective probes. The adapters below are allowed examples/requirements; exact invocation spelling may vary by OS release, but emitted normalized facts must use the schema and may contain only authorized fields.

### 7.1 Linux adapter

Permitted narrow sources include:
- /etc/os-release selected NAME/VERSION_ID fields;
- uname selected kernel/architecture fields;
- lscpu selected architecture/vendor/model/core/thread/cache/NUMA/flags fields;
- /proc/meminfo selected MemTotal/MemAvailable/SwapTotal/SwapFree/PageSize-relevant fields;
- findmnt/statfs/df against the semantic checkpoint target for filesystem type/options/capacity/free bytes;
- compiler/linker/package-manager --version outputs for candidate tools only;
- pkg-config or direct library version APIs for GMP/FLINT where installed;
- selected userspace thermal/frequency files or APIs after filtering to numeric state and non-identifying labels;
- runtime CPUID/feature helper emitted by the C1 harness.

Do not persist /proc inventories, mount tables, environment dumps or device serial/UUID sources.

### 7.2 macOS adapter

Permitted narrow sources include:
- sw_vers selected product/version/build fields;
- uname selected kernel/architecture fields;
- sysctl selected hw.physicalcpu, hw.logicalcpu, hw.memsize, cache and supported feature fields;
- vm_stat and selected swap state;
- statfs/df against the semantic checkpoint target;
- candidate tool/library version commands;
- non-invasive thermal/power status only when available without collecting identifiers.

Do not persist system_profiler broad inventories.

### 7.3 Windows adapter

Use PowerShell/CIM with explicit property selection only:
- Win32_OperatingSystem: Caption, Version, BuildNumber, OSArchitecture, selected memory fields;
- Win32_Processor: Manufacturer, Name, NumberOfCores, NumberOfLogicalProcessors, MaxClockSpeed;
- target-volume query: FileSystemType, DriveType, Size, SizeRemaining and required durability capability facts, excluding UniqueId/serial/device identifiers;
- candidate compiler/linker/runtime/library version commands;
- a C1 CPUID/feature helper for instruction features when needed.

Do not persist Get-ComputerInfo, full CIM dumps, environment dumps, network inventories or storage serial/UniqueId fields.

### 7.4 Observation normalization

Hardware-report values must identify units explicitly. Momentary free memory/frequency/thermal values are momentary_state. Vendor/model text may be retained only when returned by a permitted local source and after scanning. Unknown/ambiguous fields become UNAVAILABLE_OR_UNSUPPORTED; internet product specifications never fill local gaps.

## 8. Privacy and deterministic sensitive-data gate

Collection must filter before persistence wherever practical. Unavoidable raw output is local-restricted, immediately sanitized and deleted after the minimized record is checked.

Before any C1 report/profile commit, scan exactly the staged C1 artifact set plus generated Markdown. The scan is deterministic and fails closed on:

- schema/object keys or labels matching hostname, computer_name, device_name, username, user, home, account_id, serial, serial_number, uuid, unique_id, mac, ip_address, ssid, wifi, token, secret, password, cookie, private_key unless the schema explicitly defines a non-sensitive semantic field with no captured value;
- Unix user-home paths matching /home/<component>/ or /Users/<component>/;
- Windows user-home paths matching drive-letter:\Users\<component>\;
- MAC-address forms;
- IPv4/IPv6 literals in hardware/profile/evidence fields;
- UUID-form strings;
- email-address forms;
- PEM private-key markers;
- common credential/token markers including GitHub-token prefixes and access-key patterns;
- environment-dump markers such as HOME=, USERNAME= or USERPROFILE=;
- broad raw inventory headings known to the platform adapters.

The scanner also validates all JSON against the I1 schemas and rejects absolute local paths except explicitly normalized semantic placeholders. Hashing a prohibited identifier is not a remediation. Any allowlist change is a reviewed repository change; C1 may not invent an ad hoc bypass.

The staged diff must be reviewed after the scan. A match blocks commit until the source artifact is regenerated/sanitized.

## 9. Offline-capable dependency/build strategy

C1 uses a two-layer lock:

1. the ecosystem-native lock/pin mechanism for the selected toolchain (for example Cargo.lock where applicable, or exact C/C++ dependency source/package identities);
2. a committed CEML dependency manifest referenced by BUILD_MANIFEST.json containing component name, exact version, source/distribution channel, source/package digest when available, build options, link mode/ABI, enabled features, wrapper/binding version, and license/provenance note.

Required source/package artifacts are either vendored in repository-controlled content or placed in an approved content-addressed local cache whose digest/index is committed. Mutable "latest" dependencies are prohibited.

C1 may not silently fetch/install/upgrade anything. If an eligible dependency is absent, record UNAVAILABLE_OR_UNSUPPORTED and either choose another eligible path or stop for explicit operator authorization. Any authorized dependency/toolchain change invalidates affected observations/calibration and requires rerun.

The selected build must support an offline rebuild command that fails if network access would be needed. Scientific execution, checkpoint resume and artifact verification must never fetch code/dependencies from the network.

## 10. CEML-CAL-1 deterministic bounded calibration

config/calibration_suite_v1.json is normative and contains no machine measurements.

### 10.1 Public seed and generator

Public seed32:
000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f

Random domain prefix:
CEML-CALIBRATION-RANDOM-V1 followed by one NUL byte.

Define BLOB(x)=U64BE(len(x))||x for arbitrary byte strings.

For a generated integer stream:
msg = domain || seed32 || BLOB(UTF8(case_family)) || UENC(size_bits) || UENC(case_index) || UENC(stream_index).

Request q=ceil(size_bits/8) SHAKE256 bytes, interpret big-endian, mask unused top bits, set bit size_bits-1 so the value has exactly size_bits bits. For state inputs set bit 0 as well so the generated state is odd. Distinct stream_index values generate additional operands.

Formula-defined terminal/adversarial cases do not consume this generator and must encode their formula in the case descriptor.

### 10.2 Case/input IDs and digests

Input ID is candidate-independent:
cal1/<two-digit-family-order>/<family>/<size_bits>/<case_index>

Case ID adds the candidate:
<input_id>/<candidate_id>

All components are ASCII and candidate_id is a stable route/build-candidate identifier. Competing candidates for one comparison must therefore share the same input_id and input_digest.

For generated cases the input descriptor has exactly these members, with decimal quantities represented as canonical decimal strings:

```json
{
  "case_index": "<decimal>",
  "family": "<family>",
  "generator": "shake256-ceml-calibration-random-v1",
  "input_id": "<input_id>",
  "operand_roles": [
    {
      "forced_odd": true,
      "role": "<role>",
      "size_bits": "<decimal>",
      "stream_index": "<decimal>"
    }
  ],
  "size_bits": "<decimal>",
  "suite_version": "CEML-CAL-1"
}
```

The operand_roles array order is the operand order used in the digest preimage. forced_odd is true only for state operands; non-state generated operands use false. Formula-defined cases instead set generator to "formula-v1" and each operand-role object contains exactly role and formula; the actual formula-defined integer bytes are still included in the digest preimage. The descriptor never contains candidate_id or build identity.

input_digest =
SHA3-256(ASCII("CEML-I1-CALIBRATION-INPUT-V1") || 00 ||
BLOB(JCS(input_descriptor)) ||
BLOB(UENC(operand_0)) || ... || BLOB(UENC(operand_m))).

For an exact T-boundary state:
state_digest =
SHA3-256(ASCII("CEML-I1-CALIBRATION-STATE-V1") || 00 ||
UENC(n) || UENC(shortcut_steps) || UENC(odd_steps) || UENC(standard_steps)).

Benchmark correctness requires the candidate state_digest to equal the independently computed reference state_digest.

Normative generated-input vector:

- family = route-crossover
- size_bits = 256
- case_index = 0
- stream_index = 0
- input_id = cal1/01/route-crossover/256/0
- SHAKE output before forced bits = `c32fdab88656f59d41b5e77e8c34ac9fb77fe883438b85499979c2f596fabc0c`
- resulting odd 256-bit state hex = `c32fdab88656f59d41b5e77e8c34ac9fb77fe883438b85499979c2f596fabc0d`
- exact JCS descriptor = `{"case_index":"0","family":"route-crossover","generator":"shake256-ceml-calibration-random-v1","input_id":"cal1/01/route-crossover/256/0","operand_roles":[{"forced_odd":true,"role":"state","size_bits":"256","stream_index":"0"}],"size_bits":"256","suite_version":"CEML-CAL-1"}`
- input_digest = `84b55262e1b0543c0201479122d92f19cf8ab38550db60a3075c5564b3b7fc0a`
- initial state_digest with all counters zero = `95eef319edc55bd8a1aa5f9f210fea3f3b9bae480913f7ae1af9bc59332e6271`

C1 must reproduce this vector before accepting any CEML-CAL-1 measurement.

### 10.3 Deterministic ordering and classes

Family order is:

01 route-crossover
02 small-block-sweep
03 hierarchical-sweep
04 backend-multiplication
05 representation
06 allocation
07 compiler-build
08 parallelism
09 checkpoint
10 terminal-handoff
11 audit-cost
12 memory-scaling

Within a family: size ascending, candidate_id ASCII lexicographic, case_index ascending, repeat_index ascending.

CEML-CAL-1 generated integer sizes are:
256, 1024, 4096, 16384, 65536 and 131072 bits.

Case indices are 0,1,2 unless a formula-defined matrix states otherwise.

These inputs are engineering-only and at most 131072 bits, about 39.5 thousand decimal digits, more than an order of magnitude below the smallest provisional one-million-decimal-digit scientific rung. They are not scientific starts and may not be promoted into the ladder.

### 10.4 Global suite work bounds

I1 authorizes at most:
- 131072 generated integer bits per operand;
- 4096 represented shortcut steps in any fixed-step arithmetic case;
- 16384 shortcut steps in one affine macro construction;
- small-table width 16;
- 1 warm-up plus 5 measured repetitions per timing case;
- 1 warm-up plus 3 measured repetitions per filesystem durability/performance case;
- 2 concurrent benchmark processes;
- 16 auxiliary threads in any calibration process;
- 32 KiB canonical state magnitude in checkpoint performance cases;
- 512 MiB temporary/scratch allocation per case;
- 120 seconds wall time per case;
- 5400 seconds aggregate measured suite wall time.

C1 must impose stricter local ceilings when observed headroom requires it. C1 may reduce/abort cases but may not increase any I1 suite maximum without a reviewed I1 version change.

### 10.5 Warm-up, repetitions and variability

Warm-ups are recorded but excluded from performance statistics.
Measured timing repeats are never silently discarded. An environmentally invalid repeat is retained with invalid=true and a reason.

Required summary values use integer nanoseconds/bytes where possible:
- count valid/invalid;
- median;
- minimum;
- maximum;
- median absolute deviation (MAD).

No floating-point statistic decides correctness. Ratios used for engineering comparison may be computed from exact integer measurements with documented rounding.

### 10.6 Abort/invalid semantics

Preflight failure: case does not start; record C1_PREFLIGHT_REFUSAL.
Mid-case safety trigger: terminate cleanly if possible; record C1_RESOURCE_ABORT.
Wrong correctness digest: C1_CORRECTNESS_INVALID.
Requested route not activated or fallback occurred: C1_ROUTE_INVALID.
Timer/resource observation failure needed by a decision: C1_MEASUREMENT_INVALID.
External disturbance: C1_ENVIRONMENT_INVALID.

These are engineering events. They do not create schemas/result.schema.json records.

## 11. Calibration matrix and decision sufficiency

Every applicable row is run on the same sanitized machine/build context unless the row intentionally compares builds.

### 11.1 Route crossover

Sizes: 1024,4096,16384,65536,131072 bits; three generated states; fixed budget <=2048 T steps.

Compare direct T, each eligible small-block candidate and each eligible hierarchical candidate. All outputs must match the direct reference digest. Record wall/CPU time, peak RSS and route activation.

### 11.2 Small-block sweep

Widths: 4,8,12,16, subject to local safety preflight and exhaustive table correctness. Test at 4096,16384,65536 bits. Width is not selected unless the table route activates and every entry of the chosen table later has a V1 hook.

### 11.3 Hierarchical sweep

Eligible scheduler family:
k = max(1, min(k_cap, floor(bit_length(n)/d)))
with d in {2,3,4,6,8} and k_cap in {1024,4096,16384}; terminal safety further clamps k<=bit_length(n)-1.

Use 16384,65536,131072-bit states. C1 selects no unmeasured interpolation point; a schedule outside this family needs a reviewed C1/I1 amendment and new evidence.

### 11.4 Backend/multiplication crossover

For each available public backend route, benchmark deterministic exact products with operand bit-shapes representative of affine apply/composition: approximately equal, 2:1 and 4:1 bit-length ratios, bounded by 131072 bits per operand. Verify the exact product digest against the definition/reference backend. Private/internal APIs are ineligible.

### 11.5 Dense/sparse representation

Use generated dense states plus formula-defined sparse patterns with high/low populated regions and long zero gaps at 4096,16384,65536,131072 bits. Compare canonical UENC export, low-bit extraction and fixed-step final state. Sparse wins only if its larger invariant surface is justified by valid performance/memory evidence.

### 11.6 Allocation strategy

Run copy baseline and any safe reuse/in-place candidate on identical 16384,65536,131072-bit cases. Record wall time, peak RSS, allocator/live bytes when available and aliasing/checker evidence.

### 11.7 Compiler/build modes

I1 permits these semantic modes:
- checked: assertions plus applicable sanitizers/checkers; not a production-speed candidate;
- portable-release: optimized, no host-specific CPU tuning;
- native-release: optimized with the toolchain's documented native target mechanism, only if supported and recorded.

C1 records exact flags; I1 selects none. A native-release winner is marked non-portable and requires its own build/profile/V1 identity.

### 11.8 Parallelism

If an eligible auxiliary-parallel route exists, compare thread counts 1,2,4,8,16 clipped to observed logical CPUs and the stricter local ceiling. Results must be bit-identical. Threading that changes state-order semantics is ineligible.

### 11.9 Checkpoint

On the intended checkpoint filesystem, use valid synthetic CEML-CKPT-1 states with magnitude byte sizes 1 KiB,4 KiB,16 KiB,32 KiB. Compare eligible buffered/streamed serialization implementations only after each satisfies exact bytes and the durability sequence. Run the complete interruption matrix in Section 10 of docs/HARDWARE_AUDIT_SPEC.md before any performance winner is selected.

### 11.10 Terminal handoff

Use formula-defined n in {2^m,2^m-1,2^m+1} for m in {8,64,256,1024,4096}, omitting duplicates/non-positive/irrelevant parity cases. Compare safe macro clamp plus direct T and, where applicable, odd-only terminal handoff. First-1 state/counters must match the direct definition oracle.

### 11.11 Audit/canary cost

Compare production-eligible invariant modes:
- mandatory structural checks: counter/terminal/provenance consistency;
- divisibility canary;
- divisibility plus optional modular audit.

A mode may be disabled for production performance only if V1 has an independent route to force/verify the optimized path and the final profile records the choice.

### 11.12 Memory scaling

Across all six size classes, capture peak RSS plus available allocator/live/transient metrics for candidate routes. Account for simultaneous old/new n, affine A/B, recursion scratch, serialization buffers and both checkpoint slots. No scientific resource forecast may be presented as measured beyond the bounded domain.

### 11.13 General decision rule

A candidate is eligible for selection only if:
- exact correctness/reference digest agrees for every decision-critical case;
- requested optimized route has positive activation and zero silent fallback;
- all required observations for the decision are valid;
- no local safety rule was violated;
- build/dependency provenance is complete.

For a timing-based winner, require at least three representative size classes and at least five valid measured repeats per class. Treat two candidates as performance-tied unless the preferred candidate's median is at least 5% better on at least two of the largest three applicable classes and it has no decision-critical class more than 5% worse. A result with MAD greater than 10% of its median on a decision-critical class is noisy; rerun only within suite bounds after resolving an identified disturbance, otherwise refuse a performance winner.

For memory/storage decisions, the primary correctness/durability constraint dominates speed. A candidate causing materially lower peak resource use may be selected when performance is tied if the decision log states that objective.

When performance is tied, C1 may choose, in order:
1. documented public API over private/fragile API;
2. smaller correctness/unsafe/FFI surface;
3. fewer dependencies and simpler offline rebuild;
4. lower peak memory/storage;
5. portable over native-specific;
6. single-thread over auxiliary parallelism.

If evidence does not satisfy these rules, record no justified winner/refusal. Never extrapolate an unmeasured crossover into a selected machine-specific threshold as though it were observed.

## 12. Engineering digest domains, build identity and profile identity

These labels are engineering-only. They do not alter CEML-SCI-1 domains.

BLOB(x)=U64BE(len(x))||x.

Generic engineering artifact digest (for C1 evidence artifacts that define artifact_digest):
SHA3-256("CEML-I1-ENGINEERING-ARTIFACT-V1" || 00 ||
BLOB(ASCII(schema_version)) || BLOB(JCS(object with its top-level artifact_digest omitted))).

BUILD_MANIFEST.json and config/local_machine_profile.json use their dedicated build_digest and machine_profile_digest rules below rather than also carrying the generic artifact_digest; this avoids circular self-digest definitions.

Benchmark bundle digest:
SHA3-256("CEML-I1-BENCHMARK-BUNDLE-V1" || 00 ||
for each member in lexicographic logical-path order: BLOB(UTF8(logical_path)) || BLOB(raw_file_bytes)).

BUILD_MANIFEST.json is JCS-compatible and contains source/engine commit, target triple/ABI, compiler/linker/tool versions, exact relevant flags, native-target request/features, dependency versions/digests/build options/linkage, enabled routes/features, package/native lock identities and ordered executable/library artifact byte digests. Each build-artifact sha3_256 field is SHA3-256 of that artifact's raw bytes, rendered as lowercase hex.

build_digest =
SHA3-256("CEML-I1-BUILD-V1" || 00 || BLOB(JCS(build manifest with build_digest omitted))).

config/local_machine_profile.json contains only sanitized capability classes and all frozen engineering choices affecting executable behavior, resource ceilings, checkpoint strategy, decision/evidence links, build_digest, non-portability markers and unavailable constraints.

machine_profile_digest =
SHA3-256("CEML-I1-MACHINE-PROFILE-V1" || 00 || BLOB(JCS(profile with machine_profile_digest omitted))).

Source identity is the Git engine/source commit. Build identity is build_digest. Machine/profile identity is machine_profile_digest. None may substitute for another.

A rebuild on another machine, a dependency/toolchain/flag/feature change, or a native-target change creates a new build/profile event. V1 evidence does not transfer silently.

## 13. Checkpoint implementation mapping

state.bin encoder/decoder is exactly docs/CHECKPOINT_SPEC.md; no host-limb format is permitted.

CheckpointStore contract:

1. choose non-current slot;
2. serialize exact candidate state.bin and metadata.json;
3. durable-flush each required file through FilesystemAdapter;
4. close/reopen/re-read both;
5. validate canonical bytes, schema, all digests, provenance, counters and terminal state;
6. atomically publish slot/pointer through an adapter operation proven on the target filesystem;
7. perform directory/pointer durability operation required by the adapter;
8. re-read the published generation;
9. retain the immediately previous validated slot until the new generation is confirmed durable;
10. only then retire older generations according to policy.

FilesystemAdapter must expose:
- write_exact;
- flush_file_data_and_metadata as required by platform;
- close/reopen;
- atomic_promote;
- durable_directory_or_equivalent;
- enumerate_candidate_slots without trusting latest;
- fault-injection boundaries;
- capability/evidence descriptor.

Recovery validates both slots independently, follows digest/provenance/sequence rules, selects the unique newest valid chain member, and refuses ambiguity. It never repairs a scientific checkpoint in place.

C1 must test the actual intended filesystem/mount class. If durable promotion cannot be justified from documented semantics plus bounded process-interruption tests, the filesystem is unsupported.

Fresh-process restart is mandatory: terminate all process state, launch a new process, decode the checkpoint, rebuild derived caches, and continue. Serialization benchmarks account for old state + new body + metadata + temporary buffers + retained previous slot.

## 14. Resource-safety machinery

C1 creates measured local ceilings before non-trivial calibration. The profile must bind:
- minimum free/available memory headroom;
- maximum permitted benchmark/process memory or fraction rule;
- minimum checkpoint/scratch free-storage headroom;
- maximum tolerated swap/pagefile activity or an explicit unavailable measurement;
- maximum benchmark processes and threads;
- thermal/throttling stop condition where observable;
- per-case and aggregate work/time ceilings no greater than CEML-CAL-1;
- power/sleep precondition.

Preflight checks run before each case. Mid-case checks run at deterministic safe polling boundaries that do not alter arithmetic. On a safety threshold, abort and record an engineering event; do not increase limits. Cleanup removes reproducible temporary inputs/scratch while retaining the required digest/index evidence.

C1 must not disable swap, change BIOS/firmware, change global thermal policy or silently alter power/sleep configuration.

## 15. Required command semantic surface

Exact CLI spelling is frozen as the following logical subcommands; implementation may use a single executable or equivalent scripts, but behavior must match.

ceml hardware-report
- C1 only; collect authorized minimized facts, emit schema-valid report, run privacy scan.
- never runs trajectory calibration automatically.

ceml calibrate
- requires C1 authorization, hardware report, local safety ceilings and CEML-CAL-1.
- refuses any scientific seed/start input.
- emits raw records, summary and route evidence only.

ceml decide
- consumes valid observations/calibration and emits engineering decision log.
- cannot invent missing evidence.

ceml build-profile
- after decisions, build selected engine offline/pinned; emit BUILD_MANIFEST and local_machine_profile; rerun invalidated calibration if required.
- does not run V1.

ceml self-test
- bounded developer/I1 invariant tests and frozen vectors; not V1-PASS.

ceml validate
- disabled/refuses unless PROGRAM_STATUS authorizes V1.
- when authorized later, runs CEML-V1-SUITE-1 and emits validation evidence.

ceml prepare
- disabled/refuses unless final ladder, authorized seed lifecycle, exact build/profile and V1-PASS prerequisites exist under E1 authorization.
- verifies/regenerates manifest/start; it does not choose/reroll a start.

ceml run
- disabled/refuses unless a schema-valid E1 manifest binds exact protocol/build/profile/V1 evidence and start regeneration succeeds.

ceml status
- reports stage, run/checkpoint/artifact validity without changing state.

ceml checkpoint
- writes/promotes a checkpoint only at an exact T-boundary state through the validated filesystem adapter.

ceml resume
- validates/recover-selects a checkpoint and resumes only when stage/provenance permits.

ceml verify
- verifies canonical encodings, schemas, digests and cross-artifact provenance without modifying scientific state.

C1 completion must leave validate/prepare/run scientifically gated.

## 16. Error and scientific-status mapping

Audit/calibration errors are C1 engineering events and do not emit scientific results.

When a scientific run is later authorized:
- exact first 1 with all invariants/provenance valid -> completed;
- invariant/oracle/V1 acceptance failure discovered during active scientific execution -> validation_failure;
- memory/storage/time-policy/thermal/power safety stop -> resource_stop;
- malformed/corrupt digest/canonical/checkpoint artifact -> integrity_failure;
- deterministic seed/start regeneration mismatch -> reproducibility_failure;
- protocol/engine/build/profile/V1 identity mismatch -> provenance_failure;
- deliberate operator stop not otherwise classified -> operator_abort;
- unexpected process termination when the run is closed rather than resumed -> unexpected_termination;
- exact behavior requiring counterexample/anomaly certification -> frozen_anomaly.

No failure or long runtime implies divergence.

## 17. V1 implementation hooks

ValidationRunner must expose one callable/test target for each CEML-V1-SUITE-1 class:

1. elementary_identities -> direct C/T/U definition tests and counter bridge;
2. exhaustive_small_residues -> regenerate every enabled small-table entry;
3. randomized_bounded_differential -> CEML-VALIDATION-RANDOM-V1 generated n/k against direct oracle;
4. adversarial_patterns -> limb boundaries, powers, sparse/zero/alternating/carry patterns;
5. odd_split_lengths -> force 2m+1 recursive splits and order-sensitive composition;
6. terminal_overshoot -> powers/near-terminal and forced overlong-request decomposition;
7. serialization_digest_roundtrip -> UENC/JCS/domain vectors across independent implementations where practical;
8. checkpoint_restart_equivalence -> fresh-process interruption/resume at multiple exact boundaries;
9. fault_injection -> parity/A/B/carry/low-bit/serialized bytes/counters/product/digests/provenance corruption;
10. feature_route_activation -> REQUIRE every enabled optimized route and independently compare output;
11. formula_defined_fixtures -> 27, 2^127-1, 2^44497-1 exact frozen triples;
12. checked_sanitized_builds -> applicable overflow/UB/memory/FFI checker suites or explicit non-applicability evidence.

The direct elementary oracle remains the independence anchor. Calibration records cannot be promoted into V1 evidence.

## 18. C1 authorization, refusal and completion

C1 must refuse to:
- guess a missing machine fact;
- silently install/upgrade/replace a dependency;
- use a private/unsupported backend route;
- select unmeasured tuning;
- accept a benchmark without correctness agreement;
- accept a requested route without activation proof;
- use checkpoint storage without required durability evidence;
- exceed CEML-CAL-1 or stricter local safety limits;
- use/read/request the scientific master seed or a scientific start;
- freeze final ladder values;
- enter/claim V1 or E1.

C1 is complete only when all of these exist in one reviewed repository state:
- sanitized HARDWARE_REPORT.json and matching HARDWARE_REPORT.md;
- BENCHMARK_SUMMARY.json covering every decision-relevant applicable matrix row or explicit refusal/unavailable record;
- ENGINEERING_DECISIONS.json with no untraced selected choice;
- BENCHMARK_BUNDLES.json digest/index for retained local-only evidence;
- BUILD_MANIFEST.json with build_digest;
- config/local_machine_profile.json with machine_profile_digest;
- exact dependency/toolchain lock/pin records needed for offline rebuild;
- source/engine commit and built artifact byte digests;
- proof that the intended checkpoint filesystem satisfied the bounded CEML-CKPT-1 durability matrix;
- sensitive-data scan PASS on the committed C1 artifact set;
- production engine implementation/build produced only after the audit/calibration decisions;
- PROGRAM_STATUS still denying scientific seed/scientific execution and showing V1 not yet passed.

If a required hardware-dependent decision has no justified winner, C1 records refusal and remains open unless an I1-supported portable fallback is explicitly eligible and selected by the tie-break rule with complete evidence.

## 19. I1 decisions and deliberate deferrals

### Frozen by I1

- component and independence boundaries above;
- exact code-level mathematical invariants;
- first-1 macro safety rule k<=bit_length(n)-1 or exact handoff;
- public-API baseline and explicit rejection of private GMP/FLINT routes;
- route registry/REQUIRE activation semantics;
- C1 artifact paths and schemas;
- CEML-CAL-1 generator, ordering, case matrix and global work bounds;
- deterministic decision sufficiency/tie/refusal rules;
- platform audit adapter scope and deterministic privacy scan;
- two-layer offline dependency lock strategy;
- checkpoint adapter/recovery/fault-injection contract;
- command authorization surface;
- engineering build/profile digest procedures;
- V1 hook mapping.

### Left to measured C1 evidence

- actual machine facts and resource ceilings;
- implementation language among locally supported eligible families;
- GMP-only versus supported public FLINT route;
- dense/sparse representation;
- small-table width and hierarchical scheduler parameters within the measured suite;
- explicit-coefficient versus value-threaded form;
- allocation reuse strategy;
- compiler/toolchain and exact flags;
- portable versus native build;
- auxiliary parallelism and thread count;
- terminal handoff winner;
- audit/canary production level;
- checkpoint buffering strategy and cadence;
- checkpoint filesystem support;
- build/profile identities.

### Deferred to V1 or later

- execution and PASS/FAIL of CEML-V1-SUITE-1;
- any scientific master seed event;
- final executable ladder freeze;
- E1 manifest/start generation and scientific trajectories;
- extreme-scale performance/resource behavior beyond bounded C1 evidence;
- historical Elsenhans archive and Gerbicz-primary-source evidence gaps.

## 20. I1 exit decision

The handoff now supplies C1 with executable specificity for semantics, audit scope, privacy, deterministic bounded inputs, route activation, decision sufficiency, checkpoint durability, resource safety, evidence schemas, provenance, offline build behavior, V1 hooks and refusal gates without choosing or measuring the local machine.

**CEML-I1 PASS.**
