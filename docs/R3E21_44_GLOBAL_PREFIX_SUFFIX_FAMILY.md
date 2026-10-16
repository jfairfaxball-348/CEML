# R3E21-44 — exact 275,570,448,293,005-new-start arithmetic intersection via an eight-bit suffix certificate

**16 October 2026 | £0 research-only | option B, globally dispersed constructive counted family | finite-state theorem GO subject to exact-head CI; full bitmap, production and frontier NO-GO.**

## Owner-facing result

A new disjoint family of **275,570,448,293,005 distinct original starts** in `[B,E)` is constructed *without* scanning or storing these starts. For **every** member, the pinned Angeltveit Rust search1 66-bit root condition holds (`f=43`, positive odd terminal even-run `q`); the original start passes the exact source-search2 **mod9 and terminal flag gates** (not the bitmap); and its **literal shortened Collatz iterate satisfies T^69(n)<n**. The set is specified constructively by an exact lexicographic-five suffix selection for each eligible 58-bit prefix, with the nine old low48 cylinders removed. Thus it is an **exact cardinality**, not a rate estimate. Existing R40/R43 admitted-and-descending original starts (54,438 + 41,937 = 96,375) are disjoint, so the combined constructively certified union has **275,570,448,389,380** starts.

This does **not** prove convergence to 1 without a verified smaller-start induction base; it does **not** show that the source bitmap clears these starts, that these starts are missing from existing global exclusions, or that the conditional interval candidate upper bound improves.

## Theorem A — global exclusion of flag2 from canonical intersection

Write `L=2^66`, `P=3^43`. For any R42 canonical lift `a`, `number-1+aP≡0(mod8)`; since `P` is odd, `number+a≡1(mod2)`. The source-search2 terminal flag2 branch admits a lift only when `number+a≡0(mod2)`. **No flag2 root has a source-gate-admitted canonical lift.** This is global and includes optional ninth canonical candidates. Thus for the chosen R42 three-even construction only flag0 roots can contribute, even though R41/R42 count 465,093,429,820,084 eligible flag2 roots.

## Theorem B — a lossless finite quotient for a fixed eight-step suffix

Use the source-faithful search1 state at `i=58`:
`(i,f,flag,q)=(58,39,0,0)`, with an arbitrary genuine 58-bit prefix root `r0≡3(mod4)` and `number0=T^58(r0)+1`. The source's numerical `number>base` gate has already been proved redundant for its entire finite eligible `i≤66` tree by R41's exact 848-pair lemma, and the remaining source-search1 gates depend only on `(i,f,flag,q)`. Hence **every** 58-bit prefix reaching this state can be treated uniformly.

Let `s=0,...,255` be the next eight root bits, so `r=r0+2^58 s`. For the suffix, retain the phase `(r0 mod9,number0 mod2^11)`. As each new bit is appended at position `i`, update:

- `x=number+b·3^f`;
- if `((number&1)==0) XOR b` is true, next `(f,flag,q,number)=(f+1,(flag|[306(i+1)≥485f]) & ~2,0,x+floor(x/2))`;
- otherwise require `flag<2` and set `(f,flag,q,number)=(f,2flag,q+1,floor(x/2)+1)`;
- check `306(i+1)<485f` and the exact conditional predecessor gate at every successor;
- after the step `i→i+1`, reduce `number` modulo `2^(66-(i+1)+3)`.

**Future-equivalence proof:** two starting numbers congruent mod `2^11` enter the same branch at `i=58`; if they are congruent mod `2^k` at step `i`, their `x` values are congruent mod `2^k`, their branch parity agrees, and the respective next numbers (which divide by two) are congruent mod `2^(k-1)`. Induction preserves *every* suffix parity/flag/gate and the terminal `number mod8` through eight steps. The complete absolute root need not be stored for mod9: appended bit `b` changes `r mod9` by `b·2^i mod9`. This is a lossless quotient only for the fixed suffix problem; it is **not** a globally merged source1/bitmap automaton.

