"""R3E21-12: bounded *research-only* synchronising-inverse witness oracle.

NOT a frontier runner, a source-equivalent competitor, or a global count.
"""
from collections import Counter, defaultdict
from itertools import product

B = 2175982616 * 2**40
E = 3 * 10**21
J, MOD = 12, 729
WINDOW = 350_000


def T(n):
    return n // 2 if n % 2 == 0 else (3*n + 1) // 2


def reverse_templates():
    out = defaultdict(list)
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
                out[t].append((h, a, c))
            count += 1
    assert (count, len(out)) == (179, 335)
    return out


def barina_simple(depth):
    live = [True]
    for j in range(1, depth+1):
        seen, nxt = set(), []
        for r in range(1 << j):
            x, a = r, 0
            for _ in range(j):
                a += x & 1
                x = T(x)
            tag = (a, x)
            killed = tag in seen or (3**a < 2**j and 3**a - 2**j < r - x)
            seen.add(tag)
            nxt.append(live[r % (1 << (j-1))] and not killed)
        live = nxt
    return live


def inherited_masks():
    """Reconstruct R3E21-4's limited J=12 predicate, NOT enhanced fsieve."""
    reverse = reverse_templates()
    simple = barina_simple(J)
    assert sum(simple) == 182
    masks = {}
    for r in range(1 << J):
        if not simple[r]:
            continue
        x, a, c, path = r, 0, 0, []
        for j in range(1, J+1):
            if x & 1:
                a += 1
                c = 3*c + 2**(j-1)
            x = T(x)
            if 3**a < 2**j:
                break
            path.append((j, a, c))
        if len(path) != J:
            continue
        allowed = set()
        for t in range(MOD):
            if t in reverse:
                continue
            merges = False
            for j, a, c in path:
                yres = (3**a*t + c) * pow(2**j, -1, MOD) % MOD
                for h, alpha, d in reverse.get(yres, ()):
                    coeff = 2**h*3**a - 3**alpha*2**j
                    const = 2**h*c - 2**j*d
                    if (coeff <= 0 and coeff*B+const < 0
                            and 2**h*3**a*B+const > 0):
                        merges = True
                        break
                if merges:
                    break
            if not merges:
                allowed.add(t)
        masks[r] = allowed
    assert len(masks) == 182
    assert sum(bool(v) for v in masks.values()) == 144
    assert sorted(set(map(len, masks.values()))) == [0, 394]
    return masks


def prefix72_admissible(n):
    x, odds = n, 0
    for j in range(1, 73):
        odds += x & 1
        x = T(x)
        if 3**odds < 2**j:
            return False
    return True


def synchronising_one_step(n, max_depth=72):
    """First uniform h=1 inverse cylinder *after* J, or None.

    3^s*n + c = 2^j*T^j(n). s>=1 makes the image mod 3
    independent of the starting integer's 3-adic residue.
    """
    x, s, c = n, 0, 0
    for j in range(1, max_depth+1):
        if x & 1:
            s += 1
            c = 3*c + 2**(j-1)
        x = T(x)
        if j <= J or not s:
            continue
        if (c * pow(2**j, -1, 3)) % 3 != 2:
            continue
        if 2*3**s >= 3*2**j:
            continue
        if (2*3**s-3*2**j)*B + 2*c - 2**j >= 0:
            continue
        assert x % 3 == 2
        p = (2*x-1)//3
        assert 0 < p < n and T(p) == x
        return j, s, c, p, x
    return None


def first_crt_at_or_above(r, t, d, low):
    base = r + 2**d * (((t-r) * pow(2**d, -1, MOD)) % MOD)
    period = 2**d * MOD
    return base + max(0, (low-base+period-1)//period)*period


def check():
    masks = inherited_masks()
    n = B + 6395
    assert n < E and n % MOD in masks[n % (1 << J)]
    assert prefix72_admissible(n)
    j, s, c, p, y = synchronising_one_step(n, 32)
    assert (j, s, c, p, y) == (22, 14, 10360925,
        1818869960429518459647, 2728304940644277689471)
    assert n % 2**j == 6395
    assert 2**j*y == 3**s*n+c
    # Direct lifts check arithmetic; universal validity is proved algebraically.
    for q in range(32):
        m = n + 2**j*q
        yy = m
        for _ in range(j):
            yy = T(yy)
        pp = (2*yy-1)//3
        assert yy == y + 3**s*q
        assert 0 < pp < m and T(pp) == yy
    # CRT shows independent finite parity and 3-adic specifications coexist.
    h = 16
    t = min(masks[(1<<J)-1])
    odd_prefix = first_crt_at_or_above((1<<h)-1, t, h, B)
    x = odd_prefix
    for _ in range(h):
        assert x % 2 == 1
        x = T(x)
    assert x > odd_prefix and odd_prefix % MOD == t
    # Finite local truth-gate ONLY. No extrapolation to the whole interval.
    old = extra = extra24 = extra32 = 0
    firsts = Counter()
    for m in range(B, B+WINDOW):
        if m % MOD not in masks.get(m % (1<<J), ()):
            continue
        if not prefix72_admissible(m):
            continue
        old += 1
        result = synchronising_one_step(m)
        if result:
            d = result[0]
            extra += 1
            extra24 += d <= 24
            extra32 += d <= 32
            firsts[d] += 1
    assert (old, extra, extra24, extra32) == (141, 25, 5, 8)
    print('PASS R3E21-12 research-only exact arithmetic')
    print('old-predicate survivors in bounded [B,B+350000):', old)
    print('new uniform h=1 certificate witnesses:', extra,
          '(at j<=24:', extra24, '; at j<=32:', extra32, ')')
    print('independently verified whole-cylinder witness: n=B+6395, j=22, s=14')
    print('first-depth histogram:', sorted(firsts.items()))
    print('NO global bound, runtime, novelty or frontier claim')


if __name__ == '__main__':
    check()
