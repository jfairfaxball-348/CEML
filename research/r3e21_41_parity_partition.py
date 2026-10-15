#!/usr/bin/env python3
"""R41 exact f=43, odd incoming-q source-search1 root partition.
Research-only proof-object; NOT frontier science or a production bitmap certificate.
"""
from collections import Counter, defaultdict
from hashlib import sha256
from math import comb
import r3e21_40_source_reachable_cylinder as r40

L, LOW, B, E = r40.L, r40.LOW, r40.B, r40.E
F, CUTOFF = 43, 659

def eligible_abs(i, f, run, predecessor=True):
    return 306*i < 485*f and not (
        predecessor and run >= 2 and run%2 == 0 and 306*(i-1) >= 485*(f-1))

def automaton(rational=True, predecessor=True, doubleeven=True):
    """Exact 2-adic parity-word count with the literal source flag transition."""
    states = {(2, 0, 0): 1}  # (odd count, doubleeven flag, trailing even run)
    for i in range(2, 67):
        following = defaultdict(int)
        terminal = defaultdict(int)
        for (f, flag, run), c in states.items():
            if rational and 306*i >= 485*f:
                continue
            if predecessor and run >= 2 and run%2 == 0 and 306*(i-1) >= 485*(f-1):
                continue
            if i == 66:
                terminal[(f, flag, run)] += c
                continue
            # The free new root bit bijectively chooses the next T parity.
            odd_flag = ((flag | int(306*(i+1)>=485*f)) & ~2) if doubleeven else 0
            following[(f+1, odd_flag, 0)] += c
            if not doubleeven or flag < 2:
                following[(f, (flag<<1) if doubleeven else 0, run+1)] += c
        if i == 66:
            return (sum(terminal.values()),
                    sum(c for (f,_,q),c in terminal.items() if f==F and q%2==1))
        states = following
    raise AssertionError("no terminal")

def prefix_gate_lemma():
    # Checked as integers, never as logs/floats; bounded to EXACT source i<=66.
    assert 3**306 < 2**485
    pairs = 0
    for i in range(2,67):
        for f in range(2,i+1):
            if 306*i < 485*f:
                assert 3**f > 2**i, (i,f)
                pairs += 1
    assert pairs == 848
    return pairs

def literal_witness(n, number, a, run):
    """Exact original-start T, first descent through 2000, mod3 predecessor."""
    z, odds, q, first, predecessor = n, 0, 0, None, False
    for k in range(1,91):
        if k<=66:
            odds += z&1
        q = 0 if z&1 else q+1
        z = r40.T(z)
        if z<n and first is None:
            first = k
        if k==66:
            assert odds==43 and q==run and z==number+a*r40.POW[43]-1
        if 67<=k<=90 and z%3==2:
            p = (2*z-1)//3
            if 0<p<n:
                predecessor=True
    if first is None:
        for k in range(91,2001):
            z = r40.T(z)
            if z<n:
                first=k
                break
    return first, predecessor

