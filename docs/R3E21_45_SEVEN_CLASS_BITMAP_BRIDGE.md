# R3E21-45 — Seven prefix classes and the source-bitmap CLEAR bridge

**16 October 2026 | £0 research-only | mathematical GO pending exact-head CI; global sieve/science NO-GO.**

## Exact result and scope

Let T(n)=n/2 for even n and (3n+1)/2 for odd n, L=2^66, P=3^43, B=2392518188130438742016 and E=3000000000000000000000 exclusive.

R45 constructs **811,316,649,179,155 additional distinct original integers n in [B,E)**. Each is genuinely accepted by source-search1 (terminal f=43, flag=0, positive odd q), admitted by source-search2 mod9 and terminal flag, has the canonical lift a in 33..39 with **T^69(n)<n**, and is mathematically **CLEAR (zero) under the pinned Rust 24-bit source bitmap**. R44 already constructs 275,570,448,293,005 such NEW original starts. Thus the exact NEW disjoint canonical source-CLEAR-and-descending family has **1,086,887,097,472,160 original starts**. Adding old R41/R43 54,438 + 41,937 previously source-gate-admitted-and-descending starts gives **1,086,887,097,568,535** distinct original starts. The 96,375 old originals have not all been proved bitmap-CLEAR; do not merge that attribute into the full combined count.

## Seven new disjoint i=58 prefix state classes

The second column is source-faithful DP root-prefix counts, the third exact exclusions in all nine previously audited low48 cylinders, fourth the minimum across EVERY (root mod9, number mod2048) initial phase of valid canonical eight-bit suffixes, and fifth the exact number of NEW chosen original starts (remaining prefixes times minimum).

| (f,flag,q) | 58-bit prefixes | Old prefix exclusions | Min suffixes | New originals |
|---|---:|---:|---:|---:|
| (38,0,0) | 47,500,853,814,159 | 697 | 2 | 95,001,707,626,924 |
| (38,0,1) | 28,882,653,731,593 | 436 | 2 | 57,765,307,462,314 |
| (38,0,2) | 15,078,186,832,956 | 235 | 2 | 30,156,373,665,442 |
| (39,0,1) | 25,876,421,228,438 | 403 | 5 | 129,382,106,140,175 |
| (40,0,0) | 42,926,694,229,296 | 651 | 7 | 300,486,859,600,515 |
| (40,0,1) | 17,040,117,571,551 | 249 | 7 | 119,280,822,999,114 |
| (41,0,0) | 26,414,490,561,909 | 352 | 3 | 79,243,471,684,671 |
| **R45 total** | — | — | — | **811,316,649,179,155** |

Complete phase histograms (number of accepted suffixes: number of phases):
- f38, each of q=0,1,2: 2:71,3:752,4:1483,5:3506,6:4117,7:3971,8:3169,9:861,10:502. Exact sum 116480.
- f39,q1: 5:49,6:90,7:485,8:1844,9:2509,10:1677,11:2914,12:3744,13:2627,14:1269,15:747,16:416,17:61. Exact sum 206080.
- f40, each of q=0,1: 7:500,8:1743,9:2568,10:4281,11:3344,12:2716,13:1883,14:1117,15:219,16:61. Exact sum 197120.
- f41,q0: 3:899,4:1860,5:4590,6:4538,7:5161,8:1378,9:6. Exact sum 107520.

The phase sums are UNWEIGHTED. The demanded R45 Priority A exact **globally weighted phase histogram** over genuine initial (r0 mod9,number0 mod2048,f,flag,q) was NOT achieved. Multiplication by an assumed uniform phase rate is invalid. For the old R44 state the certified number of all accepted suffixes after old-cylinder removal remains between 5N and 17N, N=55114089658601; it is not known exactly.

## Mathematical proof

