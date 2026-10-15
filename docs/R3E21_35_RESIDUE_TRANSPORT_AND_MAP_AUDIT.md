# R3E21-35 — single-residue u128 hazard, authentic state transport and named source/map build audit

**15 October 2026 | RESEARCH-ONLY PARTIAL ADVANCE | £0 | NO SCIENCE | NO-GO even to request benchmark permission.**

## Scope, entry and evidence classes

Owner instruction "Run next session" authorises R35 alone. Entry CEML main `f87244fff819bc12feb49acf9ea85292ccb9efa8` (R34 merge). Read `AGENTS.md`, `ROADMAP.md`, `PROGRAM_STATUS.md`, `docs/CLAIM_POLICY.md`, R31–R34 reports, and the R34 fixture. No native worker, GPU, published verifier, frozen identity, website/feed, remote cloud or owner machine was changed. No frontier workload was run. Combined commit statuses at entry `[]`: **ABSENT ≠ PASS**; branch protection and independent check-runs not proved. R34's forged-only-hash rejection and R33's trace-mutating fake forgery have been reconciled; a digest is neither full event conservation nor per-start proof.

**Foreign source genuinely re-fetched, not inherited alone:**

* `vigleik0/collatz` commit `f3f09248c7ae7299b8443e112f565f309d97f161`: `main.rs` blob `4a33b870d27059feea28985e185b8c8c709eb313`; `collatz_cudav7.cu` `a783f0f39ee776c725036caec9c93d15a1c8ca72`; `collatz_openclv2.cpp` `5cbe2c1e1958cf3b2ae1224ed3f1defe19db7fdc`. Source comment proposes CUDA `nvcc -std=c++17 -O3 -arch=sm_86 -maxrregcount=34` (example, **not an observed compiled binary**); OpenCL host proposes `g++ -std=c++17 -O3 -DNDEBUG ... -lOpenCL` (example only). Actual executable, compiler and flags **UNKNOWN**.
* `xbarin02/collatz` pinned `141e13aae243d509a01a43bec597f53a5b97a09f`: `src/worker/worker.c` `c33a6a86f35a0900ea1df8b7b2dcd30863a9b8bc`, `src/gpuworker/kernel.cl` `569e0d1a46433365c822bdf4fb27a61f188cd4b5`, `src/gpuworker/gpuworker.c` `eb1bcfd3ea4397999e1d5d3c8dd2c500db1015f2`; `scripts/bootstrap.sh` `70dfe2936a003c5bf45c61ce34f4db0f39c0c4e2`; `src/worker/Makefile` `6714f397f8d08668cc787a3b84ae8ed205cf8dd0`.
* Separate `xbarin02/collatz-sieve` default tip displayed by GitHub search `e5f0c264ba1f5f9c0a7d32a10c3aa61b225c70d1`: `src/sieve.c` blob `48d81fbd3fe2b21344dd24b72febc346dc642361`; `src/fsieve.c` `a0a2386584f7c3db4074044373c9bdea0056bdb1`; `src/Makefile` `d9379f3286c3ab95279b87313237a27afc349485`; `README.md` `6dea60db39f1053ec5551f367764e6f207f52952`. These are **distinct generator candidates** and **not yet connected by a reproducible command/digest** to the named `esieve-34.lut50` and `h2esieve-24` compressed files.
* Angeltveit arXiv:2602.10466 **v1 only, 11 February 2026** in the submission history. Theorems 4.1/4.4 and the 99,781 low-state alternative are **not** newly certified by this session. Bařina 2025 peer-reviewed `n<2^71` and the mutable homepage pointer remain distinct.

Bařina's live first-party homepage, **generated Thu 15 Oct 2026 15:29:21 CEST**, separately reports first incomplete = `2175982616 × 2^40`, first unassigned = **the same**; both **author-reported, NOT reproduced by CEML**. External B=`2392518188130438742016`; exclusive E=`3000000000000000000000`; U=`2^40`; 552501489 complete units plus 350507499520-start last partial; conditional conservative candidate upper **326518028938128165 UNCHANGED**; actual survivors **UNKNOWN**. First incomplete and first unassigned must never be conflated even when numerically equal.

## Theorem A: complete classification of the *arithmetic* 16-step overflow hazard below the native cutoff