def cylinder():
    """Four disjoint 2^16-root classes; each remains below fail-closed caps."""
    sums=Counter()
    flagged=[]; admitted=[]; steps=Counter(); bands=[]
    for band in range(4):
        c=Counter()
        for j in range(band*(1<<16),(band+1)*(1<<16)):
            r=LOW+(j<<48)
            state=(2,3,2,9,0,0)
            while True:
                i,base,f,number,flag,run=state
                if not eligible_abs(i,f,run):
                    break
                # Proven independently by the exact 848-case integer lemma.
                assert number>base
                if i==66:
                    if f==43 and run%2:
                        c['roots']+=1
                        amin=max(0,(B-r+L-1)//L)
                        amax=min(63,(E-1-r)//L)
                        for a in range(amin,amax+1):
                            n=r+a*L
                            assert B<=n<E
                            c['interval']+=1
                            if not r40.gate(n,number,f,flag,a):
                                continue
                            c['admitted']+=1
                            admitted.append(n)
                            x=number+a*r40.POW[43]-1
                            word,s0=r40.original_word_score(x,0)
                            word1,s1=r40.original_word_score(x,run%2)
                            assert word==word1
                            if s0>CUTOFF:
                                c['source_clear']+=1
                                if s1<=CUTOFF:
                                    c['false_clear']+=1
                                    flagged.append(n)
                                    assert s0==791 and word&3==0
                            else:
                                c['source_live']+=1
                                if s1>CUTOFF:
                                    c['inverse']+=1
                            k,pred=literal_witness(n,number,a,run)
                            if k is None:
                                c['no_descent_through2000']+=1
                            else:
                                c['direct_descent']+=1
                                steps[k]+=1
                                if k<=90:c['direct_le90']+=1
                                else:c['direct_gt90']+=1
                            if pred:c['smaller_predecessor_67_90']+=1
                    break
                nxt=r40.source_child(*state,(r>>i)&1)
                if nxt is None:
                    break
                state=nxt
            c['tested_roots']+=1
        assert c['tested_roots']==1<<16 and c['admitted']<250000
        assert c['tested_roots']+c['interval']+c['admitted']<5000000
        bands.append(c);sums.update(c)
    h=sha256(('\n'.join(map(str,sorted(flagged)))+'\n').encode()).hexdigest()
    ah=sha256(('\n'.join(map(str,sorted(admitted)))+'\n').encode()).hexdigest()
    assert h==r40.EXPECTED_DIGEST and len(flagged)==167
    assert (sums['roots'],sums['interval'],sums['admitted'])==(12401,102090,54438)
    assert (sums['source_clear'],sums['false_clear'],sums['inverse'])==(49191,167,0)
    assert (sums['direct_descent'],sums['direct_le90'],sums['direct_gt90'],
            sums['no_descent_through2000'])==(54438,47406,7032,0)
    assert max(steps)==349 and sum(steps.values())==54438
    assert ah=='7edb1e7df2015e373d4bfc02dd120b7e645e543f2c880f3120194ccfeeecb761'
    return sums,bands,h,ah,steps

def main():
    pairs=prefix_gate_lemma()
    base,raw=automaton(False,False,False)
    assert base==1<<64
    assert raw==sum(comb(63-q,40) for q in range(1,24,2))==39001983984117856
    _,rational=automaton(True,False,False)
    _,pred=automaton(True,True,False)
    _,exact=automaton(True,True,True)
    assert (rational,pred,exact)==(9398852100800112,7645997023219688,6438209236755220)
    c,bands,h,ah,steps=cylinder()
    untouched=exact-c['roots']
    parts=(3*(1<<64),(1<<64)-exact,c['roots'],untouched)
    assert sum(parts)==1<<66
    print(f'R41_DP_PASS pairs={pairs} unrestricted={raw} rational={rational} predecessor={pred} exact={exact}')
    print('R41_PARTITION_PASS no_prefix=%d source1_rejected=%d closed_cylinder=%d untouched_roots=%d total=%d' % (*parts,1<<66))
    print('R41_CYLINDER_PASS source_roots=%d interval=%d admitted=%d source_clear=%d false_clear=%d inverse=%d direct_descent=%d direct_le90=%d direct_gt90=%d no_descent_through2000=%d smaller_predecessor_67_90=%d max_descent=%d digest=%s admitted_digest=%s' % (c['roots'],c['interval'],c['admitted'],c['source_clear'],c['false_clear'],c['inverse'],c['direct_descent'],c['direct_le90'],c['direct_gt90'],c['no_descent_through2000'],c['smaller_predecessor_67_90'],max(steps),h,ah))
    for i,c in enumerate(bands):
        print('R41_BAND_PASS i=%d roots=%d admitted=%d direct=%d' % (i,c['roots'],c['admitted'],c['direct_descent']))

if __name__=='__main__':
    main()
