# CEML Checkpoint Specification

Status: **FROZEN-SCIENTIFIC — checkpoint format CEML-CKPT-1**

## 1. Purpose and semantic boundary

A checkpoint is a durable exact mathematical state from which execution can resume without changing the subsequent CEML trajectory or deterministic scientific result.

Checkpoint cadence is an engineering parameter deferred to C1.

## 2. Artifact pair

Each checkpoint slot contains:

- `state.bin`: canonical binary current value;
- `metadata.json`: RFC 8785 JCS-compatible metadata conforming to `schemas/checkpoint_metadata.schema.json`.

A pointer such as `latest` is only an operational hint. Resume validity comes from the slot contents and digests, not the pointer alone.

## 3. Canonical body

Let `UENC(n)=U64BE(len(MAG(n)))||MAG(n)`, with minimal unsigned big-endian `MAG` and `MAG(0)=00`.

`state.bin = ASCII("CEML-CKPT-BODY-V1") || 00 || UENC(current_n)`.

No trailing bytes are permitted. The 64-bit unsigned length is a byte count; larger values require a new protocol/format version.

`body_digest = SHA3-256(ASCII("CEML-CHECKPOINT-BODY-DIGEST-V1") || 00 || state.bin)`.

The current value is always positive. A body decoding to zero is invalid.

Test vector for `current_n=1`:
body hex
`43454d4c2d434b50542d424f44592d563100000000000000000101`;
body digest
`181ce6b5c4488f56cac3a7439cf6c42048d03b195e3f0b21bf37f6c59f285a9f`.

## 4. Metadata requirements

Metadata binds at least:

- schema and checkpoint-format versions;
- run ID and monotonically increasing unbounded decimal-string sequence;
- previous metadata digest (null only for sequence zero);
- run-manifest digest;
- original start digest;
- protocol version and protocol commit;
- engine commit, build digest, machine-profile digest and V1 validation-evidence digest;
- map-semantics version;
- body byte length and body digest;
- current-value digest;
- exact `shortcut_steps`, `odd_steps`, `standard_steps`;
- `terminal_reached`;
- metadata digest.

`current_value_digest = SHA3-256(ASCII("CEML-CHECKPOINT-CURRENT-V1") || 00 || UENC(current_n))`.

Counter invariant: `standard_steps = shortcut_steps + odd_steps`.

If `terminal_reached=true`, current_n must be 1. If current_n is 1, `terminal_reached` must be true. `previous_metadata_digest` is null if and only if sequence is zero.

No elapsed time, macro-block count, allocator state or implementation cache is part of the scientific checkpoint state.

## 5. Metadata canonicalization and digest

Remove the top-level `metadata_digest` member. Canonicalize the remaining object using RFC 8785 JCS and UTF-8.

`metadata_digest = SHA3-256(ASCII("CEML-CHECKPOINT-METADATA-V1") || 00 || canonical_metadata_without_digest)`.

Render as lowercase hex.

## 6. Derived caches and scheduler state

Tables, affine caches, recursion stacks, multiplication scratch space, thread schedules and other derived engineering state are disposable. Resume must reconstruct them from frozen build/configuration and the exact checkpoint.

If a future implementation requires additional non-derived mathematical state for exact continuation, CEML-CKPT-1 is insufficient and the checkpoint format must be versioned before use.

## 7. Crash consistency and atomic promotion

Never overwrite the sole valid checkpoint.

For each promotion:

1. choose a non-current slot/temp location;
2. write complete `state.bin` and `metadata.json`;
3. perform the platform's required durable file flushes;
4. re-read both artifacts and fully validate lengths, canonical encodings, schema, provenance and digests;
5. atomically publish the new slot/pointer using guarantees established for the audited target filesystem;
6. durably flush directory/pointer metadata where the platform requires it;
7. retain at least the immediately previous fully validated checkpoint until the new promotion is known durable.

C1 must test the target filesystem semantics. If it cannot demonstrate an equivalent crash-consistent promotion, scientific checkpointing on that storage is unsupported.

## 8. Resume validation

Before accepting a checkpoint, resume must:

- parse only supported schema/format versions;
- reject non-canonical or malformed integer/body encodings;
- verify body length/digest, current-value digest and metadata digest;
- verify manifest/start/protocol/build/profile/validation identities;
- verify sequence/previous-digest chain where the previous slot is available;
- verify exact counter invariant and terminal consistency;
- refuse ambiguity between multiple purported current checkpoints rather than guessing.

Corrupt, unknown-version or provenance-mismatched checkpoints are never repaired in place for scientific continuation.

## 9. Restart equivalence

For bounded V1 fixtures, create checkpoints at multiple valid boundaries, stop, deserialize into a fresh process/state, rebuild all derived caches, resume, and compare with uninterrupted execution.

Required equality is exact for every subsequent mathematical state observed at comparison boundaries and for all deterministic scientific result fields, including final value and all three counters. Timing, logs and route-performance diagnostics are excluded.

## 10. Failure categories

- malformed/digest mismatch: `integrity_failure`;
- unsupported semantic version: refusal; if it blocks an active run, `integrity_failure`;
- manifest/start regeneration mismatch: `reproducibility_failure`;
- build/profile/validation identity mismatch: `provenance_failure`;
- crash without any accepted resumable state after recovery: `unexpected_termination`.

None implies divergence.
