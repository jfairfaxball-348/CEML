# CEML-P1 — Exact induction, elementary exclusions and certified minimal sieve

**Decision 2026-10-11 — P1 PASS for cloud mathematical specification ONLY.** This document supplies ordinary mathematical proofs, not Lean formalisation, new production code, independently reviewed mathematics, or a scientific verification batch. No local machine was accessed. Entry main: `7c94c18aab946f3c225dc5d904c7e2b22fc534c9` (P0 PR #2 squash merge). Sources revisited on 2026-10-11. Original R1–C1 source and evidence unchanged.

## 1. Domain, precise map, and induction theorem (PROVED, conditional on external base)

Positive integer domain, all endpoints mathematical arbitrary-precision integers:
`T(n) = n/2` for n even and `T(n)=(3n+1)/2` for n odd. The ordinary Collatz map C instead performs `3n+1` followed by a halving when n is odd; each T-step corresponds to exactly one or two ordinary steps. "Converges" means eventually reaches 1. At n=1, T(1)=2 and T(2)=1, so 1 is terminal for convergence certification, not a claim of a fixed point.

Let `A(B)` be the explicitly accepted **external** proposition `forall 1<=m<B: m reaches 1`, where B>=2 is an exact **exclusive** bound. P1 neither independently recomputes A(B) nor treats a reported server boundary as peer-reviewed fact.

**Ascending-prefix theorem:** Assume A(B). For each n>=B in increasing order, suppose `A(n)` is available from A(B), the finite chain of **committed, gap-free predecessor batches** and the provisional proofs for the lower integers of the *current, uninterrupted logical batch*. If one of the following is supplied by an exact finite certificate, convergence of n follows:
- (forward descent) an exact finite iterate `T^j(n)=m` for j>=1, with `1<=m<n`;
- (reverse predecessor) an integer `1<=p<n` with an exact finite path `T^j(p)=n` for j>=1;
- (external/committed basin) a forward iterate `T^j(n)=m<B` or `m<S`, respectively, if that external base or prior completed batch is actually accepted.

**Proof:** in the first case, n follows its exact path to m, whose convergence is already known; in the second, the already known convergence of p implies the suffix of its trajectory starting at n converges; in the third, the previously accepted basin supplies the same implication. Ordinary strong induction on n then establishes A(E) if and only if every n in [B,E) has such a certified argument (perhaps E is reached over several contiguous batches). An uncommitted lower batch cannot be used as a durable premise for a later batch. A single batch's provisional in-memory proof prefix is mathematically conditional and may justify following local steps, but **not** an advertised or restartable verified interval unless the entire batch is atomically certified. If any n is unresolved, mark the batch incomplete and do not promote its endpoint or downstream derived claims.

**Stopping caveat:** "Below initial n" is sufficient only when ascending certification really exists; "below committed S" is sufficient independently of provisional lower-in-batch certificates; "below external B" uses A(B); first hitting 1 is always sufficient. No one is licensed to substitute one test for the other under another execution order (e.g. parallel/random order).

## 2. Implementation-ready exclusion rules and elementary proofs

Each rule below has proof status **PROVED SUBJECT ONLY TO THE ASCENDING-PREFIX INVARIANT A(n)**. Check `n>=B>=2` before calling predicates; all arithmetic exact integers; no float modulo or unchecked overflow. First applicable rule owns the integer for accounting.

| ID / precedence | Exact applicability and integer predicate | Required witness; proof / exceptions |
|---|---|---|
| **E2**, first | `n>=2 and n%2==0` | `T(n)=n//2`, positive and less than n. n=1 not eligible. |
| **Q4**, second | `n>=5 and n%4==1` | Put `k=(n-1)//4>=1`. Then `n->6k+2->3k+1<n`. n=1 is explicitly excluded. |
| **P3**, third | `n>=2 and n%3==2` | `p=(2*n-1)//3`, a positive odd integer `p<n`, satisfies `T(p)=n`; for n=2, p=1 and T(1)=2, so the exceptional 1-cycle interpretation is sound. This is **reverse coalescence**, not forward descent. |
| **M9**, fourth | `n>=4 and n%9==4` | Put `h=(n-4)//9>=0`, `p=(8*n-5)//9=8h+3`. Then `0<p<n`, `p->12h+5->18h+8->9h+4=n` under T (odd, odd, even). A certified p entails certified n. At n=4, p=3. |
| **S2K4-03**, fifth | `n>=3 and (n%16)==3` | Put `q=(n-3)//16>=0`; the fixed T prefix is `16q+3 -> 24q+5 -> 36q+8 -> 18q+4 -> 9q+2`. Its end is positive and `9q+2 <16q+3` (difference `7q+1>0`), for **every q>=0**. This is a forward descent certificate. |
| **EXPLICIT** | no prior rule matches | Must compute exact trajectory until a justified stop; failure/resource bound means unresolved, not presumed convergence. |

The first four rules are elementary for all stated positive domains; **M9 is a transparent proof-backed portion of the published 3^2 sieve**, not blanket authority to import the rest of the external code. P3 eliminates n≡2,5,8(mod9), and M9 adds n≡4(mod9), giving exactly 4/9 residue classes modulo 9 in the *unfiltered all-integers* view, matching Bařina's published 44.44% modulo-9 figure. When applied **after even/Q4**, M9 adds only the previously uncovered n≡31(mod36), or four classes modulo 144. Percentages here are counts of algebraically removed *starts*, NOT hardware throughput.

Proof of P3's divisibility and strict inequality: n=3k+2, k>=0; p=2k+1 is odd, and `(3p+1)/2=3k+2`; `n-p=k+1>0`. Proof of M9 above includes its full three-step exact orbit; n-p=h+1>0.

## 3. Minimal nonredundant 2^k residue sieve (PROVED)

**Lift/parity lemma.** Fix k>=1, r in 0,...,2^k-1. Let the low-residue reference path use the parity word `e_0,...,e_(k-1)` (for r=0 the formula extends T(0)=0 *only for building a mathematical table*). For n=r+2^k q, q>=0 and n>0, at step j<=k:
`T^j(n)=T^j(r)+3^(a_j)*2^(k-j)*q`,
where `a_j` is the sum of the first j parity bits of the r-path. Induction: for j<k the displayed correction is even, so the parity bits agree, and the next T-step divides by 2, multiplying the correction by 3 in the odd case. Thus
`2^k T^k(n)=3^a n+b`,
where `a=sum e_j` and
`b=sum_(j=0)^(k-1) e_j 2^j 3^(sum_(i=j+1)^(k-1) e_i)`.
All numbers are exact nonnegative integers; check parity and exact divisibility when generating entries. Composition after blocks (k1,a1,b1), then (k2,a2,b2) is `(k1+k2,a1+a2,3^a2*b1+2^k1*b2)`, with ordered blocks, not reversed.

**Universal whole-class criterion:** From the lemma, `T^k(2^k q+r)=3^a q+T^k(r)`. Therefore an entry is safe for all q>=q_min exactly when
`(2^k-3^a)*q > T^k(r)-r`
for all q>=q_min. If `2^k-3^a>0`, checking q_min (and only q_min) proves the inequality universally. If zero, check the constant strict inequality. If negative, no eventual-all-q exclusion is possible without a separate proof. Bounds and q_min must be proven from the positive start domain, not inferred from samples.

**Minimality:** For odd n not already removed by Q4 we have n≡3(mod4). A single T-step grows n (n>1), and two T-steps satisfy `T²(4q+3)=9q+8>4q+3`. For k=3, n≡3(mod8) gives `T³(8q+3)=9q+4>8q+3`, while n≡7(mod8) gives `T³(8q+7)=27q+26>8q+7`, for every q>=0. Therefore no forward *whole residue-class descent* for these surviving starts appears at k<=3. At k=4 the class r=3 succeeds, so k=4 is the mathematically smallest useful NEW prefix sieve beyond E2/Q4.

**Complete odd-residue k=4 classification (all q>=0):**

| r (mod16) | parity bits e0e1e2e3 | a | b | T^4(16q+r) | decision |
|---:|---|---:|---:|---|---|
| 1 | 1010 | 2 | 7 | 9q+1 | Q4 pre-empts; r=1,q=0 excluded |
| 3 | 1100 | 2 | 5 | **9q+2** | **S2K4-03 safe all q>=0** |
| 5 | 1000 | 1 | 1 | 3q+1 | Q4 pre-empts |
| 7 | 1110 | 3 | 19 | 27q+13 | no T^4 descent |
| 9 | 1011 | 3 | 29 | 27q+17 | Q4 pre-empts; T^4 itself does not descend |
| 11 | 1101 | 3 | 23 | 27q+20 | no T^4 descent |
| 13 | 1001 | 2 | 11 | 9q+8 | Q4 pre-empts |
| 15 | 1111 | 4 | 65 | 81q+80 | no T^4 descent |

Even residues are already E2. For non-Q4 odd residues r=7,11,15 the k=4 T^4 multiplier is larger than 16 and the positive offset prevents a descent for any q>=0. Thus no hidden exclusions are silently inferred from this particular 16-class table. Higher k could remove more but is **DEFERRED** as an implementation choice, not a P1 proof prerequisite.

**Machine-readable minimal table specification for P2 (not yet a frozen schema):**
`table_id="S2K4-03-v1"; map="T"; modulus=16; residue=3; steps=4; parity_lsb_first="1100"; odd_count=2; affine_a=9; affine_b=5; q_min=0; T4_r=2; predicate="n>=3 and n%16==3"; witness="T^4(n)=(9*n+5)/16<n"`. Notice `(9n+5)/16` is an integer only on this residue class; the exact divisibility must be checked by the verifier. The table may be generated, rather than shipped as a large precomputed dependency. It neither uses random data nor assumes the old C1 table architecture.

## 4. Joint residue ledger and exact counts (PROVED)

Use priority **E2 > Q4 > P3 > M9 > S2K4-03 > EXPLICIT**, with a separate `BELOW_BASE` category if a requested interval includes n<B (normal frontier batches have S>=B). For every n>=2 the function is single-valued. After the first three rules, precisely r≡3 or 7(mod12) remain, **not** all odd starts. With M9 and S2K, the full predicates have period lcm(2,4,3,9,16)=144. Their disjoint assignment on every 144 consecutive integers n>=2 is:

| Category | Count per 144 | Residues for the two new categories |
|---|---:|---|
| E2 | 72 | even |
| Q4 | 36 | odd ≡1(mod4) |
| P3 | 12 | odd ≡3(mod4), ≡2(mod3) |
| M9 | 4 | **31,67,103,139 (mod144)** |
| S2K4-03 | 5 | **3,19,51,99,115 (mod144)** |
| EXPLICIT | **15** | 7,15,27,39,43,55,63,75,79,87,91,111,123,127,135 (mod144) |
| TOTAL | **144** | |

Thus the mathematically required explicit-candidate density for the stated exact precedence is **15/144 = 5/48 ≈ 10.4167%**, *before* any longer exact trajectory or additional sieve. This is not an empirical convergence rate or processing-speed forecast.

For arbitrary half-open [S,E), integer S>=2, E>=S, let
`R(M,r;S,E) = floor((E-1-r)/M)-floor((S-1-r)/M)`,
which counts `n in [S,E)` congruent to r(mod M), 0<=r<M (mathematical floor even for negative intermediate expressions). Sum R over the disjoint residue lists of the fixed 144-class truth table to obtain expected counts. For each prefix [S,c) during execution, checked category counts must equal the corresponding exact integer formula and sum exactly to c-S. Since the rule predicates depend **only on residue**, not input magnitude, this accounting identity is exact for n>=2, including edge/batch boundaries. Absent a runtime per-start audit, arithmetic counts and a purported cursor are not alone sufficient proof the worker actually evaluated every EXPLICIT candidate; a separate independent execution/commit-integrity check is still required at P2.

## 5. Independent reference specification and bounded P1 fixture observations

Reference test generator (pure mathematical scaffold; NOT production implementation):

```python
def T(n):
    assert n > 0
    return n // 2 if n % 2 == 0 else (3*n + 1) // 2

def assign(n):
    assert n >= 2
    if n % 2 == 0: return "E2"
    if n % 4 == 1: return "Q4"
    if n % 3 == 2: return "P3"
    if n % 9 == 4: return "M9"
    if n % 16 == 3: return "S2K4-03"
    return "EXPLICIT"

def require_witness(n):
    kind = assign(n)
    if kind == "E2": assert T(n) == n//2 < n
    if kind == "Q4": assert T(T(n)) == 3*((n-1)//4)+1 < n
    if kind == "P3":
        p = (2*n-1)//3
        assert (2*n-1)%3 == 0 and 1<=p<n and p%2==1 and T(p)==n
    if kind == "M9":
        p = (8*n-5)//9
        assert (8*n-5)%9 == 0 and 1<=p<n and T(T(T(p)))==n
    if kind == "S2K4-03":
        q = (n-3)//16
        assert T(T(T(T(n)))) == 9*q+2 < n
```

**Independent oracle/test requirements at P2/L1:** regenerate every declared parity word via simple T; independently reconstruct a,b from recurrence `a_0=1,b_0=0; (a,b)->(3a,3b+2^j)` on odd parity and unchanged on even parity, with the appropriate j; compare direct T^k(r+2^k q) at q=0,1 and several integers; assert 2^k divisibility; compare precomputed and independent bitwise predicates for every r modulo 144 and all n=2..10,000; verify boundary n=1 is excluded, n=2,3,4,5,7,31 and high-bit exact integers; demonstrate failures on flipped coefficients, wrong parity, reversed composition, truncating integer widths, a dropped/duplicated cursor and non-atomic completion. For k<=7 independently exhaust all r modulo 2^k and compare the affine identity using bounded **k-step identity checks only**, not full convergence. These finite tests supplement the algebraic proofs; they cannot establish universal convergence, validate the future native engine, or certify any scientific frontier batch.

**P1 bounded cloud mathematical fixtures actually checked:** for each n from 1 through 10,000, only the appropriate fixed-length E2/Q4/P3/M9/S2K witness identities were tested: **zero mismatches**. The k<=7 parity-affine recurrences for residues r<2^k had **zero mismatches**. A complete 144-residue precedence check yielded counts 72/36/12/4/5/15. These are tiny mathematical identity/unit fixtures, **not scientific Collatz verification runs**, production acceptance or V1.

## 6. Source-critical review: mod 3, frontier, Tao

**Bařina primary peer-reviewed 2025:** https://doi.org/10.1007/s11227-025-07337-0, published May 2 2025, reports all starts n<2^71 verified. Section 3.2 derives the 3^k sieve from the odd precursor 2n+1 -> 3n+2 and reports 4/9 removed mod9, versus 1/3 mod3. Our P3 and M9 supply an independent elementary proof of these two levels; larger mod27, mod81 and published speed optimisations are **DEFERRED** (not implied universally by unreviewed code). Section 3.3 uses low-bit lifted 2^k prefixes; section 4 distinguishes assigned vs completed 2^40 work units and server-side checksums. Sections 5–6 contain hardware- and distributed-system-specific performance, not local throughput evidence.

**Source-pinned implementation:** https://github.com/xbarin02/collatz/tree/141e13aae243d509a01a43bec597f53a5b97a09f, especially `doc/ALGORITHM.md` and `src/mod3-sieve/main.c`. The latter constructs affine `a*n+b` classes and uses an *eventually-large-n* comparison by leading coefficient (`a_l<a_r`). This is **not** an automatically globally valid all-n exclusion: finite thresholds/exceptional small integers are required. Accordingly P1's activated M9 and S2K rules are proved directly for all eligible positive integers, with no unproved adoption of compressed external large sieves or native 128-bit arithmetic.

**Live operational frontier:** https://pcbarina.fit.vut.cz/, retrieved 2026-10-11. Site generated at Sun, 11 Oct 2026 13:29:26 +0200; still displayed homepage n<2075*2^60 and lowest incomplete ID `2175982616` of size `2^40`, "all work units below verified". Exact numbers, recomputed:
- Published exclusive B = 2^71 = **2361183241434822606848**.
- Rounded headline exclusive B = 2075*2^60 = **2392312122059207475200**.
- Reported first incomplete unit starts at B = 2175982616*2^40 = **2392518188130438742016**; ends exclusively at 2175982617*2^40 = **2392518189229950369792**.
- The operational B is **author-reported, dynamic and NOT independently replicated by CEML**; first incomplete is not automatically unassigned forever, and other people may have examined starts there. No P1 batch is run or certified.

**P2 base acceptance policy decision:** *No silent accepted base.* The default trust tier/reference anchor is the **peer-reviewed published B=2^71**; the intended direct-above-live-frontier mode may be selected ONLY with a separate explicit `operational_reported_external_assumption` and a frozen dated source snapshot. This mode cannot claim an independently established whole basin below the live B, cannot call work globally novel without contemporary checks, and cannot promote a discontinuous local run as an extension from published B unless the entire intervening region is also evidenced. P2 must encode these separate choices in identifiers/claims, and require explicit, offline files rather than web lookups at runtime. Evidence gaps: complete live unit manifest, independent replication/verification, current assignments, external checker overlap.

**Terence Tao primary:** https://doi.org/10.1017/fmp.2022.8, *Forum of Mathematics, Pi* 10 (2022), e12, Theorem 1.3: for every f(N)->infinity, Col_min(N)<f(N) for logarithmic-density-one N; this is not a bound for each N, and f is not a fixed global basin B. **Tao-based skip eligibility: NONE (proved non-derivable from the cited universal quantifiers alone)**. No density or average-case heuristic may exclude a particular n. Source https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/almost-all-orbits-of-the-collatz-map-attain-almost-bounded-values/1008CC2DF91AF87F66D190C5E01C907F .

## 7. P1 gate resolution and what is still open

**PASS — mathematics gate:** precise external-base-dependent strong induction, E2/Q4/P3/M9 elementary proofs, smallest useful nonredundant k=4 residue prefix table, exact disjoint precedence and 144-class counting formula, independently specified mathematical fixtures, conservative Tao boundary, and published-vs-live source distinction. A formal proof assistant and external proof review have not been conducted. This is not new Collatz theorem novelty; it is a sound adaptation of well-known techniques.

**NOT P1 blockers / intentionally deferred:** larger mod 3^k and 2^k sieves, external compressed LUTs and performance, 128-bit overflow/native-GMP crossover, command-line format, signed/unsigned exact counting representation, fixed snapshot schema, atomic crash-proof ledger and replay checks, local file durability, working machine acceptance, and detailed one-time Codex handoff. All belong to future P2 or later L1. P2 must independently scrutinize the coverage protocol/recording audit to prevent a mathematically correct exclusion theory being undermined by an incomplete worker scan.

**ABSOLUTE STOP:** Do not commence P2 automatically; a new explicit owner invocation is required. No local Codex, production verifier, scientific trajectory or scientific interval has been executed by P1.
