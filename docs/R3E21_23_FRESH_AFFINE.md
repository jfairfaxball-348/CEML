# CEML-R3E21-23 — Fresh nine-step affine reverse families and authenticated disjoint CRT mass

**14 October 2026 — RESEARCH ONLY.** A new conditional mathematical exclusion lower, independent of the already consumed CEML sieve families, is supported by an exact deterministic symbolic calculation and a genuine 22-digit trajectory-prefix witness. It is not full Collatz convergence, a new scientific interval, a native verifier result or a claim of world novelty.

## Entry and complete accounting

Pinned LIVE remote main: 464f18ff638c2544b23e00eb444947326d5e16c7; tree cc658587e6f2a09ac9db0b0f7ea27a61e0310b9e (R3E21-22 merge). At entry open PRs 0; Actions runs 0; commit check-runs 0; combined status "pending" with ZERO individual contexts: ABSENT, NOT PASS. Repository rulesets []; main branch response publicly unprotected; detailed protection API HTTP403: UNKNOWN rather than waived evidence.

The true shortened map is T(n)=n/2 for even positive n and T(n)=(3n+1)/2 for odd positive n. B=2392518188130438742016; E=3000000000000000000000 EXCLUSIVE; W=607481811869561257984. A(B) is inherited from a DYNAMIC EXTERNAL operational report only; it has not been independently reproduced. Actual S_old is UNKNOWN; the independent old upper bound is 330156319374735841. Four mutually disjoint previously consumed certified minima: h1=3007471253458601, h2=220259463699144, P3/P4=52093319358849, Q6=10905604613006. Previously official conditional conservative upper=326865589733606241.

**R3E21-23 NEW certified conditional lower at least 21708672114515.** Subtract exactly ONCE, yielding **NEW conditional conservative upper 326843881061491726**. This is only a 0.006640% saving on the previous upper, not tenfold; the additional fresh lower needed to reduce the *new* bound to a tenth of the old upper remains roughly 294.157 quadrillion. It is not an exact number of explicit checks, nor a speed benchmark. Novelty versus full Bařina CTZ v2/v3 and Angeltveit search1/2/3 is UNPROVED; matched-runtime and full-window comparison NOT_RUN.

## The new mathematical object — 21 nine-step reverse residues

Consider all genuine length-nine T parity words having exactly six odd inputs and ending with an even step. With affine carry H(w), their exact identity is

    512 T^9(p) = 729 p + H(w)

where H(w) is recursively H -> 3H+2^i on odd step i and unchanged on even step. Writing y=T^9(p), the inverse is p=(512 y-H(w))/729, valid precisely when y is in the associated residue r(w)=H(w)*512^(-1) (mod729) and p>0. Integrality fixes the input mod512 and hence authentic parity word; the research script also directly tests true nine-step paths, not just the algebra.

There are 28 such words and 22 distinct target residues; 6 residues have two words. For each residue retain the candidate with larger H, which yields the smaller positive p at the high target and is conservative for strict-smaller induction. One residue is 433, the already consumed Q6 word (H=809): EXCLUDE IT. The remaining 21 possible new target residues are exactly

    91 103 121 175 182 319 334 337 364 410 425
    445 496 524 562 587 604 661 688 695 724

Their word identities are not asserted to be new in the literature. Some might be aliases under a different source grammar. We therefore separately reject all source P1, P2, P3, P4, the consumed h1/h2 and Q6 on EVERY relevant true forward prefix; this establishes newness relative to *CEML's consumed disjoint mathematical certificates*, not relative to complete competitor executables.

For authentic j-step n -> y with s odds and carry C, 2^j y=3^s n+C and 0<=C<=2^(j-s)(3^s-2^s). The signed strict inequality for each new word H is

    729*2^j*(p(y)-n) = (512*3^s-729*2^j)*n +512*C-H*2^j.

Over all 21 residues, j=13..72, s=8..j with negative coefficient, the largest sufficient input threshold calculated using the proved C maximum is **486401989**, attained at (residue 524,j71,s45). Thus n>=B makes the negative-slope condition 512*3^s<729*2^j sufficient for p(y)<n uniformly; integrality and positivity follow from the true residue word and y>=n>=B for kept prefix cylinders. The new code verifies this exhaustive *finite arithmetic proof obligation* with exact Python integers.

