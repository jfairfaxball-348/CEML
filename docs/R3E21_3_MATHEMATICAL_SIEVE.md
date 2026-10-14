# CEML-R3E21-3 — Exact symbolic descent and reverse-coalescence research

**14 October 2026; research only; entry main** 74c3f816595ecb46fb97ef94842963eb67591749. **Status: mathematics proved as stated, finite enumerations independently checked, performance unmeasured, no novelty claim.** This owner-authorised standalone R3E21-3 research session did **not** execute or close the still-future R3E21-2. No scientific Collatz interval, site publication, local RUN1 action or accepted verifier identity was changed.

## 1. Actual baseline and evidence

CEML's P1 frozen mathematical precedence E2/Q4/P3/M9/S2K4-03 leaves 15/144 = 10.41667% as EXPLICIT. R3E21-1 separately proved forward 2^5 residue families 32q+11 and 32q+23, reducing that to 20/288 = 6.94444%, and exhibited a reverse 3^6 coalescence subfamily; none was activated in production. The accepted 7,936-batch conditional RUN1 aggregate is [2,392,518,188,130,438,742,016, 2,392,518,188,130,518,594,186), 79,852,170 starts, contingent on an *author-reported* externally completed operational basin. It is not an independently established new global frontier.

Published Barina (2025), DOI 10.1007/s11227-025-07337-0, verifies below 2^71 (peer-reviewed computational report). His distinct live page reports below 2075*2^60, and a dated lowest-incomplete unit at 2175982616*2^40, but these are different trust tiers and subject to change. This research uses the 2026-10-14 repository-pinned operational B=2175982616*2^40 only as a *conditional baseline*, with target E=3*10^21 exclusive; the mathematical lemmas themselves do not rely on that author's assertion. Barina already uses 2^k and 3^k sieves and reports effective GPU 2^24 and CPU 2^34 tables, so none of the classical sieve ideas below is claimed novel or superior to his best implementation.

## 2. Mathematical red-team of the attached cycle-focused report

**All-rotations integrality is redundant.** For a binary parity word w of length k and weight a, define A(w) by 2^k T^k(n)=3^a n+A(w) for that prescribed word and D=2^k-3^a (odd). If D divides A(w) and n=A(w)/D is integral, then the congruence 3^a n+A(w)=0 mod 2^k forces exactly the prescribed parity at *every* step: reduction modulo 2 gives the first parity; divide by 2 and induct on the suffix. Thus T^k(n)=n with the valid parity word, and the states of every cyclic rotation are automatically integers; the rotated D-divisibilities bring no independent obstruction. Positivity additionally requires D>0 for nonzero positive words. The suggested balance-from-independent-rotation-divisibility strategy consequently loses its proposed extra equations, although genuinely new global orbit-size/word-order restrictions remain possible.

At length 40 there are exactly (2^40-2^20-2^8+2^4)/40 = **27,487,764,474 primitive binary necklaces**, even before per-rotation work: a proposed exhaustive k<=40 experiment is not a small bounded run. The 2-adic conjugacy/parity-cycle equations describe cycles, not arbitrary-start convergence; companion-repository orientation/carry lemmas do not currently provide forward-descent certificates for complete classes. Tao's logarithmic-density-one theorem and inverse-tree lower bounds likewise cannot be promoted to universal finite exclusions. Modular necessary conditions, speculative automata potentials and probabilistic drift do not authorise skips. Relevant positive tools are exact affine parity lifting and the pre-existing 2^k/3^k descent/coalescence sieves.

## 3. PROVED — uniform high-n prefix descent theorem

For T(n)=n/2 when n even, T(n)=(3n+1)/2 when n odd, let e_0,...,e_{j-1} be the actual parity bits of the first j steps and s_j=sum e_i. Direct induction gives

2^j T^j(n) = 3^{s_j} n + A_j,    A_j = sum_{i=0}^{j-1} e_i 2^i 3^{s_j - s_{i+1}}.

Every summand is nonnegative; A_j <= 3^{s_j}(2^j-1) < 2^{2j} whenever 3^{s_j}<2^j. For any fixed K>=1 and **every n>=2^{2K}**, if **any j<=K** satisfies 3^{s_j}<2^j, then

(2^j-3^{s_j})n >= n >= 2^{2K} > A_j,

so T^j(n)<n. This certifies all such n by strong induction over previously proved lower starts. No probabilistic or sample assumption occurs. Prefix parities depend only on n modulo 2^K: two starts congruent modulo 2^K have identical first K parity bits, by the affine identity and stepwise 2-adic lifting.

