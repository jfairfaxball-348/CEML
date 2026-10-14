# CEML-R3E21-11 — Four/five-bit packet truth gate and a carry-state nonidentifiability theorem

14 October 2026. Research-only mathematical session. Owner invocation of the then-live `NEXT_SESSION_PROMPT.md`. Entry `main=a5651c75dd31700c33f8ab7a79b4a62c056f57a5` (PR #37 merged normally, two parents `d3ca9b102bffa2f0beef99a461c5ec35e8519656` and `c048fa2f69c1a03030245cdeb8ecbb4ebbf1c25a`). Before the work: no open PR; Actions runs 0, check-runs 0, commit statuses 0 = **ABSENT / NOT PASS**; rulesets `[]`; public main `protected=false`; detail protection API 403 = **UNKNOWN**. All work is conditional arithmetic, not operational science.

## Outcome and claim boundary

**No newly reproduced stronger absolute full-[B,E) bound.** The prior certified-by-author conditional conservative upper **330156319374735841** therefore remains the published research bound. As in R3E21-10, assume *externally* A(B), that every positive integer below `B=2175982616*2^40=2392518188130438742016` converges. `E=3*10^21=3000000000000000000000` is exclusive. This is neither an exact number of survivors nor proof of any further convergence, accepted CEML scientific batch, novel Collatz theorem, actual runtime speedup or new global frontier. Do not silently upgrade a locally stronger truncated-depth majorant into a global depth-72 saving.

Independently reconstructed the existing 144 live depth-12 cylinders (38 additionally empty), common `394/729` mask, and their depth-12 odd-step summaries, using the source-stated parity, equal-path and reverse-template predicates. Prior full R3E21-10 fixture was **attempted in an independent Python reconstruction** but the full 72-level global carry calculation did not finish within the local evaluation budget (~200 seconds). Therefore R3E21-10's global total is **inherited source-reported proof/fixture evidence rather than independently re-executed in this session**. This limitation is material.

## New proved nonidentifiability theorem (precise scope)

For any depth-d valid parity cylinder, let its first representative be n and let s be its d-step odd count. The affine-lift identity gives
`T^d(n+2^d*729*h)=T^d(n)+3^s*729*h`
for every integer h for which the enlarged starting number is in the intended domain. Since `gcd(3^s*729,2^k)=1`, the k-bit orientations as h runs through `0..2^k-1` form a complete permutation modulo `2^k`. Throughout the sweep, n mod `2^d`, n mod 729, the first d parity words and s do not change. This proves that the *low-bit prefix information and input modulo-729 mask phase by themselves* never identify a packet's k-bit carry orientation. It is a scoped information-loss theorem for this quotient, NOT an impossibility theorem for a transfer with additional numerical position or carry state.

**Explicit in-window k=5 witness.** The reconstructed live root `(r,s)=(27,9)` has `first=2392518188130438742043`, `first mod729=104`. Put `n_h=first+4096*729*h`, `h=0..31`; all are in `[B,E)`, share depth-12 parity prefix, root residue 27, s=9 and phase 104. The 12-step iterates satisfy `T^12(n_h)=T^12(first)+3^9*729*h`. Modulo 32 their orientations are precisely `(9+11h) mod32`, a permutation of `0..31`. An independent direct numerical T iteration checked the equality for all 32 representatives. The theorem does not say `N` alone always fails to distinguish different *fixed-window first members*, and does not prevent caching actual first or extended-phase information.

## Exact packet-width audit and reproducible finite-window outcomes

The previous R3E21-10 packed polynomial/cyclic convolution identity works unchanged for k=4 (16 orientation classes) and k=5 (32 classes). In a separate brute quadratic oracle, the coefficient of each y is the sum over every child index `i<2^k` whose **one common** orientation `y+3^s*i mod 2^k` admits all intervening high-base strict-descent tests; it recurses to identical deeper child bounds. Comparing this *independent explicit orientation loop* against packed convolution on depth-20 truncated transfers gave **9,216 states per width** (18,432 total): d in {11,12,13,14,15,16,19,20}; 0<=s<=d; N in {0,1,2,3,4,5,7,8,9,15,16,17,18,19,31,32,33,40}; t in {0,1,91,728}. Empty children, N<2^k, terminal fallback and mixed admissible words are included. Every comparison passed in the separate independent small-state run. The packed multiplication is exact because every unfurled coefficient is bounded by the exact parent mask count and the chosen digit radix is strictly greater than that cap; cyclic folding is performed explicitly. These checks validate bounded use, not all global states.

Use the *same* four non-aligned high-base windows and the same previously fixed 144 roots/394 mask, with a common truncated max depth of **20**, and independently count the actual admissible 20-step prefixes. Results:

| Half-open window | Root-cylinder points | Direct truth (mask + 20 prefix steps) | Q3 upper | Q4 upper | Q5 upper |
|---|---:|---:|---:|---:|---:|
| [B+1, B+14) | 0 | 0 | 0 | 0 | 0 |
| [B+12345, B+12845) | 16 | 3 | 8 | 8 | 8 |
| [B+9999, B+9999+2^17+17) | 4609 | 1351 | 1886 | 1847 | 1847 |
| [E-3*2^16-77, E-13) | 6914 | 2040 | 2662 | 2662 | 2613 |
| **Totals** | **11539** | **3394** | **4556** | **4517** | **4468** |

Thus the five-bit *depth-20 finite-window majorant* is **88 smaller than** three-bit, and four-bit is **39 smaller**. This is a genuine, exactly checked scope-limited improvement, not a certified saving of 88 from the earlier global full-interval upper. At different depths, the packet groupings are not automatically nested; e.g., a generic Q5 transfer is not thereby proved globally <=Q4 or <=Q3 without a separate argument. These four windows are examples, not sampling-based estimates for the full interval.

## Complexity, adaptive packets, and the actual obstruction

For packet width k, L=2^k, each memoised state requires at most `(k+1)*L` subproblem lookups and digit work plus k+1 big-integer polynomial multiplications of bit width `O(L*log(C+1))`, where C is the whole-parent exact modulo-729 count. For k=4 this is 80 potential child calls; for k=5 it is 192. Multiplication size and memo cache, not just orientation-loop count, determine practical cost. If N<L the number of nonempty child indices is only N; an `O(L*N)` direct orientation loop may outperform radix convolution and is mathematically equivalent. Empty U masks, N=0/1, or infeasible slope are exact early stops. Choosing the better packet bound via `min` of independently proven upper bounds is always safe **provided both refer to the same parent state, depth, phase, actual interval and root assumptions**; it cannot be done by subtracting local savings from an unrelated global maximum.

A quantitative structural *state-cap* applies when all subproblems arise from residue cylinders of the **fixed single [B,E) interval**. At each d, a residue class modulo 2^d occurs either `floor((E-B)/2^d)` or `ceil((E-B)/2^d)` times. Consequently N takes <=2 possibilities for that depth. Since `0<=s<=d` and `0<=t<729`, memo states at d=12..72 are bounded by `2*729*sum_{d=12}^{72}(d+1)=3,824,334`, before removing unreachable combinations. This upper bound is not a promise that millions of big-int operations will finish cheaply; fixed actual-orientation refinements may introduce additional non-memoised work. It is also not a universal cap for unrelated signed synthetic windows.

The full Q3 recomputation did not complete under the available run budget; consequently we did **not** run/reproduce full Q4 or Q5 over [B,E). This is a *resource limitation of this experiment*, not a mathematical no-go theorem, a proven lower complexity bound, or evidence that wider packets cannot improve the global bound. The precise current gap is integrating width 4/5 or true anchored orientation with the original complete length-72 transfer and independently obtaining its **numerical** bound.

## External competitor / novelty truth gate

Read the actual public `xbarin02/collatz-sieve/src/fsieve.c` enhanced source, including `is_live_in_sieve_2_34v2`, CTZ-compressed odd/even runs, terminal/equal-path treatment, and the `smallest_predecessor` congruence recursion and v3 variant. Read actual `vigleik0/collatz/main.rs`, including `precompute`, `search1`, `search2` (mod9 and 24-step lookahead), `search3`, plus Angeltveit's arXiv:2602.10466v1 algorithm description. The pinned source identities previously established in R3E21-10 are retained; this session did not produce a full source-equivalent high-base mask generator or counts for these rivals. Angeltveit explicitly notes the nonlinearity of his search and difficulty adapting it to arbitrary [K,L) intervals (arXiv v1 §1), so comparing its [1,2^72) aggregate or projections against CEML's specific nonaligned [B,E) bound is unsound. Likewise the depth-12 *simple subset* of Bařina is not the full enhanced k34 v2/v3 sieve. A genuine matched full-[B,E) competitor count remains **UNAVAILABLE**; global champion **INCOMPARABLE**, originality and prior-art priority **UNPROVED**. No deterministic pointwise skip follows from Tao's almost-everywhere logarithmic-density result.

## Audit and handoff

Fixture: `python research/r3e21_11_packet_gate.py` (bounded research-only; earlier R3E21_8/9/10 imports). This file encodes the exact fixture assertions above. Separate independent bounded probes passed; no hosted CI was available. No local user computer, Codex, production worker, science, existing frozen identities/certificates, feed/site, Lean, expenditure or external contact was touched. R3E21-2 remains separately FUTURE / UNEXECUTED. `NEXT_SESSION_PROMPT.md` queues **R3E21-12, separately FUTURE / UNEXECUTED**.
