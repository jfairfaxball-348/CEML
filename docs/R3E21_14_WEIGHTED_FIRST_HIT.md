# CEML-R3E21-14 — Adaptive weighted first-hit inverse-cone cover

**14 October 2026. Research-only. Conditional on external A(B).** Invoked separately by the owner from live main `983425edb283963726aa7cebb874f030469529ec`, the two-parent merge of R3E21-13 PR #41 (parents `78fd37269c57cb7d96df87eb25865b5cbe39c5fb` and authored `dfc9a88b51e8ca1e0f07f339e23967fc5251792d`). No open PR on entry. GitHub Actions runs/check-runs/commit statuses were 0 = **ABSENT NOT PASS**; rulesets empty, main reported unprotected, detailed protection 403 = **UNKNOWN**. R3E21-2 remains FUTURE. No operator, science, production verifier, local Codex, Lean, certificates, feed, website, spend or outreach.

## Theorem: a full-[B,E) disjoint weighted first-hit cover

Fix the **external-only** hypothesis A(B): every positive integer strictly below
`B=2175982616*2^40=2392518188130438742016` converges. Let `E=3000000000000000000000` be exclusive and `W=E-B=607481811869561257984`. The *actual* `S_old` is the subset of this interval passing the preserved CEML J12 simple equal-terminal/Bařina-core + 179 inverse-template/direct + lifted reverse predicate and all 72 strict high-base slope-prefix screens. Inherited independently proved **cardinality majorant** (not an exact survivor count):
`|S_old| <= 330156319374735841`.

**Result (conditional):** at least **3,007,471,253,458,601 distinct elements of S_old** have the strict smaller-positive-odd-predecessor `h=1` certificate at some true parity prefix `13<=j<=67`. In consequence,
```
|S_old \ new_h1| <= 330156319374735841 - 3007471253458601
                 = 327148848121277240.
```
Compared with the previous R3E21-13 majorant `330156318951644865`, this decreases the **conservative upper** by `3007470830367625` (roughly 3.007 quadrillion). The new lower bound covers ~0.91092342535% of the *older majorant* (a comparison of bounds, not a measured percentage of exact survivors). It is **not** a frontier advance, exact count of actual residuals, runtime improvement, novel path-merging theorem or independent reproduction of external A(B). The remaining majorant is still huge.

### Finite-state certificate and complete slope protection

Use the exact R3E21-13 high-base offset theorem, proved for every *genuine* parity word of depth `j<=72` at `n>=1455237284`. Write `s` for the odd-step count and `e=-1` before any odd step, thereafter the parity of the number of even steps since the last odd step. If `e=0` and `2*3^s<3*2^j`, then `y=T^j(n) ≡ 2 (mod 3)` and `p=(2y-1)/3` is an **integer, positive, odd, strictly less than n**, satisfying `T(p)=y`. This requires exact signed-offset domination; **not** valid for arbitrary small n or for arbitrary longer reverse words. Prune any prefix with `3^s<2^j`, the previously proven high-base early-descent screen.

Crucially `3^46>=2^72` but `3^45<2^72`. Therefore at *any* prefix of length `j<=67` with `s>=46` and an h1 first-hit already recorded, **all** of its 72-step extensions remain slope-safe: even an all-even suffix cannot violate any later prefix inequality. This turns such a prefix into a wholly certifiable old-predicate cylinder without enumerating its remaining parity extensions.

Independently reconstruct the actual J12 mask: 182 old simple-live low-bit roots, 38 whose allowed 729-mask is empty, and **144 whose entire allowed residue set U is exactly the same set of 394/729 phases**. Reconstruction includes 179 reverse templates (335 covered input phases), all J12 forward/lifted inverse checks, positivity, strictness and the high-base B threshold. A J12 root and U jointly characterise the old pre-72 predicate; later slope-safety is supplied by the previous paragraph. This is only CEML's deliberately restricted *old* predicate, not complete enhanced Bařina or Angeltveit.

### Exact conservative CRT occupancy weight

