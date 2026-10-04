# CEML Experiment Protocol

Status: **FROZEN-SCIENTIFIC — CEML-SCI-1**

## 1. Experimental unit

One experimental unit is one exact predetermined positive odd integer for one frozen decimal-digit rung. There is exactly one scientific start per rung. R3 freezes what a rung means, not the final ladder values.

No rerolling, ranking, peak chasing, survivor selection or post-hoc substitution is permitted.

## 2. Magnitude rung

A rung value is decimal digit count `D>=1`.

The permitted set is
`R_D={n odd: 10^(D-1)<=n<=10^D-1}`.

Boundary inclusion is exact. Base-10 rendering has exactly D digits and no leading zero. Bit length is descriptive only and never changes rung membership.

The bootstrap values `10^6,10^7,10^8,10^9,10^10` decimal digits remain provisional and are not frozen by R3.

## 3. Collatz maps and terminal semantics

Reference standard map:
`C(n)=n/2` when n is even; `C(n)=3n+1` when n is odd.

Shortcut map:
`T(n)=n/2` when n is even; `T(n)=(3n+1)/2` when n is odd.

A completed trajectory begins at the generated start and ends at the **first occurrence of 1**. No conforming completed execution applies C or T to 1.

The standard-map orbit is the mathematical reference. A production implementation may use T, odd-only stepping, affine blocks or another exact representation only if it preserves the same first-1 orbit and exact counters.

## 4. Mandatory exact counters

All counters are mathematical non-negative integers with no implementation-size bound.

- `shortcut_steps`: exact number of T applications represented.
- `odd_steps`: exact number of those T applications whose input was odd.
- `standard_steps`: exact number of C applications represented.

Invariant at every checkpoint and result:
`standard_steps = shortcut_steps + odd_steps`.

For odd-only `U(n)=(3n+1)/2^v`, `v=v2(3n+1)`, one U transition increments:
`shortcut_steps += v`, `odd_steps += 1`, `standard_steps += v+1`.

"Total stopping time" must always be qualified. `standard_steps` is the standard-map total stopping time to first 1; `shortcut_steps` is the shortcut-map total stopping time.

## 5. First-1 safety

A macro/batched transform may be accepted only when it cannot hide an earlier 1. A scheduler may satisfy this either by a proof that 1 cannot occur before the block end for the current state/block, or by exact decomposition/direct stepping until the first-1 boundary is exposed.

A block that steps past 1 and later returns to 1/2/4 is invalid for CEML completion accounting.

## 6. Exactness

All candidate-affecting arithmetic, state, counters, serialization and digests are exact. Floating point may be used only for ancillary engineering observations that cannot alter a start, state, count, checkpoint, result or acceptance decision.

## 7. Scientific trajectory metrics

CEML-SCI-1 freezes no maximum/minimum/peak trajectory metric. Macro implementations may skip internal states, and R2 did not establish a common exact peak-observation contract. Engineering logs may record clearly labelled diagnostics, but they are not certified scientific result fields.

Adding a scientifically interpreted peak/minimum metric requires a new protocol/schema version.

## 8. Scientific run authorization lifecycle

A scientific run may start only when all of the following exist and agree:

1. CEML-SCI-1 or later explicitly approved protocol;
2. frozen final ladder;
3. completed seed commitment/start-precommit/disclosure procedure;
4. regenerated start digest matching the precommit;
5. V1-PASS validation evidence for the exact engine/build/profile;
6. frozen machine/build profile;
7. schema-valid run manifest with `authorization_gate="E1"`;
8. supported checkpoint format and integrity policy.

R3 itself authorizes none of these execution steps.

## 9. Completion and non-completion

`completed` requires the exact first occurrence of 1, valid counter invariant, valid provenance and valid result digest.

All other statuses are non-completions. Resource exhaustion, operator stop, crash, corruption, validation failure, reproducibility failure, provenance mismatch or anomaly freeze is not evidence of divergence.

## 10. Automatic progression

Automatic progression to another scientific rung is permitted only after a `completed` result has passed all artifact-integrity checks and no anomaly/failure remains open.

Any frozen anomaly or integrity/reproducibility/validation/provenance failure stops progression and preserves evidence for audit.

## 11. Claim boundary

A completed result supports a statement only about that exact predetermined integer under its exact protocol/build/profile. One start per rung does not establish a verified interval, a population convergence probability, or representativeness of all numbers at that magnitude.
