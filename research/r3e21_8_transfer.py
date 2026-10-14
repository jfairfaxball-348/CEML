"""R3E21-8: rigorous research-only phase/correlation transfer; never a worker.
Run: python research/r3e21_8_transfer.py. Standard-library exact integers only.
The root/predecessor reconstruction is deliberately independent of old fixture imports.
"""
from collections import defaultdict
from functools import lru_cache
from itertools import product

B = 2175982616 * 2**40
E = 3 * 10**21
M, J, D = 729, 12, 72
PRIOR = 342723929836534896
EXPECTED = 334199143141062522


def T(x):
    return x // 2 if x % 2 == 0 else (3*x+1)//2


def reverse_templates():
    table = defaultdict(list)
    for h in range(1, 10):
        for bits in product((0, 1), repeat=h):
            a = sum(bits)
            if not 1 <= a <= 6 or 2**h >= 3**a:
                continue
            off = 0
            for i, bit in enumerate(bits):
                if bit:
                    off = 3*off + 2**i
            r = off * pow(2**h, -1, 3**a) % 3**a
            for t in range(r, M, 3**a):
                table[t].append((h, a, off))
    assert len(table) == 335
    return table


def barina_core(depth):
    live = [True]
    for k in range(1, depth+1):
        seen, following = set(), []
        for r in range(1 << k):
            x, s = r, 0
            for _ in range(k):
                s += x & 1
                x = T(x)
            tag = (s, x)
            join = tag in seen
            seen.add(tag)
            slope = 3**s - 2**k
            following.append(live[r % (1 << (k-1))]
                             and not (join or (slope < 0 and slope < r-x)))
        live = following
    return live


def path(r):
    x, s, off = r, 0, 0
    steps = []
    for j in range(1, J+1):
        if x & 1:
            s += 1
            off = 3*off + 2**(j-1)
        x = T(x)
        if 3**s < 2**j:
            return None
        steps.append((j, s, off))
    return steps


def mixed_exclusion(t, steps, rev):
    for j, a, off in steps:
        target = (3**a*t+off)*pow(2**j, -1, M) % M
        for h, alpha, back_off in rev.get(target, ()):
            coeff = 2**h*3**a - 3**alpha*2**j
            constant = 2**h*off-2**j*back_off
            if (coeff <= 0 and coeff*B+constant < 0
                    and 2**h*3**a*B+constant > 0):
                return True
    return False


def roots_and_mask():
    reverse = reverse_templates()
    barina = barina_core(J)
    allowed = tuple(t not in reverse for t in range(M))
    residue = [i for i in range(M) if allowed[i]]
    assert (sum(barina), sum(allowed)) == (182, 394)
    active, empty = [], 0
    for r in range(1 << J):
        steps = path(r)
        if steps is None or not barina[r]:
            continue
        survivors = sum(not mixed_exclusion(t, steps, reverse) for t in residue)
        assert survivors in (0, 394), (r, survivors)
        if survivors:
            active.append((r, steps[-1][1]))
        else:
            empty += 1
    assert (len(active), empty) == (144, 38)
    return active, allowed


class Transfer:
    def __init__(self, mask, end_depth=D):
        self.mask = tuple(bool(t) for t in mask)
        self.k = sum(mask)
        self.depth = end_depth
        self.inverse = [pow(2**d, -1, M) for d in range(end_depth+1)]
        self.step = [pow(2, d, M) for d in range(end_depth+1)]
        self.accum = []
        for u in self.step:
            seq = [int(self.mask[(i*u) % M]) for i in range(M)]
            prefix = [0]
            for value in seq + seq:
                prefix.append(prefix[-1]+value)
            self.accum.append(prefix)

        @lru_cache(maxsize=None)
        def transfer(d, s, N, t):
            # N consecutive cylinder members, first residue t (mod 729).
            if N <= 0 or 3**s < 2**d:
                return 0
            immediate = self.exact(d, N, t)
            if immediate == 0 or N == 1 or d == self.depth:
                return immediate
            a, b = (N+1)//2, N//2
            t1 = (t+self.step[d]) % M
            # First-index next parity is unknown from (d,s,N,t).
            # Two possible orientations; the same one applies to both children.
            left_even = transfer(d+1,s,a,t)
            right_odd = transfer(d+1,s+1,b,t1)
            left_odd = transfer(d+1,s+1,a,t)
            right_even = transfer(d+1,s,b,t1)
            return min(immediate, max(left_even+right_odd, left_odd+right_even))
        self.transfer = transfer

    def exact(self, d, N, phase):
        if N <= 0:
            return 0
        cycles, tail = divmod(N, M)
        index = (phase % M)*self.inverse[d] % M
        c = self.accum[d]
        return cycles*self.k + c[index+tail] - c[index]

    def oriented(self, d, s, first, N, known_levels):
        if N <= 0 or 3**s < 2**d:
            return 0
        direct = self.exact(d,N,first % M)
        if not direct or N == 1 or d == self.depth or known_levels == 0:
            return min(direct,self.transfer(d,s,N,first % M))
        iterate = first
        for _ in range(d):
            iterate = T(iterate)
        next_parity = iterate & 1
        even_length, odd_length = (N+1)//2, N//2
        children = (self.oriented(d+1,s+next_parity,first,even_length,known_levels-1)
                    + self.oriented(d+1,s+1-next_parity,first+(1<<d),odd_length,known_levels-1))
        return min(direct,children)


