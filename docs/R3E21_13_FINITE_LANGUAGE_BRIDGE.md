# CEML-R3E21-13 — High-base inverse-word language, exact finite-state theorem, and certified marginal cover

**14 October 2026. Research only; conditional on external A(B).** Entry LIVE main `78fd37269c57cb7d96df87eb25865b5cbe39c5fb`, the normal two-parent merge of R3E21-12 PR #40 (parent `fe226fd80afd9e7e339a9686c8e1f06600fda50b`, authored head `6239c8ec0176e1d779bd1eff4d2a3dc1f8a6938f`). No open PR at entry. Hosted workflow runs **0**, check runs **0**, commit statuses **0**: **ABSENT, not PASS**. Rulesets `[]`, main reports `protected=false`, detailed protection 403/**UNKNOWN**. No local operator/Codex, scientific trajectories-to-one, production verifier, Lean, certificates, feed/site, publication, spending or external correspondence.

## Result and limits

Set
```
B = 2175982616 * 2^40 = 2392518188130438742016
E = 3 * 10^21 = 3000000000000000000000 (exclusive)
W = E-B = 607481811869561257984
U_12 = 330156319374735841 (inherited conditional cardinality MAJORANT)
```
Define **S_old** as the *actual* [B,E) integer set passing the precisely preserved depth-12 Bařina-simple/equal-terminal plus 179 inverse-template / forward-to-inverse mod729 predicate, and all 72 high-base slope-prefix tests `3^{s_i} >= 2^i`. R3E21-10's conservative transfer proves `|S_old| <= U_12`; it does not compute `|S_old|`.

**NEW exact full-interval theorem, conditionally proved by a disjoint symbolic cover:** there are **at least 423,090,976 distinct n in S_old** with a strictly smaller positive *odd* predecessor of `T^22(n)`. Therefore
```
|S_old \ new_inverse_certificates| <=
    330156319374735841 - 423090976
  = 330156318951644865.
```
This is a **valid conservative new global conditional upper bound**, not an exact actual survivor count and not a run of the full old transfer with integrated first-hit languages. The reduction is only about **0.00000012815%** of the inherited upper; it does not make the full verification tractable. It is not a Collatz proof, a new contiguous frontier, a measured runtime gain, a new world-best sieve or an originality/priority claim. The complete R3E21-13 first-hit [B,E) language count remains **OPEN**.

## Theorem A — affine offset elimination for the one-odd-step predecessor at high base

For a genuine length-j parity word `w=(b_0,...,b_{j-1})`, let `s=sum b_i` and `2^j*T^j(n)=3^s*n+C_w` for every positive member of the 2-adic word-cylinder. The nonnegative offset obeys the **sharp fixed-(j,s) bound**
```
0 <= C_w <= C_max(j,s) = 2^(j-s) * (3^s - 2^s).
```
Proof: under an adjacent switch `10 -> 01` (postponing an odd step), `C` increases by `2^i` at that pair, multiplied by `3^(number of later odd steps)` after the remaining suffix. Thus all evens then all odds maximises `C`, with the displayed finite geometric sum.

If `s>=1`, the future image `y=T^j(n)` is independent of input modulo 3 and has `y ≡ C_w*2^(-j) (mod 3)`. Equivalently, **`y ≡ 2 (mod 3)` iff the number of even steps AFTER the final odd step is even** (including zero). This is a known path-merging criterion, not a new congruence fact.

When `y≡2 mod3`, the one-step odd inverse `p=(2y-1)/3` is integral, positive and satisfies `T(p)=y`. Its strict smaller-start condition is exactly
```
(2*3^s - 3*2^j)*n + 2*C_w - 2^j < 0.  (*)
```
At arbitrary small bases, `(j,s,C_w mod3)` is not enough to decide (*): e.g. the length-3 words `101` and `011` both have `s=2` and `C≡1 (mod3)`, but `C=7` and `C=10` give respective inequalities `-6n+6<0` and `-6n+12<0`. The former fails at actual cylinder member `n=1`; the latter holds at `n=6`. **Do not identify these domains without a proved base bound.**

