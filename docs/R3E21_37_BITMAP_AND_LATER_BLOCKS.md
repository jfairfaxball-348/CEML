# R3E21-37 — all-later-block arithmetic ceiling, complete 24-bit bitmap reproduction, and source/map gap ledger

**15 October 2026 | EXACT FINITE RESEARCH TESTS / PARTIAL SOURCE AUDIT | £0 / NO SCIENCE | NO-GO.**

## 0. Authority, baseline and provenance

The owner's instruction **"run next session"** executed R37 only. Entry CEML main was **`ad9609c513560e9d47170e8a983fb6c415e87336`** (R36 merge); no open PRs observed on entry. Main commit individual statuses `[]` and associated PR-triggered workflow runs `[]`: **ABSENT / NOT VERIFIED, never PASS**. Full ruleset/branch-protection and all check-run inventory were **NOT independently established**. Research branch `research/r3e21-37-bitmap-later-blocks` holds only this report, bounded fixtures, status and next handoff. No native production changes, owner PC, hardware, actual science, payment, volunteer contacting, frozen protocols, website/feed or publication.

Read-first: `AGENTS.md`, `ROADMAP.md`, `PROGRAM_STATUS.md`, `docs/CLAIM_POLICY.md`, R31–R36 reports and R36 canonical Python certificate; R34/R35 source/state audits consulted. **Actually reran the R36 exact MITM logic** in an independent local Python runtime: for m=0,…,7, counts `1,98,4753,152096,3612280,67910864,1052618392,13834413152`; exactly **14,958,711,636** parity cylinders, **zero bounded-X0 hits**, small oracle true, about 8.36 s in this research environment. This is not GitHub CI, formal proof or a compiled source guarantee.

First-party Bařina homepage independently refreshed during R37 (generated **Thu 15 Oct 2026 16:56:04 +0200**): **lowest incomplete = 2175982616 × 2^40**; **lowest unassigned = 2175982616 × 2^40**, separately identified, both author-reported not CEML-reproduced. Inherited conditional B=`2392518188130438742016` and E=`3000000000000000000000` EXCLUSIVE; U=`2^40`; **552501489 complete units plus one 350507499520-start partial**. Old conservative conditional candidate **upper 326518028938128165 UNCHANGED**. Actual survivors, CEML reverified frontier, and external priority are **UNKNOWN**. Peer-reviewed Bařina 2025 `n<2^71` (DOI `10.1007/s11227-025-07337-0`) is an independent tier; do not conflate the live work-unit pointer. Angeltveit arXiv:2602.10466v1 dated 11 February 2026 was independently read (Theorems 4.1, 4.4, Definitions 4.2–4.3); no later revision established.

Pinned first-party source **blob SHAs re-fetched through GitHub**:
- Angeltveit `vigleik0/collatz@f3f09248c7ae7299b8443e112f565f309d97f161`: `main.rs` `4a33b870d27059feea28985e185b8c8c709eb313` (lines 1–340 independently read). CUDA/OpenCL code pins from R36 are **inherited, NOT independently re-fetched in R37**.
- Bařina `xbarin02/collatz@141e13aae243d509a01a43bec597f53a5b97a09f`: `scripts/bootstrap.sh` `70dfe2936a003c5bf45c61ce34f4db0f39c0c4e2`; `src/worker/worker.c` `c33a6a86f35a0900ea1df8b7b2dcd30863a9b8bc`; `src/worker/Makefile` `6714f397f8d08668cc787a3b84ae8ed205cf8dd0`; `src/gpuworker/gpuworker.c` `eb1bcfd3ea4397999e1d5d3c8dd2c500db1015f2`; `src/gpuworker/kernel.cl` `569e0d1a46433365c822bdf4fb27a61f188cd4b5`.
- Separate `xbarin02/collatz-sieve@e5f0c264ba1f5f9c0a7d32a10c3aa61b225c70d1`: `README.md` `6dea60db39f1053ec5551f367764e6f207f52952`; `src/sieve.c` `48d81fbd3fe2b21344dd24b72febc346dc642361`; `src/fsieve.c` `a0a2386584f7c3db4074044373c9bdea0056bdb1`; `src/Makefile` `d9379f3286c3ab95279b87313237a27afc349485`; `pack.sh` `19dbd5ee9bfa346ed8fb9304d8087be0395495e2`; `unpack.sh` `7bfb04f79fe6237131189e468136ddf890a2b09b`. **Blob pins are source-only; SHA-256 of actual unpacked map, deployed executable and compile flags NOT REVERIFIED.**

