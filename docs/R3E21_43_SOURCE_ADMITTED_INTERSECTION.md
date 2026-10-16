# R3E21-43 — exact source-gate / canonical-descent intersection in eight complete disjoint cylinders

**16 October 2026 | £0, research-only | mathematical bounded-class result GO; global source2 bitmap/interval/production NO-GO.** Parent: merged R42 main `558cc77187840a2dc4937757f744a843ab6f6e32`; R42 exact-head PR fixture [run 38864031304](https://github.com/jfairfaxball-348/CEML/actions/runs/38864031304) independently completed SUCCESS, 11 observed jobs including R42. R42 merge/main push must not inherit a PR conclusion: the merge commit has no PR-triggered run from the connector endpoint, and push requires separate audit.

## Finite intersection theorem and its exact scope

Let B = **2392518188130438742016**; E = **3000000000000000000000** exclusive; L=2^66; P=3^43. Define exactly eight disjoint low48 cylinders of 66-bit roots `r = low + j·2^48` with `0 ≤ j < 2^18`, where low is the following explicit list:

`148957342012655, 146557399178687, 130677744459943, 21359721993575, 236955905271263, 53319191503839, 202396992200703, 35120119522751`.

Each root is subjected to **every actual source-search1 66-step gate**, including the dynamic `number>base`, exact 306/485, predecessor, and doubleeven transitions. Terminal membership additionally requires **f=43, positive odd trailing even-run q**, as R41. For each eligible root, take the first eight valid lifts `n=r+aL ∈ [B,E)` (a=32..39 or 33..40) and select the unique canonical a with `number-1+aP≡0 mod8`. For each such canonical n, the prior exact R42 affine theorem guarantees **literal shortened T^69(n) < n**; R43 also actually replays 69 T-steps for every eligible canonical n. We intersect this family with **the source's exact search2 mod9/terminal flag gates**, namely `n mod9 ∈ {0,1,3,6,7}` and (if flag=2) `(number+a) mod2=0`. Terminal flag1 is absent within this domain. Crucially these are **pre-bitmap admission gates, not proof that native search2 would retain/clear that start**.

The eight complete disjoint cylinder tables (no sampling; **2,097,152** distinct potential roots visited, 262,144 per class):

| low48 | Eligible roots | Optional ninth | All clipped mod9/flag-admitted lifts | Canonical admitted AND T^69<n |
|---:|---:|---:|---:|---:|
| 148957342012655 | 2416 | 547 | 10409 | 1194 |
| 146557399178687 | 15884 | 3780 | 70550 | 8357 |
| 130677744459943 | 15884 | 3647 | 70460 | 8298 |
| 21359721993575 | 7006 | 1621 | 30405 | 3487 |
| 236955905271263 | 4910 | 1144 | 21314 | 2467 |
| 53319191503839 | 15884 | 3739 | 70639 | 8301 |
| 202396992200703 | 12401 | 2894 | 54461 | 6348 |
| 35120119522751 | 7006 | 1622 | 30383 | 3485 |
| **Sum** | **81391** | **18994** | **358621** | **41937** |

Among the **81,391 eligible roots**, exactly **75,446** have terminal flag0, **5,945** flag2. They generate exactly **670,122** clipped original-start lifts: 8×81,391 + 18,994 optional ninth lifts. Exactly **358,621** satisfy both source-search2 mod9/flag predicates. Exactly **41,937** distinct canonical lifts satisfy these gates AND exhibit genuine first-69-step strict descent; **39,454** other canonical lifts fail at least one source gate (but still descend). Each canonical root maps to a unique original n because r=n mod2^66. The set of 41,937 is disjoint from R40's **low48 = 163665130792219** cylinder. Thus adding R41's independent 54,438 original admitted-and-descending starts gives **96,375 distinct original starts** in this precisely defined finite union. This is NOT a new world-frontier number or change to a global sieve density.

Certificate: [research/r3e21_43_source_admitted_intersection.py](../research/r3e21_43_source_admitted_intersection.py) uses deterministic exhaustive 2^18 enumeration per cylinder, a second disjoint recursive source-tree enumeration per class (checked against the first with equal tallies and equal sorted SHA-256), literal-T direct step-by-step replay for *all 81,391* eligible canonical original starts, exact a clipping and gate checks, and count-conservation assertions. SHA-256 of all 41,937 distinct admitted canonical original n, sorted numerically as decimal LF-terminated lines:
`fa2add371b8e778e793adfaa84d57a72b6f7d103a74c2528435640100e8bcc24`.

Two authentic witnesses from distinct source outcomes: admitted canonical n=**2730166685562349884655** (66-bit root 48562653336245487, a=37, flag0), rejected canonical n=**2877732756852678399215** (root 40681353988347119, a=39, flag0). Both satisfy literal T^69<n; only the former passes the mod9/flag predicates. Not a source-wide false-clear or Collatz counterexample.

## Why the result is nontrivial but limited

R42 gave one descending canonical lift for **every one** of R41's **6,438,209,236,755,220** global search1 roots, without globally classifying mod9/flag overlap. R43 **now certifies a nonzero, exact overlap on eight wholly enumerated and disjoint root classes**, without any probabilistic extrapolation. It does NOT solve the requested global count over all R41 roots, prove a future-equivalence quotient for (i,f,number,flag,q), or validate search2's bitmap. The direct-witness construction is mathematical; its potential novelty and historical priority are not claimed (the method is downstream of known parity-vector/sieve techniques, Angeltveit's algorithm, and Bařina).

The eight new cylinder classes account for **81,391** R41 roots; R40 separately accounts for **12,401**; the **6,438,209,236,661,428** other eligible roots lie in neither of these nine completed cylinders. All R42 roots continue to have their unconditional canonical descent. Across eight new cylinders, **316,684** other gate-admitted original lifts have not received the specific canonical-69 certificate (some may have other descent certificates; not tested here); their exact unresolved total within those finite classes is 358621-41937. Across the full R41 root family, the symbolic **7R + m** non-canonical family from R42 is still unclassified outside these local classes and R41's local proofs; m global remains unknown. Optional ninth-lift count **18,994** is exact ONLY inside the eight R43 cylinders. The new certificate is a lower-bound example family for the global admitted/canonical intersection, not its full count.

**No deduction from the existing conditional conservative global upper 326518028938128165 is justified**, because independent disjointness from the original global sieve-mask candidate set is unproved. True unresolved interval count unknown; no verified extension of [B,E), no local science and no Collatz-conjecture proof.

## Source hierarchy and retained hazards

On 16 October 2026, directly re-read Angeltveit pinned [Rust](https://github.com/vigleik0/collatz/blob/f3f09248c7ae7299b8443e112f565f309d97f161/main.rs), [CUDA](https://github.com/vigleik0/collatz/blob/f3f09248c7ae7299b8443e112f565f309d97f161/collatz_cudav7.cu), [OpenCL](https://github.com/vigleik0/collatz/blob/f3f09248c7ae7299b8443e112f565f309d97f161/compute_kernel2.cl); original source state `number=T^i(base)+1`, search1 and search2 predicates are retained exactly on this branch. Bařina worker [pinned](https://github.com/xbarin02/collatz/tree/141e13aae243d509a01a43bec597f53a5b97a09f) versus previously observed moving HEAD `e98d0294...` and pinned [collatz-sieve](https://github.com/xbarin02/collatz-sieve/tree/e5f0c264ba1f5f9c0a7d32a10c3aa61b225c70d1) remain external provenance only. Angeltveit [arXiv:2602.10466](https://arxiv.org/abs/2602.10466) algorithm is prior work. Bařina [live author homepage](https://pcbarina.fit.vutbr.cz/) generated 16 Oct 2026 11:21:31 CEST still reported lowest incomplete = lowest unassigned `2175982616·2^40`, author operational claim, **not independent CEML rerun**; peer-reviewed 2025 n<2^71 must be kept separate.

Original LUT50 original raw map and delivered binary SHAs, arbitrary source-search2 bitmap 1=LIVE, 24-bit inverted index `(number·3^(-43)+a) mod2^24`, reset q=0 versus real odd incoming q, R39 real-parity mismatch, source native search3 exceptional paths/overflow guards j≥114, untrusted GPU host/partial-workgroup reservations, R36 j98 closure, R39 j114/j130 residuals **362205922639287064**, **1080231996567188756950656**, and full independent original-start arbiter remain untouched and unverified. R43 makes NO bitmap clearance claim and NO native correctness claim. Source-search2 could hold a bitmap-LIVE value for these 41,937 and still be correct.

Governance: **£0 research only**; no owner PC, production worker, GPU/HPC/paid cloud, BOINC volunteering, scientific batches, external contact, benchmark, website/feed, frozen changes, paper or publication. R43 exact-head CI must be observed on its own commit, PR and merge-push jobs separately; missing/pending is not PASS. **Mathematical finite intersection GO subject to CI; global source2 and production NO-GO. R44 is FUTURE / UNEXECUTED**.
