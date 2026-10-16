# R3E21-42 — one universally descending high lift per global f43 odd-q search1 root

**16 October 2026 | £0 bounded research only | global arithmetic partition and original-start theorem, not a new interval-sieve upper | GO for mathematical theorem subject to CI; NO-GO production/science.**

## Result, with the correct quantifiers

For **each** of the exactly **6,438,209,236,755,220** source-search1 66-bit roots with f=43 and positive odd terminal even-run q (R41), there is a **uniquely and constructively chosen original start n in [B,E)** whose literal shortened Collatz iterate satisfies **T^69(n)<n**. The choice is among a canonical block of eight consecutive clipped high lifts n=r+a·2^66. It is not a sampling inference, probabilistic extrapolation, conjecture resolution, or assertion that all eight/nine lifts descend. Distinct roots give distinct starts. This is a global arithmetic subpartition, **not** a verified new disjoint improvement to the existing conservative full-interval candidate upper.

Outside R40's one completed low48 cylinder, the new witnesses comprise **6,438,209,236,742,819 different original starts** with exact mathematical strict descent by step 69. The other **12,401** roots have one canonical witness each inside that cylinder and overlap R41's **54,438** fully replayed admitted descendants. The union of this new outside-cylinder family with all R41 cylinder-admitted descendants has exactly **6,438,209,236,797,257** different original starts. They have valid strictly-smaller-first-descent witnesses, **not** necessarily trajectories to 1 absent the usual lower-start induction hypothesis.

A separate exact finite automaton count partitions the 6,438,209,236,755,220 roots by terminal source doubleeven flag: **5,973,115,806,935,136** flag=0 and **465,093,429,820,084** flag=2 (flag=1 absent). The canonical block of eight clipped lifts contains **4 or 5** source-mod9-and-flag admitted original starts for each flag=0 root, and **1 to 3** for each flag=2 root. Therefore at least **24,357,556,657,560,628** distinct [B,E) original starts pass *these source-search2 mod9 and flag gates*, regardless of bitmap. This is an **exact proven lower bound, not an exact admission total and not a descent certificate for that admitted subset**. The guaranteed step-69 canonical lift may be rejected by source search2. These two claims must not be conflated.

## Theorem: canonical eight-lift, three-even descent

Let **L=2^66**, **P=3^43**, **B=2392518188130438742016**, and **E=3000000000000000000000** exclusively. By division with remainder,
B=32L+31334946695616135168 and E−1=40L+48520948206471741439.
For every root 0≤r<L, the clipped lift range
a_min=max(0,ceil((B−r)/L)), a_max=min(63,floor((E−1−r)/L))
contains eight or nine consecutive nonnegative integers. Its first eight are:
- a=33,...,40 if r<31334946695616135168;
- a=32,...,39 otherwise.
The optional ninth lift exists precisely when 31334946695616135168≤r≤48520948206471741439. Thus the first eight are always valid, positive and wholly in [B,E); there is no wrap.

The first 66 T parities depend only on r mod 2^66. For all these lifts, with the same f=43 parities, the exact lifted affine identity is
**T^66(r+aL)=T^66(r)+aP=number−1+aP**.
Since P is odd (P≡3 mod8), a↦number−1+aP maps **any eight consecutive a** bijectively to residues modulo 8. Therefore **exactly one** a in the canonical block yields T^66(n)≡0 mod8. This explicitly computable a is the *canonical lift*. The next three T operations are even, so T^69(n)=T^66(n)/8.

For any n with f odd applications in the first i steps, direct expansion gives the exact affine formula
T^i(n) = (3^f/2^i)·(n+δ),
δ=Σ_{j∈odd-step indices} 2^(j−1)/3^(number of odd steps through j).
Each summand is nonnegative and <2^(j−1), so **0≤δ<2^i**. Applied at i=66, f=43:
T^69(n)< P·(n+L)/(8L).
Since n≥B, the exact integer inequality
**(8L)B−P(B+L)=602711608716672977428071654355915277074432 >0**
implies P(n+L)<8Ln for *every* n≥B. Hence **T^69(n)<n**. This mathematical argument does not rely on source bitmap scores, a rational-log approximation, lookup map, sampled values, no-small-intermediate hypothesis, or an assumed universal Collatz result. It is valid for each of the R41 search1 roots conditional on that finite root-count/provenance theorem.

Distinct roots are distinct n mod L, so one canonical original start per root is injective. This is a **strict descent**, not yet a full convergence-to-one result without already verified lower starts.

## Source-search2 admission lower-bound theorem

For this terminal branch the finite source-search1 automaton leaves flag∈{0,2}. In the source-search2 per-lift gate, n mod9 must be one of {0,1,3,6,7}; with L≡1 mod9, this is exactly (r+a) mod9 in that set. For flag=0 there is no second gate. For flag=2 the additional exact gate is (number+a) even. Enumerate exhaustively all nine r mod9 phases, both a-window origins 32/33, and both parities of number. A block of eight a has flag0 acceptance 4..5, flag2 acceptance 1..3. The **bound** 4·5973115806935136 + 1·465093429820084 = **24357556657560628** is consequently global and constructive (at least this many distinct admissions).

The optional ninth a, 24-bit inverted bitmap index ((number·3^(−43) mod 2^24)+a) mod 2^24, reset q=0 vs real inherited q odd, and 1=LIVE bitmap remain **unclassified globally**. There is no source-wide exact count of bitmap-cleared, bitmap-live or all admitted starts; do not multiply these lower bounds by a bitmap percentage. This theorem does not close the source-search2/binary-correctness gap.

## Finite oracle, obstruction and quantified untouched work

