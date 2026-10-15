# R3E21-41 — exact global f=43 / odd-incoming-q search1 root count; closed local original-start witnesses

**15 October 2026 | £0 bounded mathematical research only | Option C (exact root partition with explicit untouched remainder) | NO-GO for production, benchmark and scientific verification.**

## Executive result and quantifiers

For the pinned Angeltveit `vigleik0/collatz@f3f09248c7ae7299b8443e112f565f309d97f161` source-search1 recursion initialised at `(base,i,f,number,doubleeven,numevens)=(3,2,2,9,0,0)`, there are **exactly 6,438,209,236,755,220 distinct 66-bit roots** satisfying *all* search1 gates and ending with **f=43 and positive odd trailing-even count q**. This is an exact root count, **NOT** the number of interval original starts, bitmap-cleared starts, or true unresolved Collatz numbers. Crucially, the `number>base` gate is mathematically redundant on the finite `2<=i<=66` admissible prefix tree (not claimed for unbounded i).

The single low-48 R40 cylinder `r ≡ 163665130792219 (mod 2^48)` contains **12,401** such roots; its **102,090** clipped `[B,E)` lifts include **54,438** admitted by the actual source search2 mod9 and doubleeven flags. **Every one of those 54,438 distinct positive original starts has a literal-shortened-T strict descent by step 349**. Of these, **47,406** descend through step 90 and **7,032** descend at steps 91–349. The R40 **167** source-CLEAR/corrected-LIVE mismatch starts are exactly reproduced (SHA-256 below), with first descents within steps 91–181. The other **6,438,209,236,742,819** search1-eligible 66-bit roots are **UNTOUCHED** by new original-start witness tests, except the symbolic search1 gate proof; none is silently called safe or sound under the source bitmap.

Thus R41 obtains option **C, a complete disjoint root-domain mathematical partition** and a strictly larger closed finite original-start witness class. It does **not** obtain option A's all-interval source-search2 bitmap soundness or an exact tally of search2-admitted original starts outside the cylinder. The target's last-global-witness obligation is therefore **NO-GO**.

## Theorem 1: finite prefix-number-gate redundancy, not an arbitrary-i theorem

For shortened `T(n)=n/2` (even), `(3n+1)/2` (odd), every positive prefix `b ≡3 (mod4)` with `i` chronological steps and `f` odd steps satisfies
`T^i(b)=(3^f b+c)/2^i`, where the nonnegative integer affine numerator offset `c` is positive after an odd step. The stored source `number=T^i(b)+1`; each extension by the high bit `bit·2^i` carries `number'=number+bit·3^f` before its new step. The source checks strict `306i<485f` before its numerical gate can contribute any reachable continuing state. Independently comparing **exact integer powers** on the finite box `2<=f<=i<=66` gives:

```
3^306 < 2^485                         [exact integer comparison]
for all (i,f) with 2<=f<=i<=66:
  if 306*i < 485*f then 3^f > 2^i    [848 eligible integer pairs]
```

Consequently `T^i(b)>b` for all surviving source prefix states in this finite domain, hence `number>b`. The numerical `number<=base` rejection never eliminates any root not already rejected by the *earlier* exact rational/source gates. This is **not** an assertion that `3^f<2^i` alone implies descent: the offset and a positive root matter. It is also **not** an unbounded all-i strengthening of the 306/485 approximation; the 848-case exact finite lemma is part of the proof-object.

The inverse predecessor `(2z-1)/3` is positive and integral exactly when the chronological state `z≡2(mod3)` and `z>=2`. After an odd T step `z≡2 (mod3)`; each following even step flips its mod3 sign. Therefore the source bitmap's reset parity is not a witness at an inherited odd q boundary. Smaller-than-original and no-small-intermediate hypotheses remain distinct and explicit.

## Theorem 2: exact global source-search1 root automaton

