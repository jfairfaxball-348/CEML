# R3E21-34 — Two-block reachable-state u128 theorem and fail-closed arbiter repair

**15 October 2026 | RESEARCH PARTIAL | £0 | NO SCIENCE | NO-GO FOR BENCHMARK.**

## 1. Entry, sources, and evidence

Entry main `c520463f9d173e661d6e7c74023c77b994612cbb`, normal merge of R33 PR #62. GitHub connector at entry: open PR inventory **[]**, combined commit statuses **[]** (ABSENT, not PASS), PR-triggered workflow runs **[]** (ABSENT, not PASS). Main tree SHA/merge parents, branch protection, rulesets, all check-runs **NOT RE-ESTABLISHED**; no invented green checks. Read AGENTS, ROADMAP, PROGRAM_STATUS, CLAIM_POLICY, R30–33 reports and R33 fixture. Source-specific proofs below are conditional on the accurate original-state transport to search3; the pinned foreign repositories could not be re-fetched through the current connector (NOT_FOUND), so the prior source pins are *inherited*, not fresh verification:

* Angeltveit `vigleik0/collatz` commit `f3f09248c7ae7299b8443e112f565f309d97f161`, Rust `main.rs` blob `4a33b870d27059feea28985e185b8c8c709eb313`, CUDA `collatz_cudav7.cu` blob `a783f0f39ee776c725036caec9c93d15a1c8ca72`.
* Bařina `xbarin02/collatz` commit `141e13aae243d509a01a43bec597f53a5b97a09f`, `src/worker/worker.c` blob `c33a6a86f35a0900ea1df8b7b2dcd30863a9b8bc` and `src/gpuworker/kernel.cl` blob `569e0d1a46433365c822bdf4fb27a61f188cd4b5`.
* `arXiv:2602.10466`: publicly available v1, 11 February 2026; independent published Bařina `n<2^71` from 2025 remains separate.

Bařina first-party homepage (generated **Thu 15 Oct 2026 14:50:22 CEST**) separately reports **first incomplete = 2175982616 × 2^40** and **first unassigned = 2175982616 × 2^40**. These are author reports, **NOT reproduced by CEML**. Freeze `B=2392518188130438742016` EXTERNAL / NOT REPRODUCED; `E=3000000000000000000000` EXCLUSIVE; 552501489 complete `2^40` work units and a 350507499520-start partial; conditional conservative candidate upper **326518028938128165** UNCHANGED; actual survivors **UNKNOWN**.

## 2. New theorem — first two 16-step Rust continuation multiplications cannot overflow

Let `T(n)=n/2` for even n, `(3n+1)/2` for odd n, and `X_j=T^j(n)+1`. For every integer `1<=n<2^72`:

* If `T^j(n)` is odd, `X_(j+1)=3 X_j/2`.
* If `T^j(n)` is even (hence at least 2), `X_(j+1)=(X_j+1)/2`. This is at most `(3/2)X_j` and, **if the even state is at least 6**, then `X_j>=7`, so `X_(j+1)<=4X_j/7=(3/2)X_j·8/21`.

**Lemma 1 (at least one even state in first 82 steps).** If all 82 T steps were odd, then `X_82=3^82(n+1)/2^82` is integral. Coprimality forces `2^82 | n+1`. But `1<n+1<=2^72` for positive n<2^72. Contradiction.

**Lemma 2 (82-step upper bound).** Regardless of parities, `X_82 <= (n+1)(3/2)^82 <= 2^72 · 3^82 /2^82 =3^82/2^10 < 2^120`. The final inequality is the exact integer fact `3^82<2^130`.

**Theorem 3 (98-step upper bound).** If any even state among the first 82 is 2 or 4, all subsequent T values lie in `{1,2}`, so `X_98<=3`. Otherwise the guaranteed even state is at least 6 and Lemma 1 contributes a multiplicative reduction of at least `8/21` against the all-odd growth cap. Therefore
```
X_98 <= (n+1) (3/2)^98 (8/21)
     <= 2^72 * 3^97 / (7 * 2^95)
      = 3^97 / (7 * 2^23) < 2^128,
```
where the strict inequality is equivalent to the independently tested integer inequality `3^97 < 7*2^151`.