For any accepted terminal `(i,f,flag,q)=(66,43,0,odd)`, `P≡3(mod8)` fixes the unique canonical `a mod8=3(1-number) mod8`. Restrict to residues `a mod8∈{1,...,7}` and select the common `a∈{33,...,39}`. These seven high lifts are inside `[B,E)` for **all** roots `0≤r<L`, irrespective of the two clipping thresholds. Thus no boundary comparison/optional ninth carries are being merged or assumed. Final source mod9 gate is exactly `(r+a) mod9∈{0,1,3,6,7}`; flag is exactly zero. The R42 affine theorem ensures `T^69(r+aL)<r+aL`.

The Python fixture evaluates **2048×256=524,288** exact suffix words and all nine mod9 phases. The independent C++ fixture directly enumerates **9×2048×256=4,718,592** phase/suffix combinations with separately coded successor arithmetic, compiled under g++ and clang++. The complete phase histogram (# accepted terminal suffixes per phase : # phases) is:

```
5:49, 6:90, 7:485, 8:1844, 9:2509, 10:1677, 11:2914,
12:3744, 13:2627, 14:1269, 15:747, 16:416, 17:61
```

There are **18,432** phases, exactly **206,080** admitted candidate suffixes across them, **minimum 5** and maximum 17; no phase is unresolved. In particular **every real eligible prefix**, no matter what its actual `number0 mod2048` and `r0 mod9`, has at least five suffixes satisfying the complete stated predicates.

## Theorem C — exact huge family and disjoint union

R41's bijection between appended root bits and parity words counts valid `i=58,f=39,flag=0,q=0` prefixes by an exact integer dynamic programme:

```
N58 = 55,114,089,659,444   (prefix roots, NOT original starts)
```

For each real prefix reaching this state, list the satisfying 8-bit suffix values `s` in ascending numeric order and **retain exactly the first five**. The finite phase theorem guarantees the list has length at least five. Each suffix determines a unique full root `r` and a unique canonical `a=33,...,39` and original `n=r+aL`. Different (prefix,suffix) pairs have different residues mod `2^66`, so all chosen original starts are distinct. We count **five**, not the varying 5–17, per prefix; no unproved uniform phase distribution is needed.

To exclude **all** previous R40/R43 root cylinders, require `r0 mod2^48` not among their nine recorded low48 values. Each old low48 cylinder has exactly `2^10` candidate 58-bit prefixes. Exhaustive source-faithful testing of these nine disjoint prefix groups gives, in R40-then-R43 order:

```
121, 26, 125, 125, 74, 52, 125, 121, 74
sum excluded eligible 58-bit prefixes = 843
```

These 9,216 prefix probes *fully* account for any overlap with the old cylinders; it is not a rate extrapolation. The new class cardinality is therefore **exact**:

```
remaining prefixes       = 55,114,089,659,444 - 843
                         = 55,114,089,658,601
new original starts      = 5 × 55,114,089,658,601
                         = 275,570,448,293,005
old disjoint starts      = 54,438 + 41,937 = 96,375
new + old certified      = 275,570,448,389,380
```

There are **6,438,209,236,755,220** R41 eligible terminal roots in total; nine old root cylinders account for **93,792** of them (12,401+81,391); the R44 family selects **275,570,448,293,005** more, leaving **6,162,638,788,368,423** eligible roots outside these ten disjoint root sets. The remainder is untouched by this new gate-and-descent construction, although *all* R41 roots retain R42's **unconditional per-root canonical descent** irrespective of source gates. Other original high lifts, including the globally unknown optional ninth count `m`, remain unclassified globally. The terminal flag2 canonical overlap is rigorously zero, but no full 66-bit exact count of flag0 gate-admitted canonical starts is asserted.

## Independent bounded concrete witness replay

The Python fixture independently obtains the first 25 lexically searched actual prefix roots in the chosen state outside all nine old cylinders; for each it constructs the first five suffixes and **replays 69 literal original-start T transitions** for **125 starts**. It checks interval bounds, mod9 admission, f43 / odd trailing q, exact `T^66(n) mod8=0`, and `T^69(n)<n`. The first example is original `n=2733576887422834181503`. SHA-256 of the **125 sorted decimal original starts, LF-delimited with terminal LF**:

`9466aa8a805c11ea60f7f0448ccd152941a25c54b21c8f8825529031c9a38518`.

This SHA is **only** for the expressly finite sample of 125 witnesses, **not** a hash of 275 trillion generated starts. No enumeration or hash of the entire constructive huge family is claimed. Retained lists and finite probes are well below the stipulated 250,000-tuples / 5,000,000-probe per finite-class caps. The Python compressed phase equivalence and C++ uncompressed phase enumeration agree on every full phase histogram bin.

## Source soundness, external prior art and immutable boundaries

Source-faithful check: pinned `vigleik0/collatz@f3f09248c7ae7299b8443e112f565f309d97f161` `main.rs` search1 at lines 206–277 and search2 mod9/flag gate at 280–316; pinned `collatz_cudav7.cu` and `compute_kernel2.cl` retained as distinct native/GPU implementations. Pinned `xbarin02/collatz@141e13aae243d509a01a43bec597f53a5b97a09f` `src/worker/worker.c` and `xbarin02/collatz-sieve@e5f0c264ba1f5f9c0a7d32a10c3aa61b225c70d1` `src/sieve.c` inspected; live worker HEAD `e98d0294a7ff77e783907e307a80e83b92f4a164` differs from pin, live sieve HEAD matches pin. No claim of a new result *about* the compiled production versions follows from this. Angeltveit's source is **prior art** for search1, parity gates and the mod9 sieve: novelty claim, if any, is strictly the separate new finite-prefix/suffix counting *application*, not those inherited algorithms. A hostile review must verify the exact 848-case finite prefix lemma, parity-word-root bijection, source gating, independent carry quotient, full original-start and larger-start induction hypotheses, and prior literature before a publication claim. No publication priority/novelty is asserted.

Additional unresolved blocks unchanged: R36 j98 complete; R39 j114/j130 m≤3 partial remainder `362205922639287064 / 1080231996567188756950656`; j≥114 pre-multiply native guards, incoming-even/mod3 predecessor, twoeven, independent source raw LUT50/binary identity, 24-bit index `(number·3^(−43)+a) mod 2^24`, reset q=0 versus inherited odd q, full independently generated original-start arbiter, and GPU host/exception/partial-workgroup paths. **Bitmap bit 1 = LIVE**, and a source-gate-admitted start is *not* thereby bitmap CLEAR. No native production, paid/cloud compute, benchmarking, volunteer execution, hardware, owner PC, scientific batches, publication, website/feed, frozen identity changes or external contact.

Peer-reviewed Bařina historical `n<2^71` remains distinct from author-reported live first-incomplete `2175982616×2^40`, and both remain distinct from an independently reproduced [B,E) certificate; the source-moving upper frontier must be refreshed before any frontier claim. Baseline is `B=2392518188130438742016`, `E=3000000000000000000000` exclusive, 552,501,489 full `2^40` units + 350,507,499,520-start partial. **Conditional global candidate upper 326,518,028,938,128,165 UNCHANGED; actual survivors UNKNOWN.** Neither the 275-trillion arithmetic family nor its locally proved disjointness from *R40/R43* proves disjointness from already deducted full-interval global sieve masks.

**GO:** large exact source-gate-admitted canonical 69-step descending original-start family, subject to new R44 PR-head and main-push jobs. **NO-GO:** complete full-map bitmap/source3/native scientific verification, changing candidate upper, asserting the entire interval, or claiming Collatz conjecture. Next R45 should bridge this spectacular count to verified global prior-mask disjointness / bitmap and precise further arithmetic counting without repeating sample cylinders.
