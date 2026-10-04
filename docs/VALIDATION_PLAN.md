# CEML Validation Plan

Status: **FROZEN-SCIENTIFIC VALIDATION CONTRACT — V1 not yet executed**

No implementation is trusted because it is fast, because one implementation returns 1, or because multiple checks share the same affine recurrence.

## 1. Independence architecture

### A. Definition oracle — mandatory independence anchor

Implement a small direct elementary iterator from the definitions of C and T, without affine batching, base tables, production low-bit extraction or production transform composition. It must use exact arbitrary-precision arithmetic.

At least one V1 execution of this oracle must be in a separately authored code path; a separate language/runtime is preferred where practical. Shared big-integer libraries are acceptable, but shared CEML batching code is not.

### B. Affine differential

For bounded n and k, compare each affine block against exactly k direct T steps, including exact resulting n, shortcut count and odd count. Composition tests include non-commuting blocks and associative three-way splits.

### C. Count-conversion oracle

For direct C, T and odd-only U paths verify `standard = shortcut + odd`.
For each U step with valuation v verify increments `(shortcut,odd,standard)=(v,1,v+1)`.

### D. Implementation-lineage/backend checks

Where available, compare against an independently authored implementation/lineage. Every enabled multiplication/backend/feature route must also be forced active and compared with the definition oracle or a state already certified by it. A route that tests only its own shared recurrence does not count as independent.

## 2. Frozen deterministic validation seed

CEML-V1-SUITE-1 uses the public non-scientific 32-byte seed

`000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f`

for deterministic randomized bounded validation inputs, under the distinct prefix `CEML-VALIDATION-RANDOM-V1\0`.

This seed is not the scientific master seed and cannot generate scientific starts because the domain prefix and purpose are different.

## 3. Required deterministic test classes

V1 must execute all of the following.

1. **Elementary identities:** parity, one-step C/T/U, valuation and counter increments.
2. **Exhaustive small residues/base tables:** for every entry of every enabled small table/block width, regenerate from direct T; I1/C1 may choose widths, but V1 coverage is exhaustive for the chosen finite tables.
3. **Randomized bounded differential tests:** derive inputs deterministically from the frozen V1 seed/prefix; record generated-case digests. Include varied n and k and repeat generation to prove determinism.
4. **Adversarial integer patterns:** values around every relevant limb/word boundary; `2^m-1`, `2^m`, `2^m+1`; long low-zero runs; sparse high/low limbs; alternating low bits; all-one low words; carry/borrow boundaries.
5. **Odd split lengths:** recursive/block lengths `2m+1`, with explicit `k1+k2=k`, direct-state comparison and order-sensitive fixtures.
6. **Terminal/overshoot:** start 1, powers of two, values whose block ends at 1 and values for which an overlong block would pass first 1. Force terminal-safe decomposition and prove no count past first 1 is accepted.
7. **Serialization/digest round trips:** UENC canonical/non-canonical cases, RFC 8785 official examples, CEML domain-prefix vectors, JSON parse/canonicalize/digest agreement across at least two independent implementations where practical.
8. **Checkpoint stop/resume:** multiple boundaries including before/after odd steps, limb boundaries and terminal handoff; fresh-process resume must equal uninterrupted mathematical state/counters/result.
9. **Fault injection:** corrupt one parity decision, affine coefficient, carry/limb, low-bit extraction, serialized value byte, serialized counter, multiplication result, body digest, metadata field and manifest/provenance field. Each injected fault must be detected by the intended independent oracle/integrity check.
10. **Feature-route activation:** instrumentation must prove each enabled optimized route is actually exercised by at least one validation case; compare its result against an independent reference.
11. **Selected exact formula-defined fixtures:** the frozen fixtures below.
12. **Checked/sanitized builds:** execute at least one recorded applicability/coverage case for this class. For every unsafe/fixed-width/compiler-sensitive path that exists, run the I1/C1-specified overflow/UB/memory checks; if none exists, the evidence artifact must explicitly establish non-applicability rather than omitting the class.

## 4. Frozen exact fixtures

These R2 fixtures are carried forward with their R2 provenance classification.

| Start | Standard steps | Odd steps | Shortcut steps | Required result |
|---|---:|---:|---:|---|
| 27 | 111 | 41 | 70 | first 1 |
| `2^127-1` | 1660 | 593 | 1067 | first 1 |
| `2^44497-1` | 598067 | 214150 | 383917 | first 1 |

The 27 odd count is fixed by the frozen invariant `111-70=41`. The two Mersenne triples were produced by the direct Python R2 reference, with standard totals independently agreeing with the audited Boutoukoat lineage as recorded in `docs/ALGORITHM_AUDIT.md`.

V1 must recompute them; stored expected values are not self-authenticating.

## 5. Generator/encoding vectors

V1 must reproduce every `ceml-start-v1` vector in `docs/RANDOMNESS_AND_REPRODUCIBILITY.md`, including a rejection path, start digests, the seed-commitment vector and the checkpoint-body vector.

## 6. Objective V1 acceptance criteria

V1 is PASS only when a schema-valid `schemas/validation_evidence.schema.json` record with `suite_version="CEML-V1-SUITE-1"` shows:

- all twelve required classes `executed=true`, `passed=true`, with at least one case, zero class failures and a non-null artifact digest;
- zero unexplained arithmetic/state/count disagreements;
- zero deterministic-regeneration disagreements (any such issue is counted as an arithmetic/reproducibility disagreement and blocks closure);
- zero canonical serialization/digest disagreements;
- exact checkpoint/resume equality for deterministic scientific fields;
- zero undetected required fault injections;
- zero uncovered enabled routes;
- required checked/sanitized build coverage complete;
- zero unresolved blocking correctness/integrity issues;
- exact protocol, engine commit, build digest and machine-profile digest recorded.

There is no tolerated unexplained-disagreement count.

Development history may contain failures, but the final PASS record must reference evidence showing they are resolved; a PASS record cannot encode a failed required class.

## 7. Validation-evidence digest

Remove top-level `evidence_digest`, JCS-canonicalize the remaining record, encode UTF-8, then compute

`SHA3-256(ASCII("CEML-VALIDATION-EVIDENCE-V1") || 00 || canonical_bytes)`.

Render as 64 lowercase hexadecimal characters.

## 8. Failure and freeze rule

Any arithmetic/oracle disagreement, failed invariant, nondeterministic regeneration, unexplained count mismatch, corrupt checkpoint, canonicalization mismatch or provenance mismatch blocks V1 and E1.

During a scientific run the same classes stop automatic progression and preserve evidence. Resource exhaustion is `resource_stop`; it is not divergence. Suspected counterexample behaviour is `frozen_anomaly` and requires a separate certification programme.

## 9. Validation evidence content

The machine-readable evidence record binds protocol/build/profile identities, the frozen suite version/seed, required-class results, exact pass/fail counts, route coverage, fault-injection coverage, checked/sanitized-build evidence, fixture results and its SHA3-256 record digest.

Raw logs may be large and local, but retained artifact digests/locators must make the acceptance record auditable.
