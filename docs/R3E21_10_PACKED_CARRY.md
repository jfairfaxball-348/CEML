# CEML-R3E21-10 — Exact integer cyclic carry convolution and three-bit transfer

14 October 2026. ONE newly owner-authorised research-only mathematics session. Repository jfairfaxball-348/CEML; LIVE entry main d3ca9b102bffa2f0beef99a461c5ec35e8519656. PR #36 / R3E21-9 has exactly one authored head 235aa66c26f5684552e4381892c387596693b154 and a normal two-parent merge whose parents are ab6c7c295903675fe264291c7e34710d245eb1d4 and 235aa66c26f5684552e4381892c387596693b154. No open PR on entry. Actions workflow runs 0, check runs 0, statuses 0: ABSENT, NOT PASS. Rulesets []; main branch reports protected=false; detailed protection HTTP 403 means UNKNOWN. No local user-machine access/Codex, production workers, scientific batch, V2/I1/I2 identities/certificates, public website/feed, spending, external contact or Lean.

## Result — a rigorous conditional upper bound, NOT the exact remaining count

Retain precisely external A(B), namely that *all positive integers below* B=2175982616*2^40=2392518188130438742016 converge (external operational assumption, not independently established by CEML). E=3000000000000000000000 is exclusive; W=607481811869561257984. Preserve the certified R3E21-4..9 depth-12 Bařina-simple/equal-terminal and 179 strict predecessor templates, the exact common U mask with 394 allowed residues modulo 729 over 144 live depth-12 cylinders (38 empty), and high-base descent inequalities through depth 79.

**NEW theorem: at most 330,156,319,374,735,841 explicit starting integers in [B,E) are not excluded by the composite.** Reduction from R3E21-9's prior proved *upper* 333,316,047,378,995,972 is exactly **3,159,728,004,260,131**, or **0.94796756085%** of that prior upper; new upper is **0.0543483463906%** of the interval. This is NOT a count of actual survivors, completed verification, a new frontier, measured CPU/GPU acceleration, independently reproduced A(B), a novel theorem priority claim or a Collatz convergence proof.

Exact reproduced intermediate transfer values:
- Inherited R3E21-9 two-bit + eight known orientations upper: 333316047378995972.
- Three-bit phase/unknown orientation recursion: 333056528710095310.
- Three-bit recursion with eight known actual numerical orientations: 330670142619755865.
- **Three-bit recursion with ten known actual numerical orientations: 330156319374735841** (best).

## The exact carry/convolution theorem

Fix any actual depth-d low-bit cylinder after d shortened T steps with s odd steps. Its numerical members in [B,E) are first+i*2^d, 0<=i<N. Let t=first modulo 729, and let C_d(N,t) be the **exact** count in U, computed by the doubled 729-period cyclic sum (R3E21-8); no independence or uniform phase assumption.

The affine-lift identity is T^d(first+i*2^d)=Y+3^s*i, Y=T^d(first). For a k-bit packet, L=2^k, g=3^s mod L is invertible, and the first k shortened-map parities of child index class i depend **jointly** on r_i=(y+g*i) mod L for the single common packet orientation y=Y mod L. Let a_j(r) denote the odd count within the first j steps of the T-orbit of residue r modulo L; the first k parity steps depend only on r, so each a_j is defined exactly. Child i has count N_i=max(0,ceil((N-i)/L)), phase t_i=t+i*2^d mod729, and depth d+k with s+a_k(r_i) odd steps. If any intermediate j has 3^(s+a_j(r_i))<2^(d+j), that child is safely excluded (proved high-base strict descent under A(B)).

Define Q_k(d,s,N,t)=0 if N=0 or 3^s<2^d; otherwise D0=C_d(N,t). At terminal depth 72, N<=1 or D0=0, Q_k=D0. Where d+k>72, use the already proved R3E21-9 two-bit Q_2 as a safe fallback. Otherwise

Q_k(d,s,N,t) =
  min( D0, max_{0<=y<L} sum_{0<=i<L, nonempty, admissible(r_i)}
      Q_k(d+k,s+a_k(r_i),N_i,t_i) ).

All child index classes are disjoint and exhaustive; one *true* common y exists for every actual cylinder. Induction on the remaining depth and the exact mask cap prove Q_k is a conservative universal upper. It is not an exact count: maximising separately at descendants discards longer-range compatibility.

**The nonquadratic transfer:** for each a=0..k, define b_a[r]=1 exactly when residue r gives a valid length-k prefix and a_k(r)=a. Define h_a[z]=Q_k(d+k,s+a,N_i,t_i) where z=g*i modulo L. Then the entire array of L orientation sums is

S[y] = sum_a sum_{z modulo L} h_a[z] * b_a[(y+z) mod L].

This is a *cyclic correlation*, not L independently evaluated L-child sums. Let A_a(X)=sum_i Q_k(child_i,s+a) X^((-g*i) mod L), and B_a(X)=sum_{r:b_a[r]=1} X^r. Coefficients of their ordinary product, folded modulo X^L-1, give S[y] exactly. Compute all (k+1) product pairs by radix/bit-packing polynomials into arbitrary-precision nonnegative integers and multiplication, then extract/fold L digits. Choose radix R=2^w, w=bit_length(D0)+1: every unfurled product coefficient is bounded by sum_i C(child_i)=D0<R, so **no cross-coefficient carries** occur in the integer product; cyclic folding is exact too. This remains correct for large N, irregular upper/lower endpoints, different child sizes, arbitrary phase, and N<L. At each memo state the procedure needs O((k+1)L) child requests and digit work, plus (k+1) exact integer multiplications of O(L log(D0+1))-bit operands, instead of explicit O(L^2) orientation-by-index loops. This is a nonquadratic **structural algorithm**, not a blanket assertion about asymptotic CPU time or memory (big-integer multiplication costs are real).