Let `X=T^j(n)+1`, `0<X<2^120` at entry of any Rust search3 loop. Decompose `X=2^16 q+r` with `0<=r<2^16`. The source precompute encodes 16 steps as `(s(r),c(r))`, producing the exact integer `Y=q·3^s+c`. The low-residue map is the shifted map: even `x` -> `3x/2`, odd `x` -> `(x+1)/2`. Its formal zero sentinel is valid algebraically in the lookup even though real X>=2.

**Lemma A1.** For every 16-bit residue, `0<=c(r)<=3^s`. To prove: after i steps on `r` with s growth steps, maintain `x_i<=3^s 2^(16-i)`. At an even `x_i`, the next value is `3x_i/2`; at an odd `x_i` the integer upper bound is even for `i<16`, so `x_i<=bound-1` and `(x_i+1)/2<=bound/2`. Thus `c<=3^s`. Moreover `s=16` iff `r=0`: 16 all-growth steps require `2^16|r` because gcd(3,2)=1, and r is a 16-bit residue.

**Theorem A2.** If `s<=15`, then `q<=2^104-1` and
`Y<= (q+1)3^s <= 2^104·3^15 <2^128` (strict `3^15<2^24`). Thus **no u128 multiply OR addition can overflow for any of 65535 nonzero low residues** at any search3 loop whose entry is below `2^120`. If `s=16`, necessarily `r=c=0`, and overflow happens iff
`q >= floor((2^128-1)/3^16)+1`.
The **smallest purely arithmetic dangerous X** is
`518059092085797269936906884792713216`, a multiple of `2^16` strictly below the source cutoff. This is a generic shifted-state candidate, **not** a constructed authentic `n<2^72`.

For every search3 block after the first, the prior successful block has either returned after a strict original descent, returned due to `X>=2^120`, or re-enters with `X<2^120`. The first entry `X_66<2^111`. Hence **all later potential pre-multiply overflows are confined to the single exact residue/threshold above**, provided source state transport is authentic. This does not exclude such a state from actual trajectories. The native guard remains post-multiplication and is therefore structurally insufficient as a general safety proof. Debug/release/Rust compiler behaviour unverified.

## Theorem B: source search1/search2 *state transport*, not pruning validity

Rust `main.rs` begins `search1(3,2,2,9,0,0,...)`. For the shortened T map, `T^2(3)+1=9` and both steps are odd. Claim invariant for every reached recursion node `(base,j,k,number)` before any pruning: `number=T^j(base)+1`, `base≡3 (mod4)`, `base<2^j`, k equals the number of odd shortened-T steps in the j-prefix for all starts sharing base modulo `2^j`, and **for each high-bit lift** `a`: `T^j(base+2^j a)+1=number+3^k a`.

Induction: adding `2^j` changes the shifted state by `3^k` and exchanges parity since `3^k` is odd. Each `search1` left/right child in source adds either zero or `3^k` to `number` and applies exactly the appropriate shifted even/odd map. Its child index fixes the new bit at `2^j`. The binary children are disjoint and exhaustive among starts congruent 3 mod4 **before pruning**. At `j=66`, `search2` lifts `base+highbits·2^66` and `number+highbits·3^k`, reproducing authentic `X_66` for all `0<=highbits<64` without duplicate roots, conditional on branches admitted. Since `n+1<=2^72` and `X_j<=(n+1)(3/2)^j`, all j<=66 intermediate lifted states are <`2^111` (check `3^66<2^105`); native u128 search1/2 additions/products of these values cannot overflow. This **discharges R34's state-transport premise** and makes its proved 82/98 bounds applicable to authentic candidate starts.

This proof **does not establish that any source pruning is sound**, nor that `number <= base`, `306j>=485k`, `numevens`, `doubleeven`, the 24-bit bitmap, a-mask and mod9 ordering together emit **all required candidates**. The source is a whole-prefix programme and has no certified `[B,E)` adapter. For any accepted low root `r`, always apply clipped `a` in 0..63 with `B<=r+2^66 a<E` **before a proof label or dispatch**. At B, `a=32`, `r=B mod2^66 <B`; filtering roots on r>=B loses B.

## Search3 third block and beyond: precise unresolved reachable question

R34 proves `X_82<2^120`, `X_98<2^128` for all authentic `n<2^72`. This session sharpens the only possible native overflow **from the third 16-step block onwards** to an entry `X_j` such that `j>=98`, `X_j<2^120`, `X_j≡0 (mod2^16)`, and `X_j>=518059092085797269936906884792713216`, while the original trajectory has never strictly descended or tripped the cutoff and survives source1/2 masks. **No authentic witness is supplied and no all-path impossibility proof is claimed.**