**Scope precisely:** For an authentically reconstructed original start `n<2^72`, **if** Rust search3 begins from `X_66=T^66(n)+1`, an exact 16-step table at its first two blocks computes `X_82<2^120` and `X_98<2^128`. Both *results* fit u128; the first result is below the high-state cutoff. This proof is independent of how hard n is and does not require enumerating search1 leaves. It does **not** prove every native intermediate table multiplication order or all later calls; source search1/search2 input identities are not fully audited.

R33's `x=2^120−2^16` (130-bit 16-step result) remains a correct **unrestricted-state** guard insufficiency but does **not** refute this first-two-block theorem. At 98 steps a state can theoretically be below `2^120` while a *third* 16-step operation exceeds `2^128` under arbitrary state arithmetic; whether such a state can occur among authentic accepted 72-bit starts is **UNKNOWN**. No bug in an actual verification run is established. Compile-mode checked/wrapping overflow remains UNKNOWN without actual Rust build identity.

**Required pre-multiply guard for every 16-step block:** compute `s,tail` from the exact low-16 table, `q=number>>16`, and **before** `q*3^s+tail`, demand `q <= floor((2^128−1−tail)/3^s)`. Otherwise reserve an ordered `UNRESOLVED(original_n,event_ordinal,PREMULT_OVERFLOW)` and stop this start, never checksum it. Re-test the bound at every block; the theorem alone is not a permit to omit checks later.

## 3. Bitmap, recursion, and interval mask — precise remaining proof obligations

The 24-bit precompute `main.rs` lines **125–180** combines descent, two-even and predecessor reductions. R33 established genuine local two-even meeting and lookup algebra, **not** that its source `maxval` cleared-bit rule is sound for all `2^24` low words. Outstanding obligations are: exact parity word and maxval at lines 125–180, `numevens` backtrack and `doubleeven` flag recurrences, witness strictly below **original** n, and explicit 99,781 minimum-path hypothesis OR a separately authenticated smaller earlier hit. This session supplies no every-bit proof and does not call samples equivalent to one.

R32's exact `n=r+2^66*a` decomposition establishes unique clipped a **only if** every source search1 low-root is visited exactly once. The actual `search1` branch and flag state invariant is still missing. Proposed fail-closed search2 dispatch, not present in pinned Rust:

```
for each unique search1 low-root r (0 <= r < 2^66):
    # all source exclusion masks still require independently proved meaning
    for a in 0..63:
        original_n = r + (a << 66)  # arbitrary precision in spec
        if not (B <= original_n < E): continue  # BEFORE proof labels, hash, or search3
        if not authoritative_source_mask_proved(r, a):
            emit UNRESOLVED(original_n, reason="UNPROVED_MASK"); continue
        if source_marks_candidate(r, a):
            guard_then_search3(original_n)
        else:
            emit_proof_node_with_original_n_and_independent_witness(...)
```

`B div 2^66=32`, `(E-1) div 2^66=40`: low root `r=B mod 2^66` is below B, yet `r+32*2^66=B`. Dropping roots `r<B` is unsound. The proposed order enforces endpoint exclusion before all labels/dispatch. Native source order, duplicate-free recursion visits and true bitmap predicates remain **SOURCE UNKNOWN**, not certified by this pseudocode.

## 4. Event generation, kernel seals, and independent arbiter

