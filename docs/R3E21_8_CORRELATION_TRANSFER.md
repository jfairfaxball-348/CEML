# CEML-R3E21-8 — Correlation-preserving arithmetic progression transfer

14 October 2026. ONE owner-invoked mathematical research-only session, entry live main 3fb3d36072e595df1c466f5c9178f5a80fdc83a4. R3E21-7 was authored by single-parent 3fec2d294cf9e88f969391d312e2b388772fdebd and merged normally in two-parent merge 3fb3d36072e595df1c466f5c9178f5a80fdc83a4 (PR #34). Entry open PRs none. GitHub Actions total 0, check runs 0, individual statuses 0: ABSENT, not PASS; rulesets [], detailed branch-protection query 403/UNKNOWN. No worker, scientific batch, local Codex, Lean, publication/site, certificate, frozen identity, spending or external contact.

## Research result — proved conditional upper bound

Fix the external assumption A(B) (all positive starts below B converge), B=2175982616*2^40=2392518188130438742016 and exclusive E=3*10^21, interval width W=607481811869561257984. Reuse the **same** R3E21-4/6/7 forward low-bit, Bařina simple-core/equal-terminal, reverse 179-template and lifted coalescence predicates; do not change the meanings of their witnesses. The 182 retained depth-12 roots consist of 144 having a common 394/729 modulo-729 allowed set U, and 38 with empty masks. All inverse-predecessor inequalities from the inherited proof remain conditional on A(B).

**Result: at most 334199143141062522 explicitly unresolved starts in [B,E).** This is a new, strictly stronger **conservative conditional upper**, not the exact surviving number. It improves the prior R3E21-7 bound 342723929836534896 by **8524786695472374**, or **2.4873625543%** relative to that bound. New upper as percentage of W: **0.0550138517090%**. The independent phase-state DP alone gives 334199143141076940; resolving the genuine next parity orientation on eight levels below each of the 144 numerical roots gives the additional 14418 reduction. These two refinements are evaluated on the same partition, not added to the earlier selective 55259 saving (which is already superseded). No claim about exact survivor count, operational throughput, total runtime, true speedup or extended verification frontier follows.

### Correlation-preserving theorem

For a genuine admissible shortened-map parity prefix of length d with s odd steps, its actual intersection with the integer interval is an arithmetic progression

n_i = n_0 + 2^d*i,  0 <= i < N,

where n_0 is the first integer in that cylinder inside [B,E). Put t=n_0 mod729, u_d=2^d mod729 and the exact modulo-729 mask count

C_d(N,t) = sum_(i=0)^(N-1) 1_U((t+u_d*i) mod729).

This is computed without enumeration as floor(N/729)*394 plus a doubled cyclic-prefix-sum tail of length N mod729. Signed endpoints are handled by exact mathematical ceiling division.

The standard affine parity-lift identity yields

T^d(n_i)=T^d(n_0)+3^s*i,

so the *next parity alternates with the index i*. The even-index subsequence has length ceil(N/2), phase t and step 2^(d+1); the odd-index subsequence has length floor(N/2), phase t+2^d and the same new step. Importantly the two orientations are alternatives for the **same actual cylinder**, not separately free phase choices.

Define F(d,s,N,t) as the following universal upper. If 3^s<2^d, set F=0 (proved high-base descent through depth 79 for every n>=B). If d=72 or N<=1, set F=C_d(N,t). Otherwise put a=ceil(N/2), b=floor(N/2), t'=(t+2^d) mod729 and

F = min( C_d(N,t), max(
  F(d+1,s,a,t) + F(d+1,s+1,b,t'),
  F(d+1,s+1,a,t) + F(d+1,s,b,t')
)).

Every occurrence of F with a descending state is zero. This is **safe for every actual numerical cylinder** by induction on remaining depth: stop is a valid mask upper, and if splitting, the next parity of the first point is either 0 or 1; the *same* choice forces the other child's opposite parity. The max covers both possibilities and no child is counted twice. The high-base prefix theorem legitimately removes a descending child under A(B). Therefore the min of the stop and split bounds remains safe. Root cylinders are pairwise disjoint, so their individual F values add.

For the first eight levels below each root, replace the unknown orientation by the actual parity of T^d(n_0) computed using exact (research-only) integer iterates, and take the minimum of exact stop and disjoint oriented child sums. Below those eight levels use the proven F. This is an additional safe refinement, not an assumption of random or independent parity.

Memoisation keys (d,s,N,t), where 0<=t<729 and N halves on each split; the actual fixture uses 1,305,998 cached states, with no traversal of the 2^72 numerical residues or 29,715,960,543,835,736 R3E21-7 stopped leaves. The full result is a bound because the unknown orientation is maximised afresh at subtrees, potentially allowing incompatible orientations along different paths. An exact full-predicate [B,E) survivor count remains unresolved.

### Precise obstruction to coarser carry state

The compressed key (d,s,n mod729) alone **does not determine** the next orbit parity: at depth d=13, residues v=91 and v=3007 both have s=10, v mod729=91, and non-descending length-13 parity prefixes, but T^13(91)=668 is even while T^13(3007)=21683 is odd. Thus any exact transfer or carry DFA omitting the next-orientation information is unsound. The F recurrence avoids that unsoundness by a max over the two coherent orientations; it is not falsely advertised as an exact finite automaton. Tracking a minimal compatible orientation/carry invariant is an open mathematical improvement target, not a proved impossibility theorem.

### Independent research fixtures

Run from repository root: python research/r3e21_8_transfer.py. The script independently reconstructs the original 179 reverse templates, depth-12 Bařina simple generator, lifted coalescence masks, and 144 active/38 empty roots (without importing older research code). It tests 980 direct modulo-729 cyclic counts across four masks, signed phases, zero/full length, N=1, N=729, N>729, 2^j depths; plus 2000 independent signed/off-boundary fixed-interval CRT endpoint oracles for j=1,4,12,20,79 (including 2^j far larger than width). An independent per-n shortened-trajectory oracle tests 11,539 eligible depth-12 cylinder members in four unaligned windows near B and E through depth 20 and confirms they never exceed the phase DP's upper. It separately checks the two-orientation counterexample and every relevant integer high-base inequality for j<=79. It reproduces exact phase-only and oriented-eight results above. Tests do not verify orbits to 1 or run scientific batches. This is reproducible author arithmetic, not formal Lean proof or external peer review.

### Source-pinned comparison and novelty gate

Bařina: xbarin02/collatz-sieve/src/fsieve.c **git blob a0a2386584f7c3db4074044373c9bdea0056bdb1** retrieved as a blob, not mistaken for a commit: real v2 is CTZ compressed with beta>=2 precursor; v3 recursively transports residues 2 mod3, 4 mod9, 10 mod81, 182 mod243 and a double-even predecessor. The repository's existing source-pinned research/r3e21_7_source_probe.py independently reproduces bounded k8/k10/k12/k14 v2/v3/joint counts (17,17,17;49,47,47;155,145,145;494,437,437), but neither that semantic probe nor our new phase DP reconstructs the actual enhanced k34 bitmap or validates all high-base uses of its low-residue semantics.

Angeltveit: vigleik0/collatz/main.rs **git blob 4a33b870d27059feea28985e185b8c8c709eb313**, alongside collatz_cudav7.cu and collatz_openclv2.cpp source paths and arXiv:2602.10466v1. The actual search1 branch descent/path-merge/odd-even-even apparatus, precomputed mod9 and lookahead24 bitvectors in search2, and final search3 are stronger and structurally different from this bound. The preprint estimates fewer than 0.02% checks in [1,2^72); it is not a certified matched-[B,E) count. Neither full Rust/CUDA/OpenCL semantics nor true run-time nor a matched-window count has been reproduced here. **External global champion: INCOMPARABLE / UNDETERMINED**. No novelty, priority, mathematical breakthrough, or world-best sieve claim is justified; numerical phase tracking, bit recursion, and adaptive pruning are closely related to prior work. Tao's logarithmic-density theorem does not justify pointwise exclusions.

### Gate

R3E21-8 research work complete with a significant upper-bound improvement, source-aware but non-novelty-certified. R3E21-9 is FUTURE/UNEXECUTED and requires separate owner invocation. R3E21-2 remains FUTURE/UNEXECUTED. Production science, local machine/Codex, source hashes, certificates, website/publication feed and the historical frontier stay unchanged.