1. Count genuine search1 i=58 root prefixes starting at (i,f,flag,q,number)=(2,2,0,0,9), using one odd successor with f+1,q=0 and one even successor with q+1 only if flag<2. At each i enforce 306i<485f and the exact conditional smaller-predecessor guard. Inherited R41 exact finite 848-pair number>base redundancy is required; no new assumption that number>base always holds in an arbitrary state. The automaton ends with exactly 303 distinct states and the stated counts.
2. For each new state retain the **11 low number bits at i58**. Every successor divides by two once; after eight steps enough bits remain to know all branch parities, guards, terminal q/flag and terminal number mod8. Appending bit at position i changes root mod9 by exactly bit times 2^i mod9. Exhaust all 2048 by 9 phases and 256 suffix words per state. State-specific histograms are exact, not stochastic.
3. Terminal f43/flag0/odd-q states have unique canonical a residue 3(1-number) modulo 8, with a=32+residue if residue is nonzero. All a=33..39 are inside [B,E) for ALL 66-bit roots, so optional ninth lift and clipped-lift phase boundaries are not assumed. Source mod9 gate is exactly (r+a) mod9 in {0,1,3,6,7}. The R42 affine lemma, independently replayed original shortened T trajectories, proves T^69(n)<n. R44 parity already excludes flag2 from canonical gate intersection.
4. For each of nine old low48 cylinders, evaluate its entire 1024-completion set of 58-bit prefixes (9,216 explicit root-prefix probes total); subtract precisely the seven exclusion counts shown, never an exclusion rate. New state classes are pairwise disjoint and disjoint from R44 (39,0,0); each (prefix,suffix) has a distinct 66-bit root, and only one canonical high lift. This proves disjointness from all previously enumerated R40/R43 originals, NOT from a previously counted global CEML sieve mask.
5. **New bitmap theorem:** The unique canonical congruence gives number−1+a3^43=0 mod8. This equals the literal T^66(n), so its next three shortened T steps are all even. In pinned Angeltveit Rust main.rs precompute, raw 24-step bitmap bit 1 means LIVE exactly when maximum score <= the f43 cutoff. The first cutoff is 485*42−306*66=174; f43 cutoff is **659**. Three initial even steps force curval>=3*306=**918**, greater than 659, so bit=0: **source-CLEAR** for EVERY new canonical start, independent of subsequent 21 bits. Indexing is by the exact 24-bit permutation (number*3^(−43)+a) mod2^24, with wrap, checked for all residues by inherited R39 two-parity independent bitmap fixtures. The pinned abstract source-bit CLEAR property is NOT compiled native binary attestation. The full source-LIVE counterexample requested conditionally in Priority C CANNOT occur inside these all-three-even canonical families.

## Reproducibility

- Python: research/r3e21_45_multi_class.py. Seven 524,288-probe compressed phase scans; 9,216 exact old-cylinder prefix probes; independent source prefix DP; 132 original T^90 replays spanning the first four genuine prefixes per eight classes (seven new and R44), each taking the guaranteed lexicographically first suffixes. Among the 132 originals, source-CLEAR=132, source-LIVE=0, corrected-CLEAR=132. The SHA-256 of **only these 132 explicitly enumerated distinct sorted decimal-LF starts** is b60a5e41435c2b5169d1071d821c73c6c8c76dce77698f41350dfeec9ab6d090. There is NO SHA for the trillion-size implicit set.
- Independently coded C++: research/r3e21_45_independent_phase.cpp; g++ and clang++ each check all 9*2048*256=4,718,592 phase/suffix probes PER CLASS (seven separately bounded classes, 33,030,144 total) against all expected histogram bins. No class exceeds the permitted 5,000,000 probes, no 250,000-entry retained table, no owner hardware or science.
- Literal numerical safety: e.g. integers 2733576887422834181503 and +1 coincide as IEEE double, so floating phase merging is invalid.
- Every R36–R44 CI job, both compiler paths and exact merged-main jobs must stay green. No source protocol or frozen evidence changed.

**Untouched complement:** R41 eligible terminal roots 6438209236755220; subtract nine old low48 root cylinders 93792 and this new-plus-R44 exact selected root set 1086887097472160 gives **5351322139189268 eligible roots outside these particular selected sets**. This is not a count of unresolved trajectories. Source flag2 canonical overlap zero; global optional ninth lift unknown.

**Inherited blockers:** R36 j98 complete, R39 j114/j130 m<=3 residuals 362205922639287064 / 1080231996567188756950656. Native guard, original-start arbiter, raw LUT50, GPU host/error/partial-workgroup and independent whole-interval certificate all NOT ESTABLISHED. Search1/source-bitmap is an Angeltveit prior-art algorithm; Bařina's peer-reviewed historical n<2^71 differs from moving author-reported current incomplete 2175982616*2^40. Angeltveit pinned HEAD f3f09248c7ae7299b8443e112f565f309d97f161 (Rust/CUDA/OpenCL); pinned Bařina worker 141e13aae243d509a01a43bec597f53a5b97a09f is NOT worker HEAD e98d0294a7ff77e783907e307a80e83b92f4a164; pinned/current Bařina sieve e5f0c264ba1f5f9c0a7d32a10c3aa61b225c70d1. No novelty/publication, live source binary, or priority claim.

**Fixed global boundary:** 552501489 full 2^40 units plus 350507499520-start last partial, B/E as above, conditional global candidate upper **326518028938128165 UNCHANGED**, actual survivors **UNKNOWN**. Although 1.086 quadrillion NEW originals are source-bitmap CLEAR and descend, a *named exact already-counted global-mask set difference* has not been proved. **DO NOT SUBTRACT THE NEW FAMILY FROM THE CONDITIONAL UPPER.** Neither 1-convergence for arbitrary larger starts nor whole-[B,E) certification follows. No paid/cloud GPU, native execution, owner PC, BOINC, contact, website/feed, frozen protocol or scientific frontier work.

**R46 should solve globally weighted source phases or a precise global-mask overlap obstruction, not simply multiply a phase average.**
