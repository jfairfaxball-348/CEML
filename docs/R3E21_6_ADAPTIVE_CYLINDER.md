# CEML-R3E21-6 — Adaptive finite-interval 2-adic cylinder bound

**14 October 2026. Research-only; independently owner-invoked R3E21-6.** Entry main \`542d7a407647d95bcaed27bf715aa8b9262e8a19\`: R3E21-5 was authored in sole-parent commit \`5de72683677a2089b858bc7d42ac8eafc10cc0f7\`, merged normally as two-parent main via PR #32. Entry open PRs none, hosted Actions total 0, check runs 0, commit statuses 0 (pending summary means ABSENT, not PASS), public main marked unprotected, rulesets empty; detailed protection returns 403/UNKNOWN. This report is not an actual scientific verification.

## Headline: a smaller proved *upper bound*, still not the exact count

Fix **B = 2175982616 × 2^40 = 2392518188130438742016** and **E = 3000000000000000000000** exclusive; interval width **607481811869561257984**. Assume explicitly **A(B)**: every positive integer below B eventually reaches 1. This assumption is from an external author-reported operational frontier, not independently reproduced or promoted by CEML.

Our fixed, existing **depth-12 Bařina simple generator / 179 reverse templates / mod 729 / j≤12 lifted path-merge** predicate, combined with exact high-base forward-descent pruning, has **at most 342723929836590155** explicit survivors in **[B,E)**. Previous certified R3E21-5 bound: 435451429222552323. **Saving in absolute upper bound: 92727499385962168 (21.2945676976% of previous upper bound).** The new upper bound is **0.0564171507920%** of the interval width; this is **not** an exact survivor count, a time/throughput forecast, a proof of Collatz convergence, or an improved world frontier.

The improvement corrects a genuine source of avoidable pessimism: R3E21-5 maximised modulo-729 phases separately for each length-62 numerical word and paid two whole-boundary-block capacities. R3E21-6 bounds *entire variable-length numerical low-bit cylinders* directly within [B,E), avoids a separate boundary-block charge, and chooses an adaptive depth with a provably safe binary tree DP. Source-critical priority remains Angeltveit/Bařina, not an ownership/novelty claim.

## Precise mathematical statement and proof

Let T be the shortened positive Collatz map, \`T(n)=n/2\` for even n, \`T(n)=(3n+1)/2\` for odd n. For the first j steps of the actual orbit, let s_j be the odd-step count. The standard parity/low-bit bijection says the first j parities depend only on n mod 2^j; extending a low-bit cylinder by one binary digit produces one child with next parity even and one with next parity odd, bijectively. For every n≥B and every **1≤j≤79**, the exact checked inequality

\`(3B+1)^s < 2^j B^s\`, for \`s=max{a: 3^a<2^j}\`,

certifies that an orbit with \`3^{s_j}<2^j\` descends strictly below its own start by or before depth j. Proof: if a previous descent happened we are done; otherwise all intermediate iterates are ≥n≥B, so each odd multiplier is at most \`3+1/B\`. The product bound gives T^j(n)<n. Every less-than-start witness is used under global strong induction plus A(B); it does not individually settle the entire interval.

Let \`J=12\`, \`M=729\`, and retain the 182 source-reconstructed low-J admissible residue classes r. For each let \`s_r\` be its odd count, and \`U_r⊆{0,...,728}\` the already-proved exact truth-table set **not** removed by direct reverse templates and j≤12 lifted reverse path merging. All allowed starts in the r-cylinder must have \`n mod M∈U_r\`. Overlap of those two reverse exclusion types is resolved by the existing exact set membership, not by probabilistic independence.

For any subinterval \`[S,H)⊆[B,E)\` of width \`W=H-S\`, put

\`N_j=ceil(W/2^j)\`, \`q_j=floor(N_j/729)\`, \`t_j=N_j mod729\`;

\`H_j(U,t)=max_{z∈{0,...,728}} Σ_{i=0}^{t-1}1_U((z+i 2^j) mod729)\`;

\`G_j(U,W)=q_j |U|+H_j(U,t_j)\`.

**Cylinder-cap lemma.** For every fixed *actual but unknown* numerical low-j-bit residue \`v\`, the list of starts n∈[S,H) satisfying n≡v(mod 2^j) is a contiguous arithmetic progression of length at most N_j and step 2^j. Its mod729 phase is unknown, but gcd(2^j,729)=1; each 729 consecutive positions contains precisely |U| hits, and the remaining tail has at most H_j hits. Thus the number of such starts with n mod729∈U is at most \`G_j(U,W)\`. This statement includes signed bounds, n with large high bits, nonaligned endpoints, short and zero-length windows, and j larger than interval width; **it does not assume independent CRT phases**. All counts are mathematical unbounded integers.

**Adaptive-parity theorem.** For fixed r and U_r, let \`F_r(j,s)\` be a safe upper on survivors in an *arbitrary actual* low-j-bit cylinder extending r whose first j parities have s odds. At the chosen maximum depth D≤79, set \`F_r(D,s)=G_D(U_r,W)\`. For J≤j<D set

\`F_r(j,s)=min{ G_j(U_r,W), Σ_{e∈{0,1}:3^(s+e)≥2^(j+1)} F_r(j+1,s+e) }\`.

The first term is safe by the cylinder-cap lemma. For the second, the two binary children are **disjoint** and exhaustive. A child with insufficient odd count descends below its starting n by the uniform high-base lemma, so under A(B) and induction it need not be explicitly checked; each remaining child is bounded recursively. Both alternatives are valid, so their minimum is valid. Critically the function of \`j,s,U_r,W\` is a *universal majorant over every actual cylinder having those states*; we have not incorrectly claimed that its numeric phase is determined by those states. Since the 182 low-12 residue cylinders are disjoint, their upper bounds add without overlap:

\`Survivors([S,H)) ≤ Σ_{r live} F_r(J,s_r)\`.

This is a finite-state dynamic programme over j and s, with each cyclic maximum determined by an exact sliding window of length 729. Per mask computation is O(729D+D²) operations and polynomial space (plus memoisation), not O(2^D). For full [B,E), the **computed** result at D=79 is 342723929836590155. No exhaustive enumeration of 2^62, 2^72 or 2^79 numeric low-bit words takes place. The bound can remain loose because each stopped cylinder maximises its phase and count separately. It is not the exact correlation-resolving automaton demanded in the original ambitious prompt.

Depth cross-checks (same [B,E), same underlying masks):

| Maximum parity depth | Certified adaptive upper |
| --- | ---: |
| 62 | 415260975758799476 |
| 65 | 355387192082135541 |
| 67 | 350643238506944522 |
| 72 | **342723929836590155** |
| 79 | **342723929836590155** |

The DP's non-increasing behaviour with extra permitted depth follows from having the option to stop at the same node; the invariance at 72–79 is observed for these masks and width, not a general optimal-depth theorem.

## Validation and adversarial witnesses (nonproduction only)

Reproduction: \`python research/r3e21_6_adaptive.py\` from repo root. Uses \`research/r3e21_4_certificates.py\` as the **frozen research dependency**, not the offline production verifier. Independently reconstructs 179 reverse templates, 182 retained low-12 classes, checks the exact integer high-base inequalities j=1..79, asserts D62/D65/D67/D72/D79 results, and compares five **direct per-n shortened-parity-prefix** oracles against the adaptive D16 bound. Source-subset comparisons are at the same exact [S,H), not an unmatched projection. No orbit to 1 was computed for frontier certification.

| Synthetic [S,H) width | Direct CEML composite D16 survivors | Adaptive D16 upper | Bařina simple 2^16 core survivors | Angeltveit mod9-only subset survivors | Intersection of latter two |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 0 | 144 | 0 | 8 | 0 |
| 500 | 5 | 144 | 13 | 277 | 5 |
| 131089 | 1648 | 2160 | 3441 | 72827 | 1908 |
| 196738 | 2436 | 3266 | 5169 | 109299 | 2848 |
| 196672 | 2459 | 3266 | 5162 | 109262 | 2862 |

Windows sit near B or E with nonaligned endpoints; the direct oracle uses the actual n, not hypothetical high-base low-bit equality for mod729. These checks demonstrate positive smaller-witness algebra for the inherited sieve on previous R3E21-4's 200 exact CRT witness fixtures, strict high-base inequalities here, and disjoint-child accounting; they do **not** formally certify every arithmetic step in Lean. A dedicated counterexample search tested zero/full cyclic windows and independent prefix membership in earlier R3E21-5; no new unsafe branch was accepted.

## Source-critical rival stress test: no full matched-domain champion established

Primary pinned Bařina source: [xbarin02/collatz-sieve, fsieve.c blob a0a23865](https://github.com/xbarin02/collatz-sieve/blob/a0a2386584f7c3db4074044373c9bdea0056bdb1/src/fsieve.c). In \`is_live_in_sieve_2_34v2\` the CTZ-compressed odd/even runs include the \`beta≥2\` two-even precursor; \`v3\` invokes \`smallest_predecessor\` recursively with restricted residue/predecessor transports \`2 mod3\`, \`4 mod9\`, \`10 mod81\`, \`182 mod243\`, plus the even-even predecessor. The generator combines v2 and v3; the simple \`2^16\` core in our table **does not** implement those enhancements or compare binary map bytes. The exact full enhanced 2^34 map cannot be reconstructed here without its massive state/mask artifact and a high-base validity audit; its **[B,E)** count is not asserted.

Primary pinned Angeltveit source: [vigleik0/collatz main.rs blob 4a33b870](https://github.com/vigleik0/collatz/blob/4a33b870d27059feea28985e185b8c8c709eb313/main.rs), [2026 preprint arXiv:2602.10466v1](https://arxiv.org/html/2602.10466v1). \`search1\` recursively branches low numerical bits with a descent test, parity-weight rational threshold, an odd-even-even state, and backward path-merging by parity/even-run pattern; \`precompute\` and \`search2\` use mod9 bitvectors, B=24 lookahead and \`search3\` tests remaining trajectories. Our same-domain \`n mod9∉{2,4,5,8}\` test is **only one rigorously identified source-subset**, NOT all \`search1/search2/search3\`. Full fixed-interval lookahead counts, source runtime/bitvector equality and signed-offset/high-base translation are not independently established. The paper's **<0.02% at [1,2^72)** is a projection on another domain; it is not a matched-[B,E) proof or a measurement here. The paper itself warns that low-bit traversal is inconvenient for arbitrary numerical intervals.

**Decision:** CEML has a stronger *locally calculated proved conditional upper bound* than its previous R3E21-5 bound. **Best external competitor is INCOMPARABLE on matched [B,E) evidence.** Finite parity recursions, adaptive low-bit pruning, inverse sieves, path-merging and the idea of minimising branch costs are close to established literature; **originality/publishability is UNDETERMINED**, not certified. No credit is claimed for Angeltveit's path merging or the Bařina sieve rules. Tao's logarithmic-density theorem supplies no pointwise skip.

## Next obligation

R3E21-7 should investigate an **exact numeric correlation count** by incorporating actual low-bit residue mod729 (or a proved discrepancy/carry state) into the adaptive trie, not another independent worst-phase maximum. A reasonable sharp target is a *safe stronger [B,E) upper bound* with exact phase information on a selectively expanded subset of high-contribution nodes, and a tested **actual enhanced Bařina / full Angeltveit** matched-domain comparison, otherwise a documented negative complexity result. Retain high-base integer conditions, signed endpoints and external source pins. R3E21-2 remains separately FUTURE/UNEXECUTED. No local scientific, production, site/publication, hardware, Lean or external-contact action was taken.