## Freshness, source control and disjoint-prefix stopping proof

Reconstruct the inherited J12 182 source roots and all 179 nine-or-shorter restricted inverse templates, the 144 live roots and their *identical* allowed input-phase mask U mod729 of size 394. Each root has at least 8 odd steps, so along a fixed true parity word the current y mod729 is **exactly** C_j*2^(-j) mod729. This does NOT supply an independent new 729 factor: input n mod729 is separately and only ONCE masked by U.

A state (j,s,C_j mod729,hit), initially at each of the 144 eligible true depth12 parity roots, advances along each authentic parity bit b. Reject if 3^s<2^j (old forward strict-slope failure). Reject if any inherited h1=(2y-1)/3 at y=2 mod3, h2=(4y-5)/9 at y=8 mod9, P2=(8y-5)/9 at y=4 mod9, P3=(64y-73)/81 at y=10 mod81, P4=(128y-211)/243 at y=182 mod243, or Q6=(512y-809)/729 at y=433 mod729 has negative signed slope. The earlier R3E21-13/15/17/18 high-base threshold proofs make these valid strict-positive-smaller exclusions for n>=B; the extra P2 test only makes the new set SMALLER. Set hit at any NEW 21-residue inverse whose 512*3^s<729*2^j. First stop only if hit and s>=47 by j<=67.

**Why no hidden late overlap at depths up to 72?** Since 3^47>2^72 and 2^t 3^47>3^a 2^72 for ALL inherited inverse pairs (t,a)=(1,1),(2,2),(3,2),(6,4),(7,5),(9,6), every later true extension through j72 remains non-descent on the old slope and cannot acquire a new negative-slope inherited predecessor. Therefore all stopped full dyadic cylinders, input-masked by U, lie inside actual S_old and outside the four already consumed certificate sets at ALL j13..72, including Q6 and the P2 source alias. Early-stop leaves are prefix-free, hence disjoint even if a trajectory has multiple new words.

An entire stopped cylinder is an authenticated true parity family. No conjectural independence or no-overlap inference is used. Conditional strong induction applies to the new smaller **positive** precursor p(y) because its true T^9 path coalesces with T^j(n). It is not necessary to know the remainder of either orbit if every smaller positive start is already certified.

## Exact unconditional integer counting of the stopped family (conditional induction)

At each depth k, for any dyadic cylinder in [B,E), at least N_k=floor(W/2^k) actual values occur. Their input phase modulo729 advances by stride 2^k coprime to729. For U, define the exact all-phase lower

    g(k)=394 floor(N_k/729)
          + min over a=0..728 of #{0<=i<N_k mod729: (a+i*2^k) mod729 in U}.

No approximate density, iid assumption, independent future phase or endpoint alignment enters this bound. The self-contained code computes each min by a 729-state cyclic sliding window and independently direct-brute checks fine-depth remainders. The forward multiplicity antichain stops **10387180339353** pairwise disjoint genuine dyadic cylinders. The independent memoised backward evaluation (348941 distinct states in the original research run) confirms the same total weighted exact integer lower

    sum_k stopped_cylinders(k)*g(k) = 21708672114515.

Stop-depth histogram (depth: number of cylinders):
53:7; 54:251; 55:4677; 56:61162; 57:625486; 58:5269205; 59:37783366; 60:237093141; 61:1331173893; 62:6793164766; 63:31933036933; 64:139221037762; 65:563325347947; 66:2117978502274; 67:7526317238483.

**Separate measures, not conflated:** gross unmasked total actual full-window mass lies between 64011865372386 and 74399045711739 by uniform exact endpoint bounds (its exact value is NOT computed); the input-U-masked fresh family has certified membership in S_old at least 21708672114515, with exact size UNKNOWN; certified fresh DISJOINT lower is the SAME 21708672114515, and nothing else is subtracted. There is no basis to identify these as a complete survivor count. The intentionally already-consumed singleton Q6=433, when included as the sole proposed new gate under Q6-pruned ancestors, yields ZERO.

