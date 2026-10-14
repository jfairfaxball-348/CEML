"""R3E21-5: research-only finite-interval certificate; never a frontier worker.
Run from research/: python r3e21_5_bound.py
Depends on R3E21-4's exact research fixture definitions, not production code.
"""
from r3e21_4_certificates import (
    B, E, J, MOD3, T, reverse_templates, barina_core, prefix,
    extensions, find_merge,
)


def cyclic_max(allowed, length, step):
    """Exact maximum over 729 phase shifts of a cyclic window."""
    if length == 0:
        return 0
    if length == MOD3:
        return sum(allowed)
    assert 0 < length < MOD3
    seq = [int(allowed[(step*i) % MOD3]) for i in range(MOD3)]
    count = sum(seq[:length])
    biggest = count
    for i in range(1, MOD3):
        count += seq[(i+length-1) % MOD3] - seq[i-1]
        biggest = max(biggest, count)
    return biggest


def prepare():
    reverse = reverse_templates()
    barina = barina_core(J)
    assert sum(barina) == 182
    assert sum(barina_core(16)) == 1720
    rows = []
    for r in range(2**J):
        path = prefix(r)
        if path is None or not barina[r]:
            continue
        alive = tuple(t not in reverse and not bool(find_merge(t, path, reverse))
                      for t in range(MOD3))
        rows.append((r, path[-1][1], alive))
    assert len(rows) == 182
    assert sum(extensions(J, s, 58)*sum(alive) for _, s, alive in rows) == 189572393577180314
    return rows


def interval_upper(start, end, k, rows):
    """Proved upper for starts >=B. Full 2^k blocks and at most two edge blocks."""
    assert B <= start <= end and k >= J
    L = 1 << k
    first = (start + L - 1)//L
    last = end//L
    full = max(0, last-first)
    cycles, tail = divmod(full, MOD3)
    complete = 0
    edge_cap = 0
    period = 0
    for _, s, alive in rows:
        weight = extensions(J, s, k)
        a = sum(alive)
        period += weight*a
        edge_cap += weight
        complete += weight*(cycles*a + cyclic_max(alive, tail, L))
    if first > last:  # no full block; possibly two intersecting edge blocks
        edges = min(2, (end+L-1)//L - start//L)
    else:
        edges = int(first*L > start) + int(last*L < end)
    return complete + edges*edge_cap, (full, cycles, tail, complete, edges*edge_cap, period)


def test_small_windows(rows):
    """Independent K16 short-prefix membership oracle for synthetic windows.
    No full Collatz orbits to 1 and no scientific/operational batches.
    """
    k = 16
    live = {r:allowed for r, _, allowed in rows}
    good = [prefix(r, depth=k) is not None for r in range(1<<k)]
    windows = [(B+1, B+14), (B+12345, B+12845),
               (B+9999, B+9999+2**17+17),
               (B+2**17-7, B+5*2**16+123),
               (E-3*2**16-77, E-13)]
    results = []
    for a, b in windows:
        actual = sum(good[n % (1<<k)] and
                     (n % (1<<J)) in live and live[n % (1<<J)][n % MOD3]
                     for n in range(a,b))
        bound, _ = interval_upper(a,b,k,rows)
        assert actual <= bound, (a,b,actual,bound)
        results.append((b-a,actual,bound))
    return results


def main():
    rows = prepare()
    for j in range(1,70):
        weak = [s for s in range(j+1) if 3**s < 2**j]
        if weak:
            s = max(weak)
            assert (3*B+1)**s < 2**j * B**s, (j,s)
    sweep = {k:interval_upper(B,E,k,rows)[0] for k in range(35,70)}
    champion = min(sweep, key=sweep.get)
    assert champion == 62, (champion,sweep[champion])
    cap, data = interval_upper(B,E,62,rows)
    assert data == (131,0,131,422893825289456829,12557603933095494,
                    2282468043343095762), data
    assert cap == 435451429222552323, cap
    assert 568717180731540942-cap == 133265751508988619
    assert cyclic_max((True,)*MOD3,131,1<<62) == 131
    assert cyclic_max((False,)*MOD3,131,1<<62) == 0
    samples = test_small_windows(rows)
    assert [v[1] for v in samples] == [0,5,1648,2436,2459],samples
    print('PASS: K62 high-base and 35..69 depth sweep; 182 CRT prefix cells;')
    print('      K16 Barina 1720; 5 exact synthetic nonaligned windows.')
    print('champion depth:',champion,'upper:',cap,'saving:',568717180731540942-cap)
    print('pieces:',data,'synthetic:',samples)
    print('depths:',sweep)


if __name__ == '__main__':
    main()
