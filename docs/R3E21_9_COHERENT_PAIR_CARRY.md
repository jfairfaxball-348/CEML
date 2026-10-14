# CEML-R3E21-9 — Coherent two-bit carry transfer

14 October 2026. One owner-authorised **research-only** session; repository `jfairfaxball-348/CEML`. Entry LIVE main: `ab6c7c295903675fe264291c7e34710d245eb1d4`, a normal two-parent merge of PR #35: parents `3fb3d36072e595df1c466f5c9178f5a80fdc83a4` and authored R3E21-8 head `38b95202d8bc97b3c767bd1089c80f5884ac8234`. No open/intervening PRs or R3E21-9 branches at entry. GitHub Actions runs 0, commit check-runs 0, statuses 0 = **ABSENT, NOT PASS**. Rulesets `[]`, main reports `protected=false`; detailed protection API gives 403/**UNKNOWN**, not proof of no restrictions. No local Codex, scientific batch, production/certificate/source-identity mutation, website, publication, Lean, costs or contact.

## Result (conditional proved upper bound, NOT exact survivors)

Assume external A(B): every positive integer below `B=2175982616*2^40=2392518188130438742016` converges. Set exclusive `E=3*10^21`, width `W=607481811869561257984`. Retain, unchanged, the certified R3E21-4/6/7 exclusions: depth-12 simple Bařina/terminal-mask and lifted inverse proof, 179 reverse templates, common exact mask U of **394 out of 729 residues** on **144 active depth-12 roots** (38 empty), and uniform high-base slope-prefix descent through depth 79. These are conditional exclusions under least-counterexample induction, not CEML independent confirmation of A(B).

**NEW theorem: at most 333,316,047,378,995,972 explicit starts are not yet excluded by this composite in [B,E).** This is a strictly stronger *conservative mathematical upper bound*, reducing the R3E21-8 upper 334,199,143,141,062,522 by **883,095,762,066,550** (0.2642423777% of the previous upper). The new upper is 0.0548684817992% of W. It does not assert these numbers all actually survive, nor that this many trajectories were computed, nor a practical speedup, convergence theorem, new frontier, record, novelty or priority.

Independent transfer totals:
- Previous orientation-free one-step phase bound **334199143141076940**, reproduced.
- Previous true eight-level orientation bound **334199143141062522**, reproduced.
- New globally coherent two-bit transfer before fixing root orientations **333316047379009407**.
- New two-bit transfer with eight actual orientation levels per root **333316047378995972**.

This computes exactly a *conservative bound* by a state-space recursion; it does **not** enumerate the ~2^72 possible parity words, the previously identified 29,715,960,543,835,736 stopped numerical leaves or a sampled fraction of those leaves.

## Precise new arithmetic invariant and proof

Fix an actual admissible depth-d numerical cylinder, with first integer n0 in [B,E), N members `n_i=n0+i*2^d`, initial d-step odd count s, and t=n0 mod729. The affine parity-prefix lift identity is **exact**:

`T^d(n_i)=Y+3^s*i,` where `Y=T^d(n0)`.

Consequently, for *four* consecutive index classes `i mod4`, all of the next **two** parity bits depend on one shared value `y=Y mod4`, not on independent free orientations. Put `g=3^s mod4` (1 for even s, 3 for odd s); for i in 0..3 set `v_i=(y+g*i) mod4`; the next bits are `e_{i,0}=v_i mod2`, `e_{i,1}=T(v_i) mod2`. The second identity is sound because parity after one shortened-map step depends only on the input modulo 4. A lift of the first index by multiples of 4 has identical two-step parities. The four child progressions have lengths `N_i=max(0,ceil((N-i)/4))` and modulo-729 phases `t_i=(t+i*2^d) mod729`, each with numerical spacing `2^(d+2)`.

Let `C_d(N,t)` be the **exact** number among that cylinder in the unchanged U mask. It is calculated by `floor(N/729)*394` plus an exact cyclic 729-prefix tail, with signed ceil endpoints (R3E21-8). Define Q(d,s,N,t)=0 when N=0 or 3^s<2^d (the proved uniform high-base descent). At depth D=72, N<=1, or when C=0, Q=C. Otherwise define:

`Q(d,s,N,t)=min(C_d(N,t), max_(y=0,1,2,3) sum_(i=0..3) A_i(y))`

where `A_i(y)=0` if `3^(s+e_{i,0})<2^(d+1)`, and otherwise `A_i(y)=Q(d+2,s+e_{i,0}+e_{i,1},N_i,t_i)`. At the last depth where d+2>D, use the already proved R3E21-8 one-step split with Q children. The cap by C is essential: it respects the unchanged exact CRT mask and can only strengthen the bound.

