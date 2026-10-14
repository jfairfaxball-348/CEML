# CEML-R3E21-21 — Exact dyadic interval/carry transfer, endpoint collision and long-block hostile gate

**14 October 2026 — research only.** A constructive deterministic counting theorem and a self-contained bounded research-only Python implementation are obtained. **No new complete depth-72/full-window exclusion lower or independent majorant reduction. Official conditional conservative upper stays 326865589733606241.** No Collatz-to-one science or new frontier is claimed.

## Entry, provenance, and preserved accounting

Live main entry **b2a3cb3dc4873627ec16093269609bee69453a09**, the merged R3E21-20 PR #48 (authored head bfe293e68357902df0df80c720b1eb5e50896536). At entry there were zero open PRs; GitHub commit statuses and PR-triggered Actions for main were empty: **ABSENT NOT PASS**. No hosted check or protection-policy success is inferred; detailed protection/ruleset observations not freshly accessible here are **UNKNOWN**. This is distinct from local research reproducer assertions.

Set B=2392518188130438742016, E=3000000000000000000000 exclusive, W=607481811869561257984. A(B) remains an **external-only**, unreproduced convergence assumption. Actual S_old is **UNKNOWN**; the independent old majorant is 330156319374735841. Previously consumed **disjoint lower exclusions**, never subtracted twice: h1=3007471253458601, h2=220259463699144, P3/P4=52093319358849, Q6=10905604613006. Their sum is 3290729641129600 and the official CONDITIONAL CONSERVATIVE upper is 326865589733606241. Another 294179030760245617 certified *fresh* exclusions would be required to lower that upper by 10x. The 62289308018259707 high-odd architecture saturation is only a **possible-candidate upper**, not additional actual exclusions. R3E21-20's endpoint-blind 361949403623614344 upper at depth63 is weaker than the official bound, and its P2 shift is already h2.

The source-pinned comparison remains: Bařina `xbarin02/collatz-sieve/src/fsieve.c`, pinned blob `a0a2386584f7c3db4074044373c9bdea0056bdb1`, `smallest_predecessor` four recursions **versus** his full CTZ/v2/v3 executable; Angeltveit `vigleik0/collatz/main.rs`, pinned blob `4a33b870d27059feea28985e185b8c8c709eb313`, search1/search2/search3 (306/485 rational path, mod9/24-lookahead, chunk continuation). Their entire actual [B,E) outputs were not executed in equivalent conditions: competitor speed/coverage **INCOMPARABLE**; mathematical priority **UNPROVED**. Read R3E21-17 through 20 as prior controls.

## Theorem 1: exact interval-conditioned parity/carry transfer at arbitrary finite depth

Let the genuine shortened map be T(x)=x/2 for even x and T(x)=(3x+1)/2 for odd x. Suppose a genuine depth-j parity cylinder of positive inputs in [B,E) is represented by

- n(q)=a+2^j q, with integers q in the half-open interval [L,R);
- T^j(n(q))=y+3^s q, where y=T^j(a) and s is the number of odd inputs in the fixed prefix.

This invariant follows by induction from the standard affine parity-word identity and does **not** require T^j(n)<n, statistical drift, or any convergence assumption. Because 3^s is odd, child parity b is achieved exactly by q=k+2u with k congruent to b−y (mod2). The child is