A sharper per-word exact condition also holds without the uniform floor: for any word with 2^j>3^{s_j}, descend precisely when n>A_j/(2^j-3^{s_j}); smaller exceptions must be proved individually. The high-floor bound 2^{2K} is sufficient, not optimal.

For K=35 this floor is 2^70=1,180,591,620,717,411,303,424, below the fixed research B=2,392,518,188,130,438,742,016. The theorem is therefore safe for every n in [B,E), conditional on the external basin for use as a convergence proof.

## 4. PROVED recurrence; exact finite residue arithmetic

Let c[j,s] count parity words length j, weight s, whose *every* nonempty prefix satisfies 3^(prefix odd-count)>=2^(prefix length). Set c[0,0]=1 and

c[j,s] = 1_{3^s >= 2^j} (c[j-1,s] + c[j-1,s-1]).

Every parity word length K corresponds bijectively to a low-bit residue modulo 2^K, so S_K=sum_s c[K,s] is the **exact** number of large-n classes not eliminated by the above prefix theorem. The count is not a computational sample. Small independent exhaustive low-residue recursion (K<=12) and direct T prefix checks confirm the recurrence. Representative counts: S_5=4, S_16=2114, S_24=286581, S_27=1762293, S_30=12771274, S_32=41347483, S_34=151917636, S_35=263841377.

The parity-prefix theorem is a **sufficient** elimination rule only; the surviving class set is not a set of known divergent orbits.

## 5. PROVED reverse-coalescence family generator; exact 3^6 coverage

For any prescribed binary word w of length j and weight a>=1, let A(w) be its affine numerator above. If 2^j<3^a, put m=3^a and

r(w) = 2^{-j} A(w) (mod m).

For every n>=3^a with n congruent to r(w) mod m, set

p=(2^j n - A(w))/3^a.

The congruence makes p integral, A(w)<2^j 3^a ensures p>0, and 2^j<3^a gives p<n. The equality 3^a p+A(w)=2^j n forces the prescribed parity bits by the same mod-2 induction, so the actual shortened trajectory of p reaches n in exactly j steps. Under a certified ascending induction, convergence of p implies convergence of n. This is reverse **coalescence**, not forward descent.

Enumerating all words with 1<=a<=6, 1<=j<=9 and 2^j<3^a yields 179 certificates, covering a union of **335 of 729** n-residues modulo 3^6. All 335 have directly replayed exact p->n test witnesses for n=729+r. This reproduces Barina's reported 45.95% mod-3^6 elimination (335/729), including mod-9 P3/M9 (324 classes); the additional 11 are genuinely additional to mod 9, **not** a novelty assertion. The reverse membership may be represented by 729 truth bits plus template witness metadata; lifting to every n>=729 follows from the preceding algebraic proof, not tests.

## 6. Exact combination, overlap and finite-range bounds

The forward survivor predicate is modulo 2^K, and reverse survivors are the other **394 of 729** classes modulo 729. By the Chinese remainder theorem, intersection has exactly

C_K = S_K * 394 classes modulo P_K = 2^K * 729,

with no overlap double count. Exact large-n candidate density is C_K/P_K. These densities are periodic algebraic coverage, *not* measured runtimes and not a proof every residual trajectory converges.

| Prefix K | S_K | residual after 3^6 reverse | naive flat 2^K-bit mask |
|---|---:|---:|---:|
| 5 | 4 | 6.755830% | 4 bytes minimum |
| 16 | 2,114 | 1.743387% | 8 KiB |
| 24 | 286,581 | 0.923201% | 2 MiB |
| 27 | 1,762,293 | 0.709638% | 16 MiB |
| 30 | 12,771,274 | 0.642840% | 128 MiB |
| 32 | 41,347,483 | 0.520305% | 512 MiB |
| 34 | 151,917,636 | 0.477922% | 2 GiB |
| **35** | **263,841,377** | **0.4150130471%** | **4 GiB** |

For K=35, **C_35=103,953,502,538**, **P_35=25,048,249,270,272**, exact density **51976751269/12524124635136**. On the fixed half-open research interval [B,E), width **607,481,811,869,561,257,984**, partitioning into full P_35 periods plus at most one shorter remainder proves that the exact number of residual candidates lies in

[**2,521,128,681,930,256,170**, **2,521,128,785,883,758,708**].

