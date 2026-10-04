# Security and Integrity Policy

Status: **R3 FROZEN-SCIENTIFIC INTEGRITY CONTRACT**

CEML scientific execution is offline-capable and does not treat the scientific seed as a long-term secret.

## 1. Sensitive-data exclusions

Do not commit credentials, tokens, private keys, usernames, hostnames, serial numbers, MAC/IP addresses, account identifiers, unrelated filesystem paths or raw unrelated software inventories. Hardware reports are sanitized before commit.

## 2. Frozen cryptographic primitives

CEML-SCI-1 uses:

- SHAKE256 from NIST FIPS 202 (August 2015) for `ceml-start-v1` deterministic expansion;
- SHA3-256 from NIST FIPS 202 for 256-bit commitments and artifact digests;
- RFC 8785 JCS (June 2020) for canonical JSON bytes.

R3 pins these specification editions. A future NIST revision is not adopted silently.

## 3. Digest rendering and domain labels

All SHA3-256 digests are 32 bytes rendered as exactly 64 lowercase hexadecimal characters.

Every preimage starts with the listed ASCII label followed by one NUL byte:

- `CEML-SCIENTIFIC-SEED-COMMIT-V1` — master-seed commitment;
- `CEML-START-V1` — canonical generated start;
- `CEML-RUN-MANIFEST-V1` — run manifest JCS bytes;
- `CEML-CHECKPOINT-BODY-DIGEST-V1` — exact checkpoint body bytes;
- `CEML-CHECKPOINT-CURRENT-V1` — canonical current integer;
- `CEML-CHECKPOINT-METADATA-V1` — checkpoint metadata JCS bytes;
- `CEML-RESULT-V1` — result JCS bytes;
- `CEML-VALIDATION-EVIDENCE-V1` — V1 evidence JCS bytes.

Scientific-start expansion uses the distinct SHAKE prefix `CEML-SCIENTIFIC-START-V1\0`. Validation and calibration use `CEML-VALIDATION-RANDOM-V1\0` and `CEML-CALIBRATION-RANDOM-V1\0`.

## 4. Canonical JSON

Digest-covered JSON conforms to RFC 8785 JCS and is UTF-8 encoded. Duplicate object names and invalid Unicode are rejected.

Exact scientific integers/counters are canonical decimal strings, not JSON numbers. A canonical non-negative decimal integer is exactly `0` or `[1-9][0-9]*`; no sign, exponent, decimal point or leading zero is allowed.

Identifier fields that the schemas constrain to ASCII must remain ASCII. Other Unicode strings are preserved byte-for-byte through JCS rules; implementations must not apply Unicode normalization during canonicalization.

For an artifact's self digest, remove exactly that top-level digest member before JCS canonicalization. Do not insert a null/zero placeholder.

## 5. Run-manifest digest

`manifest_digest = SHA3-256(ASCII("CEML-RUN-MANIFEST-V1") || 00 || JCS(manifest without manifest_digest))`.

Canonicalization sanity vector: for the synthetic object containing `a="1"`, `z="2"` and any top-level `manifest_digest`, the self-digest preimage JSON is exactly `{"a":"1","z":"2"}`; its CEML run-manifest digest is
`90cef02ce54b3454f57b23c6148914edba7ca5b93813e0847e9e0b77278382bc`.

## 6. Start precommitment

The final ladder is frozen before seed generation. The one seed commitment is committed before scientific evaluation; all ordered start digests are then committed before any trajectory inspection; the seed is disclosed and regeneration checked before execution.

Candidate substitution, a second seed under the same protocol instance, or a regenerated-start mismatch is a reproducibility failure.

## 7. Checkpoint integrity

Resume refuses corruption, noncanonical encoding, unknown semantic versions, ambiguous slots or provenance mismatch. Manual edits cannot be promoted as a continuation of the same scientific run.

At least one prior validated checkpoint is retained across promotion.

## 8. Build/provenance integrity

A scientific manifest/result binds protocol commit, engine commit, build digest, machine-profile digest and V1 validation-evidence digest. A mismatch is a provenance failure, not an invitation to continue with a "close enough" build.

Scientific execution does not fetch code or dependencies from the network.

## 9. Hash limitations

Digests detect byte/provenance changes and bind commitments; they do not prove arithmetic correctness. Independent validation supplies correctness evidence.

## 10. Repository history

Corrections use additive Git history. Published scientific history is not rewritten to conceal a failure. Superseded results remain traceable and explicitly marked.