For every fixed `i`-bit root `r`, appending either bit `b·2^i` changes the i-step shifted state `T^i(r)+1` by `b·3^f`, an odd increment. Thus exactly one appended bit yields an odd next T input and exactly one yields an even input. This proves a bijection between suffix root bits and chronological parity words. The initial `r≡3(mod4)` fixes two odd steps. A dynamic programme with integer multiplicities on **(i,f,source doubleeven flag, trailing even run)** makes precisely the pinned search1 `306i<485f`, conditional predecessor and doubleeven tests and follows the source's odd/even flag transitions. No state merging loses a future source-search1 constraint because all these future tests depend only on the recorded tuple. Theorem 1 removes the only omitted numerical prefix gate.

Here are independently asserted exact counts of the `f=43, q odd` terminal parity words, successively adding the source gates:

| Class of 66-bit roots with initial 11 parity | Count |
|---|---:|
| f=43, odd terminal q, no source cut | 39,001,983,984,117,856 |
| Also strict rational prefix cuts at every i | 9,398,852,100,800,112 |
| Also conditional predecessor prefix cuts | 7,645,997,023,219,688 |
| Also source doubleeven/flag cuts: **full search1** | **6,438,209,236,755,220** |

The first row equals the independent binomial identity `sum_{q odd,1<=q<=23} C(63-q,40)`; a no-cut DP reproduces `2^64` initial-`11` roots. All counts are exact integer recurrence outcomes. They are **not** statements about a uniform probability distribution, a finite computational scan of all 2^66 roots, or the bitmap's soundness.

This gives a disjoint, lossless partition of the **entire** 66-bit root space (sum `2^66=73,786,976,294,838,206,464`):

| Root class | Exact number |
|---|---:|
| Not initially `3 mod4` | 55,340,232,221,128,654,848 |
| Initially `3 mod4` but rejected by source search1 or not f43/odd-q | 18,440,305,864,472,796,396 |
| Full search1 f43/odd-q in R40's completed low48 cylinder | 12,401 |
| Full search1 f43/odd-q **outside** that cylinder, untouched by original-start witness research | **6,438,209,236,742,819** |

For any such root, exact [B,E) clipping gives either eight or nine high lifts: `a_min=max(0,ceil((B-r)/2^66))`, `a_max=min(63,floor((E-1-r)/2^66))`. Since `B=32·2^66+31334946695616135168` and `E-1=40·2^66+48520948206471741439`, the lift count is 8 or 9 depending on r. No global count of outside roots after source mod9/flag/bitmap application is asserted. The exact root-domain remainder is **not** a count of unresolved original Collatz trajectories.

## Theorem 3: complete bounded original-start finite stratum

Using four explicit disjoint root-index bands `j=[0,65536),[65536,131072),[131072,196608),[196608,262144)`, define `r=163665130792219+j·2^48`. For each band the fixture checks all source search1 prefix transitions, computes all exact clipped high lifts and the source mod9/doubleeven filters, and, **for every admitted original n**, replays all 90 original T transitions, checks `f=43`, inherited odd q and exact `T^66(n)+1=number+a·3^43`, evaluates both 24-state scores and continues literal T as necessary for first strict descent (ceiling 2000). None remained unresolved.

| Original-start outcome in this exact cylinder f43/odd-q class | Count |
|---|---:|
| Search1 roots | 12,401 |
| Clipped high lifts prior to source mod9/flag | 102,090 |
| Search2 source-mod9/flag admitted starts | **54,438** |
| Bitmap source-CLEAR (score >659) | 49,191 |
| Source-CLEAR / corrected-LIVE | **167** |
| Source-LIVE / corrected-CLEAR | 0 |
| Positive smaller integral predecessor at a step 67–90 (may overlap with direct descent) | 48,582 |
| Original T first strictly below starting n by step 90 | 47,406 |
| Original T first strictly below n at step 91–349 | 7,032 |
| Still without first direct descent after step 2000 | **0** |

Four band `(roots, admitted, direct-descent)` triples: `(3116,13287,13287)`, `(3095,13712,13712)`, `(3082,14198,14198)`, `(3108,13241,13241)`. These bands are disjoint and each uses at most 65536 root tests and fewer than 5 million root/lift/original-start probes, with no retained tuple table above 250000. The source-local bitmap parity error is **not** a failure of these independently certified later descents, and not a Collatz counterexample.