For a genuine depth-k parity cylinder (equivalently one residue modulo `2^k`), its members in the **nonaligned** half-open interval [B,E) are `first+i*2^k`, with at least `N_k=floor(W/2^k)` members. Since gcd(`2^k,729`)=1, their U-mask residues advance cyclically through all 729 phases. Define the **minimum actual cyclic-mask occupancy**
```
g(k)= floor(N_k/729)*394
    + min_(a in Z/729) sum_(i=0)^(N_k mod 729 - 1)
                         1_U(a+i*2^k mod 729).
```
The empty remainder contributes zero. **Every** k-cylinder contains at least g(k) starts passing its J12 input mask, regardless of low-B alignment, unknown numerical carry, input residue or phase. This is a direct deterministic uniform inequality; no CRT independence or phase expectation. The minimum is calculated by an exact 729-term circular sliding window, with a separate direct all-729-phase oracle for k>=60. Unlike the universal pigeonhole `max(0,N_k+394-729)`, it remains positive through k67.

```
k     55  56  57  58  59  60  61  62  63  64  65  66  67  68
g(k) 9110 4554 2277 1138 568 282 139  68  33  15   7   3   1   0
```

### Adaptive **disjoint** inverse-cone antichain

At any J12-root parity word keep only `(j,s,e,hit)` where `hit` is whether some depth `13..j` had the proved h1 strict condition. This is a **recogniser and conservative weight state**, *not an exact [B,E) numerical counting state*. For each hypothetical next bit `b∈{0,1}` (both genuine extensions of a 2-adic parity word), update s and e, set hit upon first certificate, and discard any child violating `3^(s+b)>=2^(j+1)`.

For j<=67, recursively define
```
V(j,s,e,hit) = max( stop, sum over slope-safe bit children V(child) )
stop = g(j) if [hit and s>=46], otherwise 0,
V(67,s,e,hit) = stop.
```
The choice `stop` consumes the **whole** cylinder; `continue` uses its two **disjoint** true parity-word children. This choice at every state recursively defines a prefix-free antichain of accepted certificates. Each leaf has a previously proved h1 inverse hit, complete 72-step slope safety, an exact allowed J12 root and at least g(depth) genuine input phases in [B,E). The lower bound for disjoint children adds, and taking max of *two separately justified lower bounds* preserves correctness. At the 144 initial J12 states, summing V gives exactly **3007471253458601**. A separate forward state-multiplicity walk reconstructs the chosen leaf-depth histogram and independently verifies the sum of `number_of_disjoint_leaves(depth)*g(depth)`.

Selected antichain leaf counts (no exponential 2^72 materialisation): at k51:40; k60:65,590,045,023; k65:81,405,456,003,279; k66:279,221,685,347,912; k67:904,913,930,865,439. Full per-depth histogram is printed by the fixture. The corresponding **fixed-k** k67-only witness count is `2,138,894,649,753,923` cylinders with `g(67)=1`, so the adaptive antichain increases even that certified lower bound. R3E21-13's small length-60 anchored sublanguage is subsumed, not added twice.

### Hostile numerical-state countermodel

Even with the same `(j,s,e,hit)`, **exact occupancy cannot be recovered without numerical position/phase**. At depth20, two genuine residue cylinders extending the **same allowed J12 root** (`2299 mod4096`) have `(s,e,hit)=(12,0,True)` but distinct exact U occupancy in the real interval:

- `r=14587 mod 2^20`: first member `2392518188130438756603`, number of members `579339801663934`, U count `313113692531675`.
- `r=26875 mod 2^20`: first member `2392518188130438768891`, **same** member count, U count `313113692531674`.

The one-unit difference is a concrete exact counterexample to treating `(j,s,e,hit)` as a faithful **exact** weighted CRT quotient. Nor may an arbitrary h>1 inverse transfer drop signed affine offsets. R3E21-13's low-base length-3 pair `101/011` already disproves the analogous naive unbounded threshold quotient. Our V never claims exact phase data: it uses the proven *minimum* g(k), so this failure does **not** invalidate the conservative bound.

