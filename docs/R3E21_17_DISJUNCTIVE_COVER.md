# CEML-R3E21-17 — Disjunctive P3/P4 predecessor cover, certified overlap and hostile audit

**14 October 2026. Research-only, conditional mathematics; NO scientific Collatz-to-one batches.** Entry: live main \`2bbde2407512b1399c69fdde739b21f262ba3286\`, R3E21-16 PR #44 merged (authored head \`06ce5e54371b5a522ebef2eae04ca91fdca9601a\`); no open PRs. Hosted commit statuses and PR-triggered Actions runs were EMPTY (**ABSENT NOT PASS**); full check-run and branch-protection/ruleset evidence were not available from the connector, hence **UNKNOWN**, not deemed PASS.

## Mathematical result and unambiguous accounting

Let \`T(x)=x/2\` when x even and \`T(x)=(3x+1)/2\` otherwise. Use external-only A(B) for all positive integers below **B=2392518188130438742016**; **E=3000000000000000000000 is EXCLUSIVE** and W=E−B=607481811869561257984.

The actual prior J12/729/179-template-plus-72-strict-slope admissible set \`S_old\` is UNKNOWN. Its inherited independent cardinality **majorant**, NOT its exact size, is 330156319374735841. Existing disjoint overlap minima already consumed exactly once: h1 at least 3007471253458601 (R3E21-14), and h1-disjoint h2 at least 220259463699144 (R3E21-15), yielding inherited conditional conservative upper 326928588657578096.

**NEW CERTIFIED CONDITIONAL THEOREM.** A finite-state prefix-free antichain Q of whole integer residue/parity cylinders (each intersected with the actual old-allowed modulo729 mask) satisfies ALL of:

1. Q lies in S_old (preserved J12 and every true 72-prefix slope test).
2. NO member of Q has a one-odd-inverse h1 certificate or a two-consecutive-odd h2 certificate at ANY depth j=13..72.
3. For EVERY member n of Q, some genuine true iterate y=T^j(n), 13<=j<=67, has at least ONE of Bařina's two different source-defined primitive predecessors **P3(y)=(64y−73)/81** (six real T steps, gate y≡10 mod81), or **P4(y)=(128y−211)/243** (seven real T steps, gate y≡182 mod243), with 0<P_i(y)<n. Hence strong induction licenses skipping n, conditional on A(B).
4. A conservative, EXACT integer CRT lower bound for the full nonaligned half-open [B,E) is **|Q| >= 52093319358849**, without enumerating 2^72 leaves.

The new lower is H1/H2-DISJOINT, so **no double subtraction**:

\`\`\`
Old S_old independent majorant        330156319374735841
minus consumed h1 lower                 3007471253458601
minus consumed h1-disjoint h2 lower      220259463699144
minus NEW h1/h2-disjoint P3/P4 lower      52093319358849
= NEW CONDITIONAL CONSERVATIVE UPPER   326876495338219247
\`\`\`

The new saving is ~0.015933% of the previous conservative upper, and ~0.000008575% of the interval width. It is **not** an exact actual survivor count, measured throughput/speedup, production sieve, independently confirmed external A(B), new frontier, factor-of-ten reduction, formalisation, or proof of Collatz convergence.

## 1. Hostile prior art FIRST

Pin **Bařina**, \`xbarin02/collatz-sieve/src/fsieve.c\` blob \`a0a2386584f7c3db4074044373c9bdea0056bdb1\`: CTZ v2 277–311, \`smallest_predecessor\` 313–361, CTZ v3 364–403, generator enabling both 434–461. Its FOUR recursive restricted-language inverse transports are precisely:

| Primitive | y gate | p(y) | True T steps | Odd-step debit |
|---|---|---|---|---|
| P1 | y≡2 (mod3) | (2y−1)/3 | 1 | 1 |
| P2 | y≡4 (mod9) | (8y−5)/9 | 3 | 2 |
| **P3** | **y≡10 (mod81)** | **(64y−73)/81** | **6** | **4** |
| **P4** | **y≡182 (mod243)** | **(128y−211)/243** | **7** | **5** |

R3E21-15's \`h2=(4y−5)/9\` at y≡8 mod9 is a P1∘P1 composition. All P3/P4 maps used here are ALREADY IN Bařina's 2024 restricted source grammar. Their discovery, path joining, and generic reverse preimages are **NOT novel**. A different finite-state lower overlap theorem may be new *relative to previous CEML filters*, but mathematical priority remains **UNPROVED**. The earlier R3E21-16 independent bounded source-control-flow port on 2035 residues had v2 live130, v3 live126, v3-only0, v2-only4 and 2093 primitive-closure comparisons PASS. That is not native source execution on our 22-digit inputs nor a matched competitor count.

Pin **Angeltveit**, \`vigleik0/collatz/main.rs\` blob \`4a33b870d27059feea28985e185b8c8c709eb313\`, and arXiv:2602.10466 (2026), Lemmas 2.7–2.8. Source \`search1\` has the true rational slope test \`306*sigfig >= 485*threepower\`, backward even-run gate \`numevens>=2 and even\` with \`306*(sigfig−1)>=485*(threepower−1)\`, and a double-even mechanism. \`search2\` applies its mod9 filter and 24-step lookahead; \`search3\` uses a 16-step continuation. We have inspected these source gates, NOT executed their full same-input CEML-vs-competitor comparison. **Enhanced Bařina and Angeltveit full-[B,E) executable coverage remain INCOMPARABLE.** The P2=(8y−5)/9 route is tracked but contributes ZERO to our new lower, avoiding a spurious source-novelty assertion.

## 2. Uniform signed high-base witness theorem

For a GENUINE j-step word of n with s odd steps and nonnegative affine carry C,

\`2^j y=3^s n+C\`, with sharp \`0<=C<=2^(j-s)(3^s−2^s)\` from R3E21-13.

For any valid source primitive \`p(y)=(2^t y−H)/3^d\`,

\`3^d*2^j*(p(y)−n)=(2^t*3^s−3^d*2^j)*n+2^t*C−H*2^j\`.

If \`2^t*3^s<3^d*2^j\`, the sufficient high-base strictness threshold is the exact integer bound \`max(0,floor((2^t*Cmax−H*2^j)/(3^d*2^j−2^t*3^s))+1)\`. Exhaustive small FINITE arithmetic over j=13..72, s=8..j gives respective maxima (threshold,j,s):

- P2: (2910474616, 68, 43).
- P3: (5820949337, 71, 45).
- P4: (5820949363, 72, 46).

ALL are far below B. Hence at n>=B the specified target congruence AND negative exact slope imply integer, positive, STRICTLY SMALLER genuine predecessor uniformly for every n in that true parity cylinder. No claim of necessary slope condition at all small n is made.

## 3. 3-adic phase rigidity and authentic disjunction

The exact old reconstruction, independently shared with R3E21-15, yields 182 J12 simple roots; 38 have empty mod729 mask; 144 have the SAME nonempty U of size 394. Every surviving J12 parity prefix has s>=8.

Given a full authentic length-j parity word with j>=12, its 3^s*n term vanishes modulo243. Thus \`y=T^j(n) ≡ C_j*(2^j)^(−1) (mod243)\`, *independently of input n mod729* once the genuine parity word is fixed. All four primitive target gates are therefore uniform on a FIXED completed parity-cylinder atom. A "disjunction" that purports to split by unknown mod243 data WITHIN a fixed atom is impossible. Our certificate is instead an explicitly recognised **union of distinct complete arithmetic/parity cylinder classes**; both P3-only and P4-only atoms exist, and neither individual route certifies the entire union.

States: \`(j,s,c,flags)\`, \`c=C_j mod243\`, flags bit1=P2 (tracked, not consumed), bit2=P3, bit4=P4. At next actual parity bit b, \`s'=s+b\`, \`c'=c\` if b=0, otherwise \`c'=(3c+2^j) mod243\`; target residue \`y'=c'*2^(−j−1) mod243\`. Prune if any true prefix fails \`3^s>=2^j\`; prune any h1 gate \`y mod3=2, 2*3^s<3*2^j\` or h2 gate \`y mod9=8, 4*3^s<9*2^j\`. These h1/h2 gates are EXACT at n>=B by the R3E21-13/15 sharp signed-offset theorems. Set P3/P4 flags at their exact modular gates and the proven negative-slope inequalities.

**CRITICAL audited tail gate: stop at the FIRST P3-or-P4-hit state with s>=47, no later than j=67.** Since both \`3^47>2^72\` AND \`4*3^47>9*2^72\`, EVERY extension to depth72 is slope-admissible and cannot have a *new h1 OR h2* slope certificate. This completes the disjointness proof without needing to examine the descendants. Stop leaves form an actual prefix-free antichain. The weaker s>=46 condition from a first draft was **hostile-audit-rejected** because \`4*3^46<9*2^72\` and could silently permit future h2 overlap. Its unaudited 127947636332546 candidate is RETIRED, NOT a bound. The published result here uses only s>=47 and a newly recomputed total.

## 4. Full interval weighted antichain and computational certificate

For a k-bit residue cylinder, let \`N_k=floor((E−B)/2^k)\`, \`t_k=2^k mod729\`. Every full-[B,E) residue cylinder has at least N_k actual members; their mod729 phases cycle by t_k. The following is a **rigorous universal lower** not an average:

\`g(k)=floor(N_k/729)*394 + min_{a mod729} sum_{i=0}^{(N_k mod729)−1} 1_U(a+i*t_k mod729)\`.

The minimum is checked by a sliding 729-cycle sum, with an INDEPENDENT brute 729-phase oracle at k>=60. No 729-phase independence, endpoint alignment, or double-counting is assumed. The whole antichain is counted by a multiplicity-compressed greedy first-hit forward walk (states only \`(j,s,c,flags)\`), and INDEPENDENTLY by a memoised stop-or-branch *maximum* recurrence. Both give **52093319358849** exactly, on **171633** distinct recursive memo states. Forward stopped-leaf histogram (depth : number of residue cylinders) is:

\`\`\`
52:5 53:180 54:3378 55:44049 56:446396
57:3722460 58:26475259 59:164946219 60:918490621
61:4641571685 62:21555445564 63:92826591090
64:372211555693 65:1394763610857
66:4925377413665 67:16402630884481
\`\`\`

Flag-types by *number of stopped cylinders* (NOT actual point counts): P3-only 23138621310565, P4-only 76245774986, both 254116051. All are positive, so the combined source-defined language genuinely needs at least two distinct primitives.

## 5. Independent true-orbit bounded oracle and hostile phase alias

\`python research/r3e21_17_disjunctive.py\` executes only research integer arithmetic, not trajectories to 1. It separately checks the exact old mod729 roots, the full finite signed thresholds, two independent count strategies, actual 72-prefix directionality (including absence of all h1/h2), mod243 phase quotient collision and exclusive E. Explicit authentic old-admissible examples, with NO h1/h2 through j72:

- P3-only: n=2392522326193255436379, first P3 at j14.
- P4-only: n=2392598776513599946863, first P4 at j31.
- Both: n=2394950771631449919579, P3 at j14 and P4 at j39.

The bounded [B,B+350000) true 72-prefix oracle reconstructs exactly 141 S_old members but NO new P3/P4-only members *in that small window*. It is a negative LOCAL observation, not a contradiction of the antichain's distant (first depth52+) certified families and not an extrapolated rate.

Hard countermodel to a naive low-phase quotient: \`n=B+243871\` and \`m=n+4096*729\` share input n mod4096 and n mod729. They have genuine T^12 residues both 242 mod243, but their NEXT parity differs; true T^13 residues are 242 vs121 mod243. Thus \`(root, input phase)\` does not decide all future source gates, and choosing a shorter symbolic quotient without true parity words is UNSOUND.

## Verdict / follow-up

**Research result:** proved a nonempty, fully counted P3/P4 disjunctive source-defined language providing 52093319358849 fresh conservative exclusions relative to CEML's previous certificates; this is a **modest** bound improvement, not orders of magnitude. Source routes and general path merging already known; world novelty NOT established, matched competitor results INCOMPARABLE, actual remaining starts UNKNOWN.

No frozen/production verifier or certificates, local Codex/operator, scientific batch, A(B) base, feed/site, published tally, cost, outside correspondence, or R3E21-2 execution was changed. Next R3E21-18 is separately FUTURE/UNEXECUTED: a hostile bridge to a genuinely more powerful exclusion language with an order-of-magnitude potential, and a source-equivalent full competitor falsification gate.
