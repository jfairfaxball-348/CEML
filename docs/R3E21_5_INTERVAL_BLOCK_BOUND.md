# CEML-R3E21-5 — Certified finite-interval block/cyclic sieve bound

Date: 2026-10-14. Entry live main \`d4295609ab4399f49716ec346bae7fe47eb61702\`, R3E21-4 PR #31 already merged. One separately owner-authorised mathematical research-only session. **No local production worker, scientific Collatz batches, accepted V2/I1/I2 identities, historical certificates, public feed, hardware, outside contact, Lean, or publication changed. R3E21-2 remains FUTURE/UNEXECUTED.**

## Decision and result

**PROVED conditional finite-interval upper bound (research proof and reproducible integer fixtures, not independent peer review):**

> Assuming A(B), where \`B=2175982616*2^40=2392518188130438742016\` and \`E=3000000000000000000000\` is exclusive, a composite depth-62 / Barina-simple-core-through-12 / reverse-\`3^6\` / lifted-path-merge-through-12 mathematical sieve leaves **at most 435,451,429,222,552,323 explicit starting integers in [B,E)**.

The R3E21-4 local certified upper bound was 568,717,180,731,540,942. **New saving: 133,265,751,508,988,619, or 23.4326931% of that previous upper bound.** New upper / interval width \`607481811869561257984\` is 0.0716813937001%. Neither percentage is an exact surviving density, measured implementation speedup, verification of any starting integer, a proof of Collatz convergence, or a world-record frontier claim. A(B) is an **external, author-reported operational assumption, not CEML's independent proof**.

The gain comes from a *finite-interval arithmetic-cylinder majorant*, not a new sieve class: using complete \`2^K\` numerical blocks and a rigorous cyclic maximum over mod729 shifts. The prior K58 full-period upper 3C was loose. **Depth K62 wins the tested interval-bound sweep K35..69**, whereas K beyond the interval's width degenerates under coarse edge blocks. K58 with the new method already improves to 549,553,337,494,584,790; K59 to 496,025,424,505,392,240; K61 to 473,889,220,463,941,276; K62 to 435,451,429,222,552,323; K63 becomes 453,802,099,255,503,390. This is not a global depth optimum outside the enumerated range or among other algorithms.

## Mathematical theorem — arithmetic cylinders, finite intervals, no uniformity assumption

Use shortened map \`T(n)=n/2\` (even) and \`(3n+1)/2\` (odd). Assume every positive \`m<B\` reaches 1 and use the global least-counterexample induction from P1/R3E21-4. A witnessed forward descent, smaller predecessor or smaller trajectory merge implies convergence of that start **only if the other smaller starts have also been justified**.

Fix \`J=12\`, \`M=729\`, and \`K>=J\`. From the source-reconstructed R3E21-4 predicates, retain just the 182 live low-\`J\` parity-prefix/Barina-core residue classes \`r\`. Let \`U_r subset {0,...,728}\` be **exactly** the mod729 residues for which the direct inverse-template sieve and the certified j<=12 forward-to-reverse merging sieve both fail to eliminate the start. This is an exact set intersection; no independence between forward and inverse conditions is asserted. For the parity-prefix word of \`r\`, let \`s_r\` be its terminal odd weight. Let \`F_K(r)\` count all extensions to length K preserving the non-descent prefix inequalities \`3^(s_j)>=2^j\` for every j<=K. The parity-vector/low-bit bijection proves that \`F_K(r)\` is given exactly by the suffix-weight recurrence in R3E21-4 and **does not depend on numerical high block q**.

Put \`L=2^K\`. For a *complete numerical block* \`[qL,(q+1)L)\` each low-K-bit residue occurs once. For every admissible low-K-bit \`v\` with \`v mod2^J=r\`, membership in the inverse/merge sieve depends only on \`(qL+v) mod M\`, and so as q advances by one the mod-M residue advances by \`d=L mod M\`. Because \`gcd(L,M)=1\`, a run of exactly M complete blocks visits every mod-M class exactly once for each v. Hence the exact count over M successive complete blocks is

\`C_K = sum_r F_K(r)*|U_r|\`.

For \`0<=b<M\`, define the **finite cyclic-window maximum**
\`H_b(U_r;d)=max_{z mod M} sum_{i=0}^{b-1} 1_{U_r}((z+i*d) mod M)\`.
For \`aM+b\` consecutive complete blocks, each admissible v contributes at most \`a|U_r|+H_b(U_r;d)\` retained starts. Summing by r yields the rigorously certified bound
\`a*C_K + sum_r F_K(r)*H_b(U_r;d)\`.
This argument holds even though the actual phase \`z=(qL+v) mod M\` is correlated with v; replacing each correlated phase by its **maximum**, never by an average, is the inequality that makes it safe.

At each of the at most two non-complete boundary blocks, the remaining starts are a subset of the \`2^K\` low-bit residues, hence at most \`D_K=sum_r F_K(r)\` retained starts **without even invoking reverse exclusions**. The final interval upper bound is

\`U_K([S,E)) = a*C_K + sum_r F_K(r)*H_b(U_r;2^K) + h*D_K\`,

where \`q_low=ceil(S/2^K)\`, \`q_high=floor(E/2^K)\`, \`q_high-q_low=aM+b>=0\` counts complete blocks, and h is their 0/1/2 boundary-block count. If there are no complete blocks, count at most the number of intersecting boundary blocks. The witness arithmetic and K-prefix test require all starts \`S>=B\`; an arbitrary interval below B is **not** licensed by this theorem. In particular this theorem never enumerates \`2^K\` residue classes or presumes uniformity in a partial mod-\`2^K M\` period.

**Uniform K-prefix proof obligation.** R3E21-4 established: for every n>=B, if at depth j the odd-step count s obeys \`(3B+1)^s < 2^j*B^s\`, then the orbit descends below n by depth j, provided no earlier descent has occurred (otherwise it was already eliminated). The new fixture independently evaluates this *exact integer inequality* for every j<=69 at the maximal s with \`3^s<2^j\`, which proves all weak-slope prefix eliminations through K62 (indeed K69) without a finite-n slope exception. For reverse/merged witnesses the earlier R3E21-4 script explicitly checks positivity, congruences, p<n and 200 constructed positive witness paths; R3E21-5 reuses those previously documented rules, does not enlarge their j/h or alpha range, and does not replace the smaller-witness requirement by density heuristics.

## Exact certificate arithmetic for [B,E) at K62

- \`L=4611686018427387904\`, period \`L*M=3361919107433565782016\` (**larger than the interval width**).
- Complete block q-index range is \`[ceil(B/L),floor(E/L))=[519,650)\`, **131 blocks**, with one partial block on either end. Thus \`a=0\`, \`b=131\`, \`h=2\`. No unjustified K62 whole-period multiplication appears.
- \`C_62=sum_r F_62(r)|U_r| = 2282468043343095762\` (a full-period residue count; **not** an interval count).
- Exact sum of the **individual cyclic maxima**, \`sum_r F_62(r) H_131(U_r;2^62) = 422893825289456829\`.
- Coarse boundary capacity \`D_62=sum_r F_62(r)=6278801966547747\`; two edges add at most \`12557603933095494\`.
- **Final certified interval upper = 422893825289456829 + 12557603933095494 = 435451429222552323.**

Cyclic-window maxima are computed by 729-entry Boolean arrays and a sliding sum, not approximate random sampling. Periodic overlaps and direct-reverse/merged exclusion overlaps are settled upstream by the exact \`(r,t)\` truth table. The count has deliberately *not* been upgraded to an exact [B,E) survivor count: the maximising mod729 phase differs among low-K-bit residues and the boundary capacity is an inequality. Achieving exactness requires controlling the correlation between low-K-bit parity survival and mod729 residues under high-bit range restrictions.

## Reproduction, adversarial checks and source challenge

Run **\`python research/r3e21_5_bound.py\`** at the CEML repository root (Python's script directory resolves the separately preserved \`research/r3e21_4_certificates.py\`). The session's mathematical fixture passed:
1. Reconstruction of 179 reverse templates / 335 covered residues via the R3E21-4 dependency, Barina simple-core \`1720/65536\`, 182 eligible J12 low-bit classes, and exact prior K58 full-period survivor count \`189572393577180314\`.
2. Exact high-base integer inequalities for every j=1..69; exhaustive **K35..K69** upper-bound sweep finds unique minimum K62 and asserts its full six-tuple decomposition, saving and total.
3. Direct five-window bounded K16 prefix-membership enumeration at non-aligned portions near B and E (widths 13, 500, 131089, 196738, 196672). Exact counts \`0,5,1648,2436,2459\` are no greater than their independent block upper bounds \`1735,1735,4983,6496,6496\`. No full orbits to 1 and no production scientific batches were executed.
4. Edge-case cyclic-window length zero/full, all-live and all-dead sets; the count uses ordinary unbounded Python integers, exact division and modular arithmetic.

**External algorithms investigated, not silently outranked.** Bařina's source-pinned \`collatz-sieve/src/fsieve.c\` (R3E21-4 source blob a0a2386584f7c3db4074044373c9bdea0056bdb1) has *more* than the simple k16 mask: \`is_live_in_sieve_2_34v2\` handles CTZ-compressed paths and a two-even-step preimage test; \`smallest_predecessor\` in \`v3\` recursively examines the restricted congruence transports \`2 mod3\`, \`4 mod9\`, \`10 mod81\`, \`182 mod243\`, and also a double-even comparison. It is a restricted recursive predecessor search, not the globally smallest preimage. The same generator combines affine descent and equal-terminal/odd-count trajectory groups. R3E21-4 independently matched **1720/65536** simple-k16 survivors but **did not** verify distributed binary map bytes. Here the code branches and mathematical dependencies were revisited; the full k34 *enhanced* mask and its [B,E) survivor count are **not independently reproduced**, so a bit-for-bit/full-strength victory would be false.

Angeltveit, *An improved algorithm for checking the Collatz Conjecture for all n<2^N*, arXiv:2602.10466v1, Sections 2–5, and source \`vigleik0/collatz/main.rs\` (R3E21-4 pinned blob 4a33b870d27059feea28985e185b8c8c709eb313): \`search1\` branches over low-bit parity cylinders, cuts on descent and two merge mechanisms; \`precompute\` and \`search2\` add mod9, odd-even-even and multi-bit lookahead before \`search3\` performs remaining trajectories. Its published \`<0.02%\` at \`N=72\` is a projected fraction over **[1,2^72)**, not an executed or proved [B,E) bound; its fully adapted matched [B,E) count is **not available from our tests**. Path-merging, reverse coalescence, adaptive parity-prefix exploration and the multiplicative stopping principle are established prior art. Rewriting these for a non-aligned interval and proving an upper bound is not yet demonstrated to be publishably novel.

**Matched-domain limitations:** our K35..69 rows are genuinely on *identical [B,E)* under the same composite mathematics. The 1720/65536 Barina k16 simple-core reference is honestly labelled a different, *weaker* rule/depth, and neither the enhanced full k34 Barina algorithm nor Angeltveit's complete depth-N adaptive lookahead has a verified same-window count here. Both external contenders are **INCOMPARABLE / LEADERSHIP UNDETERMINED** rather than beaten. Likewise no source-matched full binary mask, interval-wide exact count, runtime acceleration, or global novelty review was achieved. This is the explicit remaining source/algorithm audit shortfall, not permission to fill it with projected densities. No theorem of Terence Tao is invoked for a pointwise skip.

## Governance and future handoff

The new interval theorem is **agent-assessed proved conditional arithmetic with executable bounded fixtures**. It is a valid numerical refinement of the local R3E21-4 baseline, not yet a deployable proof-carrying per-start certificate format or independently machine-checked theorem. Per rejected parity cylinder the uniform K-prefix lemma supplies a strict smaller *forward* witness; per Barina equal-terminal class and direct/lifted reverse rule the R3E21-4 source supplies the smaller positive witness. The interval count itself is an upper bound on the set *not ruled out by those sufficient predicates*, rather than proof that every omitted start has been processed in an actual frontier ledger.

**Champion:** CEML's local *proved [B,E) upper bound* is now the K62 cyclic-block bound 435,451,429,222,552,323. Global strongest mathematical sieve: **external Angeltveit/Bařina remain potentially superior; no matched-domain numerical ranking justified**. Next R3E21-6 should attack the missing parity-prefix-versus-mod729 phase correlation to calculate an exact or meaningfully sharper [B,E) count, with source-matched competitor tests. R3E21-2 engineering remains FUTURE/UNEXECUTED. No production changes are authorised by this mathematical record.

**Entry provenance:** R3E21-4 one-commit head e0c5dbcfa83654e6c3d5d67791603fa7c69b9a81 was merged as two-parent main d4295609ab4399f49716ec346bae7fe47eb61702 (#31). On this R3E21-5 entry, open PR list empty, hosted Actions runs/check runs/statuses ABSENT (not PASS); main reports unprotected, rulesets returned empty; detailed protection endpoint returned 403, therefore inaccessible/UNKNOWN. These are GitHub evidence labels, not local testing substitutes.