This session implements k=3 throughout the depth-72 state recursion, not an infeasible enumeration of 2^72 words or 29,715,960,543,835,736 leaves. After retaining exact U mask and actual phase at every memo state, the first 10 numerical binary orientations are additionally fixed from the **actual** Y at each root. An efficient oriented refinement propagates T^d(first) to children as T(Y) and T(Y+3^s), a genuine higher-order numerical carry invariant; no new attempt to infer Y from the insufficient tuple (d,s,N,t) is made. Each refined node is also capped by its own exact CRT mask count.

## Necessity and limitation of the state

R3E21-9's explicit d=13 collision remains an exact obstruction. Starting 639 and 6471 both give d=13, s=11, input residue mod729=639, and next parity 1, while T^13(first) mod8 is respectively 1 and 7 and the *following* parity differs (0 versus 1). Both prior 13-step prefixes stay in the non-descending slope region. Therefore (d,s,n mod729,next parity) cannot deterministically supply a two-bit or three-bit carry; a packet's Y modulo 2^k (or an equivalent distinguishing invariant) is sufficient for its k parity steps. It need not be minimal for all quotient automata. The fully exact long-range finite-state quotient and exact [B,E) survivor count remain unknown.

A naive recursive k=4 exploration was not completed within the bounded research experiment; this is NOT a complexity impossibility or a proof of exponential lower bound. One single k=4 packet restricted to the 144 roots and using inherited two-bit children saves just 337 relative to the two-bit orientation-free root upper (333316047379009070 versus 333316047379009407); this is not competitive with the global compressed three-bit refinement. Our constructive subquadratic correlation identity is valid for general k, but unbounded k=4/k=5 performance and eventual bound improvement are NOT claimed.

## Independent arithmetic and consistency evidence

Exact research-only cloud arithmetic reconstructed 144 live roots/394 mask from the 179 reverse templates and depth-12 Bařina-simple generator, and independently reproduced R3E21-9's orientation-free 333316047379009407 and oriented-eight 333316047378995972 totals. The separate nonproduction fixture research/r3e21_10_packed.py supplies a quadratic, logically independent direct k=3 recurrence oracle against packed convolution for 6840 synthetic states, including d=0,1,3,12,13,17,19, N=0..18, phases 0,1,2,91,728; it additionally reuses the independent predecessor fixtures checking 980 brute cyclic CRT cases, 2000 signed/off-boundary exact intervals including zero/full masks, q=0/q>=1 and strides beyond width, 11539 direct eligible high-number shortened-prefix starts, and high-base j<=79 inequalities. For four nonaligned depth-20 test windows, 11539 root-cylinder test members included 3394 fully prefix-admissible U members; un-oriented packed-three-bit bound is 4556 and eight-orientation bound is 3958, so both safely dominate brute truth. The fixture checks the separate two-bit arithmetic packet oracles and independently asserts all displayed full-window totals. No scientific Collatz-to-one trajectory or operating batch is performed. Executable results are author verification, not independent peer review or Lean formalisation.

## Source-complete competitor attempt and novelty gate

Independently retrieved and inspected actual git **blob** a0a2386584f7c3db4074044373c9bdea0056bdb1 from xbarin02/collatz-sieve/src/fsieve.c. Its enhanced is_live_in_sieve_2_34v2, CTZ-predecessor and smallest_predecessor v3 recurrences plus coalescence/terminal checks are **not** equivalent to the preserved CEML depth-12 simple-core. This session did not reconstruct full enhanced k34 mask under all exact high-base strict witness inequalities or obtain a true like-for-like full [B,E) count.

Independently retrieved actual git blobs 4a33b870d27059feea28985e185b8c8c709eb313 (vigleik0/collatz/main.rs), a783f0f39ee776c725036caec9c93d15a1c8ca72 (CUDA collatz_cudav7.cu), and 5cbe2c1e1958cf3b2ae1224ed3f1defe19db7fdc (OpenCL collatz_openclv2.cpp), alongside Angeltveit's arXiv:2602.10466v1. These implement search1 low-bit/descend/merge, precompute/search2 with mod9 and up-to-24-step lookahead, and search3 remaining trajectories; they are not reproduced by CEML's universal root upper. No verified complete matched high-base [B,E) output or production comparison was reconstructed. Even an Angeltveit estimate for [1,2^72) is not like-for-like with our specific [B,E). Source-complete competitor ranking **INCOMPARABLE**, novelty **UNPROVED**. Bit-parity automata, modular sieves and path merging are extensively prior-developed. Nothing in Tao's logarithmic-density theorem yields deterministic exclusions of named integers.

## Gate and handoff

This report establishes one further conditional arithmetic upper bound and a rigorous compressed-carry transfer; it does NOT establish a world-leading sieve, exact residue survivors, measured speedup, science or a frontier result. No production/frozen/scientific/publication files touched. R3E21-11 is written solely as FUTURE/UNEXECUTED; R3E21-2 remains FUTURE/UNEXECUTED and separately gated.
