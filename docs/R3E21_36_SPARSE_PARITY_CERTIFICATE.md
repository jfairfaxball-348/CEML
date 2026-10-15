# R3E21-36 — 114-bit sparse parity-cylinder certificate: third Rust block safe

**15 October 2026 | RESEARCH ONLY / £0 / NO SCIENCE | substantial computer-assisted mathematical advance, source/build remains NO-GO.**

## 0. Claim boundary and provenance

This R36 session was invoked by the owner's "Run next session" and executed R36 only. Entry CEML main `ef83fe7b876692c38e0dc95837313360aee5f1f1`; entry open PR inventory empty, combined commit statuses `[]` = **ABSENT**, associated workflow runs `0` = **ABSENT/NOT RUN**, not PASS. No owner PC, local science batches, native production source changes, distributed client work, hardware benchmark, spending, V2/I1 identity, website/feed or publication submissions.

Read `AGENTS.md`, `ROADMAP.md`, `PROGRAM_STATUS.md`, `docs/CLAIM_POLICY.md`, R31–R35 reports and R34–R35 research fixtures. Source-reverified (GitHub fetch at named immutable commits, not compiled identities):
- Angeltveit `vigleik0/collatz@f3f09248c7ae7299b8443e112f565f309d97f161`: `main.rs` blob `4a33b870d27059feea28985e185b8c8c709eb313`; `collatz_cudav7.cu` `a783f0f39ee776c725036caec9c93d15a1c8ca72`; `collatz_openclv2.cpp` `5cbe2c1e1958cf3b2ae1224ed3f1defe19db7fdc`. Exact Rust search3 after-operation guard and 24-bit precompute reviewed. Proposed CUDA/OpenCL compile flags are recipes, not observed binaries.
- Bařina `xbarin02/collatz@141e13aae243d509a01a43bec597f53a5b97a09f`: `scripts/bootstrap.sh` `70dfe2936a003c5bf45c61ce34f4db0f39c0c4e2`; `src/worker/worker.c` `c33a6a86f35a0900ea1df8b7b2dcd30863a9b8bc`; `src/worker/Makefile` `6714f397f8d08668cc787a3b84ae8ed205cf8dd0`; `src/gpuworker/kernel.cl` `569e0d1a46433365c822bdf4fb27a61f188cd4b5`; `src/gpuworker/gpuworker.c` `eb1bcfd3ea4397999e1d5d3c8dd2c500db1015f2`.
- Separate `xbarin02/collatz-sieve@e5f0c264ba1f5f9c0a7d32a10c3aa61b225c70d1`: `src/sieve.c` `48d81fbd3fe2b21344dd24b72febc346dc642361`; `src/fsieve.c` `a0a2386584f7c3db4074044373c9bdea0056bdb1`; `src/Makefile` `d9379f3286c3ab95279b87313237a27afc349485`. These sources are not evidence of generated/deployed map hashes.

External status **first-party author report, not CEML reproduction**: Bařina homepage generated Thu 15 Oct 2026 16:30:17 +0200 separately lists first incomplete and first unassigned both `2175982616 * 2^40`. The already frozen baseline is `B=2392518188130438742016`, exclusive `E=3000000000000000000000`, `U=2^40`, exactly 552501489 full units plus 350507499520 starts in the partial. Mathematical conditional **old** candidate upper `326518028938128165` **UNCHANGED**; actual survivors **UNKNOWN**. Published Bařina 2025 `n<2^71` is a separate peer-reviewed tier (DOI 10.1007/s11227-025-07337-0); Angeltveit arXiv:2602.10466 still lists v1, submitted 11 February 2026. Neither is CEML frontier evidence.

## 1. New result: an authentic third Rust search3 block cannot overflow u128

Use shortened `T(n)=n/2` for even n, `(3n+1)/2` for odd n, and `X_j=T^j(n)+1`. R35 establishes exact source transport to X66; R34 proves the first two continuation results satisfy `X82<2^120`, `X98<2^128`. R35's **unrestricted-state** precise overflow criterion for a search3 entry `0<X<2^120` is

