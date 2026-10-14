# CEML-R3E21-22 — Universal reverse-basin hypothesis, run-cone generating function, and exact compression gate

**14 October 2026 — RESEARCH ONLY. NO NEW GLOBAL SIEVE MARGINAL. OFFICIAL CONDITIONAL CONSERVATIVE UPPER REMAINS 326865589733606241.** This session executes the live R3E21-22 mathematical research mandate with the owner's supplementary universal-generator/reverse-basin investigation. No Collatz-to-one scientific starts, owner computer, native verifier, operator, source identities, certificates, feed/site, hardware procurement, correspondence or R3E21-2.

## 1. Entry and authoritative accounting

Entry LIVE GitHub main was \`b45e0149b3c935082f8e1f6c25448ae6129ca06a\` (R3E21-21 merge). Main's connector-reported individual commit statuses were **empty: ABSENT NOT PASS**. This invocation did not establish hosted individual check runs, current Actions runs, all open PRs, detailed branch protection or ruleset state; those are **UNKNOWN**, not PASS. Research branch \`research/r3e21-22-reverse-compression\` was created from the pinned main. The R3E21-21 report/source and inherited R3E21-15–20 claims were read; R3E21-19 and R3E21-20 standalone reproducer scripts were **NOT independently rerun** here. The newly authored bounded research-only script did run and pass its own independent assertions. No claim of full inherited fixture replay.

Let \`T(n)=n/2\` for even positive n, \`T(n)=(3n+1)/2\` for odd positive n. The target is **[B,E)**, \`B=2392518188130438742016\`, \`E=3000000000000000000000\` EXCLUSIVE and \`W=607481811869561257984\`. Convergence below B, \`A(B)\`, remains **EXTERNAL-ONLY**; no external verification was rerun. Exact old admissible set \`S_old\` is **UNKNOWN**. Its independent inherited majorant is \`330156319374735841\`. Four previously consumed **pairwise disjoint** certified minima are h1 \`3007471253458601\`, h2 \`220259463699144\`, P3/P4 \`52093319358849\`, and Q6 \`10905604613006\`. Their sum is \`3290729641129600\`; the official **CONDITIONAL CONSERVATIVE UPPER** is exactly \`326865589733606241\`. A tenfold new upper would need \`294179030760245617\` genuinely **fresh and disjoint** exclusions, not simply a large known theorem-covered family.

## 2. Positive structural theorem: infinitely many whole residue classes certified by one formula

For each integer \`k>=1\`, let \`ell(k)\` be the smallest **positive** integer \`ell\` satisfying \`2^(k+ell)>3^k\`. Write \`u_k\` for the unique odd solution modulo \`2^ell\` of \`3^k u_k ≡ 1 (mod 2^ell)\`. Set

\`M_k=2^(k+ell)\` and \`r_k=(2^k u_k-1) mod M_k\`.

**Theorem (odd/even run-cone).** Every positive \`n≡r_k (mod M_k)\` can be written uniquely as \`n=2^k m-1\`, \`m\` odd and \`3^k m≡1 (mod 2^ell)\`. The first \`k\` genuine shortened-T steps are **odd**, with

\`T^i(n)=3^i 2^(k-i)m-1\` for \`0<=i<=k\`.

The next \`ell\` genuine steps are **even**, and

\`T^(k+ell)(n)=(3^k m-1)/2^ell < n\`

whenever the exact signed condition \`(2^(k+ell)-3^k)m>2^ell-1\` holds. Thus one finite symbolic residue rule proves strict descent for an *entire infinite arithmetic progression* apart from explicitly bounded exceptional small parameters. Strong induction, conditional on A(B) when relevant, certifies them without following their individual trajectories.

**Proof.** Each odd iterate of \`2^k m-1\` transforms \`3^i 2^(k-i)m-1\` into \`3^(i+1)2^(k-i-1)m-1\` while \`i<k\`. At time k the value is \`3^k m-1\`, divisible by \`2^ell\` by the congruence and with \`ell\` even iterations; the stated strict inequality is its exactly rearranged comparison with the original n. Inverting \`3^k\` modulo \`2^ell\` is valid since it is odd. The modulus \`2^(k+ell)\` imposes the required parity and congruence simultaneously. QED.

Examples (genuine, not guessed): \`k=1: n≡1 (mod4)\` (n>1); \`k=2: n≡3 (mod16)\`; \`k=3: n≡23 (mod32)\`; \`k=4: n≡15 (mod128)\`. The classes for different k are **disjoint**, since \`v_2(n+1)=k\`. The ordinary generating function of their positive starts is a (small-parameter-tail-adjusted) sum of geometric series \`∑_k z^(r_k)/(1-z^(M_k))\`; it is a compact infinite family representation, **not** a rational finite-state formula for the full Collatz basin. Its asymptotic natural density is \`∑_(k>=1) 2^(-k-ell(k)) ≈ 0.3568627488379456\`; existence follows by bounding the remaining k>K union inside \`n≡-1 (mod 2^(K+1))\`, of density \`2^(-K-1)\`. A finite number of initial exceptional values per k does not affect density because the same geometric tail controls their union.

### Exact full-window arithmetic without trajectory enumeration

The script computes for each k the exact half-open arithmetic-progression count

\`N_k=ceil((E-r_k)/M_k)-ceil((B-r_k)/M_k)\`.

All k>=72 have no possible n in [B,E) since n≥2^k-1>E; k=1..71 suffice. **Exactly 43** run-cone classes have nonempty intersection, with **exactly 216787629252827377045** distinct actual integers in their disjoint union. Their greatest needed certified descent depth is **69**; the others have zero members in this interval. The test reconstructs this entire count with arbitrary-precision integer ceilings and independent direct enumeration on many small, nonaligned windows. It directly checks authentic T prefixes for each nonempty representative and thousands of bounded small odd starts. No orbit-to-one run is involved.

**Crucial overlap result:** every one of these 216787629252827377045 starts has a **strictly smaller forward iterate by step <=69**, so they are **ALL ALREADY EXCLUDED** by the inherited J12-to-72 forward-descent condition defining S_old. Their intersection with S_old is empty. The exact certified *fresh* contribution to CEML's current candidate obligation is **ZERO**, not the displayed enormous total. This is a mathematical compression of a sublanguage, **not** an improvement of the existing sieve. The result illustrates both the value of algebraic families and the indispensability of overlap accounting.

## 3. Positive general theorem: affine lifting of two-path coalescence

If **authentic** finite paths satisfy \`T^j(a)=T^t(b)=z\`, with s and u odd steps respectively, let \`h=max(s,u)\`. Then for every nonnegative integer q the *entire parametrised pair*

\`n(q)=a+2^j 3^(h-s)q,  m(q)=b+2^t 3^(h-u)q\`

has genuine fixed parity prefixes, and

\`T^j(n(q))=T^t(m(q))=z+3^h q\`.

If \`0<m(q)<n(q)\`, every such n has an authenticated smaller trajectory representative. In particular, when the input slope of n exceeds that of m and the base inequality holds, one two-path witness generates an infinite safe arithmetic progression. This is a whole-class theorem, not the invalid inference from a single sample's quotient.

**Concrete non-descent/tail-merge separation:** for every q>=0, \`n=31+72q\` and \`m=27+64q\` satisfy \`T^3(n)=T^6(m)=107+243q\`, while \`0<m<n\`. Every first-three-step forward iterate of n is **greater** than n, so the smaller-trajectory certificate is logically distinct from forward descent at that horizon. Exact full-window occupancy of this class is **8437247387077239694**. **Hostile prior-art check:** \`m=(8n-5)/9\`, with n≡4 mod9; it is exactly **Bařina's already known P2 inverse** at the starting time, NOT a fresh inverse-language discovery. R3E21-20 proves P2 equals h2 at the *preceding* genuine step for j>=1, but does not eliminate the starting-time boundary case. This family cannot be subtracted from the CEML majorant, as no fresh disjointness from S_old and all prior gates has been proved. First-hit labelling alone is not such a proof.

**Proof of the lifting theorem.** On any fixed genuine parity cylinder \`a+2^j q'\`, the exact R3E21-21 affine formula is \`T^j(a+2^j q')=T^j(a)+3^s q'\`. Substitute \`q'=3^(h-s)q\`, and similarly for b. Both sides equal \`z+3^h q\`. The slopes and positive strict numerical inequality decide induction eligibility; equality or reversed ordering does not. QED.

## 4. Hostile no-go: finite seed basins and bounded universal descent

**Theorem (finite-seed bounded-backward obstruction).** Let F be finitely many completely verified seeds whose forward orbits enter the 1↔2 cycle, and let H be the finite union of their orbit values. In at most K reverse steps, at most \`|H|*(2^(K+1)-1)\` positive starting values can meet H: every y has at most two positive immediate predecessors, \`2y\` and, only for y≡2 (mod3), \`(2y-1)/3\`. Thus no finite list of specific verified seeds expanded only to a fixed reverse depth covers all positive integers. Unbounded depth or a parameterised *infinite seed family* is required. This does **not** disprove that all numbers eventually reach 1; that reverse-basin equality **is the conjecture**.

**Theorem (all-odd uniform-depth obstruction).** For every K>=1 and every positive odd m, \`n=2^K m-1\` has K consecutive genuine odd steps and \`T^i(n)=3^i 2^(K-i)m-1 > n\` for all 1<=i<=K. Consequently **no fixed universal forward-descent horizon K** can eliminate every positive input. In the literal target interval the all-odd class at K=69 occurs **once**, namely \`n=2951479051793528258559\` (m=5). It has no strict forward descent in its first 69 steps. The class at K=68 occurs twice. These are *not* certified CEML survivors: an authentic smaller predecessor or a later strict descent may still certify them. This theorem refutes only universal fixed-depth direct descent, not all possible finite algorithms or all compact grammars.

**Adversarial false-run example:** 11 has three-step iterate 13>11 (the first odd block does not imply descent); descent needs the explicit congruence and signed coefficient, not a suggestive residue family label.

## 5. Three R3E21-22 compression routes investigated

**A. Shifted rational generating functions and dyadic residue packets.** The run-cone classes admit an exact, compact O(log E) symbolic parameterisation, exact nonaligned interval counts and a provably disjoint union (by v_2(n+1)). This is a real positive compression **for a thin, specifically structured certificate language**, including arbitrarily large k in its symbolic statement. It does **not** compress arbitrary genuine 72/160/256 prefix languages. For arbitrary words, R3E21-21 already constructs exact high-bit interval/carry transfer, and gives explicit same-(j,s,C mod729) endpoint/phase collisions. A quotient forgetting the low-bit residue and actual endpoints is unsound. The all-odd branch forces unbounded direct-descent horizons. No polynomial bound on a full exact compressed state set was proved.

**B. Renewal/return kernel.** Run-cones give an exact deterministic first return after k odd plus ell even steps on the prescribed residue. However an arbitrary odd m outside the modular subcone may have fewer than ell even steps; no uniform renewal contraction or exhaustive return decomposition follows. The all-odd cylinders at every K are explicit hostile cases. No independent-parity, multiplicative (394/729)^r, Markov-spectral or full-modulus binomial estimate was used. In particular the j256 >=162 odd necessity from R3E21-20 is still NOT a valid uniform frequency estimate over this short actual interval.

**C. Canonical first-hit and finite coalescence quotient.** The affine tail-lift makes authentic trajectory joining a whole-class statement under precise slope and residue hypotheses. R3E21-16 already proves finite graph-quotient collapse: a safe connected-component exclusion needs a positive strictly smaller representative, and every finite witness composes to a two-path one. The explicit 31+72q example is already P2; the 216.8e18 run-cone family is already direct-descent-excluded. Without exact membership of S_old and all consumed h1/h2/P3/P4/Q6 gates, an earliest-certificate priority partition cannot establish a new disjoint marginal. Consequently **certified fresh exclusion lower 0** and **official upper unchanged**. Even knowing an exact full-window size of a new-looking family is insufficient.

**Complexity/cost verdict:** A compact formula does compress selected reverse/descent cones *enormously* relative to enumerating individual starts, but it achieves **zero new candidate-obligation compression**. No certified bounded-state exact aggregate evaluator beyond 72 for arbitrary certificates, no 10x/100x, no global completion, no independent world novelty, and no guaranteed runtime benefit was established.

## 6. Prior art and proof provenance

Engaged R3E21-14's predecessor first-hit disjoint counting, R3E21-15 two-odd tail merges, R3E21-16 finite graph-quotient collapse, R3E21-17 P3/P4, R3E21-18 nine-step source-grammar gap, R3E21-19 high-odd architecture cap, R3E21-20 P2 shift and long-block threshold, and R3E21-21 exact carry/endpoints with adversarial collisions. The inherited 62289308018259707 high-odd figure is only a **ceiling**, not a new exclusion. These are prior-session claims and not all were reproduced afresh.

Source pins retained for scrutiny: Bařina \`xbarin02/collatz-sieve/src/fsieve.c\`, blob \`a0a2386584f7c3db4074044373c9bdea0056bdb1\`, four recursive \`smallest_predecessor\` primitives vs the **full** CTZ/v2/v3 executable (not interchangeable); *Improved verification limit*, J. Supercomput. 81:810 (2025), DOI https://doi.org/10.1007/s11227-025-07337-0. Angeltveit \`vigleik0/collatz/main.rs\`, blob \`4a33b870d27059feea28985e185b8c8c709eb313\`, \`search1/search2/search3\` incl. rational/double-even, mod9/24-lookahead and 16-step continuation; https://arxiv.org/abs/2602.10466 (2026). The general reverse-branch/tail-merger idea is **not asserted to be original**. Neither complete competing executable was rerun on the same [B,E) inputs; matched performance/coverage **INCOMPARABLE**.

## 7. Verification, exact custody and next sharp question

Self-contained \`research/r3e21_22_reverse_compression.py\` executed under Python with **PASS**: arbitrary-precision full-width ceilings, 43 nonempty residue cones and 216787629252827377045 union count; max descent depth 69; genuine T-prefix/orbit algebra on class representatives and bounded starts; signed run inequalities; exact small-endpoint independent enumeration; literal K69 no-descent witness; affine coalescence identities and known P2 alias. No trajectories to one, no production runs. **R3E21-19 and -20 standalone scripts were not independently rerun**; original inherited independent evidence is cited as previous-session provenance, not falsely promoted to current PASS. Hosted check runs/Actions/protection not independently established: UNKNOWN.

**Most promising next theorem target:** Find a genuinely *new* parameterised affine tail-meeting or return family that lies **inside actual S_old after all 72 forward-slope tests**, misses h1/h2/P3/P4/Q6 at **every consumed time**, and has an exact **positive disjoint intersection lower bound** on [B,E). Alternatively establish an exact non-phase-blind finite-window transfer identity for the complete certificate disjunction with state-cost subexponential in depth 160/256. A symbolic generator alone is insufficient; **prove fresh overlap subtraction or retain upper 326865589733606241**.
