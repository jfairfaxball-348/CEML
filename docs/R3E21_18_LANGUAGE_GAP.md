# CEML-R3E21-18 — An infinite non-source predecessor family, exact marginal and phase-freezing obstruction

**14 October 2026 — RESEARCH ONLY, conditional mathematical sieve; NO scientific Collatz-to-one run.**

## Entry, custody and inherited truth

Entry LIVE main \`bd0c7370219a46e4dacb1a4e0b11586c51a60df0\` is the normal two-parent merge of R3E21-17 PR #45, with authored parent \`882c62891558e027756ffed303d2251a3b08acd3\`. At entry open PRs 0, GitHub Actions runs 0, check runs on main SHA 0, individual combined statuses 0 (aggregate "pending" with EMPTY individual checks is **ABSENT, NOT PASS**), rulesets [], public main protected=false; detailed branch protection HTTP403 **UNKNOWN**. Do not promote an absent hosted check to "passed".

Use shortened positive map T(n)=n/2 for even n and (3n+1)/2 for odd n. B=2392518188130438742016, E=3000000000000000000000 **EXCLUSIVE**, W=607481811869561257984. The assumption A(B) (every positive m<B eventually reaches 1) is externally inherited **only**, not independently verified here. The actual old J12/729/179-template, 72-prefix strict-slope survivor set S_old is UNKNOWN. Its inherited independent majorant is **330156319374735841**. Disjoint previously consumed conservative minima: h1 **3007471253458601**, separately h1-disjoint h2 **220259463699144**, separately h1/h2-disjoint P3/P4 **52093319358849**. Hence last upper **326876495338219247**, not an exact survivor count.

**NEW CONDITIONAL FULL-[B,E) THEOREM:** a further prefix-free set Q6 contained in S_old, disjoint from ALL of those previously consumed families, is uniformly certified to contain **at least 10905604613006** distinct actual integers. Every n in Q6 meets a strictly smaller positive n' at a genuinely authenticated common forward tail. Consequently the conditional conservative explicit-check majorant becomes

\`\`\`
independent old cardinality majorant       330156319374735841
minus old h1 lower                           3007471253458601
minus h1-disjoint h2 lower                    220259463699144
minus h1/h2-disjoint P3/P4 lower               52093319358849
minus NEW all-above-disjoint Q6 lower          10905604613006
= CONDITIONAL CONSERVATIVE UPPER            326865589733606241
\`\`\`

This is **not** actual remaining count, speed, total output of an executable competitor, proof of Collatz, external frontier, production filtering, or an order-of-magnitude advance. The NEW lower removes only **0.00333630737%** of the immediately prior upper. To reach a tenfold lower upper requires excluding a vastly greater number of starts; this session does **not** rule out such a future theorem.

## Theorem A — strict non-closure of the FOUR Bařina recursive primitives

Inspect source-pinned xbarin02/collatz-sieve \`src/fsieve.c\`, blob \`a0a2386584f7c3db4074044373c9bdea0056bdb1\`, \`smallest_predecessor\` lines 313–361. The exact restricted primitive gates and maps (t genuine T steps, a odd steps) are:

| Route | y congruence | p(y) | (t,a) |
|---|---|---|---|
| P1 | y ≡ 2 mod 3 | (2y−1)/3 | (1,1) |
| P2 | y ≡ 4 mod 9 | (8y−5)/9 | (3,2) |
| P3 | y ≡ 10 mod 81 | (64y−73)/81 | (6,4) |
| P4 | y ≡ 182 mod 243 | (128y−211)/243 | (7,5) |

**Exact infinite counterfamily.** For every integer q>=0 define

\`y_q = 433+729q\`, \`p_q = 303+512q\`.

Then \`0<p_q<y_q\` and **T^9(p_q)=y_q**, with *genuine parity word* \`OOOOEOEOE\` (O means an odd input). Indeed this word has 6 odds and affine carry C=809, so \`2^9 y = 3^6 p + 809\`, equivalently

\`p(y)=(512y-809)/729\`, integrality gate \`y ≡ 433 (mod729)\`.

The base case is the completely explicit true path

\`303→455→683→1025→1538→769→1154→577→866→433\`.

Adding 512q to the input preserves the nine-bit true parity word; the affine formula adds 729q to the output. Yet every y_q has residues \`1 mod3\`, \`1 mod9\`, \`28 mod81\`, \`190 mod243\`. **NONE of the four source primitives has even a first inverse move from y_q.** The restricted recursive minimum is y_q for EVERY budget, while a strictly smaller true predecessor p_q exists. Hence the four-primitive recursive graph is **not** the complete reverse graph, even with unlimited recursion budget. This is a strict algebraic non-closure result **about that particular source grammar**. It does NOT show that Bařina's complete accelerated v2/v3 executable fails on those inputs; the executable has additional CTZ/forward/double-even gates. Nor does it show originality relative to all known Collatz inverse path theory.

**Independent source comparison:** Bařina (2025), *Improved verification limit for the convergence of the Collatz conjecture*, J Supercomput 81, 810, describes accelerator families; Angeltveit (2026), *An improved algorithm for checking the Collatz conjecture for all n<2^N*, arXiv:2602.10466, Lemmas 2.7–2.8 and source \`vigleik0/collatz/main.rs\` blob \`4a33b870d27059feea28985e185b8c8c709eb313\`, provide different, broader tail-merging/forward-looking routes. Neither complete implementation was reproduced on exactly [B,E); **NOVELTY UNPROVED and full matched competitor counts INCOMPARABLE**. P3/P4 and source recursive compositions from earlier CEML sessions remain known prior art.

## Theorem B — signed affine high-base and phase freezing

For an authentic j-step parity word of n with s odd inputs and carry C>=0,

\`2^j T^j(n) = 3^s n + C\`, \`0<=C<=2^(j-s)(3^s-2^s)\`.

For the new inverse with (t,a,H)=(9,6,809),

\`729*2^j*(p(T^j(n))-n) = (512*3^s-729*2^j)*n + 512*C-809*2^j.\`

An exhaustive finite exact signed-integer bound for j=12..72, s>=6 finds: when \`512*3^s<729*2^j\` the largest sufficient n threshold from Cmax is **486401988**, at (j,s)=(71,45); when the opposite slope holds, potential small-n adverse offsets are confined below **82**, at (28,18). Equality of coefficients is impossible on j>=12. Since B is enormously larger, the exact strict positive-and-smaller criterion for all actual n>=B in the target congruence class is **precisely** its indicated negative slope and \`T^j(n)≡433(mod729)\`. Positivity holds because a positive target of that class is at least 433.

**Phase-freezing lemma (an obstruction to fake 3-adic gains).** Once a true length-j parity word has s>=a odd steps, \`T^j(n)≡C*2^(-j)(mod3^a)\`, independent of the input's numerical mod3^a phase. Proof: \`3^s n ≡0 (mod3^a)\`, and 2 is invertible mod3^a. Every preserved nonempty J12 root has s>=8, so at all subsequent genuine parity prefixes target residues modulo 3^a (a<=8, in particular 729=3^6) are DETERMINED by the word alone. A proposed additional independent 1/729 selection INSIDE a fixed parity cylinder is mathematically false. The old input 394/729 mask still matters for counting actual points, and must be handled via CRT rather than by treating two 3-adic phases as independent.

This identifies lost information in a naïve symbolic-state shortcut: mod729 input phase and future true word are not freely independently selectable, and a shorter root-only automaton is not enough to identify further parity.

## Theorem C — full-window fresh marginal via a source-external inverse object

Independently reconstruct the R3E21-15 source-based J12 live roots (182), of which 38 have empty old mod729 phase mask and **144 have the identical allowed mask U of size 394/729**. The fixture reconstructs all **179** old templates, not merely hardcodes those 144 roots. Each root is a true depth12 parity cylinder; every such surviving prefix has s>=8. Use exact finite states \`(j,s,C_j mod729,hit6)\`, starting at j12. On every genuine parity extension:

- Require strict old slope \`3^s>=2^j\`.
- Reject any previously consumed P1/h1 or P1²/h2, P3 or P4 **negative-slope and correct-residue** witness at a true depth j=13..72.
- Mark \`hit6\` once the new y≡433 (mod729) and \`512*3^s<729*2^j\` strict predecessor is available.
- Stop first when \`hit6\` and s>=47, at depth j<=67; otherwise follow true parity children through j67.

This **last stop is essential for hostile future-tail disjointness**: \`3^47>2^72\`, \`4*3^47>9*2^72\`, and for ALL P1/P2/P3/P4, \`2^t*3^47>3^a*2^72\`. Thus at every deeper true prefix through j72, neither the old slope gate nor any of the P1/h2/P3/P4 negative-slope tests can appear. In particular no later P3/P4 witness can contaminate the claimed *fresh* overlap. We do not exclude P2 at earlier times, since P2 is not one of the already **consumed** CEML-R3E21-14/15/17 overlap lower families. Hence this is NOT a proof that the whole exhaustive Bařina executable omits Q6.

The stopped cylinders are prefix-free genuine mod2^j integer cylinders. For each depth k<=67 let \`N_k=floor((E-B)/2^k)\` and stride \`u_k=2^k mod729\`. Every integer cylinder contains >=N_k points; modulo729 phases are a cyclic progression with coprime stride. The worst-phase all-endpoint rigorous lower is

\`g(k)=floor(N_k/729)*394 + min_{a mod729} sum_{i=0}^{N_k mod729-1} 1_U(a+i*u_k mod729).\`

The exact **minimum over all 729 phases**, including nonaligned B/E endpoints, is computed with a cyclic sliding window and independently brute-checked at all k>=60. No equidistribution/independence or fractional rounding is used. A direct forward multiplicity antichain counts stopped cylinders (depth:number):

\`\`\`
53:5; 54:183; 55:3452; 56:44715; 57:444970
58:3615408; 59:24959993; 60:150717839; 61:813301404
62:3985167231; 63:17948960651; 64:74811820363
65:289742018391; 66:1048307318233; 67:3571909421095
\`\`\`

Exactly **5007697793933 disjoint stopped cylinders**; independently solving a memoised \`max(stop, sum(children))\` recursion with **371601 cached states** reproduces the forward weighted result

\`SUM_k stopped_cylinders(k)*g(k) = 10905604613006.\`

Because g(k) is a lower bound per actual cylinder and the leaves are disjoint and old-admissible by proof, this is a rigorous disjoint **lower** on new actual [B,E) removed starts, not a guessed true survivor count.

## Hostile bounded direct truth and limitations

\`python research/r3e21_18_language_gap.py\` passes the source-family infinitely parametrised symbolic proof spot checks; source root/179-template/144-mask reconstruction; full finite j,s signed thresholds; a genuine forward antichain and separate backward memo maximum; all-729-phase brute checks at fine depths; and a separate **actual big-integer shortened-map 72-prefix oracle** on [B,B+350000), without iterating any orbit to 1.

That small interval contains **113** actual old-admissible starts surviving the four *previously consumed* h1/h2/P3/P4 tests, of which **one**, n=B+143519 = **2392518188130438885535**, has the newly authenticated witness at j=60, s=38:

\`y=T^60(n)=2803258757066889700603\`; \`p=(512y-809)/729=1968818221698556278063 < n\`; \`T^9(p)=y\`.

It has no earlier consumed h1/h2/P3/P4 certificate through the actual entire 72-prefix; this is a bounded independent concrete test of *fresh* coverage. A 350000-point sample does not establish a global frequency, and the fixture's 72-prefix oracle is NOT Collatz-to-1 verification.

**Research gate verdict:** a rigorous mathematical gap in the restricted source grammar and a measurable additional disjoint CEML-exclusion family are established, but the arithmetic scale barely changes; **the key demand for orders of magnitude is NOT MET**. It would be misleading to declare that another isolated longer inverse word solves the frontier gap. Generic branching quotienting remains canonically pairwise (R3E21-16), finite mod3 phase is frozen by true parity words, and a real breakthrough would need a non-local, many-times/renewal/class-uniform theorem, far larger *fresh* mass, and direct matched competitor falsification. No general ceiling on all positive predecessors or 10x/100x impossibility has been proved.

No native science, local operator/Codex, production verifier, frozen certs/snapshots, A(B) modification, site/feed/publication, resources, outside outreach, or R3E21-2 action. R3E21-19 is explicitly FUTURE / UNEXECUTED.
