# CEML-R3E21-19 — Nonlocal saturation: a rigorous high-odd stopping ceiling (14 October 2026)

**RESEARCH ONLY. NO NEW EXCLUSION / NO CHANGE TO THE OFFICIAL CONDITIONAL UPPER.** This session proves a decisive **architecture-specific** no-go theorem. It does **not** bound the true survivors, all inverse paths, all finite-budget grammars, or a strengthened whole-program Bařina/Angeltveit sieve.

## Authority, baseline and custody

LIVE entry main = `7eeb707704670fbaaa750f6cc8a5cf46bb1a2202`; R3E21-18 PR #46 merged into main (author head `11a574610f4a9b47c25aea8565918f8904af6e80`). No open PRs; Actions runs zero, individual commit statuses zero despite GitHub aggregate 'pending': **ABSENT NOT PASS**. Rulesets []; main publicly marked unprotected, branch-protection detail 403/**UNKNOWN**. Current actual old/post-rule survivor count **UNKNOWN**.

B = 2392518188130438742016, E = 3000000000000000000000 EXCLUSIVE, W = 607481811869561257984. The assumption A(B) is *external-only*, not independently rechecked. Inherited independent majorant 330156319374735841, disjoint consumed minima h1=3007471253458601; h2=220259463699144; P3/P4=52093319358849; nine-step inverse Q6=10905604613006. Their arithmetic produces the UNCHANGED conditional conservative upper **326865589733606241**. Do not confuse this with a measured work queue, remaining exact cardinality, speedup, global frontier or any proof of Collatz.

## Theorem 1: exhaustive ceiling for the currently used high-odd disjoint stop

Let V be the following set of genuine dyadic parity cylinders, rooted in one of the inherited 144 eligible 12-bit roots and whose input n mod729 lies in the common old allowed mask U (size 394):

1. At every authentic prefix from j=13 until stopping, enforce the inherited non-forward-descent slope 3^s >= 2^j and reject ALL previously consumed strict-lower-inverse gates h1, h2, P3, P4, using their true target residues and negative-slope conditions. For n >=B, the sharp signed high-base thresholds from R3E21-13/15/17 make these gates equivalent to the actual predecessor inequalities.
2. STOP at the **first** prefix with s>=47 and j<=67. DO NOT require a new inverse hit at all: allow an omniscient idealised mechanism to certify every such cylinder. If j=67 arrives without s>=47, the path contributes no stop.
3. At j>=47 odd inputs and j<=67, all downstream prefixes through 72 are safe from newly arising consumed h1/h2/P3/P4 *and* forward-slope failures. Indeed 3^47>2^72, and 2^t*3^47>3^a*2^72 for (t,a)=(1,1),(2,2),(6,4),(7,5). Thus V is a **prefix-free** disjoint language that includes every possible R3E21-17/18-style fresh hit subsequently stopped under the same s>=47, j<=67 condition.

**Proven ceiling (not achieved exclusions):** The union of all possible actual members of V in [B,E), including its old U input-mask condition, contains **at most 62,289,308,018,259,707** integers. This is a fully endpoint-safe UPPER on the total possible *high-s stop architecture's* contribution, not a certified LOWER on any new excluded family. Even ignoring the U mask entirely produces an independent looser **UPPER 89,547,365,280,396,712**. Both are far below the number **294,179,030,760,245,617** of additional exclusions needed to reduce the current inherited *majorant* by 10x, and far below **323,596,933,836,270,179** required for 100x.

In the deliberately impossible idealisation where every candidate in V has a qualifying certificate, the inherited upper could improve through this particular bookkeeping by at most 62,289,308,018,259,707. The arithmetically best upper one could derive **by subtracting only such candidates** would be no smaller than 264,576,281,715,346,534. This is **NOT a lower bound on true remaining integers** and does not exclude radically better independent cardinality bounds. Since Q6 was already consumed and is inside V, even this comparison generously overestimates *fresh* opportunity.

## Exact finite-state proof and all-endpoint occupancy

For a true word with j steps, s odds and affine carry C, 2^j T^j(n)=3^s n+C. Once s>=8 (true at each eligible J12 root), for **every subsequent j**, T^j(n) mod729 = C*2^(-j) mod729. This is independent of the separate input n mod729 allowed mask U. Therefore each genuine state can be compressed **without loss** to (j,s,C mod729) for the four consumed gates; phase independence cannot be multiplied across multiple times.

Advance b in {0,1} by j'=j+1, s'=s+b, c'=c (b=0) or (3c+2^j) mod729 (b=1). Drop forward-slope failures and the four prior gates exactly as in the proof. The first-s>=47 stopping antichain has **10,419,725,171,289,927** distinct dyadic cylinders; depth histogram:

`47:1 48:45 49:1025 50:15785 51:185098 52:1763990 53:14235784 54:100071478 55:625428763 56:3529402099 57:18200971694 58:86593465771 59:382986329187 60:1584390774299 61:6161456074871 62:22614289247623 63:78580837327321 64:259083180924310 65:811526764882527 66:2415589448043344 67:6824092752144912`.

For any depth-k class with r fixed modulo 2^k, its size in this **nonaligned half-open interval** is N_k or N_k+1 where N_k=floor(W/2^k). As consecutive class members move by 2^k, the input phase cycles through all 729 residues, since gcd(2^k,729)=1. Write N_k=729q+u and d_k=2^k mod729. Its count surviving U is bounded **above** uniformly over unknown starting phase by