## A. Later Rust 16-step blocks: exact mathematical bottleneck, not a safety theorem

Use shortened `T` and `X_i=T^i(n)+1`, with **original** `1<=n<2^72`. R35's strict entry hazard (if reached with `0<X_j<2^120`) is
`X_j % 2^16 == 0` and `X_j >= D=518059092085797269936906884792713216`.
R36 proved no such original-start entry at j=98. **R37 does not prove all later entries safe and finds no authentic violating original n**. The source calls `search3` blocks until original descent or printed high cutoff, and high-cutoff `println!;return` is an **unresolved event**, not verified convergence.

An exact all-j **necessary bound** follows. While no small {1,2} cycle occurs, an even T-state is at least 6; at an odd state `X_{i+1}=(3/2)X_i`; at even state `X_{i+1}=(X_i+1)/2 <= (4/7)X_i = (3/2)(8/21)X_i`. If m even states occur before j,
`X_j <= 2^72 * 3^j * 8^m / (2^j * 21^m)`.
If this rational bound is below D, danger is **impossible**, with no floating-point assumptions. This gives the largest potentially hazardous m:
- **j=98, W=114:** m<=7; `sum_{m=0}^7 C(98,m)=14958711636`; R36 certificate exhausts these.
- **j=114, W=130:** m<=14; **362205922639534084** possible prefix position words. An R36-style split at m=14 has **41,146,859,952** left tuples and as many streamed right tuples, before ordering/rank/modular clipping; completely infeasible at R36's modest cap.
- **j=130, W=146:** m<=21; **1080231996567188757316932** possible words. Split at m=21 has `C(130,10)=266401260897200` left candidates and `C(130,11)=2906195573424000` right candidates; no exhaustive certificate attempted.

The **inverse parity congruence still holds** at any j: for m even positions `e_1<...<e_m<j`, followed by 16 odd states, `X0 ≡ -Σ_{k=0}^{m-1} 3^k (2·3^{-1})^{e_{k+1}} (mod 2^{j+16})`, where `X0=n+1 ∈ [2,2^72]`. The rank and inverse are modulo the entire j+16 bits, not j. The 16-odd suffix is necessary for low16 zero. The R36 meet-in-the-middle decomposition remains complete **only when all allowed m words are examined**. R37's standard-library `research/r3e21_37_audit.py` tests three independently enumerated miniature words against literal trajectories. No unbounded automaton, 2^72 scan or unjustified extrapolation.

**Additional necessary source gates for any future proof:** retain all prior `X_{66+16q}<2^120` high-cutoff continuations, the first-descent absence `T^i(n)>=n` until exit, exact whole original-start identity and the source lookup recurrence (with guarded pre-multiply, before mutate). A proof may reject whole parity cylinders by rational interval inequalities at each prefix, but a heuristic typical parity count cannot close these finite sets. The time/memory ceiling above is the **reason for stopping** rather than calling a partial search complete. An authentic later-block witness requires a concrete original n, 66-bit source root and high lift, full chronological literal-T path through first offending block, true `X_j`, lookup and exact source return behaviour; **NONE PROVIDED**.

