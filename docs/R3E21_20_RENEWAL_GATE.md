# CEML-R3E21-20 — Shift-collapse of P2, deterministic long-block necessity and an endpoint-counting barrier

**14 October 2026. RESEARCH ONLY. No new certified global marginal. No Collatz-to-one scientific execution.**

## Scope, inherited numbers, authority

Entry live main was 60a0c191826c08a2870edf4601c3bc6d395c5cac, the two-parent merge of R3E21-19 PR #47 (authored head ce88cf60a959dba72012fc1a158719dc35a05d43). Open PRs zero. GitHub Actions runs zero; individual check runs and commit statuses zero (the empty aggregate status may say pending: **ABSENT NOT PASS**). Rulesets []; public main indicated protected=false, detailed protection endpoint 403 **UNKNOWN**. The live repository was inspected and previous reports 17,18,19, AGENTS, status, charter, roadmap, claim policy and source-pinned Bařina/Angeltveit extracts considered.

Let T(n)=n/2 for even n and T(n)=(3n+1)/2 for odd n. The half-open interval has B=2392518188130438742016, E=3000000000000000000000 (EXCLUSIVE), width W=607481811869561257984. A(B), convergence below B, is **external-only and not reproduced here**. Actual S_old (the old J12/729/179 plus all 72-prefix conditions) is **UNKNOWN**. Its inherited independent cardinality majorant is 330156319374735841. Previously CONSUMED disjoint marginal lower bounds are h1=3007471253458601, h2=220259463699144, P3/P4=52093319358849, Q6=10905604613006. The current **conditional conservative upper 326865589733606241 is UNCHANGED**. Do not confuse it with an exact survivor set, verified frontier, compute throughput, or a proved worldwide improvement.

## Theorem A: Bařina P2 is an exact one-step shift of h2 along true forward paths

Bařina's four-primitive restricted inverse grammar contains P2(y)=(8y−5)/9 when y≡4 (mod9), and h2(z)=(4z−5)/9 when z≡8 (mod9), the latter being two chained P1 odd inverses. Take ANY positive n, ANY j>=1 and y=T^j(n)≡4 (mod9). Let z=T^(j−1)(n). An odd shortened-T step always produces an output congruent to 2 (mod3), whereas y≡1 (mod3). Therefore the last step is necessarily EVEN, z=2y, and z≡8 (mod9). Algebraically,

P2(y)=(8y−5)/9=(4(2y)−5)/9=h2(z).

Thus the predecessor is the **identical positive integer**, and the strict comparison P2(y)<n is equivalent to h2(z)<n, with exact genuine 3-step/2-step paths both sharing the same tail. Consequently an implementation checking h2 at every immediately preceding genuine time gains ZERO independent exclusion from a later P2. If a finite search begins after the preceding time or fails to evaluate h2 there, a boundary convention must be audited; the theorem alone does not say that an arbitrary executable omits P2 safely. This is a formal algebraic identity, not a new statement that Bařina was unaware of it or proof about his full CTZ v2/v3.

This is stronger than a slope-only no-go: it needs no j<=72, high-B bound, 729 phase approximation or independence assumption. Source comparison: Bařina restricted smallest_predecessor P2 gate (blob a0a2386584f7c3db4074044373c9bdea0056bdb1), distinct from his complete CTZ v2/v3 gate and extra double-even path. Angeltveit source main.rs blob 4a33b870d27059feea28985e185b8c8c709eb313 has search1 rational 306/485 and double-even, search2 mod9/24-lookahead and search3 16-step continuation. No full matched actual-input competitor execution was attempted; full-source coverage comparisons remain **INCOMPARABLE**, originality **UNPROVED**.

## Theorem B: long-block no-descent inequality, with a precise forbidden shortcut

For every n>=B, let x_i=T^i(n) and s_j be the number of odd inputs among the first j genuine steps. If x_i>=n for EVERY i=0,...,j, then every odd multiplier is (3+1/x_i)/2 <= (3+1/B)/2, and every even multiplier is 1/2. Hence

1 <= x_j/n <= (3+1/B)^(s_j)/2^j.

Therefore absence of strict descent by time j IMPLIES the **exact rational** necessity

(3B+1)^(s_j) >= 2^j B^(s_j).

Conversely, if this fails, SOME prefix i<=j has x_i<n, a valid strong-induction certificate. This is a genuine arbitrary-depth theorem, independent of the affine-carry Cmax bounds which deteriorate at long depths. Exact integer thresholds for no descent: j=72 demands s>=46; j=128 demands >=81; j=160 demands >=101; j=192 demands >=122; j=256 demands >=162. It DOES NOT assert that such high-odd paths actually exist for every n, or that any particular n converges.

Every length-j parity vector occurs once among a COMPLETE residue system modulo 2^j, but the target [B,E) is only ~2^69.04 wide. At j=256, the combinatorial tail fraction for >=162 odds over ALL 2^256 vectors is approximately **1.2733713e−5**. Multiplying W by this fraction would fabricate a roughly 7.7e15 remaining-count bound: UNJUSTIFIED. For j>69 each 2^j residue cylinder contains at most one target integer, and the very large parity-word language has no equidistribution theorem on this narrow interval. Sequential blocks also are not independent random trials merely because the full 2-adic parity-vector map is bijective. The missing ingredient is an exact, deterministic interval-conditioned *transfer/counting theorem* controlling high input bits and carries. Tao's almost-all/logarithmic-density work does not itself give this finite, contiguous, proof-safe count.

