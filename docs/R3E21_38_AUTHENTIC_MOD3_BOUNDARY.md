# R3E21-38 — authentic initial-even parity counterexample and complete two-parity bitmap certificate

**15 October 2026 | research only | original-start witness and exact finite arithmetic; not a Collatz counterexample | NO-GO.**

## Executive decision

**The source's leading-even mod-3 lookup assumption is false for a genuinely reachable original integer.** This is no longer merely a hypothetical 24-bit residue. Rust `search1` admits the concrete original `n=2736476243348084729115`, inside the inherited [B,E) research window. Rust `search2` admits its mod-9 and doubleeven masks, but the compiled-formula `initialbitarray` prunes it with the unqualified `numevens=0` 24-window reset. Its actual incoming `search1` numevens is **1**, and the alleged preimage at the second in-window even step is **not integral**. This is an **authentic source-LOCAL witness misclassification**, NOT a proven globally false convergence assertion: the literal trajectory reaches a genuinely smaller state at step **116**. Source-wide pruning correctness, alternative coalescence and all-prior-disjoint global exclusion still require proof.

This report does **not** promote a new CEML verified start, negative conclusion about the Collatz conjecture, new sieve majorant, or claim of Barina/Angeltveit deployed binary unsoundness. The prior conditional upper `326518028938128165` remains untouched; actual survivors remain UNKNOWN.

## Entry, authority, versions and live audit

Owner's direct "run next session" authorises exactly R38. Initial CEML main **`446b138c1c8ee00e1f0ac5d838df7d6572a4ff1f`**, main tree **`277e5b366bfc604a6f8df2ccf6131870fa898f64`**, parents `75d6938bc4d9ff3aaf65244580783244ec1ded54` and `73207db2e815bad40653ba155ce123771921a521`; open PR list [] on entry. Main CI had a prior R36/R37 push success [run 38765759377](https://github.com/jfairfaxball-348/CEML/actions/runs/38765759377) at DIFFERENT commit `75d6938...`. No R38 CI was present on entry. Branch rules, all check-runs and deployed identities were not fully available. Review [AGENTS](../AGENTS.md), [ROADMAP](../ROADMAP.md), [claim policy](CLAIM_POLICY.md), [R31](R3E21_31_INTERVAL_EXCEPTION_AUDIT.md)–[R37](R3E21_37_BITMAP_AND_LATER_BLOCKS.md) for earlier gates. No science, owner PC, paid/cloud/GPU processing, benchmark or production change.

