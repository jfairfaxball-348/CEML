# CEML-R3 Reproducibility and Validation Audit

Status: **CEML-R3 FROZEN-SCIENTIFIC DECISION RECORD**

Date: 2026-10-04

## 1. Research questions

R3 asked what later CEML implementations must mean by a trajectory, a magnitude rung, a reproducibly random start, a canonical artifact, a valid checkpoint, a completed result and an independently validated build. It also asked which failures must halt scientific progression.

R3 does not select a production architecture, machine profile, compiler flags, arithmetic backend, macro size, checkpoint cadence, resource ceiling or final ladder. It does not generate the scientific master seed or execute any scientific trajectory.

## 2. Source strategy and primary standards

R3 used the repository R1/R2 evidence as the algorithmic baseline and consulted primary standards for cryptographic and canonicalization primitives.

| Source | Status / version used | Exact proposition used |
|---|---|---|
| NIST FIPS 202, *SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions*, August 2015, DOI 10.6028/NIST.FIPS.202, accessed 2026-10-04, https://csrc.nist.gov/pubs/fips/202/final | Current final FIPS publication at access time; NIST notes a future update is planned | SHA3-256 and SHAKE256 are fully specified binary hash/XOF functions. SHAKE256 is used for deterministic expansion; SHA3-256 is used for 256-bit commitments/digests. |
| NIST SP 800-185, *SHA-3 Derived Functions: cSHAKE, KMAC, TupleHash, and ParallelHash*, December 2016, DOI 10.6028/NIST.SP.800-185, accessed 2026-10-04, https://csrc.nist.gov/pubs/sp/800/185/final | Current final recommendation at access time; NIST notes a revision is planned | Confirms the SHA-3 family supports explicit customization/domain-separation constructions. CEML nevertheless chooses plain SHAKE256 plus an unambiguous CEML framing so independent implementations need only FIPS 202. |
| RFC 8785, *JSON Canonicalization Scheme (JCS)*, June 2020, accessed 2026-10-04, https://www.rfc-editor.org/rfc/rfc8785.html | Primary JCS specification; Informational RFC, not IETF Standards Track | Deterministic property ordering, primitive serialization and UTF-8 output for canonical JSON; Appendix D recommends strings for integers outside IEEE-754 exact range. |

The planned revisions to FIPS 202/SP 800-185 do not silently change this protocol. CEML-SCI-1 names the cited editions. A future standards revision requires an explicit protocol-version decision.

## 3. Findings and frozen decisions

### 3.1 Collatz semantics — FROZEN-SCIENTIFIC

The mathematical reference map is the standard Collatz map
`C(n)=n/2` for even `n`, and `C(n)=3n+1` for odd `n`.
Evaluation terminates at the **first occurrence of 1**; the map is never applied to 1 in a completed CEML trajectory.

The shortcut map is
`T(n)=n/2` for even `n`, and `T(n)=(3n+1)/2` for odd `n`.
Implementations may internally batch T or use an equivalent exact transform.

Every scientific state carries three exact non-negative unbounded counters:
`shortcut_steps`, `odd_steps`, and `standard_steps`, with
`standard_steps = shortcut_steps + odd_steps`.

For an odd-only transition `U(n)=(3n+1)/2^v`, `v=v2(3n+1)`, increments are `shortcut += v`, `odd += 1`, `standard += v+1`.

"Total stopping time" is used only with an explicit map qualifier. `standard_steps` is the conventional standard-map total stopping time to first 1; `shortcut_steps` is the CEML shortcut total stopping time.

A macro operation may not cross first 1 invisibly. It must either be proven not to contain 1 before its end or be decomposed until the exact first-1 boundary is exposed.

No peak/minimum trajectory metric is part of CEML-SCI-1. Such a metric requires a later protocol version with a definition observable under all conforming exact implementations.

### 3.2 Magnitude rung — FROZEN-SCIENTIFIC

A rung is an exact **decimal-digit count** `D >= 1`. The permitted set is all positive odd integers with exactly D base-10 digits:
`R_D = { n odd : 10^(D-1) <= n <= 10^D-1 }`.

Let `a_D` be the smallest odd member: `a_1=1`; for `D>=2`, `a_D=10^(D-1)+1`.
Let `M_D=((10^D-1-a_D)/2)+1`. Every member is uniquely `a_D+2j` for `0<=j<M_D`.

This freezes rung meaning only. It does **not** freeze the final list of D values.

### 3.3 Random-start generator — FROZEN-SCIENTIFIC

The generator is `ceml-start-v1`, specified in docs/RANDOMNESS_AND_REPRODUCIBILITY.md. It uses FIPS 202 SHAKE256 and rejection sampling, with a fixed 256-bit master seed interpreted as exactly 32 raw bytes.

For each frozen ladder position, derivation binds both `D` and zero-based `rung_index`. Rejection retries are deterministic and cannot depend on trajectory behaviour. The accepted index is uniform over the finite rung set by construction.

The actual scientific master seed does not exist as a result of R3.

### 3.4 Seed commitment — FROZEN-SCIENTIFIC

At the later authorized seed event, the final ladder must already be frozen. Exactly one 32-byte master seed is generated from an approved OS cryptographic random source in a recorded one-shot event. Its SHA3-256 commitment is committed before any scientific trajectory evaluation.

