"""R3E21-6 research-only exact arithmetic bound. NEVER a production frontier worker.

Run from repository root: python research/r3e21_6_adaptive.py
Uses only the frozen R3E21-4 mathematical fixture (not production tools).
"""
from functools import lru_cache
from r3e21_4_certificates import (
    B, E, J, MOD3, T, barina_core, prefix, reverse_templates, find_merge,
)

OLD_BOUND = 435451429222552323
NEW_BOUND = 342723929836590155
MAX_DEPTH = 79


def rows():
    reverse = reverse_templates()
    barina = barina_core(J)
    assert sum(barina) == 182
    result = []
    for r in range(1 << J):
        path = prefix(r)
        if path is None or not barina[r]:
            continue
        allowed = tuple(t not in reverse and not bool(find_merge(t, path, reverse))
                        for t in range(MOD3))
        result.append((r, path[-1][1], allowed))
    assert len(result) == 182
    return result


@lru_cache(maxsize=None)
def cyclic_max(allowed, depth, length):
    """Exact maximum over the 729 CRT phases for consecutive steps 2**depth."""
    assert 0 <= length < MOD3
    if not length:
        return 0
    delta = pow(2, depth, MOD3)
    sequence = [int(allowed[(i * delta) % MOD3]) for i in range(MOD3)]
    current = sum(sequence[:length])
    best = current
    for i in range(1, MOD3):
        current += sequence[(i + length - 1) % MOD3] - sequence[i - 1]
        best = max(best, current)
    return best


def cap(allowed, depth, width):
    """Upper for a single unknown numerical 2**depth cylinder in width=E-S."""
    count = (width + (1 << depth) - 1) // (1 << depth)
    whole, remainder = divmod(count, MOD3)
    return whole * sum(allowed) + cyclic_max(allowed, depth, remainder)


def adaptive_bound(start, end, maximum_depth=MAX_DEPTH, data=None):
    """Rigorous [start,end) upper from exact ternary-filter masks and parity DP.

    Key: for a prefix cylinder with parity odd-count s at depth d,
    either stop (count at most cap), or split its two disjoint binary
    extensions and drop an extension if 3**(s+e)<2**(d+1).
    No unknown mod729 phase is treated as an independent probability.
    """
    assert B <= start <= end and maximum_depth >= J
    width = end - start
    data = rows() if data is None else data
    answer = 0
    for _, initial_odd, allowed in data:
        @lru_cache(maxsize=None)
        def visit(depth, odd):
            direct = cap(allowed, depth, width)
            if depth == maximum_depth:
                return direct
            children = sum(visit(depth + 1, odd + bit) for bit in (0, 1)
                           if 3 ** (odd + bit) >= 2 ** (depth + 1))
            return min(direct, children)
        answer += visit(J, initial_odd)
    return answer


def check_high_base():
    for depth in range(1, MAX_DEPTH + 1):
        weak = [odd for odd in range(depth + 1) if 3 ** odd < 2 ** depth]
        if weak:
            odd = max(weak)
            assert (3 * B + 1) ** odd < 2 ** depth * B ** odd


def independent_oracle(start, end, k, data):
    """Small bounded direct-orbit-prefix predicate, NOT trajectories to 1."""
    masks = {r: allowed for r, _, allowed in data}
    barina16 = barina_core(16)
    count = barina_count = mod9_count = barina_mod9_count = 0
    for n in range(start, end):
        k16 = barina16[n % (1 << 16)]
        mod9 = n % 9 not in (2, 4, 5, 8)
        barina_count += int(k16)
        mod9_count += int(mod9)
        barina_mod9_count += int(k16 and mod9)
        r = n % (1 << J)
        alive = (r in masks and masks[r][n % MOD3]
                 and prefix(n % (1 << k), depth=k) is not None)
        count += int(alive)
    return count, barina_count, mod9_count, barina_mod9_count


def check():
    data = rows()
    check_high_base()
    assert sum(sum(u) for _, _, u in data) > 0
    result = adaptive_bound(B, E, MAX_DEPTH, data)
    assert result == NEW_BOUND, result
    assert OLD_BOUND - result == 92727499385962168
    for depth, expected in ((62, 415260975758799476),
                            (65, 355387192082135541),
                            (67, 350643238506944522),
                            (72, NEW_BOUND), (79, NEW_BOUND)):
        assert adaptive_bound(B, E, depth, data) == expected
    windows = [
        (B + 1, B + 14, (0, 0, 8, 0)),
        (B + 12345, B + 12845, (5, 13, 277, 5)),
        (B + 9999, B + 9999 + 2 ** 17 + 17, (1648, 3441, 72827, 1908)),
        (B + 2 ** 17 - 7, B + 5 * 2 ** 16 + 123, (2436, 5169, 109299, 2848)),
        (E - 3 * 2 ** 16 - 77, E - 13, (2459, 5162, 109262, 2862)),
    ]
    for start, end, expected in windows:
        got = independent_oracle(start, end, 16, data)
        assert got == expected, (start, end, got, expected)
        bound = adaptive_bound(start, end, 16, data)
        assert got[0] <= bound, (start, end, got, bound)
    print('PASS R3E21-6: 182 surviving low-12 classes, high-base through 79,')
    print('  adaptive DP depths 62/65/67/72/79, five direct independent K16 windows,')
    print('  matching Barina simple-core and Angeltveit mod9-only subset windows.')
    print('interval:', B, E, 'upper:', result, 'saving:', OLD_BOUND-result)


if __name__ == '__main__':
    check()