Author-published baseline retained: B=`2392518188130438742016`, E=`3000000000000000000000` **exclusive**, U=`2^40`; 552501489 full units and one 350507499520-start partial. First-party [Bařina live homepage](https://pcbarina.fit.vut.cz/) on 15 October still displayed **first incomplete** and **first unassigned** separately as `2175982616 × 2^40`; the current page content was checked but its generated-at field was not independently pinned here. Author-reported only, NOT CEML science. Independent [2025 published report](https://doi.org/10.1007/s11227-025-07337-0) proves a historical computational record `n<2^71` at a different evidence tier. [Angeltveit arXiv 2602.10466](https://arxiv.org/abs/2602.10466) v1 (11 February 2026) governs Theorems 4.1/4.4, Definitions 4.2/4.3; no revised v2 established. A theorem's intermediate-state condition >=99781 must never be dropped; the bounded literal-T base 1..99781 is rechecked in R38 Python, but no formal proof claimed.

First-party source read/refetched:
- `vigleik0/collatz@f3f09248c7ae7299b8443e112f565f309d97f161`: `main.rs` blob `4a33b870d27059feea28985e185b8c8c709eb313`, CUDA `collatz_cudav7.cu` `a783f0f39ee776c725036caec9c93d15a1c8ca72`, OpenCL `collatz_openclv2.cpp` `5cbe2c1e1958cf3b2ae1224ed3f1defe19db7fdc`, `compute_kernel2.cl` `92f7a7f4c24db7b7a930d18c2203c0138a5075ad`.
- `xbarin02/collatz@141e13aae243d509a01a43bec597f53a5b97a09f`: bootstrap `70dfe2936a003c5bf45c61ce34f4db0f39c0c4e2`, CPU worker `c33a6a86f35a0900ea1df8b7b2dcd30863a9b8bc`, worker Makefile `6714f397f8d08668cc787a3b84ae8ed205cf8dd0`, GPU host `eb1bcfd3ea4397999e1d5d3c8dd2c500db1015f2`, kernel `569e0d1a46433365c822bdf4fb27a61f188cd4b5`.
- `xbarin02/collatz-sieve@e5f0c264ba1f5f9c0a7d32a10c3aa61b225c70d1`: `src/sieve.c` `48d81fbd3fe2b21344dd24b72febc346dc642361`; `src/fsieve.c` `a0a2386584f7c3db4074044373c9bdea0056bdb1`; **newly identified** LUT50 `src/lut50/fdc.c` `1ed04b4231e9f596d2c7cfee7b9de4eac8bb0cbe`, decoder `fdd.c` `0074ab223043d6a133ba857046ee377c41cf9af9`; both explicitly have 50-entry uint64 dictionaries. Source SHA/blobs are NOT SHA-256 maps or compiled binaries.

## A. Precise theorem: the inherited parity is necessary

For shortened `T`, immediately after any odd T-state the resulting state is `2 mod 3`, because `(3z+1)/2 ≡ 2 (mod 3)`. Each subsequent even T-state halves its current value, toggling residues `2↔1 (mod 3)`. Thus after `q` consecutive even steps since the most recent odd T-step, the current state is `2 mod3` **iff q is even**. Genuine `search1` roots begin with two odd T-steps (`n≡3 mod4`), so the immediately prior odd always exists. The search1 `numevens` is precisely this trailing run length.

In `main.rs` precompute (lines 125–180), the first two even steps of each independent 24-bit window start with `numevens=0` even when the incoming search1 `numevens` is odd. At an in-window even index `i`, the `+179` inverse-mod3 score is valid only if `(incoming_q + even_run_length_in_window)%2==0` until the next odd step resets the run. Resetting q invents the parity of the would-be predecessor. For q even original and corrected agree; for q odd they can differ in BOTH directions. This lemma is exact elementary modular arithmetic. It does not establish the other bitmap predicates (direct, doubleeven lookahead, theorem4.1/4.4) or complete original-start exclusion on its own.

**Safe prospective approach:** use two independently audited bitmap classes keyed on `search1.numevens%2`, or conservatively suppress initial-run inverse-mod3 shortcuts until an in-window odd step has occurred. The former preserves more power; both require original-start witness proof of all other rules, correct `doubleeven` propagation, threshold equality and native implementation validation before deployment. No production code modified.

## B. Authentic original-start trace / actual source pruning

One concrete original integer:
```
n = 2736476243348084729115
B <= n < E; n < 2^72; n % 9 = 6; n % 4 = 3
n = r + 37*2^66; r = 6358120439071089947
66-step true odd count f = 43;  search1 incoming numevens = 1
search1 number + 37 * 3^43 = T^66(n)+1
search2 magic index ((number * 3^(-43)) mod 2^24) + 37 (mod 2^24)
X66 low24 = 13704093; parity word = 0x9faddc
array a=f-42=1; cutoff=174+485=659
source score reset q=0: 791 => bitmap CLEARED
corrected score q=1: 612 => bitmap LIVE
T^66(n)=12173793236889640180636, residue mod3=1
T^67(n)=6086896618444820090318, residue mod3=2
T^68(n)=3043448309222410045159, residue mod3=1
```
At 67, `(2*T^67(n)-1)/3` is integral but strictly GREATER than the original n; at 68 the source-imagined `(2*T^68(n)-1)/3` is **not an integer**. Complete independent literal-T prefix through step 116 shows no strict descent for steps 1..115; first smaller state occurs at 116. All values through step 90 exceed 99781. The source search1 path's 65 entry assertions, actual f, `number`, mod9 live bit, `doubleeven` continuation masks, lookup index and full literal shortened-T path were checked by committed Python research fixture `research/r3e21_38_authentic_mod3.py`. A separate deterministic, capped C++ exploratory source-path sampler originally located candidate n in [B,E); **the sampler itself is not retained as a universal witness and does not establish a population frequency**. The committed fixed witness makes its discovery method irrelevant to reproducibility.

This establishes an **authentic local bitmap proof failure**; the known descent at 116 means it is not a false convergence result, and the unproved existence/absence of a completely different predecessor certificate must not be silently settled in either direction.

## C. Complete two-parity bitvector certificate

Committed `research/r3e21_38_two_parity_bitmap.cpp` scans all `2^24=16,777,216` low-X residues with positive high lift, derives a genuine 24-step parity word, and independently calculates source q=0 and corrected incoming q=1 scores. Locally ran the complete finite C++ scan with exact assertions:

| a | cutoff | source live (q even) | corrected live (q odd) | source cleared / corrected live | source live / corrected cleared |
|---:|---:|---:|---:|---:|---:|
|0|174|333343|333343|0|0|
|1|659|1590275|1650277|60002|0|
|2|1144|3837929|3837929|0|0|
|3|1629|6750160|6738759|0|11401|
|4|2114|9809263|9809263|0|0|
|5|2599|12495505|12498034|2529|0|
|6|3084|14479396|14479880|484|0|
|7|3569|15712298|15712298|0|0|

Distinct low-residue scores disagree for **399426** residues; aggregated `63,015` potentially unsafe SOURCE-CLEAR residue/threshold pairs for odd entering parity, plus `11,401` SOURCE-LIVE where parity correction permits a clear. All R37 63,015 gap pairs are explained exactly as parity-specific **score** discrepancies. These are **not** a count of actual incorrect original-start exclusions or of complete soundness failures, and are not claimed distinct input n.

Re-running `research/r3e21_36_sparse_parity_mitm.py` and the exact committed R37 C++ / Python via the *new PR workflow head* is the accepted external rerun method; the separate R36/R37 past green runs apply only to their earlier SHAs. A missing/pending/failed R38 Actions job must be recorded separately and never called PASS.

## D. Later Rust j>=114: exact finite stopping criterion, not a theorem

Preserve R36 **complete j=98 (first third-block) zero-hazard computer certificate** and R37 necessary bound for pre-block state `X_j<2^120`, divisible by 2^16 and `X_j>=D=518059092085797269936906884792713216`. Among j=114 prefixes at most 14 even T-states could satisfy this necessary growth inequality, but their **362205922639534084** parity words cannot be exhausted with the original MITM (a 41,146,859,952-tuple half-list at m=14). j=130 permits at most 21 and **1080231996567188757316932** words. **Stop any purported completeness claim** when the rank-partition's left list exceeds a specified memory cap (e.g. 250000 entries) or projected right probes exceed 5 million; report exact enumerated classes and untouched remainder. These caps are research budgets, NOT an exhaustive certificate for large j.

A valid stronger search must carry `X0=n+1∈[2,2^72]`, each 114+-bit parity-cylinder congruence, exact half-open modular interval wrap splits, rank ordering, source `X_{66+16q}<2^120` previous cutoffs, no earlier original descent and prior source masks. Lossless state merges require canonical proof of identical future constraints. Miniature enumeration vs literal T can validate a construction but does not replace its full termination proof. No reachable j>=114 overflow is demonstrated or excluded universally. Use a reservation **before** mutation, then `checked_mul` and `checked_add` for **every** 16-step block; high cutoff is unresolved, not success. Immutable original n must survive root/lift and exception transfer. No native patch applied.

## E. Map, precalc and exceptions: one genuine provenance advance, other gaps

The separate `collatz-sieve/src/lut50/fdc.c` is the genuine first-party **50-word dictionary encoder** from 64-bit words to index bytes; `fdd.c` reverses this. This resolves the R37 assertion that no specific LUT50 encoder was found, but **not** which raw `esieve-34.map` source was used to encode `esieve-34.lut50`, no generator/proof was found for `h2esieve-24`, and no downloaded/decompressed raw/archived map bytes or SHA-256 were obtained. The `fdd.c` reads an arbitrary byte index into `dict[index]` without a range check; any actual map must prove every byte <50 before trusting that decoder. The map distribution's named `esieve-34.lut50.gz` and `h2esieve-24.gz` exist as first-party repository objects but their compressed object SHA-1 is NOT a SHA-256 file attest. Bootstrap dynamically pulls repositories, then `unpack.sh` prefers raw, lz4, lzo, gzip; actual recipe for CPU `USE_LIBGMP=1 USE_SIEVE=1 USE_PRECALC=1 SIEVE_LOGSIZE=34 USE_SIEVE9=1 USE_LUT50=1`, GPU `SIEVE_LOGSIZE=24 USE_SIEVE3=1` is a textual recipe, not a deployed build identity.

`USE_PRECALC` identity `T^R0(N0)=N` remains CONDITIONAL: independently audit every `L++`, zero-ctz, alpha/beta R clamp, `alpha==64` clamp63, dictionary selector, R decrements, unsigned carries, shifts, GMP and GPU checksum/fallback with end-partial. Original-start exact [B,E) roster must be constructed independently before pruning. Every abort, print, cutoff, impossible shift, missing map, GPU group and overflow path must reserve typed `UNRESOLVED(original_n, ordinal, source, pre_state)` before mutation, seal its event and reconcile against independently generated per-original ordered packets and whole-launch roster. **A joint omission of reservation and event is invisible to producer-only hashes; independent source-control-flow/roster proof is essential.** Existing toy event-only, reservation-only and joint-omission tests from R34/R37 remain evidence, not native implementation. No new native producer, auditor or compiled build delivered.

## F. Evidence matrix and decision

| Tier | Grade |
|---|---|
| Symbolic q-parity mod3 lemma | **EXACT PROOF** for initial even run under a prior odd step |
| 24-bit two-parity scoring | **LOCAL COMPLETE 2^24 PASS**; GitHub R38 CI to be checked at PR SHA |
| Authentic original-start source path and 116-step literal T | **LOCAL BOUNDED PASS**, reproducible fixture; not a convergence counterexample |
| R36 j98 finite zero hazard | **INHERITED proved reduction + computer certificate**; new PR rerun required |
| Other bitmap predicates + complete 66-step source equivalence | **NOT PROVED** |
| All later j>=114 overflow safety | **UNKNOWN** |
| First-party LUT50 encoder | **IDENTIFIED AND PINNED**; map provenance still **NOT VERIFIED** |
| Raw map SHA-256 and two compiled binary identities | **ABSENT / NOT ATTESTED** |
| Full precalc/ctz/clamp and CPU/GPU exception emitters | **UNPROVED / NOT IMPLEMENTED** |
| Independent arbitrary-precision original-start arbiter | **PARTIAL BOUNDED LITERAL-T only** |
| 20 cold/20 warm p50/p95 on [2^70,2^70+2^40) | **UNEXECUTED**, frozen spec |
| Actual scientific frontier, published tally, survivor count | **NOT RUN / UNKNOWN** |

**GO:** next strictly bounded mathematical/source-correctness R39. **NO-GO:** production code, hardware, volunteering, benchmark, science, source-paper accusation or priority/publication claim. Next handoff is full `NEXT_SESSION_PROMPT.md`, R39 FUTURE / UNEXECUTED.
