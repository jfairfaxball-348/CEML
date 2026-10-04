# CEML Result Record Policy

Status: **FROZEN-SCIENTIFIC — result schema CEML-RESULT-1**

Canonical schema: `schemas/result.schema.json`.

## 1. Purpose

A result is compact deterministic scientific evidence about one predetermined start. It is not a trajectory dump or an engineering telemetry record.

CEML-SCI-1 intentionally excludes wall-clock/CPU timing, peak/minimum state metrics and macro-block counts from the canonical scientific result. Those may appear in separately labelled run/engineering logs.

## 2. Required identity

Every result binds:

- experiment and schema version;
- run ID and run-manifest digest;
- protocol version and protocol commit;
- rung definition/version, decimal digits and zero-based rung index;
- generator version, seed commitment and start digest;
- engine commit and build digest;
- machine-profile digest;
- V1 validation-evidence digest;
- map-semantics version.

## 3. Exact outcome fields

Every result records:

- status;
- final value as canonical non-negative decimal string or null;
- exact `shortcut_steps`, `odd_steps`, `standard_steps` as canonical decimal strings;
- optional final checkpoint metadata digest;
- status detail for non-completions;
- result digest.

The counter invariant is `standard_steps = shortcut_steps + odd_steps`.

For `completed`, final value is exactly `"1"`, status detail is null, and the counters are the exact first-1 counts.

For a non-completed result, final value is the last exact accepted state if one can be certified, otherwise null. It does not imply anything about future trajectory behaviour.

## 4. Frozen status semantics

- `completed`: first occurrence of 1 reached exactly; required counters/provenance/integrity valid.
- `frozen_anomaly`: automatic progression stopped because exact behaviour requires anomaly/counterexample investigation.
- `operator_abort`: deliberate clean stop not classified as resource/integrity/validation failure.
- `validation_failure`: an invariant/oracle/acceptance requirement failed.
- `resource_stop`: memory, storage, time policy, power/thermal safety or another explicit resource condition stopped progress.
- `integrity_failure`: artifact/canonicalization/digest/checkpoint integrity failed.
- `reproducibility_failure`: deterministic regeneration or committed start/seed relationship failed.
- `provenance_failure`: required protocol/build/profile/validation identity does not match the authorized manifest.
- `unexpected_termination`: execution ended unexpectedly and the run is being closed rather than resumed from a valid checkpoint.

Only `completed` is a trajectory completion. No other status is evidence of divergence.

## 5. Canonical result digest

The JSON instance must be RFC 8785 JCS compatible. All exact integers are decimal strings; JSON numbers are not used.

To compute `result_digest`:

1. remove the top-level `result_digest` field;
2. JCS-canonicalize the remaining object and encode UTF-8;
3. compute `SHA3-256(ASCII("CEML-RESULT-V1") || 00 || canonical_bytes)`;
4. render 64 lowercase hexadecimal characters.

Self-digest omission is exact; no placeholder is inserted.

## 6. Certification reference

A completed result is publishable as CEML scientific evidence only when its `validation_evidence_digest` identifies a V1-PASS record for exactly the engine/build/profile and protocol named by the run manifest.

A later discovery can supersede a result, but history is not rewritten. Corrections create new records/versioned status with traceable provenance.