All starts for the frozen ladder are deterministically derived and their ordered start digests committed before any trajectory is inspected. The seed is disclosed in lowercase hexadecimal before scientific evaluation begins, allowing independent regeneration. No reroll is permitted.

Validation/calibration randomness uses fixed public validation seeds and distinct domain prefixes; it never uses the scientific master seed.

### 3.5 Encodings and digests — FROZEN-SCIENTIFIC

Unsigned integer binary encoding `UENC(n)` for `n>=0` is:

1. `MAG(n)` = minimal unsigned big-endian magnitude bytes, except `MAG(0)=00`;
2. `UENC(n) = U64BE(len(MAG(n))) || MAG(n)`.

The unsigned 64-bit length is a byte count. No leading zero magnitude byte is allowed for nonzero n. A decoder rejects non-minimal encodings, length mismatch or forbidden trailing bytes.

Digest algorithm is FIPS 202 SHA3-256. Digest text is exactly 64 lowercase hexadecimal characters. Every digest preimage begins with an ASCII domain label followed by one NUL byte.

JSON artifacts use RFC 8785 JCS UTF-8 canonicalization. Scientific integers/counters are JSON decimal strings matching `0|[1-9][0-9]*`; digest-covered schemas do not use JSON numbers for exact scientific quantities. Self-referential digest fields are **omitted**, not zeroed, from their own digest preimage.

Frozen domain labels are listed in docs/SECURITY_AND_INTEGRITY.md.

### 3.6 Checkpoint/restart — FROZEN-SCIENTIFIC

A checkpoint consists of canonical `state.bin` plus canonical JCS `metadata.json`. The body contains only the exact current integer; metadata binds exact counters and provenance. Derived tables, caches, recursion stacks, allocator state and thread schedule are disposable.

Resume accepts only a checkpoint whose versions are supported, all digests match, provenance matches the run manifest, counter invariants hold, and first-1 state is consistent. Otherwise resume refuses.

Promotion is copy-on-write/slot based: write candidate body and metadata, durably flush, verify by re-read, atomically publish using target-filesystem guarantees, then retain at least the immediately previous valid checkpoint. Cadence is not frozen.

Restart equivalence means resumed execution reaches exactly the same subsequent mathematical states and deterministic scientific result fields as uninterrupted execution from that checkpoint. Timing, logging and engineering route counters are outside this equality.

### 3.7 Result semantics — FROZEN-SCIENTIFIC

Frozen statuses:
`completed`, `frozen_anomaly`, `operator_abort`, `validation_failure`, `resource_stop`, `integrity_failure`, `reproducibility_failure`, `provenance_failure`, `unexpected_termination`.

Only `completed` means first 1 was reached with all required exact counters and provenance valid. Every other status is non-completion and explicitly **not evidence of divergence**.

### 3.8 Validation architecture — FROZEN-SCIENTIFIC

V1 requires a definition-level direct elementary C/T oracle that does not reuse affine batching; affine-vs-direct differential tests; count-conversion checks; exhaustive bounded residues; deterministic randomized bounded tests; adversarial limb/low-bit patterns; odd split lengths; terminal/overshoot fixtures; serialization/digest round trips; checkpoint stop/resume equivalence; fault injection; feature-route activation; and exact formula-defined fixtures.

The direct elementary oracle is the required independence anchor. Multiple implementations of the same affine recurrence do not replace it.

## 4. V1 objective acceptance

V1 passes only if every required test class is executed and evidenced, with zero unexplained arithmetic/state/count disagreements, zero canonicalization/digest disagreements, deterministic regeneration, exact restart equality, all enabled routes forced and independently compared, all required injected faults detected, applicable checked/sanitized suites passing, no unresolved blocking correctness/integrity issue, and schema-valid validation evidence bound to protocol/engine/build/profile.

Any unexplained disagreement is a V1 failure, not a warning budget.

## 5. Anomaly/failure freeze rules

Arithmetic/oracle disagreement, reproducibility mismatch, provenance mismatch, checkpoint corruption, unsupported version, invalidating unexpected termination, or suspected counterexample behaviour stops automatic progression. Preserve the last accepted checkpoint, failing artifact bytes, manifests, logs, build/profile identities and independent reproducer inputs.

Resource exhaustion produces `resource_stop`; it never implies divergence. Suspected counterexample behaviour produces `frozen_anomaly` and begins a separate certification programme; it is not reported as a counterexample by CEML alone.

## 6. Deferred risks

Legitimately deferred:

- R4: privacy-safe local hardware audit specification and bounded calibration permissions;
- I1: code-level interfaces and implementation mapping;
- C1: measured language/backend/compiler choice, block sizes, thresholds, memory strategy, checkpoint cadence and resource ceilings;
- V1: actual execution of the frozen validation suite;
- E1: final ladder values and actual scientific seed event.

The unresolved R2 Elsenhans archive and Gerbicz-primary-source evidence gaps remain historical evidence gaps and do not alter the R3 contract.

## 7. Repository changes

R3 freezes the randomness, experiment, checkpoint, result, validation and integrity documents; upgrades the run/checkpoint/result schemas; adds a validation-evidence schema; updates programme gate state; and prepares the R4 handoff.

## 8. R3 decision

All R3 exit criteria are satisfied without production implementation, scientific seed generation, giant/scientific execution or machine-specific tuning.

**CEML-R3 PASS.**