### Independent finite research-only gates

Fixture `python research/r3e21_14_weighted_cover.py` executed in a sandbox (not native CEML science) with exact Python integers: 182/144/38 root and complete common-mask reconstruction; direct 729-phase occupancy checks for k60..67; 2,048 actual 11-step parity lifts of the certified 22-prefix (142 depth33 slope-safe, identical to independent symbolic step counts); explicit 729-cyclic and interval-oracle collision; and direct **[B,B+350000)** full old-root/U/depth72 predicate check of **141** old admissible points, with **25** strict smaller-positive h1 hits. All these 25 are accounted for by true mathematical path merging; **19** have first hit at j<=66 and satisfy the source's exact `306*(j-1)>=485*(s-1)` rational search1 gate; **six first hit at j71** and require investigating Angeltveit's search2 precomputation, not a claim they escaped it. Rechecked adaptive V by a second, nonrecursive stopped-antichain walk: sum = 3007471253458601. These are proof-supporting finite fixture tests, **not external independent verification**, full trajectories, a deployed sieve, or a proof assistant.

### Hostile competitor overlap / novelty

The core h1 certificate and even-trailing parity criterion are **explicit prior art**: Vigleik Angeltveit, *An improved algorithm for checking the Collatz conjecture for all n<2^N*, arXiv:2602.10466v1 (11 February 2026), Lemmas 2.7–2.8, https://arxiv.org/html/2602.10466v1. Source-pinned `vigleik0/collatz` Rust **git blob** `4a33b870d27059feea28985e185b8c8c709eb313` implements `search1` (descent, path merging and odd-even-even), `search2` (mod9 bitset and a 24-step precomputed lookahead) and `search3`. The 19 bounded first hits through j66 match the source's rational h1 gate; six j71 hits fall beyond `MAXBITSINITIAL=66` and no complete search2 run was performed. This is strong **prior-art overlap**, **not a new mathematical inverse criterion or proven improvement over Angeltveit**.

Source-pinned David Bařina enhanced `xbarin02/collatz-sieve` `src/fsieve.c` **git blob** `a0a2386584f7c3db4074044373c9bdea0056bdb1`: `is_live_in_sieve_2_34v2` uses CTZ-compressed alternating runs, descent and extra coalescence; `smallest_predecessor` recursively traverses mod3/mod9/mod81/mod243 shorter-preimage branches and `is_live_in_sieve_2_34v3` invokes it for CTZ-compressed runs. These are more than our old J12 mask. We inspected and specified their real branches, but **did not reproduce a complete source-equivalent enhanced v2/v3 oracle on identical [B,E) inputs**. It would be false to say our 3-quadrillion saving is marginal to Bařina. Angeltveit's already-known Lemmas imply a theoretical path-merging overlap even before his exact implementation is rerun. Full enhanced Bařina vs Angeltveit vs CEML matched **complete [B,E) residual counts remain INCOMPARABLE**. **NOVELTY/PRIORITY UNPROVED.** Tao's logarithmic-density result supplies no pointwise skip.

### Decision and next route

**A mathematically valid, full-window, multi-prefix conservative first-hit cover HAS been constructed**, avoiding enumerating 2^72 words or 29.7 quadrillion stopped leaves; exact numerical quotient remains obstructed. Its improvement is ~0.91% against the preceding upper, still nowhere near resolving the 327 quadrillion remainder. A more aggressive phase/carry optimisation of the same h1 prior-art sieve risks diminishing returns and competitor redundancy. The next R3E21-15 session should therefore attack **compact tail-coalescence equivalence classes / certified finite representative covers**, demanding a disjoint *marginal relative to the full old predicate* and a genuine source-equivalence/novelty kill. No k4/k5 packets, blanket CRT heuristics or hardware pivot.

All frozen scientific identities, existing publications, records and the external base are unchanged. R3E21-15 is **FUTURE / UNEXECUTED**, and R3E21-2 stays FUTURE.