- n'(u)=(a+2^j k)+2^(j+1)u;
- T^(j+1)(n'(u))=T(y+3^s k)+3^(s+b)u;
- u ranges exactly over [ceil((L−k)/2), ceil((R−k)/2)).

This transports actual high-bit information, affine output/carry and both half-open endpoints with **zero error**. The coefficient of the signed forward comparison is 3^s−2^j, and the signed constant is y−a. Consequently the exact condition T^j(n(q))≥n(q) clips a **linear half-line** of q, without a drift approximation. For a genuine affine inverse predecessor P(y)=(m y−h)/d, if y mod d is fixed and integrality/positivity are verified, P(T^j(n(q)))≥n(q) is likewise a linear half-line. Intersecting these exact constraints with [L,R) gives a closed interval or the empty set; a general *disjunction* of alternative certificates may require a finite interval union rather than one cell, which must be retained, not discarded.

For all inherited live J12 roots s≥8, so 3^s is divisible by 729 and every later authentic T^j(n(q)) mod729 is frozen by the true parity prefix. Thus h1=(2y−1)/3 at residue 2 mod3; h2=(4y−5)/9 at 8 mod9; P3=(64y−73)/81 at 10 mod81; P4=(128y−211)/243 at 182 mod243; and Q6=(512y−809)/729 at 433 mod729 have exact phase gates throughout each cell. Check the **positive** numerator, signed strict-smaller inequality and underlying authentic inverse word before excluding. P2=(8y−5)/9 at 4 mod9 is exactly a shifted earlier h2 and contributes no new gate.

Finally input n mod729∈U is counted **exactly** for every cell. Since gcd(2^j,729)=1, q runs a cyclic permutation of the 729 residues; for length N=729v+r, the exact U count is 394v plus the length-r cyclic sum beginning at actual (a+2^j L) mod729. There is no universal-max-per-cylinder slack, product of independent mod729 factors, or unknown endpoint approximation. This theorem is exact at **any finite j**; it is not an efficiency theorem.

## Reproduced quantitative bounded evidence

`research/r3e21_21_exact_transfer.py` is self-contained, uses Python arbitrary-precision exact integers, reconstructs the 182 J12 roots, 179 old templates, 144 nonempty roots and shared |U|=394, and transfers authentic input intervals for the relaxation **J12+U, then forward non-descent plus h1/h2/P3/P4/Q6 tests at each depth 13..j**. All counts below are exact for **this specific truncated relaxation**, not for S_old or the final 72-level scheme:

| Depth j | Nonempty exact cells | Exact eligible starts in [B,E) |
|---:|---:|---:|
| 12 | 144 | 11542623161487612644 |
| 13 | 250 | 10019638161013552641 |
| 14 | 455 | 9117870726522332897 |
| 15 | 856 | 8576810265827601055 |
| 16 | 1467 | 7349404591103440853 |
| 17 | 2700 | 6763255758684148017 |
| 18 | 5046 | 6319886770059298313 |
| 19 | 9298 | 5822662226319000746 |
| 20 | 17893 | **5602543300469234251** |

The reported j20 relaxation mass is about **17.14 times LARGER** than the official majorant (which applies to far stronger prior sieve conditions). It is **not** an improvement, and cannot be subtracted from the official bound. The script also checks 40000 real starts [B,B+40000) against a separately written genuine-positive-integer truncated-T/predicate oracle, with identical memberships. This runs NO trajectory to one. Entry R3E21-19 and R3E21-20 reproducer source was inspected, and the new independent root/mask reconstruction and signed oracle were run; **the two previous scripts were not both independently rerun as standalone full commands in this session**, so do not assert a full inherited-fixture replay.

## Theorem 2: explicit information loss in phase-only finite-state compression

At j=20 the genuine parity cylinders r=188443 and r=405531 both have (s,C mod729)=(15,698), but their exact U input populations in [B,E) are, respectively, **313113692531676** and **313113692531673**. Here endpoint lengths coincide (both endpoints are divisible by 2^20); the discrepancy is the differing actual input-phase alignment.

More sharply at j=22, genuine parity cylinders r=1253403 and r=2097179 both have (s,C mod729)=(16,559). The numbers of input points before U masking are respectively **144834950415984** and **144834950415983**; their exact U populations are **78278423132918** and **78278423132917**. This explicitly exhibits **exclusive-right-endpoint** and phase differences behind the same compressed state. Hence (j,s,C mod729, multiplicity) alone is **not an exact endpoint/count transfer state**: one must retain at least the cylinder's input residue/phase and actual integer bounds, or prove a separate rigorous aggregate correlation identity. This disproves that proposed state sufficiency, **not** the possibility of some different small exact automaton.

The observed exact-cell count increased 144→17893 between depths12 and20. Naively splitting all 144 roots to depth72 allows as many as **166020696663385964544** branches; this is an upper on raw branching, **not** a proved lower on optimal compressed state complexity. No polynomial state bound or practical j256 evaluator was obtained. Most importantly, an exact arithmetic algorithm that cannot yet evaluate the depth-72/256 full-window mass is not a claimed 10x sieve.

## Route 2: long renewal without false independence

R3E21-20's signed rational necessity for no forward descent, (3B+1)^s≥2^j B^s, remains valid and forces at least **162 odd inputs among 256 genuine steps**. Counting the >=162 parity vectors modulo 2^256 and multiplying their fraction by W remains invalid: W=607481811869561257984 is shorter than 2^256, and each such vector's cylinder holds at most one target start. There is no justified iid or spectral contraction from the initial and endpoint phases.

The research script gives a bounded adversarial *deterministic frequency check*: for 256 starts in [B,B+256), **8** have no strict descent in their first 32 shortened steps; for the adjacent equal-size block [B+256,B+512), only **1** does. For 20 steps the corresponding counts are **13** and **5**. These unequal exact counts refute an assertion that all equal-size aligned windows have *identical exact proportions*. They are **not** a statistical refutation of an iid *heuristic*, nor do they transfer to W or 256-step counts. To use the binomial tail, one would need a proved bound on the intersection of the interval with the inverse parity language, including high-bit carries, or exact blockwise symbolic counts.

## Route 3: full early-certificate union and canonical earliest hit

For any fixed finite list of authentic strict-smaller witnesses (including direct descent), define the first certified time j; at tied time order candidate witnesses by an explicit fixed index. Every excluded actual input then has a **unique canonical label**, giving a disjoint partition of the *full early-certificate union*. The proof is simply well-ordering of the finite list of genuine checks; it gives **no** counted lower until label preimages are counted with exact signed positivity and with prior S_old membership and already consumed h1/h2/P3/P4/Q6 exclusions filtered. The above interval transfer can represent intersections of affine gate constraints, but the phase/high-bit state burden and multi-time overlap have not been conquered. P2 shifts h2 and is not fresh. No newly proved globally disjoint marginal follows from this partition alone.

## Verdict and continuation

**Positive:** a fully deterministic **zero-error** interval-conditioned lift/count method of arbitrary finite depth, with exact signed predecessor clipping, exact CRT cycle occupancy and a self-contained small-depth reproduction. **Negative:** the compressed-state collision formally kills the tempting endpoint-blind exact transfer; no efficient long-depth aggregator or 10x/100x global mass gain yet exists. Keep the old conditional conservative upper **326865589733606241 UNCHANGED**; actual S_old UNKNOWN.

**R3E21-22 must develop compression**, not another tiny depth extension: partition the full dyadic interval into exact blocks; seek a certified quotient that preserves a finite collection of shifted-phase/carry generating functions, prove an aggregate count identity or a state-count lower barrier, and attempt one serious long-block certificate union with exact early-hit disjointness. Distinguish proof from experimental state counts and test on the literal nonaligned B/E.

No native Collatz-to-one scientific batch, owner machine/local Codex, production, verifier/frozen identities/certificates, site/feed, expenses, correspondence, R3E21-2 or independent A(B) verification occurred.