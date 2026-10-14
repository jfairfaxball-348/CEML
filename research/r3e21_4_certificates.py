"""R3E21-4: bounded mathematical sieve certificates. Not a frontier worker."""
from collections import defaultdict
from itertools import product
from fractions import Fraction

B = 2175982616 * 2**40
E = 3 * 10**21
J = 12
K = 58
MOD3 = 729

def T(n):
    return n // 2 if n % 2 == 0 else (3*n + 1) // 2

def reverse_templates():
    table = defaultdict(list)
    count = 0
    for h in range(1, 10):
        for bits in product((0, 1), repeat=h):
            a = sum(bits)
            if not 1 <= a <= 6 or 2**h >= 3**a:
                continue
            offset = 0
            for i, bit in enumerate(bits):
                if bit:
                    offset = 3*offset + 2**i
            residue = offset * pow(2**h, -1, 3**a) % 3**a
            for t in range(residue, MOD3, 3**a):
                table[t].append((h, a, offset, bits))
            count += 1
    assert (count, len(table)) == (179, 335)
    return table

def barina_core(depth):
    """Reconstruct src/sieve.c's slope/q>=1 and equal-(odd count,end) joins."""
    live = [True]
    for k in range(1, depth+1):
        seen = set()
        nxt = []
        for r in range(1 << k):
            x = r
            a = 0
            for _ in range(k):
                a += x & 1
                x = T(x)
            tag = (a, x)
            join = tag in seen
            seen.add(tag)
            slope = 3**a - 2**k
            kill = join or (slope < 0 and slope < r-x)
            nxt.append(live[r % (1 << (k-1))] and not kill)
        live = nxt
    return live

def prefix(r, depth=J):
    x, a, offset = r, 0, 0
    path = []
    for j in range(1, depth+1):
        if x & 1:
            offset = 3*offset + 2**(j-1)
            a += 1
        x = T(x)
        if 3**a < 2**j:
            return None
        path.append((j, a, offset))
    return path

def extensions(j, odd, K):
    row = {odd: 1}
    for d in range(j+1, K+1):
        row = {s:row.get(s,0)+row.get(s-1,0)
               for s in range(d+1) if 3**s >= 2**d}
    return sum(row.values())

def find_merge(t, path, reverse):
    for j, a, offset in path:
        m_res = ((3**a*t+offset) * pow(2**j, -1, MOD3)) % MOD3
        for h, alpha, off2, bits in reverse.get(m_res, ()):
            coefficient = 2**h*3**a - 3**alpha*2**j
            constant = 2**h*offset - 2**j*off2
            # The affine inverse p(T^j(n)) is positive and less than n for all n>=B.
            if (coefficient <= 0 and coefficient*B + constant < 0
                    and 2**h*3**a*B + constant > 0):
                return j, a, offset, h, alpha, off2, bits
    return None

def first_at_least_B(r, t):
    base = r + 2**J * (((t-r)*pow(2**J, -1, MOD3)) % MOD3)
    period = 2**J * MOD3
    return base + max(0, (B-base+period-1)//period)*period

def check():
    reverse = reverse_templates()
    barina = barina_core(J)
    assert sum(barina) == 182
    assert sum(barina_core(16)) == 1720
    # Independent high-floor replacement, all slopes at all depths <=K.
    for j in range(1, K+1):
        weak = [a for a in range(j+1) if 3**a < 2**j]
        if weak:
            a = max(weak)
            assert (3*B+1)**a < (2**j)*(B**a), (j,a)
    reverse_rest = [t for t in range(MOD3) if t not in reverse]
    assert len(reverse_rest) == 394
    groups = defaultdict(int)
    witness_checks = 0
    for r in range(1 << J):
        path = prefix(r)
        if path is None:
            continue
        for t in reverse_rest:
            merge = find_merge(t, path, reverse)
            groups[(path[-1][1], bool(barina[r]), bool(merge))] += 1
            if merge is not None and witness_checks < 200:
                n = first_at_least_B(r,t)
                j,a,offset,h,alpha,off2,bits = merge
                m = n
                for _ in range(j):
                    m = T(m)
                assert (2**j)*m == 3**a*n+offset
                assert m % (3**alpha) == off2*pow(2**h,-1,3**alpha)%(3**alpha)
                p = (2**h*m-off2)//(3**alpha)
                assert 0 < p < n
                for bit in bits:
                    assert p & 1 == bit
                    p = T(p)
                assert p == m
                witness_checks += 1
    assert witness_checks == 200
    assert sum(v for v in groups.values()) == 226*394
    counts = {}
    for depth in (35,58):
        baseline = sum(extensions(J,s,depth)*count for (s,_,_),count in groups.items())
        combined = sum(extensions(J,s,depth)*count for (s,barina_live,mixed),count in groups.items()
                       if barina_live and not mixed)
        expected_baseline = {35:103953502538,58:242542007249756164}[depth]
        expected_combined = {35:79744060642,58:189572393577180314}[depth]
        assert (baseline,combined) == (expected_baseline,expected_combined)
        period = 2**depth * MOD3
        q,rem = divmod(E-B,period)
        counts[depth] = {'baseline_period_survivors':baseline,
            'combined_period_survivors':combined,
            'period':period,'full_periods':q,'trailing_length':rem,
            'combined_period_fraction':str(Fraction(combined,period)),
            'finite_lower':q*combined,'finite_upper':(q+1)*combined}
    assert counts[58]['finite_upper'] == 568717180731540942
    print('PASS: 179 reverse templates; 335/729 classes; Barina k16 1720;')
    print('      K58 high-base theorem; 200 exact mixed trajectory witnesses;')
    print('      CRT/group aggregation; combined K35/K58 counts.')
    print('residual groups:',sorted(groups.items()))
    for depth,c in counts.items():
        print(depth,c)

if __name__ == '__main__':
    check()