`X % 2^16 == 0` and `X >= D=518059092085797269936906884792713216`.

We prove a **finite computer-assisted theorem**: for **every** positive `n<2^72`, `X98` cannot satisfy both conditions. It follows that if source search3 reaches the third 16-step block under authentic state transport and the preceding source cutoff, its exact `q*3^s+c` lies within u128; an authentic third-block overflow is impossible. This is not a claim about blocks four and beyond, source bitmap/pruning, or a compiled binary.

### 1.1 Reduction to seven or fewer even T-states

For positive T-state `z`, if odd then `X_next=(3/2)X`; if even then `X_next=(X+1)/2`. If z=2 or 4, the path enters the {1,2} cycle immediately and X98<=3, hence cannot meet D. Otherwise every even T-state is at least 6, making the ratio to the all-odd multiplier at most `(1+1/7)/3=8/21`. If at least eight even states occur in the first 98 steps then

`X98 <= 2^72*(3/2)^98*(8/21)^8 < D`,

where the strict inequality has been checked by **exact integer cross multiplication**:
`2^72 * 3^98 * 8^8 < D * 2^98 * 21^8`.
Thus only 0..7 even states in the first 98 steps could be hazardous. No heuristic probability is used.

### 1.2 A 114-bit exact inverse parity-cylinder congruence

If `X98 % 2^16=0`, the next 16 genuine T-states are all odd (the shifted even X is repeatedly transformed by 3X/2; its 2-adic valuation drops by exactly one each step). Choose the `m<=7` positions of even T-states among steps 0..97:
`0<=e_1<...<e_m<=97`. Steps 98..113 are odd. Every such 114-step parity word uniquely specifies the start `X0=n+1` **modulo 2^114**. An induction on the affine parity recurrence gives

`X0 == -sum_{k=0}^{m-1} 3^k * (2*3^(-1))^(e_{k+1})  (mod 2^114)`.

The inverse `3^(-1)` exists modulo `2^114`. This is an identity for each 114-step parity cylinder, not an assumption that a word is attainable by a bounded start. An actual `1<=n<2^72` would require its representative `X0` in the **inclusive range** `[2,2^72]`.

### 1.3 Lossless meet-in-the-middle certificate

The committed fixture `research/r3e21_36_sparse_parity_mitm.py` tests **all**
`sum_{m=0}^7 binom(98,m)=14,958,711,636` words. It groups the first floor(m/2) zero positions and the remaining positions: the left list is sorted by the exact 114-bit sum; the right side is streamed. Each right tuple's required left residues lie in an exact modular interval; wrapped intervals split into two ordinary ranges, binary searched without approximation. An explicit `last(left)<first(right)` condition rejects non-increasing or overlapping position tuples. This pair partition is bijective with the complete allowed position family.

Exact per-m counts, **zero** residues in [2,2^72] for every count:

| even positions m | number of words | compatible bounded X0 |
|---:|---:|---:|
| 0 | 1 | 0 |
| 1 | 98 | 0 |
| 2 | 4753 | 0 |
| 3 | 152096 | 0 |
| 4 | 3612280 | 0 |
| 5 | 67910864 | 0 |
| 6 | 1052618392 | 0 |
| 7 | 13834413152 | 0 |
| **total** | **14958711636** | **0** |

Actual fixture run, local capped ordinary research CPU: **R36_MITM_PASS**, all m, no matches; ~11.2 s and 133144 KB peak RSS on this environment. Maximum left group is `binom(98,3)=152096` entries; maximum right streaming family is `binom(98,4)=3612280`, ~3.93 million binary-range probes across m, and recursion is bounded depth 4. No 2^72 candidate traversal or frontier run occurred. A separately written bounded C++ 128-bit modular version independently returned zero hits for all eight m groups; the committed Python remains the canonical portable stdlib certificate. Independently checked miniature settings `(J,W,N,mmax)=(10,14,7,3),(12,16,8,4),(14,20,8,4)` against literal-T brute force: exact match in all three; the fixture also tests the derived congruence on every `n<2^12` with at most seven even states in its first 12 steps.