**Fail-closed Rust pseudopatch (not production):**
```
original_n = immutable(root + (lift << 66))
ordinal = monotone_per_original_n()
pre_X = number
lookup = multisteparray[pre_X & 65535]
power, add = THREEPOWERSU32[lookup & 31], lookup >> 5
q = pre_X >> 16
if q > (u128::MAX - add) / power:
    reserve_unresolved(original_n, ordinal, "PREMULT_OVERFLOW", pre_X)
    return UNRESOLVED
next_X = checked_add(checked_mul(q, power)?, add)?
number = next_X
if number < original_n: return PROVED_DESCENT(trace_to_original_n)
if number >> 64 >= 1 << 56:
    reserve_unresolved(original_n, ordinal, "HIGH_CUTOFF", number)
    return UNRESOLVED
```
Each exceptional return must be reserved **before** any unchecked multiply/add, before loss of original_n, before output or termination. A failed reservation aborts launch; a mere printed value or tally is not success. Reserve and seal per-start event ordinals in the actual loop; no native Rust source patched or compiled. The Rust pseudocode uses `checked_*` on **every** block (the exact Rust syntax and high-cutoff return values require implementation review).

## B. Exhaustive source-compatible 24-bit bitmap: positive reproduction and precise missing theorem

Source `main.rs:125–180` uses `upordown`, integer `curval`, `maxval`, `numevens`, `doubleeven` and `cutoffs=174+485a` for a=0..7. In shifted-X notation, bit1 of `upordown` means odd T-state; for bit1, the score changes by **−179**, and for bit0 (even T-state) by **+306**, hence `curval_i=306i−485 f_i`. The program additionally tests `curval+306` for two-even patterns and `curval+179` every second run-even as a mod-3 backward shortcut, then sets **1=LIVE** precisely when `maxval<=174+485a`. Unset bits are source-pruned. The index permutation is inverse `3^(42+a)` modulo `2^24`; bit-padded last 64-bit read is copied to enable up-to-64 high lifts. Mod9 live residues are `{0,1,3,6,7}` with `2,4,5,8` excluded.

An independently coded, capped C++ arithmetic fixture `research/r3e21_37_bitmap_audit.cpp` **actually scanned all 2^24=16,777,216 residues**, using a *positive high lift and genuine shortened-T transitions* to construct the parity word, and separately reconstructing the source shifted-X parity encoder. **All 16,777,216 parity words matched**; source score implementation yields these exact **LIVE** cells (not sample estimates):

| a | cutoff | live count | density (approx) | 24-window-only gap |
|---:|---:|---:|---:|---:|
| 0 | 174 | 333343 | 0.0198687911 | 0 |
| 1 | 659 | 1590275 | 0.0947877765 | 60002 |
| 2 | 1144 | 3837929 | 0.2287583947 | 0 |
| 3 | 1629 | 6750160 | 0.4023408890 | 0 |
| 4 | 2114 | 9809263 | 0.5846776366 | 0 |
| 5 | 2599 | 12495505 | 0.7447901368 | 2529 |
| 6 | 3084 | 14479396 | 0.8630392551 | 484 |
| 7 | 3569 | 15712298 | 0.9365259409 | 0 |

Live counts reproduce the paper's eight reported densities at its display precision, and the independent source-compatible encoder matches literal parity words over the **entire** low24 domain. This is a real **finite bitmap-generation equivalence test for the audited code fragment**, **NOT an end-to-end proof of every cleared bit's mathematical validity for all 72-bit starts** or of compiled Rust source equivalence.

**Important newly isolated proof obligation: leading even-run mod3.** The source starts `numevens=0` for each 24-bit window. After two even steps **before any odd step in that window**, it adds `+179` for the reverse mod-3 witness; that conclusion requires the actual corresponding state be `2 mod3`, a fact **not determined by low24 parity alone**. Once an odd step has occurred, every following even-run state mod3 can indeed be tracked from the odd-step output ≡2 mod3. The separate conservative score omits `+179` **only for initial even runs**; compare all residues: exactly **60,002** a=1, **2,529** a=5 and **484** a=6 residue/threshold pairs were source-pruned but not prunable by this guarded 24-window-only score; all other a zero. Example input low shifted-X residue **109** gives parity word `0xf76bec`, source `maxval=791`, guarded `maxval=612`; at a=1 cutoff 659 the source clears, the conservative calculation leaves live.

