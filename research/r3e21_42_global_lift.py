#!/usr/bin/env python3
"""R42 global canonical high-lift descent, bounded original-T reproducibility.
Research-only mathematical proof fixture, not a frontier computation.
"""
from collections import defaultdict, Counter
from hashlib import sha256
import r3e21_40_source_reachable_cylinder as r40

B,E,L,P = r40.B,r40.E,r40.L,3**43
R=6438209236755220
CYL=12401
ALLOW={0,1,3,6,7}
LOWER_REM=B%L
UPPER_REM=(E-1)%L
assert B//L==32 and (E-1)//L==40
assert P%8==3 and L%9==1

def terminal_flag_partition():
    # Independent implementation of the R41 finite-state terminal flag tally.
    states={(2,0,0):1}
    for i in range(2,67):
        following=defaultdict(int)
        terminal=Counter()
        for (f,flag,q),c in states.items():
            if 306*i>=485*f: continue
            if q>=2 and q%2==0 and 306*(i-1)>=485*(f-1): continue
            if i==66:
                if f==43 and q%2: terminal[flag]+=c
                continue
            oddflag=(flag|int(306*(i+1)>=485*f))&~2
            following[(f+1,oddflag,0)]+=c
            if flag<2: following[(f,flag<<1,q+1)]+=c
        if i==66: break
        states=following
    assert terminal=={0:5973115806935136,2:465093429820084},terminal
    assert sum(terminal.values())==R
    return terminal

def fixed_eight(r):
    amin=max(0,(B-r+L-1)//L)
    amax=min(63,(E-1-r)//L)
    assert amax-amin+1 in (8,9)
    assert amin==(33 if r<LOWER_REM else 32)
    assert amax==(40 if r<=UPPER_REM else 39)
    return list(range(amin,amin+8)),amax-amin+1

def canonical_a(number,aa):
    hits=[a for a in aa if (number-1+a*P)%8==0]
    assert len(hits)==1
    return hits[0]

def source_gate_count(r,number,flag,aa):
    return sum(r40.gate(r+a*L,number,43,flag,a) for a in aa)

def main():
    flags=terminal_flag_partition()
    # Exact bound from the 66-step affine offset delta < 2^66.
    assert P*(B+L)<(1<<69)*B
    assert (1<<69)*B-P*(B+L)==602711608716672977428071654355915277074432
    minimum={0:8,2:8};maximum={0:0,2:0}
    for amin in (32,33):
        for residue in range(9):
            for flag in (0,2):
                for parity in (0,1):
                    count=sum((residue+a)%9 in ALLOW and
                              (flag==0 or (parity+a)%2==0)
                              for a in range(amin,amin+8))
                    minimum[flag]=min(minimum[flag],count)
                    maximum[flag]=max(maximum[flag],count)
    assert minimum=={0:4,2:1},minimum
    assert maximum=={0:5,2:3},maximum
    admitted_floor=4*flags[0]+flags[2]
    assert admitted_floor==24357556657560628

    # Exactly 500,000 distinct low-66 roots, spread throughout the root space:
    # NOT one low48 prefix. No assumption that nonqualifying roots survive.
    counts=Counter();seen=set();witnesses=[];same_dp_pair={}
    for j in range(500000):
        root=3+4*((j*0x9e3779b97f4a7c15)&((1<<64)-1))
        assert root not in seen
        seen.add(root)
        state=r40.brute_root(root)
        counts['root_probes']+=1
        if state is None: continue
        i,r,f,number,flag,q=state
        if f!=43 or q%2!=1: continue
        assert i==66 and r==root and flag in (0,2)
        aa,width=fixed_eight(r)
        a=canonical_a(number,aa)
        n=r+a*L
        assert B<=n<E and (number-1+a*P)%8==0
        z=n
        for k in range(1,70):
            z=r40.T(z)
            if k==66: assert z==number+a*P-1 and z%8==0
            if k in (67,68): assert z%2==0
            if k==69: assert z<n
        admitted=source_gate_count(r,number,flag,aa)
        assert admitted>=minimum[flag]
        counts['certified']+=1
        counts['flag%d'%flag]+=1
        counts['window%d'%width]+=1
        counts['canonical_source_admitted']+=int(r40.gate(n,number,43,flag,a))
        counts['fixed_eight_source_admitted']+=admitted
        witnesses.append(n)
        key=(f,flag,q)
        previous=same_dp_pair.get(key)
        if previous is None: same_dp_pair[key]=(root,root%9,number%8)
        elif (previous[1]!=root%9 and previous[2]!=number%8
              and counts['merge_obstruction']==0):
            counts['merge_obstruction']=1
            print('R42_MERGE_OBSTRUCTION_PAIR first=%d second=%d terminal=%s rmod9=%s numbermod8=%s' %
                  (previous[0],root,key,(previous[1],root%9),(previous[2],number%8)))
    assert counts['root_probes']==500000
    assert counts['certified']>100 and counts['flag0']>0 and counts['flag2']>0
    assert counts['window8']>0 and counts['window9']>0
    assert counts['merge_obstruction']==1
    assert len(set(witnesses))==counts['certified']
    digest=sha256(('\n'.join(map(str,sorted(witnesses)))+'\n').encode()).hexdigest()
    print('R42_GLOBAL_THEOREM_PASS roots=%d flag0=%d flag2=%d exact_one_canonical_descent_per_root=%d outside_old_cylinder=%d combined_with_old_admitted=%d new_admitted_lower=%d canonical_max_step=69' %
          (R,flags[0],flags[2],R,R-CYL,R-CYL+54438,admitted_floor))
    print('R42_GATE_RANGE_PASS flag0_minmax=4,5 flag2_minmax=1,3 source_mod9_residue_phases=9 a_windows=2')
    print('R42_BOUNDED_ORACLE_PASS root_probes=%d certified=%d flag0=%d flag2=%d window8=%d window9=%d canonical_source_admitted=%d fixed_eight_source_admitted=%d sha256=%s' %
          (counts['root_probes'],counts['certified'],counts['flag0'],counts['flag2'],counts['window8'],counts['window9'],counts['canonical_source_admitted'],counts['fixed_eight_source_admitted'],digest))
if __name__=='__main__': main()
