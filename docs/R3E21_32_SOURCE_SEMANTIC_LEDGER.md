# R3E21-32 — Source-derived clipped search and adversarial exception ledger

**15 October 2026 | RESEARCH PARTIAL COMPLETE | £0 | NO SCIENCE | NO-GO to request hardware benchmark.**

## 1. Entry, sources, arithmetic and provenance

Entry main `9d8ade853f9777c492ed098495a3ab985b3de3c4` (normal merge of PR #60); reconstructed main tree `3f8660fc1720bc1b0674dd77ad6acd9beebff195` from its recorded parent tree `006b8eb8d49271977f1353f9c945609a6011df26` plus the exactly three PR #60 paths and current blob SHAs. Main combined commit statuses were `[]`: ABSENT, NOT PASS. Full branch protection/ruleset/check-run/open-PR inventory was not re-established this session: UNKNOWN. No owner-machine, science or GPU execution.

Re-read `AGENTS.md`, `PROGRAM_STATUS.md`, `ROADMAP.md`, `docs/CLAIM_POLICY.md`, and R30/R31 source and claim audits; R27–R29 facts remain historical and are not transformed into a new result here. Source pins re-fetched through GitHub:

- Bařina `xbarin02/collatz` commit `141e13aae243d509a01a43bec597f53a5b97a09f`: `src/worker/worker.c` blob `c33a6a86f35a0900ea1df8b7b2dcd30863a9b8bc`, `src/gpuworker/kernel.cl` blob `569e0d1a46433365c822bdf4fb27a61f188cd4b5`. Other R31-pinned host/compat sources not re-fetched independently in this invocation. These are source snapshots, NOT build provenance.
- Angeltveit `vigleik0/collatz` commit `f3f09248c7ae7299b8443e112f565f309d97f161`: Rust `main.rs` blob `4a33b870d27059feea28985e185b8c8c709eb313`; CUDA `collatz_cudav7.cu` blob `a783f0f39ee776c725036caec9c93d15a1c8ca72`. The OpenCL host source remains R31-pinned but was not re-fetched this session. `arXiv:2602.10466` submission history shows **v1 only, 11 February 2026**, and Section 1 acknowledges interval adaptation difficulty.
- Bařina first-party homepage was read 15 October 2026: generated **12:53:31 CEST**, *lowest incomplete* and *lowest unassigned* separately **2175982616 × 2^40**. Its headline `2075×2^60` and its separately published 2025 result `n<2^71` are not interchangeable. The live operational pointer is author-reported, not reproduced by CEML. Homepage is mutable: recheck again next session.

Freeze `B=2392518188130438742016`, `E=3000000000000000000000` EXCLUSIVE, `U=2^40=1099511627776`, `E-B=607481811869561257984 = 552501489 U + 350507499520`. Last partial starts `2999999999649492500480`. Conditional old conservative candidate upper **326518028938128165** UNCHANGED. True inherited and remaining counts UNKNOWN; no new exclusion or scientific convergence was certified.

## 2. Angeltveit low-bit source-to-specification audit

**Proved, independent of machine source.** At `N=M+A` and `[L,H)⊆[1,2^N)`, every start has a unique `(r,a)` where `n=r+2^M a`, `r=n mod 2^M`, `0≤a<2^A`. Its clipped highbits lie in the half-open range

`max(0,ceil((L-r)/2^M)) ≤ a < min(2^A,ceil((H-r)/2^M))`.

The child split at bit `j` is the disjoint union of low-bit residues `r` and `r+2^j`. Exactly the first `j` parity steps are shared between `r` and `r+2^j q`; inductively `T^j(r+2^j q)=T^j(r)+3^{s_j(r)}q` with `s_j` genuine odd steps. This is an exact equality on positive starts; the formal affine extension at `r=0` is the algebraic even-branch zero value, not a scientific Collatz start.

**Additional source-derived identity.** Rust `search2` computes `index = (magicnumbers[s-offset] * (number as u32)) & (2^24-1)` with `number=T^M(r)+1`. Since `magicnumbers` are powers of inverse 3 modulo `2^32`, for each high-bit `a`,

`((number+a·3^s)·3^{-s}) mod 2^24 = (number·3^{-s}+a) mod 2^24`.

Thus consecutive highbits correspond to *consecutive* 24-bit bitvector positions (with cyclic wrap), conditional on the authentic `search1` state and the exact array generator. In the source Rust defaults `M=66,A=6,Blookahead=24`, the bitmap offset is up to 63; the allocated array has `2^(24-6)+1` u64 words, permitting the `index/64+a+1` padded read for `a=0` outer word index. This is a bounds calculation at the source defaults, **not** a certification of every reachable state/alternate constant or GPU conversion. The `search2` caller's low-bound `s≥THREEPOWEROFFSET` must be established from actual `search1` invariant before subtraction, not inferred merely from a toy.

**Mod9 mask identity.** Source precompute sets `redmod9step = 2^M mod9`, then keeps exactly residues outside `{2,4,5,8}`. Since `(r+2^M a) mod9 = (r mod9+a·redmod9step) mod9`, this mask is arithmetically equivalent to those four authentic smaller-preimage exclusions. At `M=66`, the stride is `1` mod9; the initial `B` lies in high block `a=32` (its low residue is `31334946695616135168`), and `E-1` lies in high block `a=40`. A test that retains only low roots `r≥B` would omit `B` completely.

**Genuinely authenticated smaller witnesses.** For `n≡2 mod3`, `p=(2n-1)/3<n`, `T(p)=n`. For `n≡4 mod9`, `p=(8n-5)/9<n`, `T^3(p)=n`. At `n=15`, the shortened path reaches `20` in six steps, while `13<15` maps to `20` in one step; the odd-run/two-even witness `7=(15-1)/2<15` also shares `20` with 15. These are sound sample identities, not a validation of all Rust `numevens`, `doubleeven`, cutoff and `initialbitarray` branch decisions.

**Still unproved (NO-GO):** source `search1` pruning equivalence, all `doubleeven`/path-merging gates, the entire `precompute()` 24-step `maxval/cutoffs` bitmap meaning, `THREEPOWEROFFSET` assumptions in all calls, theorem 4.1/4.4's **99,781 minimum-state condition OR authenticated earlier-small-hit escape**, valid complete 16-step search3 table/lookup, correct application of the clipped a-mask **after all masks and before every search3 dispatch**, exact Rust 72-bit and retuned CUDA/OpenCL equivalence, and durable capture of all exceptional starts. Small toy tests cannot prove these universally.

The Rust source defaults `MAXBITS=72`, `LASTBITS=6`, `STEPSIZEINITIAL=24` and `search1→search2→search3`. CUDA/OpenCL source defaults at `MAXBITS=45` and different 32-bit layout; changing `MAXBITS` is a new implementation needing proofs of carries, shifts, allocation and kernel dispatch. Rust `search3` prints base and returns upon a high-state limit, without a certified smaller witness. CUDA source prints original limbs then resets its arithmetic state to 2 at cutoff. Both are **UNRESOLVED**, never a successful descent by declaration.

## 3. Bařina class3 and accelerated branches

**Proved mathematical cover.** Every positive `n>1` outside class `3 mod4` has a direct descent or smaller preimage: even n descends once, `1 mod4` descends in two steps, and class `3 mod4` remains the superset of explicit obligations; optional `n≡2 mod3` / `n≡{2,4,5,8} mod9` removals use the exact preimage witnesses above. For arbitrary positive half-open `[L,H)`, class3 is `3+4t` for `ceil((L-3)/4)≤t<ceil((H-3)/4)`; for aligned endpoints the +3 loop must use **H+3 exclusive**. The final partial cannot be accepted through an unmodified fixed-size task bound. CPU `USE_PRECALC` generates `N0=(task_id<<task_size)+(h<<R0)+L0`, and a compressed state `(H>>R0)*3^Salpha+L`; the missing proof is `T^R0(N0)=N` with a fully authentic parity prefix and no shifted unsigned overflow for every h. In the source this logic exists under `USE_PRECALC` and `USE_SIEVE`, not in the bare loop.

**Source branch audit (NOT build proof).** CPU branch without `USE_PRECALC`: `solve_task` enumerates +3/stride4, with `USE_SIEVE`, `USE_SIEVE3`, `USE_SIEVE9` conditionally compiled. With `USE_PRECALC`: sieve map is applied to R lowbits then `precalc` and `calc`, and `USE_SIEVE3/9` tests N0 in `calc`. `USE_LUT50` changes `GET_INDEX/IS_LIVE` table encoding; map file names are `esieve-K.map` vs `esieve-K.lut50.map`. Optional SIEVE_LOGSIZE, actual map-generator bytes and map hash are **not pinned here**; no assertion that every cleared map bit has a certified smaller witness. CPU `_USE_GMP` selects arbitrary-precision fallback; absent it, the source prints `ABORTED_DUE_TO_OVERFLOW` and aborts. GPU OpenCL kernel partitions `n_minimum` and `n_supremum` per global id using `(task_size-task_units)`, iterates class3, applies bitmap/optional modulus masks, then on overflow zeroes checksum and exits; `gpuworker` abort/fallback semantics and all launched workgroups are **UNPROVED**. CUDA/OpenCL/host branches were not compiled.

First build/semantic blocker for each variant: **CPU bare**—exact interval wrapper, CTZ/overflow and per-start completion instrumentation; **CPU map/LUT50**—source-to-map-generator bit meaning + immutable map/build flags; **CPU precalc**—authentic `T^R0` equality for every h and no overflow; **GPU**—complete per-workgroup roster and never-silent exceptions, 128-bit bounds and kernel/build equivalence. None passes a 2^40 arbitrary interval source-equivalence review.

## 4. Adversarial exception conservation and finite fixture

Define `D=[L,H)` as a disjoint partition into individually certified **PROVED** earlier descent/preimage leaves, individually **RESOLVED** literal-T strict descents or independently certified coalescence, and **UNRESOLVED** original starts/events. A completed unit requires every start represented once, source-specific rejection leaves proved, every dispatched kernel acknowledged, and zero unresolved. Never infer completeness from a checksum, lack of printf output or a worker returning normally. Multiple events for one start are an ordered stream `(original_start,event_ordinal,reason,operation,exact_state)` but represent one unresolved original start until independently arbitrated.

A bounded independent Python standard-library fixture was executed outside GitHub in this session. It enumerated **112** diverse clipped toy windows (M=2…8, A=1…4), confirmed a unique exact [L,H) roster, verified literal shortened-T parity-affine prefixes, proved congruence between source-style mod9 mask and direct residues, and checked exact modulo-2^24 inverse-3 index transport. It checked the true mod9/inverse rules across toy inputs and accepted one 64-start [103,167) independently traced/proved roster. Output `R32_TOY_PASS clipped_windows 112 toy_starts 64`. Adversarial cases REJECTED: truncated frame, omitted/duplicated/reordered start, false witness, recomputed valid hash covering false witness, silent reset-to-2, falsified bitmap rule, missing kernel completion, u128 multiply overflow, ctz(0), illegal 32/64/128-bit shifts, missing 32-bit limb carry, out-of-range lookup and bogus early descent. The test script was executed in the ephemeral session sandbox; **not** a built/pushed binary, proof of source exception capture or hosted CI result. Any positive toy result is `TOY_ONLY`, never a frontier verification.

**Important threat separation:** a full roster already formed independently can detect missing *records*, but cannot establish that the producer exposed every source skip/exception branch. In particular a genuine exceptional kernel that reports a normal checksum without appending an event is indistinguishable to a hash-only validator. Required addition is branch-covered, fail-closed source instrumentation, complete kernel launch/completion indices, sealed device-to-host buffer lengths/overflow flags, no asynchronous truncation, and an independently executed arbitrary-precision literal-T arbiter for every exceptional start. A BOINC quorum, second GPU with the same algorithm, or equal XORs do not prove semantic coverage or error independence.

## 5. Acceptance matrix and owner-only performance gate

| Component | Mathematical interval cover | Source/build equivalence | Exceptions | Accepted? |
|---|---|---|---|---|
| Bařina CPU bare | class3/residue theorem PROVED | incomplete task adapter and overflow/build proof | incomplete | NO |
| Bařina CPU map/precalc/LUT50 | residue theorem only; bitmap UNKNOWN | generator+precalc+flags UNKNOWN | GMP flag-dependent | NO |
| Bařina OpenCL GPU | class3 formula PROVED | dispatch+mask/CTZ/128 unknown | checksum abort, no full ledger | NO |
| Angeltveit Rust 72 | clipped low-bit theorem / mod9 and index algebra PROVED | 24-step bits, search1/3 complete equivalence UNKNOWN | print/return unresolved | NO |
| Angeltveit CUDA/OpenCL 45 defaults | B out of domain | retune/carries/launch UNKNOWN | print/reset, nondurable stdout | NO |
| Independent literal-T big-integer arbiter | toy exact per start | accepted large-scale implementation absent | only effective if full roster known | NO |

Required independence includes the *mathematical* exclusion argument, source implementation, 128-bit representation, compiler/driver, independent task roster, per-start exception stream, and CPU arbitration. Build identifiers must include pinned commit, flags/macros, compiler, driver, device/GMP, binary/kernel/map digests, exact [L,H), source version and immutable receipt. Mismatch -> **STOP/UNKNOWN**, not a silent pass.

Previously covered candidate interval `[2^70,2^70+2^40)` is held as a **NOT_RUN owner-only hypothetical benchmark**: 20 cold plus 20 warm timings *per accepted source build*, raw timestamps/results, independently checked p50/p95, failures, cancellation, costs and immutable runtime manifest. No source-equivalence gate passed, hence do not request benchmark execution yet. No cost or throughput forecast extrapolated from the website's five-second rate to Angeltveit.

## 6. Final decision and smallest next deliverable

**NO-GO even to request separate GPU permission.** The newly authenticated inverse-3 bit cursor and mod9 clipping do not establish that the complete `initialbitarray` skip predicates preserve every would-be checked start, or that every high excursion is recorded. **Smallest proof target:** for one fixed Angeltveit Rust 72-bit `search2` state, prove the 24-step bitmap's entire cleared-bit meaning against *literal T or a strictly smaller explicit meeting witness*, with exact 99,781 earlier-hit treatment, array bounds and clipped a-mask, plus a fail-closed high-value exception path. Then handle `search1`, continuation and the remaining source branches. Separately, establish Bařina's map-source identity and true prefix for `USE_PRECALC`; do not mistake faster code for a verified interval.

No scientific run, paid GPU, owner PC, native/frozen verifier, certificate, website/feed, experiment publication, BOINC recruitment, contact, spending, formal Lean or global Collatz proof occurred. Conditional candidate upper remains **326518028938128165**, actual survivors UNKNOWN.