**CRITICAL QUANTIFIER BOUNDARY:** These **63,015 are diagnostic residue/array pairs, not distinct unsound original integers or proof of false clearing**. An original source candidate also has 66 prior steps with odd-count `42+a`, mod3 information, other predecessor witnesses, direct earlier descent, `search1` flags and mod9 filters. Those might establish the missing witness for every reachable such case; none was exhaustively audited. The relevant 24-bit precompute cannot on its own supply the promised mod3 witness for an unconstrained incoming high lift. Next gate must either prove a source-conditional inherited invariant covering the cases or exhibit an authentic 72-bit original n with all earlier branches traced. Do **not** use the gap count as an exclusion or a source bug announcement.

**Low-state/base dependency clarified.** Theorems 4.1/4.4 explicitly assume every intermediate state ≥99,781 for the rational bound; the article takes verification of all ≤99,781 as given. R37 independently directly enumerated literal shortened-T starts **1..99,781**, each reached 1 within ≤221 steps (maximum at original n=77,031; maximum peak 785,412,368). These are bounded base computations **not a Lean proof**. An audited source application of Theorems 4.1/4.4 must either retain the high-state hypothesis or switch to separately verified base when it encounters a low state. Simply ignoring the hypothesis is a proof gap, but a valid low-state fall can itself be a separately witnessed safe case. Search1/2 full early-pruning, `doubleeven` propagation, `threepower` array admissibility, padded word wrap and `search3` final status are **NOT jointly proved**.

## C. Map → unpack → make → worker: recovered routing, still not attested

The bootstrap actually **builds** CPU `USE_LIBGMP=1 USE_SIEVE=1 USE_PRECALC=1 SIEVE_LOGSIZE=34 USE_SIEVE9=1 USE_LUT50=1` and GPU `TASK_UNITS=16/20 SIEVE_LOGSIZE=24 USE_SIEVE3=1`, then invokes `./unpack.sh esieve-34.lut50` to the CPU directory, `./unpack.sh h2esieve-24` to GPU directory, then renames `h2esieve-24.map` to `esieve-24.map`. `unpack.sh` prefers a preexisting raw map, else LZ4, else LZO, else gzip and exits on no map. **The bootstrap dynamically `git pull`s both repositories without pinning those upstream revisions**, so a frozen text bootstrap recipe cannot determine the bytes at historical deployment.

CPU worker `init()` requests `esieve-34.lut50.map`, LUT50 `GET_INDEX=((n & mask)>>6)`, and dictionary bit index `n&63`, 1=LIVE; direct mode requests `esieve-34.map` and reads `(n>>3, n&7)`. GPU host maps `esieve-24.map`, kernel receives compile options (OpenCL 2.0 selection and sieve switches). `collatz-sieve/src/sieve.c` generates a named `sieve-K.map`, `fsieve.c` a named `fsieve-K.map`, while `pack.sh` only compresses named existing *.map bytes. No inspected source establishes *the particular* end-to-end encoder/generator for CPU **`esieve-34.lut50.map`** and GPU **`h2esieve-24.map`**. Public first-party compressed filenames exist, but byte downloads/decompression and independent digests **were not performed**. In particular a `sieve-34.map` or `fsieve-34.map` is not implicitly the deployed LUT50 map. Map **generation and decoding semantics differ from a map's mathematical proof**.

CPU `USE_PRECALC` path is `solve_task` → only `4k+3` low-prefix indices passing sieve → `precalc(L0,R0)` → `calc` looping high h `0 <= h < 2^(task_size-R0)`, reconstructing `N0=H+L0` and `N=(H>>R0)*3^Salpha + L`, then `check(N,N0)`. This is the *intended* affine identity `T^R0(N0)=N` after exact low-prefix transportation, not yet an every-path proof. Relevant hostile cases from pinned `worker.c`: `L++`; `ctzu64` on possible zero; `alpha>R` and `beta>R` clamps; `==64` clamp to63; LUT_SIZE64 clamp to40; potential shifts, unsigned carries and assertions, and branches where `R==0` sends an adjusted L to `calc`. `check` and GMP `mpz_check2` may follow different arithmetic representations and route overflow depending on compile macros, not on the recipe alone. GPU host uses OpenCL platform/device loop, source read, dynamically composed `clBuildProgram`, per-workgroup checksums, and potentially errors/partial groups; **no compiled build, launch roster, exact final partial equivalence or checksum-to-every-original-start proof** exists. No stdout/return value can promote absent events to success.

