"""R3E21-7 research-only exact selected-cylinder counting; NEVER frontier science.
Run: python research/r3e21_7_correlated.py (imports frozen R3E21-6/4).
"""
from bisect import bisect_right
from collections import Counter
from functools import lru_cache
from r3e21_4_certificates import B, E, J, MOD3, T
from r3e21_6_adaptive import rows, cap, adaptive_bound, check_high_base

DEPTH = 72
SAMPLES = 65536
PREVIOUS = 342723929836590155
REDUCTION = 55259
NEW_UPPER = PREVIOUS - REDUCTION
DATA = rows()
MASKS = {mask for _, _, mask in DATA}
assert {sum(mask) for mask in MASKS} == {0, 394} and len(MASKS) == 2
MASK = next(mask for mask in MASKS if any(mask))
WIDTH = E - B

@lru_cache(None)
def optimum(depth, odd):
    direct = cap(MASK, depth, WIDTH)
    if depth == DEPTH:
        return direct, True
    split = sum(optimum(depth+1,odd+e)[0] for e in (0,1)
                if 3**(odd+e) >= 2**(depth+1))
    return (direct,True) if direct <= split else (split,False)

@lru_cache(None)
def leaf_count(depth, odd):
    if optimum(depth,odd)[1]:
        return 1
    return sum(leaf_count(depth+1,odd+e) for e in (0,1)
               if 3**(odd+e) >= 2**(depth+1))

@lru_cache(None)
def cyclic_lookup(depth,mask):
    delta=pow(2,depth,MOD3)
    seq=[int(mask[(i*delta)%MOD3]) for i in range(MOD3)]
    sums=[0]
    for bit in seq+seq:
        sums.append(sums[-1]+bit)
    return pow(delta,-1,MOD3),sums

def exact_cylinder(start,end,depth,residue,mask):
    assert start<=end and 0<=residue<(1<<depth) and len(mask)==MOD3
    step=1<<depth
    lo=(start-residue+step-1)//step
    hi=(end-residue+step-1)//step
    size=max(0,hi-lo)
    cycles,tail=divmod(size,MOD3)
    inv,sums=cyclic_lookup(depth,mask)
    phase=((residue+step*lo)%MOD3)*inv%MOD3
    return cycles*sum(mask)+sums[phase+tail]-sums[phase]

def unrank(root,initial_odd,rank):
    residue=root;orbit=root
    for _ in range(J):
        orbit=T(orbit)
    depth,odd=J,initial_odd
    while not optimum(depth,odd)[1]:
        for e in (0,1):
            if 3**(odd+e)<2**(depth+1):
                continue
            size=leaf_count(depth+1,odd+e)
            if rank>=size:
                rank-=size
                continue
            bit=(orbit&1)^e
            residue+=bit*(1<<depth)
            orbit=T(orbit+bit*3**odd)
            odd+=e;depth+=1
            break
        else:
            raise AssertionError("rank not contained in any child")
    assert rank==0
    return depth,residue,odd

def small_oracles():
    check_high_base()
    masks=[tuple(False for _ in range(MOD3)),
           tuple(True for _ in range(MOD3)),MASK,
           tuple((t%9) in (0,1,3,6,7) for t in range(MOD3))]
    cases=0
    for start in (-43,0,B+1,B+300,E-111):
        for width in (0,1,13,117,1511):
            for depth in (1,4,7,12,20):
                step=1<<depth
                for residue in (0,1,step//2,step-1):
                    for mask in masks:
                        count=exact_cylinder(start,start+width,depth,residue,mask)
                        direct=sum(n%step==residue and mask[n%MOD3]
                                   for n in range(start,start+width))
                        assert count==direct,(start,width,depth,residue)
                        if start>=B:
                            assert count<=cap(mask,depth,width)
                        cases+=1
    return cases

def main():
    assert adaptive_bound(B,E,DEPTH,DATA)==PREVIOUS
    cases=small_oracles()
    active=[(r,s) for r,s,mask in DATA if mask==MASK]
    cumulative=[];total_leaves=0
    for root,odd in active:
        total_leaves+=leaf_count(J,odd)
        cumulative.append(total_leaves)
    assert len(active)==144
    assert total_leaves==29715960543835736
    assert sum(optimum(J,s)[0] for _,s in active)==PREVIOUS
    savings=Counter();previous_rank=-1
    for i in range(SAMPLES):
        rank=((2*i+1)*total_leaves)//(2*SAMPLES)
        assert previous_rank<rank<total_leaves
        previous_rank=rank
        pos=bisect_right(cumulative,rank)
        before=cumulative[pos-1] if pos else 0
        root,initial_odd=active[pos]
        depth,residue,odd=unrank(root,initial_odd,rank-before)
        assert residue%(1<<J)==root
        if i%128==0:
            x,actual_odd=residue,0
            for _ in range(depth):
                actual_odd+=x&1;x=T(x)
            assert odd==actual_odd
        charged=cap(MASK,depth,WIDTH)
        exact=exact_cylinder(B,E,depth,residue,MASK)
        assert 0<=exact<=charged,(depth,residue,exact,charged)
        savings[depth]+=charged-exact
    reduction=sum(savings.values())
    assert reduction==REDUCTION,reduction
    assert PREVIOUS-reduction==NEW_UPPER
    print("PASS R3E21-7 exact CRT oracles:",cases)
    print("stopped leaves:",total_leaves,"selected:",SAMPLES)
    print("previous:",PREVIOUS,"saving:",reduction,"new upper:",NEW_UPPER)
    print("savings by depth:",sorted(savings.items()))

if __name__=="__main__":
    main()