**Versioned specification `R34-EVENT-1` (NOT implemented in production)**: Each original start has an exact manifest leaf ID, and all exceptional operations have a monotonically ordered per-start event ordinal. Each job/task includes immutable `[L,H)`, source and binary SHA-256, map SHA-256 and flags, kernel ID/launch ordinal, device buffer **declared capacity**, reserved/committed exact event counts, overflow flag, return seal and a trustworthy mapping to original_n. A branch emitting print/return, print/reset-to-2, ctz(0), missing lookup, unsigned carry/overflow, invalid shift, or cutoff MUST reserve an UNRESOLVED slot **before** side effects or checksum contributions; failed reservation or append fails the entire launch. The host checks every launch/completion and exact reservation/event count, reports a truncated/corrupt buffer as failure, and rejects ANY unresolved start until independently arbitrated. Sorting raw GPU event order is permitted only with sealed per-original event ordinals.

The accompanying Python fixture uses a separate literal-T path checker, canonical SHA-256 recomputation and a generated-event-count/reservation ledger. It tests an event that was *reserved at simulated production but never emitted* — the arbiter rejects the mismatched commitments. A genuine production branch which omits **both** reservation and event is still invisible to such a test; source **static control-flow coverage / generated instrumentation proof** is mandatory. No claim of complete source emitter is made.

**Repair of an R33 fixture gap:** R33 accepted any `claimed_hash` string and its purported forged-hash hostile mutation simultaneously changed a trace; the resulting rejection was not a test of hash authenticity. R34 recomputes the canonical full-payload hash and tests a signature-only forgery, which correctly fails. This is a toy validator correction; hashes still cannot replace per-start proof checking.

Fixture `python3 research/r3e21_34_guard_arbiter.py` in capped local execution: **R34_TOY_PASS**, 4002 small/boundary start paths through 98 steps; 64-start [103,167) literal-T roster; 20 hostile rejections including missing producer reservation-output event, missing kernel, duplicate/out-of-order ordinal, forged hash only, reset-to-2 bogus edge and an arbitrary 130-bit pre-multiply candidate. These do not represent scientific checking or native source validation. Hosted CI **NOT_RUN**.

## 5. Bařina source path and acceptance gate

A newly located *separate* public `xbarin02/collatz-sieve` map repository documents `esieve-34.lut50.gz` and `h2esieve-24.gz`. An independent outside audit reports possible compressed SHA-256s `450596d8222a30724b732238de69b7fc13779795a52a93528941076a59e200ef` and `b0222a680a7f65a59efd413829cc56668dd5734c099bfc32c356b285a1867fa4`, respectively, **not CEML retrieved or authenticated**. These provide concrete acquisition leads but **NOT** authentic generator-predicate, unpacked-map, build-flag or production identity proofs. Still missing: `IS_LIVE` `USE_SIEVE/USE_LUT50/SIEVE_LOGSIZE` meaning for named builds, `USE_PRECALC` equality `T^R0(N0)=N` under real parity/overflow, actual GPU dispatch/CTZ/segment failures, and actual compiled CPU GMP fallback. Source commit != build artifact.

| Axis | R34 outcome |
| --- | --- |
| 82/98 shifted-T arithmetic bounds | **PROVED for n<2^72** (conditional source-state linkage) |
| Full search3 reachable long-run guard | **UNKNOWN after second block** |
| 24-step bitmap / search1 flags / clipped source order | **UNKNOWN** |
| Bařina map/precalc/CPU-GPU compiled equivalence | **UNKNOWN** |
| Exception emitter in native source | **NOT IMPLEMENTED / NOT PROVED** |
| Independent toy literal-T arbiter and hostile tests | **LOCAL TOY PASS**, not actual worker |
| 20 cold/20 warm source-distinct [2^70,2^70+2^40) benchmark | **NOT_RUN, no authority** |
| Frontier science / actual survivors / independent certification | **NOT_RUN / UNKNOWN** |

**Decision: NO-GO** even to request hardware execution. No owner PC, native verifier, frozen protocol/certificates, scientific batches, website/feed, spending, BOINC recruitment, external contact, publication or submissions. Keep conservative candidate upper unchanged. R35 should close the *third-block reachable-state* gap and pinpoint bitmap predicates/source compilation rather than retest first two blocks.
