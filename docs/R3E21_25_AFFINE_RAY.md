# CEML-R3E21-25 — Affine-ray coalescence outside the high-odd stop

**15 October 2026. RESEARCH ONLY.** One bounded, precisely screened, new disjoint family of 1,849 starts; this is a conditional finite mathematical exclusion, not 1,849 convergences computed to one, nor a full-window density extrapolation.

## 1. Entry, provenance, immutable accounting

Fresh entry main commit: 7cee0bc389c822d085d27b38c5e58bcdda824755; tree: 6c471fcfb0bdf2259afe7bc1f5272eb169cc3f05 (R3E21-24 PR #52 merged). At entry open pull requests 0, main Actions workflow runs 0, check runs 0, actual status contexts 0 (aggregate GitHub status may say pending, but **ABSENT != PASS**); repository rulesets []; detailed branch-protection request returned 403 (**UNKNOWN**). Actual hosted execution of this session's reproducer NOT_RUN.

Literal interval [B,E): B=2392518188130438742016; E=3000000000000000000000 EXCLUSIVE; W=607481811869561257984. A(B) is author-reported EXTERNAL ONLY; CEML did not reproduce it. Actual S_old cardinality UNKNOWN. Historical independently proved S_old majorant 330156319374735841. Previously deducted **once and only once**: h1 3007471253458601, h2 220259463699144, P3/P4 52093319358849, Q6 10905604613006, R9 21708672114515, R24 325852123360426. R24 entry official conditional conservative upper 326518028938131300.

**Result (conditional on the inherited exact old-source/J12/U and consumed-rule model): 1,849 additional all-prior-disjoint *finite starts*, giving conservative upper 326518028938129451.** These points are *not* an estimator of the population outside the one-million-q tested subrange. Each is an authenticated *shorter positive path meeting*, to be discharged by strict ascending induction and the separate A(B) assumption. They were not run to 1. The subtraction is relative to the actual earlier consumption families' membership, not solely their conservative numerical lower bounds.

## 2. Route B — exact infinite affine-ray meeting theorem (positive)

Let T be the shortened map. Independently authenticate the genuine first 15 parity steps of

n0 = 2392518855426464419611

and the genuine first 10 steps of

p0 = 2018687784266079354047.

Both arrive at y0 = 4311396664247964401663; the first path has s=10 odd inputs, the second has a=7. Thus for every integer q>=0, genuine parity preservation under addition of a multiple of 2^j gives:

T^15(n0 + 2^15 q) = y0 + 3^10 q;
T^10(p0 + 2^10 * 3^(10-7) q) = y0 + 3^10 q.

Explicitly n(q)=n0+32768q and p(q)=p0+27648q, with n(q)-p(q)=(n0-p0)+5120q>0 and p(q)>0. No claim of full convergence is needed to prove meeting. The proof is a pair of exact affine parity-word identities and is valid for every q>=0. Source word and sign were authenticated with actual integer T independently at q=0,1,2,1000 and the last in-range q.

For [B,E), exactly 0<=q<=18538853288987291, so the ray has **18538853288987292** distinct target starts. This is a genuinely nonlocal coalescence description with fixed-size parameters, and needs neither s>=47 nor j<=67 at its meeting. It is NOT a novel claim about all Collatz integers. It reuses a ten-step word already present in R24, so its individual word is explicitly NOT claimed novel.

Every ray start has the same J12 dyadic root. Its n mod729 varies with q by step 32768, coprime to 729. The inherited common U has 394 allowed residues and the exact full-ray J12/U INPUT-gate count is

**10019627154816176**,

from exactly floor(18538853288987292/729)*394 plus the 87-element remainder. This is NOT a fresh number: direct descent, old inverses, old R9 and new R24 may still consume almost all those points, so subtracting this input-gate count would be a serious error.

## 3. Route C — priority/overlap audit and a genuinely fresh finite lower

The bounded certificate range is **q=0,...,999999**, corresponding to precisely one million starts n(q), not a statistically selected random set. All 1,000,000 are inside [B,E), and by the theorem above all have positive smaller meeting representatives p(q). For each n(q), check:

1. The original 12-bit genuine root belongs to the inherited 144 old-live roots, and n(q) mod729 belongs to reconstructed common U (size394), with all 179 source templates rebuilt from first principles.
2. Every true integer prefix j=1,...,72 of n(q) is non-descending relative to its start.
3. Every true prefix j>=13 avoids every previously consumed h1, h2, P3, P4, Q6 and 21 additional R9 authenticated smaller-inverse gate. P2 is the already-proved one-step h2 alias when the preceding step is included, so it is not separately counted.
4. The actual authenticated 10/11/12-step multiword R24 gates are tracked over every true j=13,...,72. Reject for freshness if a hit occurs by a first s>=47 stop with j<=67. This checks exclusion by the actual R24 stopping *set*, not by the smaller conservative R24 cardinality already subtracted.
5. For every passing n, independently re-authenticate its actual 15-step word, its explicit smaller p(q) 10-step word, equality of targets, integrality, positivity, and strict p<n.

Exact reproducible partition of that *bounded* one-million-q finite set:

| Full earlier-gate outcome | Count |
| --- | ---: |
| Fails inherited J12/U, descent or a consumed previous gate | 997772 |
| Still admissible but already in the R24 first-stop family | 379 |
| All inherited screens pass, NOT R24-stopped; new affine-ray exclusion | **1849** |
| Total | **1000000** |

New strict positive proof witness at q=426:

n=2392518855426478378779; p=2018687784266091132095.

The exact first ten fresh q are 426,552,828,1952,2492,2688,3738,6080,6272,6362. Last ten: 995226,995880,996540,996864,997568,997968,998304,999336,999698,999792. Those deterministic boundary checks help detect truncated scans. q=0, an original R24 witness, is deliberately rejected as already counted.

**Scope of the certified claim:** exact under the same inherited mathematical sieve/source boundary assumptions used by R3E21-23/24. Full third-party CTZ/v2/v3 or Angeltveit equivalence is NOT proved, external A(B) is NOT validated, and actual complete S_old is UNKNOWN. This is strictly a lower bound on further mathematical exclusions under the inherited sieve definition; it is NOT an exact count of candidates remaining.

Arithmetic of the update: 326518028938131300 - 1849 = **326518028938129451**. Do not subtract the 379 prior R24 members again, the full 18.5-quadrillion ray, or its 10.0196-quadrillion J12/U input-gate occupancy.

## 4. Route A — deterministic exact high-bit/carry transfer and obstruction

For a genuine dyadic parity cell n=r+2^j q, define y=T^j(r), s odd steps. Then

T^j(n)=y+3^s q

for the authenticated parity class. To append bit b, set k=(b-y) mod2, q=k+2u and r'=r+2^j k. Thus the new cell has y'=T(y+3^s k), s'=s+b and exact high-bit quotient u. The literal endpoints determine an exact q interval by ceiling divisions. Direct non-descent clips that interval by the signed linear condition:

(3^s'-2^(j+1))*u + (y'-r') >= 0.

This gives an exact integer interval union with neither independent parity assumptions nor a fictitious uniform mod729 phase; a mod729 input mask can be counted by 729-period floor sums in each surviving cell. It can be extended to fixed authenticated inverse gates by intersecting further affine inequalities. Its correctness is elementary by induction in j.

The standalone local reproducer checked exact no-descent counts on the literal 22-digit interval [B+124000,B+126048) to depths 72,160,256 against a separately coded direct finite-prefix oracle, finding respectively 4,0,0. Every assertion passed and the source-equivalent research-only local command had a clean process exit. These are tiny bounded *non-descent* controls, NOT the old full sieve or a full-window candidate count.

**Negative feasibility result:** after depth j, distinct dyadic residues require distinct high-bit interval locations to count exact occupancy; for j>=256 and W<2^256, every individual j-cylinder holds at most one target integer. Tracking only (j,s,C mod729/6561) cannot reconstruct the per-cylinder endpoint contribution. The exact interval transfer gives a correctness method but does not prove an affordable depth160/256 aggregation over all of [B,E). If one drops the exact quotient/high-bit information, a simple binomial tail or independent 729-phase multiplication is NOT an admissible replacement. This confirms the earlier R3E21-20/21 barrier rather than claiming to have defeated it.

The R19 at-most-62289308018259707 high-odd first-stop ceiling remains in force for THAT high-s architecture. The affine-ray meeting itself lies outside that stop discipline, but only 1849 explicitly fully screened finite starts have been additionally deducted. The prior ceiling is neither newly deducted nor contradicted.

## 5. Sources, competitor gate, and validation

Read the entire R3E21-14..24 sequence at the stage appropriate to these claims; retained R19 ceiling, R20 P2 alias, R21 affine quotient, R22 coalescence lift, R23 masks/gates, and R24 word tables. Standalone R23 and R24 original scripts were inspected but NOT_RUN as separately executed commands this session; their inherited J12 mask and R9/R24 tables were rebuilt and exercised by the new bounded script. Full GitHub-committed-blob hosted execution NOT_RUN; external formal Lean check NOT_RUN; full original S_old exact cardinality UNKNOWN.

Source-pinned Bařina restricted fsieve.c blob a0a2386584f7c3db4074044373c9bdea0056bdb1: smallest_predecessor primitive families are NOT the whole CTZ/v2/v3 executable, which includes forward/CTZ and double-even mechanisms. Pinned Angeltveit main.rs blob 4a33b870d27059feea28985e185b8c8c709eb313: search1 has an affine smaller-path/bit-prefix strategy, search2 modular lookahead and search3 block continuation. This is a critical PRIOR-ART caveat: the general affine lift and the ten-step word cannot be declared globally novel. Same-window full-source benchmark / full source equivalence NOT_RUN and priority UNPROVED.

Bařina 2025 peer-reviewed 2^71 publication: https://doi.org/10.1007/s11227-025-07337-0 (published 2 May 2025). On the live project homepage checked 15 October 2026, the work-unit listing still showed lowest incomplete work unit 2175982616*2^40; it is an author-operated live pointer, not independent CEML evidence of that whole external interval. https://pcbarina.fit.vutbr.cz/ . Angeltveit preprint posted 11 February 2026: https://arxiv.org/abs/2602.10466 . Tao's log-density almost-everywhere theorem: https://arxiv.org/abs/1909.03562 ; it does NOT certify uniform elimination in this fixed target interval.

Research-only reproducer: research/r3e21_25_longblock.py. Exact local mathematical assertions PASS with clean process exit in a source-equivalent bounded stand-alone local harness (11.24 seconds for a one-million-q test); identical pushed blob execution NOT_RUN. No native verifier, local scientific machine, hardware expense, batch certification, website/feed, frozen v1/v2 identities, contact, publication, or R3E21-2.

## 6. Decision

A mathematically authentic unbounded affine coalescence ray was established; the strong 15/10 meeting identity is automatically valid on its entire 18.5-quadrillion-member finite intersection. A bounded first-million-q strict all-prior screen *certified 1849 previously uncounted starts*, but even the full ray size is too small by itself to achieve a tenfold reduction of the official upper, and overlap of almost all ray members is unknown. The next session needs a genuine exact or provably bounded **full-q symbolic priority-counting operator across many affine rays**, with a hard independent novelty gate against Angeltveit search1; never multiply the observed 0.1849% local pass fraction by the full ray length. Keep mathematical research only.

This R25 execution authorises ONLY R25; R26 is queued FUTURE / UNEXECUTED.