**Strong high-base domination theorem:** for ALL `1<=j<=72`, `1<=s<=j`, and ALL positive n at least **1,455,237,284** having the specified actual parity word,
```
0 < (2*T^j(n)-1)/3 < n, T((2*T^j(n)-1)/3)=T^j(n)
    iff  [even trailing-even count after final odd]
         AND [2*3^s < 3*2^j].
```
The left side is understood to require integrality. Sufficiency: for `delta=3*2^j-2*3^s>0`, use `C<=C_max`; exact integer maximisation over the finite `1<=s<=j<=72` triangle gives
```
max_{delta>0} max(1, floor((2*C_max-2^j)/delta)+1)
     = 1455237284, attained at (j,s)=(66,42).
```
Therefore (*), even at worst possible offset, holds above that bound. Necessity: when `2*3^s-3*2^j>0`, the `n` coefficient alone dominates `-2^j` throughout this domain (finite exact table; maximum needed `n` at most 25); nonnegative `C` cannot restore (*). Equality of coefficients occurs only for `j=s=1`, whose actual word has `C=1` and `p=n`, not strict inequality. Integrality and positivity follow as stated.

**Consequence:** for this precise high-base, depth<=72, h=1 task, the signed offset is rigorously eliminable. The certificate language is recognised by finite states `(j,s,e)`, with `e` the parity of trailing even steps (or NO_ODD). Transition for odd increments `s` and sets `e=0`; even toggles `e` after the first odd. Accept at depth j>12 when `e=0` and `2*3^s<3*2^j`, while pruning inherited `3^s<2^j`. The *first accepted depth* is well-defined and gives disjoint first-hit cylinders. This is a theorem for **one-step inverse only**. Larger h/a or lower bases may genuinely require signed C / thresholds; do not extrapolate this quotient.

Crucially this *certificate-language automaton is NOT an exact numeric counting automaton*: mapping parity words to input residues modulo `2^j`, and the nonaligned endpoints/CRT phase, still requires numerical cylinder position and exact residue-mask overlap. Merging such states based solely on (j,s,e) gives no justified **exact** [B,E) count. If a cylinder has `N_r` members, the phase set is a specific length-`N_r` cyclic progression modulo 729, not an independent random mask.

## Theorem B — global overlap from a 2,215,136-word compressed sublanguage

Take the R3E21-12 independently checked prefix `n≡6395 (mod 2^22)`. Its `j=22,s=14,C=10360925` parity word passes all 22 slope-prefix screens, and the first h=1 synchronising certificate after J12 occurs **at j=22**. Its image satisfies `y≡2 (mod 3)`, and Theorem A certifies `0<p(n)<n` for **every** such n≥B, including those with `T^22(n)>n`. The J12 residue is `r=2299`; reconstructing the *actual old* J12 simple/equal-terminal, reverse and forward-merge mask yields **exactly 394 allowed input residues modulo 729** for that root (not the full enhanced competitor sieve).

Extend that exact parity prefix from j22 to j60. Retain precisely those suffix words that satisfy `3^{s_j}>=2^j` at every j23..60 and at j60 satisfy `3^{s_60}>=2^72`. The last condition guarantees **every** extension through depth72 passes all remaining slope screens, even if all 12 extra steps are even. Count the suffix words with the finite-state integer recurrence
```
A_22(14)=1
A_j(s)=1_(3^s>=2^j) * (A_(j-1)(s) + A_(j-1)(s-1)),
     23<=j<=60.
M = sum_{s : 3^s>=2^72} A_60(s).
```
Independent exact integer execution gives:
```
s_60          46       47      48     49   50  51 52
A_60(s)    1792436   357830   57169   7037  627  36  1
M = 2215136
```
The parity-word map from residues modulo 2^60 to length-60 parity words is a bijection, and extending a fixed length-22 word gives distinct length-60 cylinder residues. Proof by induction: at depth d, increasing the input by 2^d changes `T^d` by odd `3^s`, flipping its next parity, thereby separating the two lifts. Consequently all M subcylinders are disjoint; none is multiplied by a guessed overlap rate or assumed CRT independence.

For any residue `r mod 2^60`, the number `N_r` of members in half-open [B,E) is either `floor(W/2^60)=526` or 527. Its successive members differ by `2^60`, coprime to 729, hence the first 526 members have **526 distinct residues modulo 729**. A 394-element allowed mask can reject at most `729-394=335` of these. Therefore, for EACH of the M disjoint length-60 parity cylinders,
```
at least 526-335 = 191
```
actual [B,E) integers pass the old J12 mask and all depth72 slope tests, and **also** have the already-certified strictly smaller positive odd predecessor to `T^22(n)`. Thus the exact full-interval overlap lower bound is
```
|S_old ∩ new_h1_certified| >= 2215136*191 = 423090976.
```
This is a **global theorem**, not a local-sample estimate. Empty/full masks are handled by the finite phase-pigeonhole formula `max(0, floor(W/2^k)+|U|-729)`; here it is strictly positive. Both endpoint inequalities are half-open and need no artificial alignment. Values n<B never appear. Equal p=n is rejected; the actual anchored h1 cylinder is strict. No assumption of uniform CRT frequencies, orientation independence, nor enumerating all 2^60 residues is made.