`H(k)=394q + max_{a mod729} sum_{i=0}^{u-1} 1_U(a+i*d_k mod729) + 1`.

The +1 safely handles the possible N_k+1 endpoint member. Compute the maximum using exact 729-phase cyclic sliding windows, no averaging or independence. Summing H(k) times the exact prefix-free first-stop histogram gives **62,289,308,018,259,707**. Replacing H(k) by ceil(W/2^k) gives the independent **gross cap 89,547,365,280,396,712**. Either upper is mathematically valid without knowledge of the first actual residue in any cylinder.

## Theorem 2: simultaneous-block CRT cannot multiply the 729-mask discount

For ANY finite collection of authentic forward times j_1,...,j_r >=12 along the SAME genuine parity trajectory, at every time s_{j_i}>=8. Thus every target residue T^{j_i}(n) mod729 is fixed by the **single combined parity word through max(j_i)**. All multi-time residue restrictions are correlated Boolean predicates of that word. There are not r independent new mod729 phases: the input n mod729 still has just the ONE common old mask U and exact cyclic CRT occupancy. A proposed product factor (394/729)^{r+1}, or an independent extra 1/729 at each meeting, is mathematically **invalid**. New bit-word/renewal constraints might still help; this no-go kills only artificial modular tensor multiplication, not genuine new constraints.

This strengthens the former single-target phase-freezing observation into an exact multi-time obstruction. An arbitrary authenticated finite graph of strict tail coalescences also reduces to an actual pairwise strictly smaller representative as shown in R3E21-16; mere quotient multiplicity is not a second induction certificate.

## Independent falsification and reproducibility

`python research/r3e21_19_nonlocal_ceiling.py` (research-only exact Python; no native scientific job) reconstructs all inherited 179 old templates, 182 initial J12 roots, 144 live roots and common mask |U|=394 rather than trusting a list. Two different solution directions agree: a **forward multiplicity first-stop antichain** and a separately memoised **backward sum recurrence** (191775 memoised states). They agree on the exact cylinder tally and the universal U-sensitive ceiling. **4,608 distinct true signed high-base 17-step prefix fixtures**, each with an actual CRT-approved input phase, check the mod729 phase prediction and the consumed gates against direct positive integer T-prefixes. Neither test runs any orbit to one. Overflow: Python arbitrary precision. Equality: slopes use STRICT negativity; boundaries use E exclusive. Forward/cyclic phase vs backward/different reduction, positive strict predecessor vs nonpositive/slope traps, and direct genuine parity all confronted.

The old J12 mask reconstruction and prior signed-threshold theorems are inherited hypotheses with independent *spot* re-execution, not newly reproved source claims; R3E21-13–17 source math was spot-checked via the 179-template reconstruction, all four actual gates and 4,608 prefixes, not exhaustively replayed end-to-end in this invocation.

## Pinned source semantics, novelty, and boundaries

* Bařina source `xbarin02/collatz-sieve/src/fsieve.c` blob `a0a2386584f7c3db4074044373c9bdea0056bdb1`, `smallest_predecessor` lines 313–361: **four** recursive primitives, but executable v3 lines 364–401 additionally uses CTZ, forward gates and double-even handling. Our ceiling is NOT a theorem about that complete executable.
* Angeltveit source `vigleik0/collatz/main.rs` blob `4a33b870d27059feea28985e185b8c8c709eb313`: `search1` rational slope 306/485, true path-merge/double-even, `search2` mod9 plus precomputed 24-step lookahead, `search3` 16-step chunks continued until descent. A 72-prefix finite DP here is NOT a matched same-window implementation. His theorem/paper already studies extensive predecessor/path merging; novelty of these background mechanisms is NOT CLAIMED.
* R3E21-18's infinite four-primitive grammar gap y=433+729q vs p=303+512q remains true, but no new all-source completeness or full-competitor quantitative comparison is inferred. Angeltveit 2026 arXiv:2602.10466, Bařina J Supercomput (2025), and CEML reports R3E21-13–18 remain prior-art controls. World novelty of the counting-method no-go is **UNPROVED**, and matched enhanced Bařina / full Angeltveit outputs on [B,E) are **INCOMPARABLE**.

## Verdict and change of direction

**Meaningful negative mathematics:** the once-promising recipe "mine better inverse hits, then wait until odd-count s>=47 by j<=67 for safe disjoint subtraction" is provably too small to achieve even tenfold improvement, **even if the inverse detector were omniscient**. This is stronger than merely noting Q6's 0.00334% saving. All existing official upper-bound numbers remain UNCHANGED.

To escape, a future theorem must substantially revise at least ONE of: (i) stopping/first-hit architecture (including safely handling future overlaps without the s>=47 barrier), (ii) depth window and renewal across multiple genuine blocks with newly proved induction, (iii) independent old-mass cardinality bound, or (iv) a certified alternative global checking logic. Counting more P7/P8 words within the same stop gate is explicitly **not** a route to 10x.

No native Collatz-to-one check, local operator/Codex, R3E21-2, hardware expense, protocol/certificate, A(B), frontier tally, production code, feed/site, external correspondence or publication was touched. **R3E21-20 is separately FUTURE/UNEXECUTED.**