A full resolution needs a proof-producing sparse-parity cylinder search or a sharper bound respecting n<2^72 and all earlier predicates. For the third block specifically, large `X_98` forces very few even T-steps in the first 98. The cheap R34 large-even penalty already shows that **eight or more even states >=6 among those 98** force `X_98` below the dangerous threshold; a small even state 2 or 4 forces entry into the 1↔2 loop. Cases with at most seven even steps remain an explicitly **unsearched** finite domain, not an implicit PASS. We did not run a gigantic unbounded enumeration or any frontier work.

**Mandatory proposed Rust source pseudopatch** (NOT production): at each lookup decode s and c, set q=number>>16, compute `limit=(u128::MAX-c)/THREEPOWERSU32[s]` without multiplication; if q>limit, atomically reserve `UNRESOLVED(original_n,ordinal,PREMULT_OVERFLOW,exact_pre_state)` and terminate this original start **before** mutation/checksum. Otherwise perform checked_mul then checked_add (or proven guard + widened exact reference), and explicitly reserve `HIGH_CUTOFF` on the print/return path instead of treating tally as success. For a missing event slot, fail closed at launch level. The exact strict-descent witness is the first later state X<original base, not a printed large state.

## 24-bit bitvector and source mask obligations (partial)

Source `precompute` lines 125–180: it constructs each low 24-bit shifted parity pattern, computes `curval,maxval,numevens,doubleeven`, and sets a live bit when `maxval<=firstcutoff+485a` (a=0..7), with firstcutoff `485·42−306·66=174`. `ONETHIRD=2863311531≡3^-1 (mod2^32)`. Multiplication by this odd inverse is a permutation modulo `2^24`; `search2` index `3^-k·number (mod2^24)`, then the bit for high lift h is index+h (mod `2^24`), matching the shift `number+h·3^k`. The extra padded 64-bit word permits wrapping and the 64-bit `LASTBITS=6` read. Mod9 set bits mean **LIVE** residues `0,1,3,6,7 (mod9)`, which is the complement of proven predecessor exclusions `2,4,5,8`. Arithmetic and index direction are sound.

**NOT PROVED**: every one of the `2^24` source `maxval` decisions, complete doubleeven and numevens original-start witness, low-state 99,781 alternative in Theorems 4.1/4.4, combined mask polarity at every source branch, exact recursion pruning semantics and code-level clipped interval implementation. Capped samples are not an every-bit proof. The 24-bit bitmap therefore remains a source-verification blocker.

## Bařina source-specific named build, map and compiler blockers

A **named bootstrap.sh build recipe** (source recipe, NOT an attested production build): CPU `make -C worker clean all USE_LIBGMP=1 CC=$CC USE_SIEVE=1 USE_PRECALC=1 SIEVE_LOGSIZE=34 USE_SIEVE3=0 USE_SIEVE9=1 USE_LUT50=1`; GPU `make -C gpuworker clean all CC=$CC TASK_UNITS=16 [or hostname-dependent 20] SIEVE_LOGSIZE=24 USE_SIEVE3=1`. `bootstrap.sh` calls `unpack.sh esieve-34.lut50` into CPU directory, `unpack.sh h2esieve-24` into GPU directory then renames `h2esieve-24.map` to `esieve-24.map`. This is a meaningful concrete source-to-file **path**, not an authenticated actual map byte digest or runtime binary flag provenance.

CPU `worker.c`: under `USE_SIEVE`, ordinary map uses bit `(map[(n&mask)>>3] >> (n&7)) &1`. `USE_LUT50` instead reads 6-bit-block dictionary index and dictionary bit `dict[map[(n&mask)>>6]] >> (n&63)`. A 1 means **live** in both; those encodings are not interchangeable. The generator `sieve.c` writes `sieve-K.map`, NOT directly `esieve-K.lut50.map`, and `fsieve.c` writes `fsieve-K.map`; the precise production `esieve` derivation, compressed-to-unpacked digests, generated map version, and bit soundness remain **UNKNOWN**. `sieve.c` implements a potentially valid `T^k(a·2^k+b)=a·3^c+d` kill using `3^c<2^k` and `3^c−2^k < b−d` for a>=1, plus same-(c,d) smaller low-root merging. These explain a generator family, not proof that an actual deployed map is its output.

