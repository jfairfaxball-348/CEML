# Randomness and Reproducibility

Status: **FROZEN-SCIENTIFIC — CEML-SCI-1 / generator ceml-start-v1**

## 1. Objective

For each frozen magnitude rung, CEML has exactly one start. The start is fixed by a deterministic, independently reproducible generator before any trajectory inspection. There is no behavioural reroll, candidate ranking or substitution.

R3 does **not** generate the scientific master seed.

## 2. Magnitude domain

For decimal-digit rung `D>=1`:

`R_D = {n odd : 10^(D-1) <= n <= 10^D-1}`.

Let `a_1=1`; for `D>=2`, `a_D=10^(D-1)+1`.
Let `M_D=((10^D-1-a_D)/2)+1`.

Index `j` maps bijectively to start `n=a_D+2j` for `0<=j<M_D`.

## 3. Primitive

`ceml-start-v1` uses SHAKE256 exactly as standardized by NIST FIPS 202 (August 2015, DOI 10.6028/NIST.FIPS.202). The publication was the current final FIPS 202 at the R3 access date 2026-10-04; NIST's notice that it plans a future revision does not change this frozen version.

The master seed is exactly 256 bits = 32 raw bytes. Hexadecimal is only a disclosure rendering; the generator input uses the decoded 32 bytes.

## 4. Canonical integer framing

For non-negative integer `x`, let `MAG(x)` be minimal unsigned big-endian bytes, except `MAG(0)=00`.
Let `UENC(x)=U64BE(len(MAG(x))) || MAG(x)`.

The 64-bit length is an unsigned big-endian byte count. Encodings needing more than `2^64-1` magnitude bytes are outside CEML-SCI-1 and require a protocol version change.

`D`, zero-based `rung_index` and `retry` are each encoded with UENC.

## 5. Generator algorithm

Frozen ASCII domain prefix including terminating NUL:

`CEML-SCIENTIFIC-START-V1\0`.

For a rung `D` at zero-based frozen-ladder position `rung_index`:

1. Compute `a_D` and `M_D`.
2. Set `b = ceil(log2(M_D))`, equivalently `bit_length(M_D-1)`.
3. Set `q = ceil(b/8)`.
4. For `retry = 0,1,2,...`:
   - `msg = ASCII("CEML-SCIENTIFIC-START-V1") || 00 || seed32 || UENC(D) || UENC(rung_index) || UENC(retry)`.
   - Obtain exactly q bytes `r = SHAKE256(msg, q bytes)`.
   - Interpret r as an unsigned big-endian integer and set `x = r mod 2^b` (equivalently mask away the top unused bits).
   - If `x >= M_D`, reject and increment retry.
   - Otherwise return `n = a_D + 2x` and the accepted retry value.

Because the masked x is uniform over exactly `[0,2^b)` and acceptance is the initial interval `[0,M_D)`, the accepted x is uniform over `[0,M_D)`; the start is therefore uniform over all permitted odd D-digit integers.

Rejection depends only on the generator output and finite domain. It is not a reroll in response to Collatz behaviour.

## 6. Start encoding and digest

The canonical start bytes are `UENC(n)`.

`start_digest = SHA3-256(ASCII("CEML-START-V1") || 00 || UENC(n))`, rendered as 64 lowercase hex characters.

Decimal rendering, if shown, has no leading zero and is not the digest preimage.

## 7. Independent test vectors

These vectors use the non-scientific public test seed
`000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f`.

| D | rung_index | retry sequence SHAKE output (hex) | masked x / accept | final start | start digest |
|---:|---:|---|---|---:|---|
| 1 | 0 | r0=`2a` | 2 / yes | 5 | `d9487e99d4abe61f51c82dc14937252d479f4cfa816d44594675035d6bfee7f9` |
| 2 | 0 | r0=`ea` | 42 / yes | 95 | `71fca1897e39b8df0616a3f87d31d6a04139bf86bf0099ab4316f71a7174255e` |
| 6 | 3 | r0=`60c3e8` | 50152 / yes | 200305 | `979616fd70427e9a5a1c461bd57f7aabb746915008e2fef314520999a5d6fe31` |
| 20 | 0 | r0=`df1a9d8d5a8faae26a`; r1=`8c1a5eb4a90f9420f6` | 57258076657555268202 / reject; 1900154731000766710 / yes | 13800309462001533421 | `c9a821d7a8b775fdc6d88f3655732d9e5e7eb369db8153a4e2fa502d62a51e67` |

A minimal rejection-only edge vector is `D=1, rung_index=1`: r0=`7e` gives masked x=6 and is rejected; r1=`81` gives x=1 and returns start 3 with digest `7a947a3d5d546eb6ad33bc3d1b9580e49a69af455bf0d7f1b1839b3bcccf4692`.

For the same test seed, the seed-commitment vector is
`824873c331f2b22382714991a57809abc6fc3e43600cd31556470006981b9009`.

Independent implementations must match these bytes, retries, starts and digests before V1 can pass.

## 8. Scientific seed event and precommitment

At the later gate that explicitly authorizes seed generation:

1. The final executable ladder, including the ordered `D` values and zero-based indices, must already be committed.
2. Generate exactly one 32-byte master seed from an approved operating-system cryptographic random source in a recorded one-shot event. Record the exact API/tool/version used; do not add operator-chosen entropy and do not retry because of the resulting seed.
3. Compute `seed_commitment = SHA3-256(ASCII("CEML-SCIENTIFIC-SEED-COMMIT-V1") || 00 || seed32)`.
4. Commit the seed commitment before any scientific trajectory is evaluated.
5. Derive every frozen rung start exactly once and commit the ordered tuple `(rung_index,D,retry,start_digest)` for the complete ladder before any trajectory inspection.
6. Disclose the seed as exactly 64 lowercase hexadecimal characters and verify all committed starts regenerate.
7. Scientific evaluation may begin only after the disclosure/regeneration check succeeds.

Loss of the seed before disclosure is a reproducibility failure. The run does not substitute another seed under the same protocol instance.

## 9. Domain separation from validation/calibration

The scientific prefix above is reserved exclusively for scientific starts.

Validation random inputs use the public prefix `CEML-VALIDATION-RANDOM-V1\0` and public fixed validation seeds recorded in validation evidence. Calibration inputs use `CEML-CALIBRATION-RANDOM-V1\0`.

The scientific master seed must never be reused for validation, calibration, run IDs, benchmark inputs or any engineering randomness.