## D. Fail-closed EVENT-4 integration gate

A **source-independent original-start manifest** is mandatory before any sieve pruning. For each interval `[L,H)`, define the exact roster of original integer starts and a versioned class coverage map. For every start, choose exactly one of: formally witnessed exclusion via named theorem + previous-prefix premise; strict original-start descent with full ordered trace; independently literal-T resolved exceptional event; or `UNRESOLVED`. All producer events must record immutable `original_n`, worker/build/map identities, chronology `(step,block,ordinal)`, pre-state and branch reason. Write a reservation **before every branch can silently return, overflow or abort**. An input that fails reservation is launch failure, not a dropped row. Worker/host/kernel packets and ordered event ordinals are compared to **independently calculated** per-start manifests and launch seals.

Research-only adversarial fixture shows producer-only **event omission** and **reservation omission** each break equality; **joint omission** of reservation+event **passes the producer's own equality/hash test** but fails the independently supplied roster. This is an information-theoretic indistinguishability problem for producer-only evidence, not a native event-emitter proof. Fail-closed pseudopatches cover Bařina direct/LUT50, `USE_PRECALC`/GMP, OpenCL host/kernel, Angeltveit Rust/CUDA/OpenCL; actual source edits and branch-by-branch proof remain **NOT IMPLEMENTED**.

A minimal admission gate must require (i) two truly source-distinct pinned compiled builds including all flags, map bytes and SHA-256; (ii) proof of all bitmap and low-state predicates and every precalc/ctz/clamp/overflow/shift; (iii) independently committed per-start exact partition, immutable ordered exceptions and whole-workgroup/launch seals; (iv) separate arbitrary-precision original-n literal-T arbiter; (v) source-to-build provenance and independent equivalence tests; (vi) a **new owner instruction** and budget before *any* hardware or frontier execution. Current acceptance: **NO-GO**.

## E. Evidence and honest exit

| Axis | Grade after R37 |
|---|---|
| R36 j=98 inverse congruence and exact finite zero-hit certificate | **INDEPENDENTLY LOCAL-RERUN PASS**, computer-assisted only |
| All j>=114 pre-multiply overflow absence / authentic later witness | **UNKNOWN**; finite necessary bounds only |
| 24-bit true parity ↔ source encoder, all bitmap 1=LIVE counts | **LOCAL COMPLETE 2^24 RESIDUE REPRODUCTION PASS** |
| All cleared bitmap predicates imply original-start correct exclusion | **UNPROVED**, 63,015 conditional gap pairs isolated |
| Independent base n≤99,781 shortened-T direct trajectory | **LOCAL COMPLETE BOUNDED PASS**, not formally verified |
| 99,781 guard applicability / complete search1+search2+search3 branch soundness | **UNPROVED** |
| Bařina CPU/GPU code recipe and filename routing | **RE-FETCHED SOURCE AND READ** |
| Actual generated/installed map and compiled worker SHA-256 / running flags | **ABSENT / NOT ATTESTED** |
| All precalc, GMP, GPU kernel, host fallbacks, exact partial | **NOT PROVED** |
| Complete native reservation + producer-event static source coverage | **NOT IMPLEMENTED** |
| Independent immutable manifest and event arbiter | **TOY CONSERVATION TEST ONLY** |
| Hosted CI and source-distinct native acceptances | **ABSENT/UNKNOWN** |
| 20 cold/20 warm each-source p50/p95 on [2^70,2^70+2^40) | **UNEXECUTED SPEC; NOT RUN** |
| Actual [B,E) starts, world frontier or published result | **NOT RUN / UNKNOWN** |

**Decision: NO-GO** for hardware ask, live science, crowdsourced workload or world-frontier assertion. Mathematical candidate upper and all existing historical records unchanged. A good R38 objective is to resolve **the 63,015-pair initial-even mod3 guard against a genuine prefix source state**, with proof or authentic counterexample, and only then tackle first-later-block reachability with a certificate that stops before infeasible enumeration. See `NEXT_SESSION_PROMPT.md` for the full unexecuted handoff.