The new standard-library fixture [r3e21_42_global_lift.py](../research/r3e21_42_global_lift.py) independently tallies R41 terminal flag classes by exact recurrence, tests the exact inequality and all 9×2×2 flag-admission cases, then probes **500,000 distinct globally dispersed 66-bit roots**, not a second low48 cylinder. Of these, **188** are exact f43 odd-q source-search1 roots (169 flag0; 19 flag2), with **142** eight-lift and **46** nine-lift cases. For all 188, directly executed **69 literal T steps** verify canonical T^66 state, three even steps, and strict step-69 descent. In that finite oracle **91** canonical witnesses pass the source mod9/flag admission and **792** of the eight-block lifts are admitted; these are bounded observed counts, not global ratios. SHA-256 of the 188 sorted canonical original starts in decimal LF-terminated:
**9ef6a392ba9670a432fe28c70f5107b2a8156f54d72eecef2cee74f9fc86df8d**.

A concrete non-merging countermodel: roots **19960102505848050927** and **26054861896966332583** have identical terminal R41 DP tuple (f=43, flag=0, q=1), but different r mod9 (0,1) and number mod8 (7,3). Therefore merging to (f,flag,q) **cannot recover** future source-search2 or canonical-lift choices. Any exact automaton must retain more arithmetic/carry information; R41's DP alone is **not** a source-search2 transducer. This is a specific quotient obstruction, not a proof no richer compression exists.

All **6,438,209,236,755,220 roots** now have one original strict-descent certificate; zero roots remain entirely unwitnessed by this particular selection theorem. However **7R = 45,067,464,657,286,540** other baseline eight-block original starts remain without a *global* direct-witness classification, as do the optional ninth starts for roots in the middle clipping band (their exact number m is not yet known, 0≤m≤R). Thus unresolved per-root high lifts = **7R+m**; the prior R41 bounded low48 cylinder independently certifies more of those. These are *not* counts of actual Collatz survivors, and cannot be subtracted from the conditional original-start candidate upper without disjoint prior-rule/coverage proof. The exact full source-search2-original-start partition requested in option A remains open; R42 achieves **option B**, an explicit genuinely global closed witness subpartition and a complementary exact symbolic accounting, with the optional middle-band tally unresolved.

## Source refresh and inherited protections

First-party source pins re-read 16 October 2026: Angeltveit [Rust main.rs](https://github.com/vigleik0/collatz/blob/f3f09248c7ae7299b8443e112f565f309d97f161/main.rs), [CUDA](https://github.com/vigleik0/collatz/blob/f3f09248c7ae7299b8443e112f565f309d97f161/collatz_cudav7.cu), [OpenCL](https://github.com/vigleik0/collatz/blob/f3f09248c7ae7299b8443e112f565f309d97f161/compute_kernel2.cl); [Bařina pinned worker](https://github.com/xbarin02/collatz/tree/141e13aae243d509a01a43bec597f53a5b97a09f) and [collatz-sieve](https://github.com/xbarin02/collatz-sieve/tree/e5f0c264ba1f5f9c0a7d32a10c3aa61b225c70d1). HEADs checked separately: Angeltveit f3f09248 (same), Bařina worker **e98d0294a7ff77e783907e307a80e83b92f4a164** (different), sieve e5f0c264 (same). Bařina's public live page still reports lowest incomplete/unassigned **2175982616×2^40** at this inspection; this is an author-reported operational position, **not** CEML reproduction or the peer-reviewed **n<2^71** limit. Angeltveit arXiv **2602.10466v1** is separate from live code and untested binary claims. Source-text re-reading and exact arithmetic **do not** validate delivered maps, native builds, GPU exception reservations, or a whole-interval arbiter.

R41 merged main **d072a69d0ef6df6e5a96eb0aabc0cc4b46a3ea6d**, R41 PR #72 head **426ef69a035c020fcf055fdee4ed5cb942a0ad95**: PR Action run [38814092591](https://github.com/jfairfaxball-348/CEML/actions/runs/38814092591) and main-push run [38814208642](https://github.com/jfairfaxball-348/CEML/actions/runs/38814208642) both separately reported completed SUCCESS on their exact SHAs. R42 checks must be checked independently and are not inherited. Branch main reports protected=false, repository rulesets empty; detailed enforcement not thereby universally certified.

R36 j98 closed, R39 j114/j130 m≤3 partial later-block residuals **362205922639287064** and **1080231996567188756950656** unchanged; pre-multiply guards remain necessary. R40 167 source-clear/corrected-live digest **ea27859daa20511ce786caba1c212110663e1d42fbb36f7b7a299028ed96406e** and R41 54,438 admitted digest **7edb1e7df2015e373d4bfc02dd120b7e645e543f2c880f3120194ccfeeecb761** preserved. No independent LUT50 original raw/binary digest, host flags, every source exception path, workgroup/partial-work unit reservation or independent original-start arbiter; no production CPU/GPU, paid cloud, crowdsourcing, owner PC, benchmarks, science, correspondence, publication, frozen protocol, website or feeds.

Immutable interval: B=2392518188130438742016, E=3000000000000000000000 exclusive; **552501489** complete 2^40 units plus partial **350507499520**; conditional conservative candidate upper **326518028938128165 unchanged**; **actual unresolved Collatz survivor count UNKNOWN**. The result does not independently certify a full interval or justify a novel world frontier.

**Decision:** R42 mathematical global canonical-lift theorem **GO**, subject to observing exact-head fixture CI; source-search2 bitmap-wide admission/witness intersection and native scientific operations **NO-GO**. R43 is FUTURE / UNEXECUTED.
