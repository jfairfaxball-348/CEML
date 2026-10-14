# CEML-R3E21-24 — Authentic many-word renewal and a fresh exact-CRT exclusion

**14 October 2026 — RESEARCH ONLY; conditional mathematical bound, no scientific Collatz-to-one run.**

## 1. Entry, baseline and claim control

Pinned live \`main\` at session entry: \`3e694cb63a28d23612cb99f5cf73535fdea8fc9e\`, the merged R3E21-23 result. Queried GitHub connector: open PR search returned zero; individual commit statuses returned \`[]\` (ABSENT, **not** PASS); PR-triggered workflow runs returned \`[]\` (ABSENT, **not** PASS). Full hosted check-run inventory, detailed protection and rulesets were not successfully established this session (**UNKNOWN**). No frozen scientific identities/certificates, operator, owner machine, website/feed, spending, correspondence, or R3E21-2 was touched.

The literal interval is \`[B,E)\` with \`B=2392518188130438742016\`, \`E=3000000000000000000000\` **EXCLUSIVE**, and \`W=607481811869561257984\`. \`A(B)\` is **external only**, never independently reproduced by CEML here; the **actual** historical candidate set \`S_old\` is **UNKNOWN**. The independent old majorant was \`330156319374735841\`. Already consumed disjoint minima: h1 \`3007471253458601\`, h2 \`220259463699144\`, P3/P4 \`52093319358849\`, Q6 \`10905604613006\`, and R3E21-23's R9 lower \`21708672114515\`; these were all subtracted previously, exactly once. Entry official conditional conservative upper: **326843881061491726**.

**NEW, conditional-on-inherited-sieve mathematically certified fresh lower: 325852123360426.** The new official conditional conservative upper is therefore **326518028938131300**. This is a roughly 0.100% relative decrease from the immediate predecessor, **NOT** the hoped-for 10x, an exact surviving count, a speed/throughput result, a new externally established frontier, a proof of Collatz, or proven priority over existing algorithms.

## 2. Approach A — whole authentic finite-predecessor words, not a fictional generator

For the genuine shortened map \`T(x)=x/2\` if even, \`(3x+1)/2\` if odd, every authentic parity word \`w\` of length \`t\` with \`a\` odd steps and carry \`H(w)\` obeys

\`\`\`
2^t T^t(p) = 3^a p + H(w).
p = (2^t y - H(w))/3^a,   y = T^t(p).
y ≡ H(w)*(2^t)^(-1) (mod 3^a).
\`\`\`

Integrality forces a unique input congruence mod \`2^t\`; the reproducer additionally follows every word by **actual integer T** from a positive instance, checking *each parity bit*. Where two words have the same target residue, retain the largest carry, hence the smallest predecessor for that residue. This is an authenticated multiword certificate grammar, **not** a claim that the full reverse basin is rational-semilinear, finite-state complete or universally covers all positive integers.

Investigated **four word/odd-count types**:

| word length \`t\` | odd steps \`a\` | authentic words | distinct target residues mod \`3^a\` |
|---:|---:|---:|---:|
| 10 | 7 | 120 | 85 |
| 11 | 7 | 330 | 206 |
| 11 | 8 | 165 | 121 |
| 12 | 8 | 495 | 325 |

This gives **1,110 authentic words, 737 residue gate entries** (entries across distinct moduli are not disjoint!). Crucially, **the entire previous 21-residue nine-step R9 rule**, plus Q6=433 and the inherited h1/h2/P2/P3/P4 source rules, is excluded at **every** relevant prefix before stopping. No raw count of all words or all 737 gates is subtracted.

### Exact signed proof obligations

At an authentic \`j\`-step prefix of an input \`n\`, with \`s\` odd steps and carry \`C_j\`, \`2^j y=3^s n+C_j\`; and \`0<=C_j<=2^(j-s)*(3^s-2^s)\`. For each \`(t,a,H)\` certificate,

\`\`\`
3^a 2^j (p(y)-n) =
      (2^t 3^s - 3^a 2^j)*n + 2^t C_j - H*2^j.
\`\`\`

The reproducer exhaustively verifies **all** integer \`13<=j<=72\`, \`8<=s<=j\`, all 11 inherited/new gate types, bounding \`H\` at its class minimum/maximum. A negative signed coefficient implies strict \`p<n\` for \`n>=B\`; a positive coefficient implies \`p>=n\` for \`n>=B\`; **every sufficient cut-off is < B** (largest gate threshold \`5820949363\` for inherited P4, and largest new-gate threshold \`486401991\`). Similarly forward strict descent from \`3^s<2^j\` has sufficient threshold at most \`1455237284 < B\`. Positivity of the inverse numerator follows from \`y>=n>=B\`, the authentic word, and finite bounded \`H\`. Signed ambiguity at slope equality is impossible by unique prime factorisation (\`2^t3^s=3^a2^j\` would force \`t=j,a=s\`; none of the strict families requires a gate at that identity).

## 3. Approach B — renewal state and exact all-phase CRT floor

The inherited **J12 source root/mask is reconstructed directly**: 182 roots, 179 primitive templates, 144 admissible genuine depth-12 roots with **one common** \`U subset (Z/729Z)\` of cardinality 394. Every surviving J12 root has \`s>=8\`, so every later true image residue mod **6561=3^8** is fixed by the prefix carry (since \`3^s n=0 mod 6561\`). The exact new finite gate state is \`(j,s,C mod 6561,hit)\`. It tracks *all four* inverse families simultaneously and whether a new authenticated strict-positive-smaller predecessor was seen at **any earlier time**. Reject states immediately upon inherited forward descent, h1/h2/P2/P3/P4/Q6 strict-smaller, or R9 strict-smaller. Count only a **first stop** with \`hit\` and \`s>=47\` at \`j<=67\`.

The future non-overlap lemma is finite and exact:

\`\`\`
3^47 > 2^72,
2^t*3^47 > 3^a*2^72
  for every prior and new (t,a).
\`\`\`

Thus after stopping no genuinely later j through 72 can acquire a previously missed strict-slope forward descent or inherited strict-smaller inverse. The leaves form a **prefix-free genuine dyadic antichain**: 149370690154430 stopped cylinders, so there is no multiword/multitime double subtraction.

For every depth-\`j\` dyadic cylinder the number of integers inside the *nonaligned actual* \`[B,E)\` is at least \`N_j=floor(W/2^j)\`. The separately preserved input phase mask \`U\`, **once only**, gives a certified per-cylinder lower

\`\`\`
g(j) = 394*floor(N_j/729)
  + min_{v in 0..728} # { 0<=i<N_j mod 729 :
                         (v+i*2^j) mod729 in U }.
\`\`\`

No independence, iid parity drift, product-of-phases, asymptotic-density-to-short-window substitution, or fabricated endpoint alignment. The integer sum over disjoint stopped cylinders is exactly **325852123360426** *as a conservative uniform-phase lower*. It is **not** the exact number of target integers in the antichain, because the particular input phases and literal endpoints of every individual cylinder were deliberately forgotten. The forward symbolic histogram and a separately evaluated memoised backward recurrence agreed on the same lower and 149370690154430 leaves (**2,699,890** backward memo states in the local validation). This yields the new upper \`326843881061491726 - 325852123360426 = 326518028938131300\`.

**Formal compression obstruction:** this transfer recognises finite gates compactly but is still endpoint-*inexact*. R3E21-21's explicit same-\`(j,s,C mod729)\` counterexamples with different actual interval counts remain valid. Neither a polynomial-time exact full S_old enumerator nor an efficient depth-160/256 endpoint transfer is established.

## 4. Approach C — hostile overlap and actual genuine-prefix controls

At every intermediate \`j=13..72\`, the new family rejects all **previously consumed** signatures, not just their initial target phases; strongest known high-odd protection at \`s>=47\` is retained. Merely composing h2 with its shifted P2 alias would produce **zero fresh subtraction**: that identity remains an explicit control. Earlier >200 quintillion-run cone coverage has **zero fresh contribution** because all such starts descend directly before depth 72; it is not recounted. The previous R3E21-19 ceiling \`62289308018259707\` is only an upper for a broader high-odd architecture, not a new exclusion.

A **literal 22-digit genuine 72-prefix witness**, independently checked by integer T and actual numeric predecessor inequalities:

\`\`\`
n = 2392518855426464419611
T^15(n) = 4311396664247964401663
p = 2018687784266079354047  (strictly 0 < p < n)
T^10(p) = T^15(n)
first certified first-stop depth = 52 (s=47).
\`\`\`

Every true prefix through depth72 remains >=n; none of the prior h1/h2/P2/P3/P4/Q6 or previous R9 numeric witnesses is positive and smaller. The ten-step parity word is directly authenticated, not inferred from residue alone. This is **NOT** a full path to 1.

Independent bounded \`[B,B+200000)\` actual-integer T oracle: **71** old+prior-admissible starts; **1** new raw inverse hit; **0** qualifying first stops by depth67. The zero is perfectly compatible with the rare, full-window symbolic leaf count and cannot be scaled statistically to W. Old R3E21-23 witness remains untouched.

## 5. Reproduction / source-control and limitations

Research-only self-contained Python: \`research/r3e21_24_multiword.py\`, inheriting the R3E21-23 source/mask reconstruction *within the same file*, with \`python research/r3e21_24_multiword.py\` for default mathematical checks and \`--backward\` for the expensive independent recurrence. The current-session equivalent local reproducer ran word authentication, all-signed thresholds, 72-step large witness, 200000-start literal oracle, forward antichain and backward memoised count; all **mathematical asserts printed PASS**, with the heavy backward process **timed out during interpreter teardown after the PASS output** in that local test, so do not misstate clean OS exit of that particular run. A lighter forward experiment independently agreed with the complete multiword lower. The GitHub-file version was committed and read back, but **hosted execution of that exact committed blob NOT_RUN**.

Previously inherited R3E21-19/20/21/22/23 standalone scripts individually NOT_RERUN as separate commands; inherited J12/729 construction was rerun as part of the new reproducer. Full Bařina CTZ v2/v3 and Angeltveit search1/search2/search3 source-to-source *exact equivalence*, same-window benchmark, full S_old enumeration, originality and priority remain **UNPROVED/NOT_RUN**. Bařina 2025 peer-reviewed 2^71 is distinct from the moving author-reported homepage work-unit pointer; the currently viewed homepage retains work unit \`2175982616 × 2^40\`, not independently validated by CEML. The pinned comparative source blobs remain Bařina \`xbarin02/collatz-sieve/src/fsieve.c\` \`a0a2386584f7c3db4074044373c9bdea0056bdb1\` and Angeltveit \`vigleik0/collatz/main.rs\` \`4a33b870d27059feea28985e185b8c8c709eb313\`. The four primitive routines are **not** the whole CTZ implementation.

## 6. Decision and successor

This session found a **real larger multiword fresh mathematical lower**, but it is still tiny compared with the 326.5 quadrillion-scale conditional obligation. A genuine change of strategy is required. The next investigation should seek a **new object that escapes the high-odd j<=67 saturation**, or an exact, affordable endpoint/high-bit transfer beyond depth72, not just 13/14-step increments in the same grammar. No Lean, production runs or spending.

Custody: exactly four intended changed paths on \`research/r3e21-24-multiword-renewal\`: this report; \`research/r3e21_24_multiword.py\`; an additive \`PROGRAM_STATUS.md\` entry; and \`NEXT_SESSION_PROMPT.md\` advanced to distinctly **FUTURE / UNEXECUTED R3E21-25**. No R3E21-25 execution is authorised by this closeout.