**Proof by induction:** each actual cylinder has exactly one actual y; for that y, the four index classes are pairwise disjoint and exhaustive, and their two-step parity words are *jointly* forced by the affine lift. Any branch with a descending prefix at intermediate d+1 is safely excluded by (H) and A(B), and a descending depth d+2 branch is excluded by Q's base condition. Apply the inductive bound to the remaining child progressions, take the maximum over the four possible common y, and also intersect with the exact whole-parent mask count C. Since both independent upper bounds are valid, their minimum is valid. Summing disjoint 144 root cylinders yields the asserted global upper. Replacing the first eight levels per root with the **actual** shortened-map orientation is separately safe (the same construction as R3E21-8). No probabilistic independence or incompatible child orientations enter.

This is a two-bit **quotient for one transfer packet**, not an exact finite-state automaton for the entire parity/CRT predicate. The true y changes after two iterations and cannot in general be determined from (d,s,t), so it is maximised again at descendants. The exact number of fully surviving n in [B,E) remains unknown.

## Obstruction, narrowly and constructively proved

The old collision at depth 13 between 91 and 3007 already showed that (d,s,n mod729) cannot fix next parity. A stronger counterexample shows that **adding that next parity still cannot fix the one after it**: for `n=639` and `n=6471`, after 13 shortened-map steps both have s=11, n mod729=639 and next parity 1, but parity at step 14 is respectively 0 and 1. Both 13-step parity prefixes satisfy `3^s>=2^j` at each j<=13. Hence an alleged deterministic carry transition based only on (d,s,t,next parity) is unsound. This is **not** a lower bound against all finite-state models, more elaborate quotients, or k>2 packets. A straightforward three-/four-bit recursive expansion was attempted but was not completed within the research computation budget; no output or projected improvement is claimed from those interrupted runs.

## Independent executable proof-checking fixtures

Run `python research/r3e21_9_carry.py` from the repository root. The fixture uses the pre-existing *independently reconstructed* 179 reverse templates, Bařina simple-core, 144/38 roots, exact mod729 masks, and preserves all original R3E21-8 independent checks. It **reruns** 980 independently brute cyclic CRT cases, 2,000 signed off-boundary interval cases (empty/full masks, q=0 and q>=1, spacing beyond width and near B/E), 11,539 high-number direct shortened-prefix checks to K20, and the exact high-base inequalities to depth79. New separate oracles check all four mod4 packet orientations against true T^d trajectories across d=1,3,12,13,20, with small and very large n; independently compute K<=20 direct prefix survivors in four nonaligned windows, and confirm Q dominates those direct counts. The packet recurrence independently reproduces both inherited published totals and certifies the two new exact integers above; no 3x+1 full trajectories are executed to one and no operational scientific batch is conducted. Mathematical induction, executable integers and source inspection are not peer review or a Lean formalisation.

## Source-matched competitor audit and novelty gate

Actual **Bařina** full enhanced source: `xbarin02/collatz-sieve/src/fsieve.c`, confirmed Git blob `a0a2386584f7c3db4074044373c9bdea0056bdb1`. It really contains the CTZ-compressed `is_live_in_sieve_2_34v2` and `smallest_predecessor` congruence recursion (v3), plus terminal/coalescence processing. The previous source-port k8/k10/k12/k14 tests are valid *for those subset semantics only*. This session did not reconstruct bit-for-bit complete enhanced k34 for the non-aligned high-base interval with verified witness inequalities, so no comparable full [B,E) bound.

Actual **Angeltveit** Rust `vigleik0/collatz/main.rs` confirmed blob `4a33b870d27059feea28985e185b8c8c709eb313`; CUDA `collatz_cudav7.cu` blob `a783f0f39ee776c725036caec9c93d15a1c8ca72`, OpenCL `collatz_openclv2.cpp` blob `5cbe2c1e1958cf3b2ae1224ed3f1defe19db7fdc`; preprint [arXiv:2602.10466v1](https://arxiv.org/html/2602.10466v1), especially search1/precompute/search2/lookahead B=24/search3. Its interval [1,2^72) projections and path-merge/odd-even-even filtering are not full measured or certified matched-[B,E) results. R3E21-9's coherent-packet recursion is in the broad family of parity transducer and lookahead methods developed in prior work; independent novelty **UNPROVED**, and external ranking **INCOMPARABLE**. No mathematical claim from Tao's logarithmic-density theorem becomes a deterministic named-number exclusion.

## Gate

R3E21-9 supplies a new conditional upper-bound saving, a proved two-bit transfer and an explicit carry-state obstruction; **NOT an exact residual or operational acceleration**. A separately owner-invoked future R3E21-10 can explore higher-order compressed carry matrices or better interval-wise exactness (not another infeasible naive expansion). R3E21-2 and all frozen operational/sci assets remain FUTURE/UNTOUCHED. This session introduces only one mathematics report, one research-only fixture, a status overlay, and a FUTURE/UNEXECUTED prompt.