def span(start, end, j, r):
    stride = 1 << j
    a = (start-r+stride-1)//stride
    b = (end-r+stride-1)//stride
    return r + a*stride, max(0,b-a)


def prefix_survivor(n, maximum):
    odd = 0
    for j in range(1,maximum+1):
        odd += n&1
        n = T(n)
        if 3**odd < 2**j:
            return False
    return True


def independent_fixtures(active, mask):
    masks = (mask, (False,)*M, (True,)*M,
             tuple(i%9 in (0,1,3,6,7) for i in range(M)))
    phases = (-994, -1, 0, 1, 91, 728, 729)
    cases = 0
    for m in masks:
        alg = Transfer(m, 20)
        for d in (0,1,4,12,20):
            for N in (0,1,13,728,729,730,1483):
                for phase in phases:
                    direct = sum(m[(phase+(1<<d)*i)%M] for i in range(N))
                    assert alg.exact(d,N,phase)==direct, (d,N,phase)
                    cases += 1
    assert cases == 980
    # Independent signed endpoint/ceiling oracle, including 2**j >> width.
    interval_cases = 0
    for start in (-43, 0, B+1, B+999, E-111):
        for width in (0, 1, 13, 117, 1511):
            for depth in (1, 4, 12, 20, 79):
                L = 1 << depth
                for r in (0, 1, L//2, L-1):
                    first, N = span(start, start+width, depth, r)
                    for m in masks:
                        got = Transfer(m,79).exact(depth,N,first%M)
                        direct = sum(n%L==r and m[n%M]
                                     for n in range(start,start+width))
                        assert got == direct, (start,width,depth,r)
                        interval_cases += 1
    assert interval_cases == 2000
    # Same (depth,odd-count,residue mod729), opposing next-step orientation.
    witnesses = []
    for v in (91,3007):
        x,s=v,0
        for j in range(1,14):
            s+=x&1
            x=T(x)
            assert 3**s >= 2**j
        witnesses.append((s,v%M,x&1))
    assert witnesses == [(10,91,0),(10,91,1)]
    for j in range(1,80):
        weak = [s for s in range(j+1) if 3**s < 2**j]
        if weak:
            s = max(weak)
            assert (3*B+1)**s < 2**j * B**s
    # Separate direct per-integer parity oracle; no Collatz-to-one execution.
    transfer = Transfer(mask,20)
    windows = [(B+1,B+14), (B+12345,B+12845),
               (B+9999,B+9999+(1<<17)+17),
               (E-3*(1<<16)-77,E-13)]
    trial = 0
    for start,end in windows:
        truth,majorant = 0,0
        for r,s in active:
            first,N = span(start,end,J,r)
            if N==0:continue
            truth += sum(mask[n%M] and prefix_survivor(n,20)
                         for n in range(first,end,1<<J))
            majorant += transfer.transfer(J,s,N,first%M)
            trial += N
        assert truth <= majorant, (start,end,truth,majorant)
    assert trial > 0
    return cases,interval_cases,trial


def run():
    active,mask = roots_and_mask()
    cases,endpoints,checked = independent_fixtures(active,mask)
    transfer = Transfer(mask)
    exact_phase = 0
    oriented8 = 0
    for r,s in active:
        first,N = span(B,E,J,r)
        exact_phase += transfer.transfer(J,s,N,first%M)
        oriented8 += transfer.oriented(J,s,first,N,8)
    assert exact_phase == 334199143141076940,exact_phase
    assert oriented8 == EXPECTED,oriented8
    assert 0 <= oriented8 <= exact_phase < PRIOR
    print('PASS R3E21-8: 144 phase roots, 394/729 mask, 79 high-base depths')
    print('phase CRT oracles:',cases, 'signed endpoint oracles:',endpoints,
          'direct high-n shortened-prefix test points:',checked)
    print('phase transfer:',exact_phase,'8-level orientation:',oriented8)
    print('old conservative upper:',PRIOR,'new upper:',oriented8)
    print('certified upper reduction:',PRIOR-oriented8)
    print('cache:',transfer.transfer.cache_info())


if __name__ == '__main__':
    run()