**Evidence tier:** rigorous exact arithmetic reduction plus auditable exhaustive finite **computer-assisted** certificate, locally run. **Not** Lean/formally verified; no external replication, GitHub CI or production-source equivalence is implied. A future independent implementation/CI is desirable before upgrading claim language.

### 1.4 Other loops

R35's all-loop arithmetic classification remains valid, but **blocks j>=114 are UNKNOWN** for authentic reachability. The 114-bit sparse-word argument fixes j=98 and cannot be silently extrapolated: longer trajectories can accumulate more even states while entering a later dangerous 16-step cylinder. Until an all-j invariant or a separately complete finite search is proved, pre-multiplication guards remain mandatory on **every** block.

## 2. Lower-root interval clipping and pruning boundaries

For `M=66,A=6`, every candidate `n<2^72` has a unique `n=r+2^66*a`, `0<=r<2^66,0<=a<64`. Correct half-open clipping for [B,E) is exactly
`max(0,ceil((B-r)/2^66)) <= a < min(64,ceil((E-r)/2^66))`,
with ceiling division interpreted over arbitrary signed integers. At B, `r=31334946695616135168` and `a=32`; pruning based on `r<B` **drops the actual lower endpoint**. R35's recursion/lift state invariant and index shift remain accepted as proven; **the full source pruning validity of `number<=base`, `306j>=485k`, `numevens`, `doubleeven` and the combined bit arrays remains UNKNOWN**. An integer n cannot earn a certified exclusion merely because a source branch did not enumerate it.

## 3. Twenty-four-bit bitmap — precise blocked certification

Pinned `main.rs` precompute at lines 125–180 visits `2^24` low shifted-X residues with `upordown`, `curval`, `maxval`, `numevens`, `doubleeven`; the eight ceilings are `174+485*a`, `a=0..7`. The multiplier is inverse 3 modulo `2^24`; wrapped padded bitmap addressing and mod-9 **live** polarity follow R32/R35. The 24-bit loops are source-specified, not independently oracle-replayed this session. The exact premise that **every cleared bit** entails a genuine strict original-start descent or a valid earlier-smaller-preimage witness remains **UNKNOWN**. Theorems 4.1 and 4.4 and the 99,781 low-state hypothesis were not checked against the entire bitmap. No source-specific false exclusion has been found, and no universal soundness proof is claimed. In particular, a lookup checksum or samples would not prove all 16,777,216 entries.

## 4. Bařina map and recipe audit: versioned missing links

Pinned `bootstrap.sh` names CPU `USE_LIBGMP=1 USE_SIEVE=1 USE_PRECALC=1 SIEVE_LOGSIZE=34 USE_SIEVE9=1 USE_LUT50=1` and GPU `SIEVE_LOGSIZE=24 USE_SIEVE3=1`. These are **recipe flags only**, not demonstrated runtime compile identities. The script uses `unpack.sh esieve-34.lut50` and `unpack.sh h2esieve-24` (renamed GPU `esieve-24.map`). The separate first-party `collatz-sieve` `sieve.c` writes `sieve-K.map`, while `fsieve.c` writes `fsieve-K.map`. Neither filename/path authenticates the CPU LUT50 `esieve-34.lut50.map`, its encoder/dictionary, generator command, actual shipped bytes, or the compressed source file. **Actual map SHA-256, binary SHA-256 and deployment run flags UNKNOWN.**

Under ordinary map mode the worker reads direct bits; under LUT50 it uses a 6-bit block's dictionary selector then a dictionary bit; 1 is **LIVE**. Soundness of both modes is conditional on actual map-byte provenance. The `USE_PRECALC` affine identity `T^R0(N0)=N` is algebraically available but exact code paths (`L++`, `ctzu64`, clamps, shifts and overflow) for all accepted prefixes remain **UNKNOWN**. CPU GMP fallback in an observed compiled build is **UNKNOWN**. GPU host launch, kernel, checksum, zero-ctz, last partial work unit and fallback completion equivalence are not proved. No observed successful task/partial receipt was used as proof.