## Bounded independent hostile tests

The research reproducer independently constructs all 182 roots, 179 inverse templates, 144 eligible roots and common |U|394. It tests 28 length-nine true words, six duplicate residues, high-base signed thresholds, 729-phase occupancy, the forward/backward antichain and a separate actual T/numeric-predecessor oracle for 350000 literal starts [B,B+350000). Under the strengthened prior gate set including P2 and Q6, that bounded slice has **112** eligible actual starts and **zero** new nine-step hits. This zero is not evidence against the full-window theorem; early high-odd stopped cylinders are very sparse locally. The complete genuine 72-prefix independent large-number witness is

    n = 2392531586096650219611
    T^17(n) = 3233564703996759769087
    p = 2271035841490179700647
    T^9(p) = T^17(n), with word OOOEOOEOE, H=881,
    n mod4096=91, current y mod729=604, stop depth=53.

The code checks all j<=72 genuine T values stay >=n, all prior numeric inverse gates fail to produce a positive smaller predecessor, true inverse parity word and actual strict 0<p<n. This is a research-only *prefix* oracle, NOT a full Collatz-to-one run. No novel global sampling or verification is claimed.

## Independent alternatives tested / limits

1. **Literal coalescence families**: the 21-residue entire-word union is distinct from simply copying the earlier 31+72q P2 alias and from the old <=69 direct-descent run cones. An authenticated inverse *at a later true prefix*, with high-odd future protection, is what buys disjointness; a candidate word that hits at a phase already P2/h1/h2/P3/P4/Q6 is pruned. Full Bařina/Angeltveit source-control-flow equivalence remains NOT tested.
2. **Finite-state true-first-hit language**: exact (j,s,C mod729,hit) suffices for *the gate language and antichain multiplicities*, but does NOT suffice for exact actual endpoints. Phase-min CRT bounds retain B/E and permit a rigorous lower; full endpoint-exact mass of the antichain is UNRESOLVED.
3. **Restricted cyclic occupancy**: the 729-phase minimum is a genuine all-start lower. Using its expected/average occupancy or multiplying a second 394/729 would have fabricated a stronger saving; neither is permitted. The gross high-odd saturation ceiling 62289308018259707 from R3E21-19 remains an UPPER for its own architecture, not an additional exclusion; the new family is inside that high-odd universe.
4. **Universal reverse basin**: finite verified seeds and fixed reverse depth cannot cover all positive inputs; unbounded equality of the 1-basin with all integers is the Collatz conjecture, not solved by this finite antichain.

Standalone inherited R3E21-19/20/21/22 scripts were NOT individually executed in this session; the inherited R3E21-18 mask reconstruction is INCLUDED in the standalone new script and executed as part of its self-test. Research results here rely on the correctness of previous high-base sieve proofs and the self-contained exact script, not external formal proof checking or independent peer review.

Bařina pinned baseline: xbarin02/collatz-sieve/src/fsieve.c blob a0a2386584f7c3db4074044373c9bdea0056bdb1, four primitive recursion versus full CTZ v2/v3. Angeltveit pinned baseline: vigleik0/collatz/main.rs blob 4a33b870d27059feea28985e185b8c8c709eb313, search1/2/3. The full matched competitor executions, direct comparison of output sets, formalisation, priority and performance are NOT_RUN / UNPROVED. No new external source snapshots were verified during this session.

## Custody and next problem

Exactly these four paths changed: this report; research/r3e21_23_fresh_affine.py; additive PROGRAM_STATUS.md; NEXT_SESSION_PROMPT.md. No frozen science, worker/verifier/identity, owner Windows operator, website, feed, spending, correspondence or publication records modified. A(B) is still EXTERNAL ONLY. The valuable result is a small but rigorously claimed disjoint *new lower*; the gap to 10x remains monumental. The next mathematical target is a many-word/full-depth first-hit closure rather than polishing the sparse single-template antichain. R3E21-24 is FUTURE / UNEXECUTED; generating its handover does not authorise its execution.
