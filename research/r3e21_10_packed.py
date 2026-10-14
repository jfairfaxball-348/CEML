"""R3E21-10: exact packed cyclic three-bit carry transfer (research only).

Run from repository root:
    python research/r3e21_10_packed.py

No scientific Collatz batches or operational workers are run. This fixture
does independent finite arithmetic/orbit-prefix tests, not full trajectories.
"""
from functools import lru_cache
from r3e21_9_carry import (
    B, E, M, J, D, T, CoherentTransfer, Transfer, span,
    roots_and_mask, independent_fixtures, packet_oracles,
)

OLD_UPPER = 333316047378995972
THREE_BIT_PHASE = 333056528710095310
THREE_BIT_ORIENTED8 = 330670142619755865
THREE_BIT_ORIENTED10 = 330156319374735841


def profiles(k):
    """Prefix odd counts for the first k shortened steps, indexed by mod 2**k."""
    result = []
    for residue in range(1 << k):
        x, odd, path = residue, 0, []
        for _ in range(k):
            odd += x & 1
            path.append(odd)
            x = T(x)
        result.append(tuple(path))
    return result


def packed_transfer(base, k=3):
    """Exact integer cyclic convolution for all compatible packet orientations.

    Per state: O((k+1)*2**k) recursive child requests and output digit
    extractions, plus (k+1) arbitrary-precision polynomial multiplications.
    No 2**k-by-2**k orientation/child table is traversed.
    """
    size = 1 << k
    words = profiles(k)

    @lru_cache(maxsize=None)
    def bound(d, s, N, t):
        if N <= 0 or 3**s < 2**d:
            return 0
        direct = base.exact(d, N, t)
        if direct == 0 or N == 1 or d == base.depth:
            return direct
        if d + k > base.depth:
            # Sound previously certified two-bit transfer at the boundary.
            return base.pair(d, s, N, t)

        bits = direct.bit_length() + 1
        radix_mask = (1 << bits) - 1
        g = pow(3, s, size)
        child_phases = [(t + i*base.step[d]) % M for i in range(size)]
        child_sizes = [(N + size - 1 - i)//size for i in range(size)]
        values = [0]*size

        # For an admissible length-k parity residue r, odd count a is the
        # sole child-summary parameter. The numerical index i contributes
        # a child with (N_i,t_i) and true residue r=y+3**s*i (mod 2**k).
        for a in range(k+1):
            admissible = [
                r for r, path in enumerate(words)
                if path[-1] == a
                and all(3**(s+v) >= 2**(d+j)
                        for j, v in enumerate(path, 1))
            ]
            if not admissible:
                continue

            # B_a(X) = sum_{r admissible} X**r.
            selector = sum(1 << (r*bits) for r in admissible)

            # A_a(X) = sum_i bound(child_i,s+a)*X**(-g*i mod size).
            # This index reversal makes A_a*B_a a cyclic correlation in y.
            weights = 0
            for i, Ni in enumerate(child_sizes):
                if Ni:
                    child_value = bound(d+k, s+a, Ni, child_phases[i])
                    weights += child_value << (((-g*i) % size)*bits)

            product = weights*selector
            for y in range(size):
                # Coefficient extraction is exact: each coefficient is
                # bounded by the parent direct CRT count < 2**bits.
                values[y] += (product >> (y*bits)) & radix_mask
                if y < size-1:
                    values[y] += (product >> ((y+size)*bits)) & radix_mask

        assert max(values) <= direct, (d,s,N,t,max(values),direct)
        return min(direct, max(values))

    return bound


def direct_three_bit(base):
    """Independent quadratic reference oracle, only used on small states."""
    words = profiles(3)

    @lru_cache(maxsize=None)
    def slow(d,s,N,t):
        if N <= 0 or 3**s < 2**d:
            return 0
        direct = base.exact(d,N,t)
        if not direct or N == 1 or d == base.depth:
            return direct
        if d+3 > base.depth:
            return base.pair(d,s,N,t)
        sizes = [(N+7-i)//8 for i in range(8)]
        phases = [(t+i*base.step[d])%M for i in range(8)]
        g = pow(3,s,8)
        best = 0
        for y in range(8):
            sub = 0
            for i,Ni in enumerate(sizes):
                if not Ni: continue
                word = words[(y+g*i)%8]
                if all(3**(s+v)>=2**(d+j) for j,v in enumerate(word,1)):
                    sub += slow(d+3,s+word[-1],Ni,phases[i])
            best = max(best,sub)
        return min(direct,best)

    return slow


def actual_orientation(base, upper, d, s, first, N, known, iterate, powers):
    """Real d-step iterate passed down rather than recomputed for every child."""
    if N <= 0 or 3**s < 2**d:
        return 0
    direct = base.exact(d,N,first%M)
    if not direct or N == 1 or d == base.depth or known == 0:
        return min(direct,upper(d,s,N,first%M))
    e = iterate & 1
    a,b = (N+1)//2,N//2
    left = actual_orientation(base,upper,d+1,s+e,first,a,
                              known-1,T(iterate),powers)
    right = 0
    if b:
        right = actual_orientation(base,upper,d+1,s+1-e,
                                   first+(1<<d),b,known-1,
                                   T(iterate+powers[s]),powers)
    return min(direct,left+right)


def actual_roots(base, upper, active, known):
    total = 0
    powers = [3**s for s in range(D+1)]
    for r,s in active:
        first,N = span(B,E,J,r)
        y = first
        for _ in range(J):
            y = T(y)
        total += actual_orientation(base,upper,J,s,first,N,known,y,powers)
    return total


def independent_synthetic(active,mask):
    test_base = CoherentTransfer(mask,20)
    packed = packed_transfer(test_base)
    direct = direct_three_bit(test_base)
    tests = 0
    for d in (0,1,3,12,13,17,19):
        for s in range(d+1):
            for N in range(19):
                for t in (0,1,2,91,728):
                    assert packed(d,s,N,t) == direct(d,s,N,t), (d,s,N,t)
                    tests += 1
    assert tests == 6840

    # Separate numerical shortened-trajectory prefix test, no orbits to 1.
    def prefix_true(n):
        x,odd = n,0
        for j in range(1,21):
            odd += x&1
            x = T(x)
            if 3**odd < 2**j:
                return False
        return True

    windows = ((B+1,B+14), (B+12345,B+12845),
               (B+9999,B+9999+(1<<17)+17),
               (E-3*(1<<16)-77,E-13))
    total_points = truth = upper_plain = upper_known = 0
    for start,end in windows:
        for r,s in active:
            first,N = span(start,end,J,r)
            upper_plain += packed(J,s,N,first%M)
            if N:
                y = first
                for _ in range(J):
                    y=T(y)
                upper_known += actual_orientation(
                    test_base,packed,J,s,first,N,8,y,[3**v for v in range(21)]
                )
                truth += sum(mask[n%M] and prefix_true(n)
                             for n in range(first,end,1<<J))
            total_points += N
    assert (tests,total_points,truth,upper_plain,upper_known) == (
        6840,11539,3394,4556,3958
    ),(tests,total_points,truth,upper_plain,upper_known)
    assert truth <= upper_known <= upper_plain
    return tests,total_points,truth,upper_plain,upper_known


def run():
    active,mask = roots_and_mask()
    assert (len(active),sum(mask)) == (144,394)
    # Cross-check original fixtures; their independent signed interval,
    # q=0/q>=1, mixed-depth and high-base reverse/CRT checks are retained.
    assert independent_fixtures(active,mask) == (980,2000,11539)
    assert packet_oracles() == 960
    synthetic=independent_synthetic(active,mask)
    baseline = CoherentTransfer(mask)
    old = sum(baseline.oriented_pair(J,s,*span(B,E,J,r),8)
              for r,s in active)
    assert old == OLD_UPPER

    # The packed upper and real root orientations use exact integers.
    base = CoherentTransfer(mask)
    triple = packed_transfer(base)
    phase = sum(triple(J,s,span(B,E,J,r)[1],span(B,E,J,r)[0]%M)
                for r,s in active)
    known8 = actual_roots(base,triple,active,8)
    known10 = actual_roots(base,triple,active,10)
    assert (phase,known8,known10) == (
        THREE_BIT_PHASE, THREE_BIT_ORIENTED8, THREE_BIT_ORIENTED10
    ),(phase,known8,known10)
    assert known10 <= known8 <= phase
    print("PASS R3E21-10 conditional [B,E) exact-arithmetic bound")
    print("144 roots; U=394/729; inherited tests 980/2000/11539; "
          "packet oracles 960")
    print("synthetic tests (states,points,truth,Q3,K8):",synthetic)
    print("R3E21-9 previous upper:",old)
    print("R3E21-10 three-bit:",phase,"three-bit K8:",known8)
    print("R3E21-10 three-bit K10:",known10)
    print("upper-bound reduction:",old-known10)
    print("packed-cache:",triple.cache_info())


if __name__ == "__main__":
    run()