This bound is rigorous; it does not pretend that the exact 2^35 by 729 class bitmap was enumerated. The K=24+mod9 alternative was independently enumerated using 286,581 low-bit survivors and CRT: **5,764,853,461,828,189,824** candidates in [B,E); the complementary mathematically eliminated count is 601,716,958,407,733,068,160. K=35+3^6 reduces the theoretical candidate fraction by **16.7331x** relative to the R3E21-1 K5+mod9 6.9444% baseline; this is not a throughput claim.

## 7. Prototype certificate and cost architecture (NOT deployed)

A simple research-only membership procedure: first consult an independently proved 729-residue reverse mask; otherwise consult a depth-24 2 MiB low-bit prefix mask (retains only 286581/16777216=1.70816%). Only for its rare survivors continue the exact parity-prefix counter from depth 24 to 35, using n mod 2^35, until the first descent-slope inequality holds or K=35. Recomputing at most 35 small-residue T steps on 1.70816% of raw inputs gives an elementary bound of **<0.598 symbolic T operations per raw input on average over complete periods**, plus the table/modular tests (actual cost unmeasured). Precomputed T^24(low residue), odd count and a lift formula could further reduce the rare path, at a few MiB additional data cost. A full depth-35 4 GiB bitmap is NOT necessary to obtain the mathematical coverage; neither GPU branch/divergence/memory performance nor construction cost has been benchmarked.

Necessary soundness obligations for later engineering: independent generation and checksum of all static LUTs, full parity-word witnesses or inductively checked recurrence, threshold handling for all covered n, immutable earlier proven interval, witness/precedence class accounting, 128-bit/overflow guards, atomic verifier and replay under a **new version**. No existing CEML production rule, scientific batch, certificate, source identity or public verified tally is changed by this document. Barina has more sophisticated real masks (his 2^16 published map claims 1720/65536 survivors, versus **2114/65536 for this narrower prefix-only test**), so 0.415% here must **not** be called a new state-of-the-art best sieve or a demonstrated speedup over Bařina.

## 8. Ranked mathematical alternatives and failure boundaries

1. **Primary: exact adaptive high-n forward prefixes**, with rare-survivor continuation. Completely proved, extends existing P1 coverage substantially; familiar parity mathematics, performance TBD.
2. **Supporting: 3^6 reverse coalescence**. Completely proved templates; 11 extra mod729 classes versus mod9; already Barina prior art.
3. **Mixed 2-adic/3-adic new coupling:** no additional coupled descent rule has yet been proved beyond coprime CRT product. A local necessary congruence is not sufficient.
4. **Finite-state potentials:** no exact potential/ranking-and-lifting theorem yet. Naive finite quotient SCC removal is unsound.
5. **Inverse-tree global enumeration:** exact predecessors are useful (2 above); uncontrolled tree coverage does not add safe skips and may double-count.
6. **Tao/statistical, logarithmic, cycle-only carry bounds:** important research context; no deterministic frontier skip mechanism proved.

This session makes no new universal convergence claim and does not establish a previously unknown theorem versus prior art. Its **substantive CEML result** is a proof-complete finite-range reduction and reproducible quantitative, memory-aware research design.

## 9. Tests, sources, and handoff

Research fixture: research/r3e21_3_symbolic_sieve.py, Python standard library. Passed exact DP, separate low-bit enumeration for K=1..12, direct high-n T prefixes for all 2^K classes K<=12, 179 reverse templates, 335 exact reverse witness replays, exact K24+mod9 CRT count. No scientific batches, local operator commands or production verifier tests were run; no hosted GitHub Actions existed on entry (CI ABSENT, not PASS); branch protection inaccessible (UNKNOWN). External source pointers: David Barina, *Improved verification limit*, Journal of Supercomputing 81 (2025), article 810, DOI 10.1007/s11227-025-07337-0; https://github.com/xbarin02/collatz ; https://github.com/xbarin02/collatz-sieve ; Terence Tao, *Almost all orbits of the Collatz map attain almost bounded values*, Forum Math. Pi 10 (2022), e12; CEML docs/P1_EXCLUSION_PROOFS.md and docs/R3E21_1_FRONTIER_SCALE_AUDIT.md. The attached Deep Research report pertains primarily to the separate nontrivial-cycle programme; its proposed all-rotations strengthening is explicitly corrected above.

**Next research objective**: source-pin and compare *actual* Barina full residue masks with this prefix-only sieve and identify a genuinely independent, proof-safe improvement beyond their known elimination mechanisms. Independently certify the compact hierarchy's symbolic witnesses and measure table-construction/membership cost on *bounded mathematical fixtures only* before making any operational proposal. See NEXT_SESSION_PROMPT.md; R3E21-4 FUTURE/UNEXECUTED.