## 5. Versioned source-specific fail-closed pseudopatch R36-EVENT-3 (not production)

**Rust 16-step CPU branch**: freeze `original_n`; reserve typed `UNRESOLVED(original_n,ordinal,PREMULT_OVERFLOW,pre_X)` **before** any multiply if `q>(u128::MAX-c)/3^s`. For a safe guard, require `checked_mul(q,3^s)` and `checked_add(product,c)`. On high-cutoff `print;return`, instead reserve `HIGH_CUTOFF` and seal unresolved; never tally success without original-start strict descent. Carry full 66-bit root and clipped high lift into immutable original identifier.

**Bařina CPU, direct-map/LUT50/USE_PRECALC/GMP variants**: construct independent [B,E) original_n manifest before filtering; authenticate map/binary and recipe; reserve typed `UNRESOLVED` on any invalid dictionary/map offset, zero-ctz, clamp/shift exception, n+1 carry, precompute overflow, GMP abort/fallback unavailable or unsupported early return, **before** mutation. A failed reservation is a launch-level failure. Map-excluded starts require independent mathematical witness, not a dropped roster row.

**GPU host/kernel and Angeltveit CUDA/OpenCL**: every workgroup/launch needs a precommitted exact original-n roster and bounded event capacity; pre-operation guard and saved original source index, ordered event ordinal, kernel/host error and checksum abort path; reserve prior to `printf`, reset, kernel divergence, buffer write, fallback transfer, or abort. Require readback, all workgroup seals and a whole-roster equality check. A returned checksum is **not** success proof. Every event resolves with independent arbitrary-precision literal-T trace to original-start descent or remains UNRESOLVED; required zero unresolved for accepting a range.

**Adversarial conservation result:** a producer dropping only the event while retaining reservation, or only reservation while retaining event, fails reservation/event equality. Dropping **both** is undetectable to any verifier using only producer-supplied reservation count + event packet + hash. Independent static path coverage and an independently produced full per-start roster are indispensable; R34/R35 toy counters do not prove native production emitter completeness. Event tests from earlier sessions were reviewed, **not** mistaken for production acceptance.

## 6. Evidence matrix and decision

| Axis | R36 status |
|---|---|
| Exact parity-cylinder inverse identity and rational eight-even bound | **MATHEMATICAL PROOF (written)** |
| Complete j=98 third-block hazard absence for all n<2^72 | **EXACT FINITE COMPUTER-ASSISTED CERTIFICATE PASS; independent formal verification absent** |
| j>=114 third-and-later continuation safety | **UNKNOWN** |
| Rust lifted numerical X66 state and prior X82/X98 bounds | **INHERITED MATHEMATICAL PROOFS; authentic source pruning not fully proved** |
| 2^24 bitmap every-entry and exceptions / 99,781 applicability | **UNKNOWN** |
| Source-specific Bařina generator↔deployed map and full precalc/GPU equivalence | **UNKNOWN** |
| Native source branch emitter + joint omission closure | **NOT PROVED / NOT IMPLEMENTED** |
| Immutable interval manifest + literal-T independent arbiter | **TOY ONLY, NOT PRODUCTION** |
| Hosted CI and genuine binary/map attestation | **ABSENT / UNKNOWN** |
| 20 cold + 20 warm per-source p50/p95 benchmark on [2^70,2^70+2^40) | **NOT RUN, unexecuted spec preserved** |
| New [B,E) starts, actual survivors, world frontier extension | **NOT RUN / UNKNOWN** |

**Decision: NO-GO to requesting hardware or executing frontier science**. A major mathematical source-risk subcase is closed; it neither reduces the unchanged sieve survivor upper bound nor addresses all remaining correctness gates. Research next: seek an all-later-block no-overflow invariant or an explicit authentic later-block witness; independently certify the source 24-bit bitvector and exception emission; recover authentic map construction. R37 prompt is a future handoff **not executed**.