## Theorem C: quantitative fixed-depth, endpoint-blind upper envelope; a no-go for this particular accounting shortcut

Reconstruct the inherited 182 J12 roots from genuine 12-step slopes/duplicate signatures, all 179 inverse templates, the 144 surviving root cylinders and the single common old input mask U⊂Z/729, |U|=394. Every root has s>=8, so target residues after the J12 prefix are **frozen by the parity word**: T^j(n)≡C_j 2^(−j) (mod729).

From each eligible J12 state (j,s,C mod729), extend the genuine parity bit b. Reject any new state with 3^s<2^j and the four previous gates h1, h2, P3, P4 when their exact modular and negative-slope inequalities hold. In the stronger version also reject Q6 with y≡433 (mod729) and 512·3^s<729·2^j. Due to signed high-base threshold work inherited and adversarially spot-tested from R3E21-13–18, for n>=B these negatives are genuinely strictly smaller predecessor tests; do NOT promote a slope inequality without its residue and positivity prerequisites.

At any fixed depth j<=72, let N_j=floor(W/2^j), r_j=N_j mod729, d_j=2^j mod729. Each j-bit genuine parity cylinder with its unknown integer residue carries at MOST

H(j)=floor(N_j/729)·394 + max_{a mod729} sum_{i=0}^{r_j−1} 1_U(a+i d_j mod729) + 1

actual eligible members of [B,E). The +1 accounts for the nonaligned endpoint, and is conservative at all depths. If A_j is the number of dyadic cylinders surviving all tested earlier gates, then **A_j·H(j)** is a valid cardinality upper for the corresponding actual sets. It is an upper on a **relaxation** of S_old, not an exact number and not a fresh lower exclusion.

Forward integer-state DP at all 61 levels j=12..72 gives:

| Predicate version | Best depth | Surviving dyadic words | H(j) | BEST rigorous coarse upper |
|---|---:|---:|---:|---:|
| Forward slope + four consumed families | 63 | 9540579385237983 | 38 | 362542016639043354 |
| Same + Q6 | 63 | 9524984305884588 | 38 | 361949403623614344 |
| Same + Q6 + P2 | 63 | 9524984305884588 | 38 | 361949403623614344 |

P2 has **ZERO** new candidate words at every depth; this also follows independently from Theorem A, except that the root/depth boundary convention must be included in finite-state testing. At j=63, the best Q6-assisted upper is **35083813890008103 ABOVE** the existing 326865589733606241 upper. It is mathematically valid but weaker; therefore **it cannot replace or reduce the official bound**. Its substantial slack is the uniform maximum-over-all-729 endpoint phase applied separately to each cylinder, plus the omission of some inherited old exclusions. At depths 67 and 72 the coarse caps grow respectively to 485393116462130540 and 3067348902295269816; the per-class uncertainty overwhelms remaining interval mass. This is a decisive no-go for this single-level, phase-blind H(j) accounting shortcut, NOT a no-go for exact endpoint-aware multi-depth arithmetic automata.

## Independent arithmetic falsification and custody

Self-contained script: research/r3e21_20_renewal_gate.py. It includes a copy of the R3E21-19 finite-state baseline to avoid fragile import assumptions, reruns the inherited J12/179/U reconstruction and its 4608 genuine true-prefix fixtures, then separately counts the three R3E21-20 envelopes and tests their exact stated outputs. An independently authored standalone research-only Python calculation before committing separately reproduced the same two extrema and the P2 zero count; its actual n tests in [B,B+40000) found 760 eligible J12/mask points and executed 45600 signed prefix/gate oracle checks (72-step genuine shortened T, **NOT to one**), all passing. P2 source and full CTZ vs Angeltveit gates were inspected from pinned GitHub blobs, not executed as benchmark-equivalent competitor programs. Arithmetic uses arbitrary-precision integers and E EXCLUSIVE. No CI existed and no hosted check is claimed to PASS.

The long-block inequality and P2 redundancy are rigorous exact theorems; the numerical finite-state counts are computer-assisted research certificates requiring independent code audit/replication before external use. Nothing in these results proves a 10x or 100x reduction, a speed claim, actual S_old, global novelty, or a Collatz theorem. No operator, native scientific batch, frozen identity/snapshot, local Codex, production system, public site/feed, expenditure, correspondence or R3E21-2 touched.

## R3E21-21 handover motivation

A genuine next leap requires a deterministic transfer/count for [B,E) preserving actual endpoint/high-bit information as j crosses log2(W), rather than applying 256-step binomial frequencies. Investigate exact interval automata, carry-dependent dyadic partitioning, renewal kernels with proven input-block correlations, possible algorithmic barriers, and new certified universal cardinality estimates. Test every candidate against the actual nonaligned endpoints and previously consumed disjoint families. If no fresh rigorous improvement exists, retain the bound unchanged. R3E21-21 is SEPARATELY FUTURE / UNEXECUTED.
