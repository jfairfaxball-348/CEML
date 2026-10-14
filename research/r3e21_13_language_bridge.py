"""R3E21-13: independent bounded parity-language/count oracle. Research ONLY.
No production runner, no convergence batches, no matched-competitor assertion.
"""
from collections import defaultdict
from itertools import product

B = 2175982616 * 2**40
E = 3 * 10**21
J, K, D, MOD = 12, 60, 72, 729
R22 = 6395
OLD_UPPER = 330156319374735841


def T(x):
    return x//2 if x % 2 == 0 else (3*x+1)//2


def finite_uniform_gate():
    # Maximum signed affine offset at fixed (j,s) is reached by
    # postponing all s odd steps until the end of the word.
    needed, arg = 1, None
    for j in range(1, D+1):
        for s in range(1, j+1):
            cmax = 2**(j-s) * (3**s - 2**s)
            delta = 3*2**j - 2*3**s
            if delta > 0:
                requirement = max(1, (2*cmax - 2**j)//delta + 1)
                if requirement > needed:
                    needed, arg = requirement, (j, s)
                assert delta*B > 2*cmax - 2**j
            elif delta < 0:
                assert (-delta)*B > 2**j  # even minimum C cannot save p<n
            else:
                assert (j, s) == (1, 1)
    assert (needed, arg) == (1455237284, (66, 42))
    return needed


def inherited_single_root_mask():
    # Independent direct reconstruction of the exact R3E21-4 J12 predicate,
    # restricted to the ONE relevant low-bit root; not enhanced Barina.
    live = [True]
    for j in range(1, J+1):
        seen, next_live = set(), []
        for r in range(2**j):
            x, a = r, 0
            for _ in range(j):
                a += x & 1
                x = T(x)
            tag = (a, x)
            kill = (tag in seen or
                    (3**a < 2**j and 3**a - 2**j < r - x))
            seen.add(tag)
            next_live.append(live[r % len(live)] and not kill)
        live = next_live
    r12 = R22 % 2**J
    assert live[r12] and sum(live) == 182
    preimages = defaultdict(list)
    count = 0
    for h in range(1, 10):
        for bits in product((0, 1), repeat=h):
            a = sum(bits)
            if not (1 <= a <= 6 and 2**h < 3**a):
                continue
            c = 0
            for i, bit in enumerate(bits):
                if bit:
                    c = 3*c + 2**i
            residue = c * pow(2**h, -1, 3**a) % 3**a
            for t in range(residue, MOD, 3**a):
                preimages[t].append((h, a, c))
            count += 1
    assert count == 179
    x, a, c, prefixes = r12, 0, 0, []
    for j in range(1, J+1):
        if x & 1:
            a += 1
            c = 3*c + 2**(j-1)
        x = T(x)
        assert 3**a >= 2**j
        prefixes.append((j, a, c))
    allowed = set()
    for t in range(MOD):
        if t in preimages:
            continue
        killed = False
        for j, s, offset in prefixes:
            ymod = (3**s*t + offset) * pow(2**j, -1, MOD) % MOD
            for h, alpha, inv_offset in preimages.get(ymod, ()):
                coeff = 2**h*3**s - 3**alpha*2**j
                signed = 2**h*offset - 2**j*inv_offset
                if (coeff <= 0 and coeff*B + signed < 0 and
                        2**h*3**s*B + signed > 0):
                    killed = True
                    break
            if killed:
                break
        if not killed:
            allowed.add(t)
    assert len(allowed) == 394
    assert (B+R22) % MOD in allowed
    return allowed


def count_safe_suffix_words():
    # All words share the certified length-22 prefix (j,s)=(22,14).
    # The state (j,s) suffices to count old slope-prefix viability.
    counts = {14: 1}
    for j in range(23, K+1):
        nxt = defaultdict(int)
        for s, weight in counts.items():
            for bit in (0, 1):
                if 3**(s+bit) >= 2**j:
                    nxt[s+bit] += weight
        counts = dict(nxt)
    accepted = {s:weight for s,weight in counts.items() if 3**s >= 2**D}
    assert accepted == {46:1792436, 47:357830, 48:57169,
                        49:7037, 50:627, 51:36, 52:1}
    assert sum(accepted.values()) == 2215136
    return sum(accepted.values())


def direct_small_word_oracle():
    n = B + R22
    x, s, c = n, 0, 0
    for j in range(1, 23):
        if x & 1:
            s += 1
            c = 3*c + 2**(j-1)
        x = T(x)
        assert 3**s >= 2**j
        if 12 < j < 22:
            assert not (s and x % 3 == 2 and 2*3**s < 3*2**j)
    assert (s,c,x) == (14,10360925,2728304940644277689471)
    p = (2*x-1)//3
    assert (p,T(p)) == (1818869960429518459647,x) and p<n
    # Eleven-step parity extension: direct numerical orbits and symbolic
    # (j,s) counting must agree, and the 2-adic word map is bijective.
    words, direct_good = set(), 0
    for q in range(2**11):
        v = n + q*2**22
        z = v
        for _ in range(22):
            z = T(z)
        word, ss, good = [], 14, True
        for jj in range(23, 34):
            bit = z & 1
            word.append(bit)
            ss += bit
            good &= 3**ss >= 2**jj
            z = T(z)
        words.add(tuple(word))
        direct_good += good
    dp = {14:1}
    for jj in range(23,34):
        nxt=defaultdict(int)
        for ss, w in dp.items():
            for bit in (0,1):
                if 3**(ss+bit) >= 2**jj:
                    nxt[ss+bit] += w
        dp=dict(nxt)
    assert len(words)==2**11 and direct_good==sum(dp.values())==142


def direct_qualified_member(allowed):
    # Construct a 60-bit class with all 38 following steps odd by
    # one-bit lifting. Then find a true CRT phase in the real interval.
    n = B + R22
    q = 0
    for i in range(K-22):
        x = n + (q * 2**22)
        for _ in range(22+i):
            x = T(x)
        if x % 2 == 0:
            q |= 2**i
    residue = (n + q*2**22) % 2**K
    first = residue + ((B-residue + 2**K-1)//2**K)*2**K
    assert first>=B
    qualified = None
    for z in range(first, E, 2**K):
        if z % MOD in allowed:
            qualified=z
            break
    assert qualified is not None
    x, odd = qualified, 0
    for j in range(1,D+1):
        odd += x&1
        x = T(x)
        assert 3**odd >= 2**j
        if j == 22:
            pp=(2*x-1)//3
            assert x%3 == 2 and 0<pp<qualified and T(pp)==x
    assert 3**odd >= 2**D
    return qualified


def main():
    threshold = finite_uniform_gate()
    allowed = inherited_single_root_mask()
    direct_small_word_oracle()
    words = count_safe_suffix_words()
    witness = direct_qualified_member(allowed)
    per_cylinder = (E-B)//2**K + len(allowed)-MOD
    assert per_cylinder == 191
    lower = words*per_cylinder
    assert (lower, OLD_UPPER-lower) == (423090976,330156318951644865)
    print('PASS R3E21-13 research-only finite-language gate')
    print('universal high-base h=1 offset threshold:',threshold)
    print('disjoint slope-safe length-60 words:',words)
    print('guaranteed marginal old survivors per cylinder:',per_cylinder)
    print('full [B,E) guaranteed new exclusion lower:',lower)
    print('conditional new upper:',OLD_UPPER-lower)
    print('direct independent in-interval witness:',witness)
    print('NO frontier, runtime, full first-hit count, or novelty claim')


if __name__=='__main__':
    main()