Deterministic SHA-256 on sorted ascending **decimal original starts**, each separated by LF with terminating LF:

- All 54,438 source-search2-admitted original n: `7edb1e7df2015e373d4bfc02dd120b7e645e543f2c880f3120194ccfeeecb761`
- The 167 source-CLEAR/corrected-LIVE original n: `ea27859daa20511ce786caba1c212110663e1d42fbb36f7b7a299028ed96406e` (unchanged R40 regression).

Finite results were run on a bounded research environment using standard-library Python: `python3 -B research/r3e21_41_parity_partition.py`. Existing R40 exact root enumeration and R36–R39 source-distinct bitmap/parity fixtures must remain green on the **new R41 PR head**, not borrowed from an earlier SHA. A green Actions fixture is not a compiled/deployed production verifier attestation.

## Explicit soundness, evidence and external boundaries

The reconstructed two-score filter uses actual 24 T states with inherited q on the corrected side and source q=0 on the other, index `(number·3^{-43}+a) mod2^24`, source bit **1 = LIVE**, strict score cutoff **659**, and wrap semantics inherited from R39. The new theorem proves **search1 root reachability and the local finished original starts**, not whole-source bitmap soundness, the source's coalescence proof, or all search2 admitted interval starts. `3^306<2^485` ensures the direction of the rational comparison but not its sufficiency for strict descent without an affine offset. Theorem 4.1/4.4 small-intermediate and lower-state conditions are not removed. Preserve the R36 complete j98 and R39 j114/j130 m<=3 partial certificates, with original residuals 362205922639287064 and 1080231996567188756950656; later pre-multiply native overflow guards stay required.

External pinned files were refreshed by direct exact text: `vigleik0/collatz@f3f09248c7ae7299b8443e112f565f309d97f161` (`main.rs`, `collatz_cudav7.cu`, `compute_kernel2.cl`); `xbarin02/collatz@141e13aae243d509a01a43bec597f53a5b97a09f` (`src/worker/worker.c`); and `xbarin02/collatz-sieve@e5f0c264ba1f5f9c0a7d32a10c3aa61b225c70d1` (`src/sieve.c`). On this check their current respective branch HEADs were `f3f09248...`, **`e98d0294a7ff77e783907e307a80e83b92f4a164`** (distinct from worker audit pin), and `e5f0c264...`. A current worker HEAD is not proof of a particular compiled native binary. The raw LUT50 bytes/digests, host build and flags, GPU workgroup delivery, `USE_PRECALC` all-path behavior, native exceptional-event reservations and independent original-start whole-interval arbiter remain **NOT REVERIFIED**. No full `2^72` or `[B,E)` computation was performed.

Peer-reviewed historical n<2^71 and author-reported live first-incomplete / first-unassigned `2175982616×2^40` (last R39 source timestamp 15 October 2026 17:39:51 CEST; no new authenticated live read) remain separate tiers. Retain `B=2392518188130438742016`, exclusive `E=3000000000000000000000`, `552501489` complete units plus a `350507499520`-start partial, **unchanged conservative conditional upper 326518028938128165**, actual survivor count **UNKNOWN**. The mathematical DP reduction is for a **subset of a source-search1 branch**, not a disjoint new global sieve deduction; do not subtract it from that upper bound. The 20 cold/20 warm per-source benchmark remains UNEXECUTED, no hardware or money, and all frozen V2/I1 identities and website/feed untouched.

**Decision:** GO for the **exact bounded search1 parity-root counting proof and completed 54,438 original-start direct-descent certificates** if PR-head checks are observed; NO-GO for full source bitmap soundness, production changes, benchmark permission, full-interval science, volunteer deployment or a global priority claim. **R42 is FUTURE / UNEXECUTED** and must tackle the outside-root search2/lift arithmetic without resampling another neighboring cylinder.