**Cardinality-majorant subtraction is justified in this special case.** If `|S_old|<=U_12` and a disjoint, source-equivalent global certificate proves at least `L` members of **S_old itself** are newly killed, then `|S_old\new|<=U_12-L` irrespective of whether U_12 was an exact count. It would be invalid to subtract the 25 bounded-window observations *without independent proof of how they contribute to a global overlap*, or to interpret 330-quadrillion as exact survivors; this session instead proves a full-interval overlap **lower bound** against the exact old predicate. No original R3E21-10 transfer counts are altered.

## Independent truth gates and numerical evidence

Research-only fixture: `python research/r3e21_13_language_bridge.py`. It independently reconstructs the **single applicable R3E21-4 old root mask**, not the full enhanced fsieve; enumerates all (j,s) in the 72-triangle and confirms the **1455237284** sharp worst-offset sufficient base; independently counts the 2,215,136 suffix words with only small (j,s) states; brute-checks all `2^11` short parity lifts against the symbolic recurrence (**142** admissible of 2048, word-map bijective); verifies 22-step exact affine inverse on the real B; and **constructs an explicit qualifying [B,E) integer** in a length-60 parity class with an allowed mod729 phase, testing all 72 genuine shortened-map parities. These are finite arithmetic spot-checks plus a universally quantified pencil-and-paper proof, not a formal proof assistant nor scientific Collatz verification.

## Hostile prior art and negative gates

**Not original at the certificate level.** Vigleik Angeltveit, *An improved algorithm for checking the Collatz Conjecture for all n<2^N*, arXiv:2602.10466v1 (11 February 2026), https://arxiv.org/html/2602.10466v1, explicitly proves the *same* path-merging condition in §2.3 Lemmas 2.7–2.8: `T^j(n)≡2 mod3` implies the odd predecessor and trailing-even parity criterion, with a smaller-start test. His real Rust `main.rs` (https://github.com/vigleik0/collatz/blob/main/main.rs, `search1` lines 206–277, `search2` 280–319 and precomputed 24-step lookahead) carries this certificate and more rules. He already has bitwise parity-search / merging; **this session's language is not a new Collatz sieve principle**. A potentially useful *CEML-specific analytic partial counting bound* is not thereby a publication-worthy priority claim.

David Bařina's **enhanced** `fsieve.c`, https://github.com/xbarin02/collatz-sieve/blob/master/src/fsieve.c, has `is_live_in_sieve_2_34v2` at lines 277–311, recursive `smallest_predecessor` 313–362, and enhanced v3 at 364–403. Those implement strictly more than our restricted J12 old mask, including larger inverse words, CTZ-compressed parity segments and additional predecessor/merging branches. Consequently our 423-million CEML-*old-mask* marginal has **NOT** been shown marginal to enhanced Bařina nor Angeltveit's complete search. Their matched [B,E) full global totals remain **INCOMPARABLE**. Source pins from R3E21-12 remain `fsieve.c` blob `a0a2386584f7c3db4074044373c9bdea0056bdb1` and Rust `main.rs` blob `4a33b870d27059feea28985e185b8c8c709eb313`; the URLs were re-inspected, not re-run at full size. Any new substantial originality claim would require a serious novelty and matched-domain prior-art audit.

Tao, https://arxiv.org/abs/1909.03562, supplies a logarithmic-density almost-all result, not pointwise convergence, a finite-language acceptance theorem, or authority to skip an arbitrary explicit n. No Tao skips claimed.

**Unresolved structural bridge:** finite **certificate** recognition is achieved for h=1, and a *globally certified disjoint marginal sublanguage* is counted. But we do not have an exact or sharp full-[B,E) *union* count for all first-hit h1/h>1 templates under the correlated input mod729 mask and depth72 prefix predicate. A universal automaton over (j,s,e) alone loses nonaligned numerical position; any exact whole-language transfer must preserve/calculate carry and CRT phase or prove domination that safely bounds their loss. The 423-million decrease is tiny against U_12. If the broader weighted first-hit transfer cannot be established, the next independent mathematical route is compact tail-coalescence equivalence classes and representative covers; no default to k4/k5 carry-packet tuning, root-phase heuristic, faster production or superficial percentage target.

## Finish and governance

One research-only theorem + genuine finite oracle, minimal additive status overlay, next independent R3E21-14 handoff. Historical conditional A(B), frozen protocol/source identities, verifier, all old scientific certificates/tallies, live feed and site are untouched. R3E21-2 remains FUTURE/UNEXECUTED. No formalisation or outside contact authorised. **NOVELTY UNPROVED.**