`USE_PRECALC`: `N0=(task_id<<task_size)+(h<<R0)+L0`, calculated `N=(H>>R0)·3^Salpha+L`. The abstract affine T^R0 parity-prefix identity is well-founded, but source `precalc` uses `L++`, `ctzu64`, `L--`, clamped alpha/beta and asserts. Proving `T^R0(N0)=N` for **every actual accepted prefix**, with no wrap, map guard and all macros, remains UNKNOWN. CPU `_USE_GMP` fallback is selected by `USE_LIBGMP=1` in this *script recipe only*; it is NOT evidence a particular deployed binary has GMP. GPU `kernel.cl` runs `IS_LIVE`, `ctz((uint)n)`, source ctz/overflow guards and a segment checksum; host `gpuworker.c` needs complete launch/write/read/status/workgroup and GMP CPU fallback receipts. Host and GPU independently fail-closed proof remains missing.

The R34 suggested compressed digests are leads only, **NOT reverified**. No final map SHA-256 or binary SHA-256 is asserted. No actual per-start `IS_LIVE` bit source has been independently certified for those named build recipes.

## Fail-closed exceptions: versioned research-only specification R35-EVENT-2

For *each* source variant Rust, CUDA, OpenCL/CPU Bařina, an implementer must first create a manifest `original_n`, immutable exact interval, source/build binary/map hash and compile flags, kernel group/id/launch ordinal, expected roster, reservation count, capacity and sealed completion. The **production-side** control-flow branches `print+return`, `print+reset-to-2`, `ctz(0)`, `invalid lookup/index/shift`, `unsigned carry/borrow`, `multiply overflow`, `GPU overflow checksum reset`, `GPU launch/readback failure`, `CPU fallback unavailable` must all **reserve before mutation** and append typed `UNRESOLVED(original_n,ordinal,operation,pre_state,reason)`. Failed reservation or buffer-full => atomic launch failure, never a success tally. Host requires every expected launch sealed, exact reservation/event count, no dropped device output, no duplicate/unknown original start, and independent literal-T resolution (arbitrary precision) of each exceptional start. A converted exception must retain its immutable original identity and original event history.

**Crucial negative:** a malicious/buggy producer dropping event **alone** is detectable when reservation count survives; a producer dropping reservation **alone** is detectable when event survives; a producer secretly dropping **both** is undetectable by any producer-supplied count+payload hash. Hence source static control-flow path coverage, instrumentation and an independently constructed per-start roster are a hard prerequisite; no checksum, digest or quorum can fill that gap. No production patches are applied and no genuine exception stream has been collected.

## Reproduction / evidence matrix

Local standard-library `python3 research/r3e21_35_residue_transport.py` was modeled and independently exercised against identical arithmetic; **R35_TOY_PASS**: all 65,536 sixteen-bit residues, binomial `C(16,s)` counts, exact danger threshold, 2,047 binary recursion nodes lifted across four highbit classes, and separately rejected loss of event and reservation; demonstrated joint omission still accepted by the toy producer ledger. **No source compilation, full 2^24 bitmap, per-start production event generation, CI or science.**

| Axis | R35 result |
|---|---|
| Search1/2 lifted numerical state, no u128 overflow through j=66 | **MATHEMATICALLY PROVED**, independent of pruning masks |
| Rust u128 safe for every later entry X<2^120 with low16 !=0 | **MATHEMATICALLY PROVED** |
| First two continuation blocks X82, X98 | **R34 PROOF NOW SOURCE-STATE LINKED** |
| Third-block and all later low16=0 authentic reachable danger | **UNKNOWN**, exact arithmetic condition isolated |
| All-source 24-bit bitmap, doubleeven/numevens, 99,781 condition | **UNKNOWN** |
| Clipped [B,E) source implementation and exact original-start roster | **NOT IMPLEMENTED** |
| Named Bařina recipe flags and map file routing | **SOURCE-REVERIFIED; NO ATTESTED BINARY/MAP DIGEST** |
| CPU map bit source, precalc, GPU and fallback equivalence | **UNKNOWN** |
| Exception event production coverage and independent full arbitration | **NOT IMPLEMENTED** |
| Bounded independent arithmetic/loss fixture | **LOCAL TOY PASS; hosted CI ABSENT/NOT_RUN** |
| 20-cold/20-warm each-source benchmark [2^70,2^70+2^40) | **NOT_RUN; not authorised** |
| External frontier reproduction / new [B,E) verified starts | **NOT_RUN / UNKNOWN** |

**Decision NO-GO** to request hardware benchmarking, crowd deployment or frontier science. Preserve benchmark spec, all prior science, and frozen records. R36 is a **new future/unexecuted prompt**, not implied authority.
