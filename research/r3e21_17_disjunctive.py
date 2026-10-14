#!/usr/bin/env python3
"""R3E21-17 finite exact arithmetic oracle. Research only; NOT Collatz-to-one science."""
from collections import Counter
from functools import lru_cache
from r3e21_15_tail_cover import B,E,T,roots_mask
J,K,D,MOD=12,67,72,729
PREVIOUS=326928588657578096
LOWER=127947636332546

def root(r):
    x,s,c=r,0,0
    for j in range(J):
        if x&1:s+=1;c=3*c+(1<<j)
        x=T(x)
    assert s>=8
    return s,c%243

def transfer(j,s,c,seen,bit):
    j+=1;s+=bit
    if 3**s<2**j:return None
    c=(3*c+(1<<(j-1)))%243 if bit else c
    y=c*pow(2**j,-1,243)%243
    if y%3==2 and 2*3**s<3*2**j:return None # h1
    if y%9==8 and 4*3**s<9*2**j:return None # h2
    if y%9==4 and 8*3**s<9*2**j:seen|=1 # Barina primitive 2, tracked only
    if y%81==10 and 64*3**s<81*2**j:seen|=2 # primitive 3
    if y==182 and 128*3**s<243*2**j:seen|=4 # primitive 4
    return s,c,seen

def weight(k,U):
    N=(E-B)//(1<<k);q,r=divmod(N,MOD)
    stride=pow(2,k,MOD)
    ring=[int(i*stride%MOD in U) for i in range(MOD)]*2
    v=sum(ring[:r]);mn=v
    for i in range(1,MOD):
        v+=ring[i+r-1]-ring[i-1]
        mn=min(mn,v)
    if k>=60:
        assert mn==min(sum((a+i*stride)%MOD in U for i in range(r)) for a in range(MOD))
    return q*len(U)+mn

def signed_gate_check():
    maxima={}
    for name,t,d,H in [('P2',3,2,5),('P3',6,4,73),('P4',7,5,211)]:
        biggest=(0,0,0)
        for j in range(13,D+1):
            for s in range(8,j+1):
                delta=3**d*2**j-2**t*3**s
                if delta<=0:continue
                Cmax=2**(j-s)*(3**s-2**s)
                threshold=max(0,(2**t*Cmax-H*2**j)//delta+1)
                if threshold>biggest[0]:biggest=threshold,j,s
        maxima[name]=biggest
    assert maxima=={'P2':(2910474616,68,43),
                    'P3':(5820949337,71,45),
                    'P4':(5820949363,72,46)}
    assert B>max(v[0] for v in maxima.values())
    assert 3**46>2**72 and 2*3**46>3*2**72
    return maxima

def test_witness(n,roots,U):
    assert B<=n<E and n%4096 in roots and n%729 in U
    x=n;s=0;hits=[]
    for j in range(1,73):
        s+=x&1;x=T(x)
        assert 3**s>=2**j
        if j<=12:continue
        assert not (x%3==2 and 0<(2*x-1)//3<n)
        assert not (x%9==8 and 0<(4*x-5)//9<n)
        for name,mod,res,t,d,H in [('P3',81,10,6,4,73),('P4',243,182,7,5,211)]:
            if x%mod!=res:continue
            p=((1<<t)*x-H)//3**d
            if 0<p<n:
                z=p
                for _ in range(t):z=T(z)
                assert z==x
                hits.append((name,j))
    assert hits
    return hits

def main():
    roots,U=roots_mask() # R3E21-15 reconstructs 182=>144 roots, U=394/729
    assert len(roots)==144 and len(U)==394
    safe=signed_gate_check()
    ws=[weight(j,U) for j in range(K+1)]
    assert ws[55:68]==[9110,4554,2277,1138,568,282,139,68,33,15,7,3,1]
    initial=Counter((*root(r),0) for r in roots)
    @lru_cache(None)
    def optimum(j,s,c,seen):
        stop=ws[j] if seen&6 and s>=46 else 0
        if j==K:return stop
        return max(stop,sum(optimum(j+1,*v) for b in (0,1)
                  if (v:=transfer(j,s,c,seen,b)) is not None))
    best=sum(m*optimum(J,*state) for state,m in initial.items())
    frontier=initial
    hist,types=Counter(),Counter()
    for j in range(J,K+1):
        nxt=Counter()
        for (s,c,seen),mult in frontier.items():
            if seen&6 and s>=46:
                hist[j]+=mult;types[seen&6]+=mult
                continue
            if j==K:continue
            for bit in (0,1):
                v=transfer(j,s,c,seen,bit)
                if v is not None:nxt[v]+=mult
        frontier=nxt
    greedy=sum(hist[j]*ws[j] for j in hist)
    assert greedy==best==LOWER
    assert types[2]>0 and types[4]>0 and types[6]>0
    n3=2392522326193255436379
    n4=2392598776513599946863
    n34=2394950771631449919579
    assert test_witness(n3,roots,U)==[('P3',14)]
    assert test_witness(n4,roots,U)==[('P4',31)]
    assert test_witness(n34,roots,U)==[('P3',14),('P4',39)]
    n=B+243871;m=n+4096*729
    assert n%4096==m%4096 and n%729==m%729
    a,b=n,m
    for _ in range(12):a=T(a);b=T(b)
    assert a%243==b%243==242 and a%2!=b%2
    assert T(a)%243==242 and T(b)%243==121
    old=0
    for n in range(B,B+350000):
        if n%4096 not in roots or n%729 not in U:continue
        x=n;s=0
        for j in range(1,73):
            s+=x&1;x=T(x)
            if 3**s<2**j:break
        else:old+=1
    assert old==141
    print('PASS source-route high-base bounds',safe)
    print('PASS greedy + independent recursive maximum',greedy,'states',optimum.cache_info().currsize)
    print('PASS histogram',sorted(hist.items()))
    print('PASS P3 only/P4 only/both leaf counts',sorted(types.items()))
    print('PASS authentic 72-prefix witnesses for P3, P4, P3+P4; low-window old',old)
    print('PASS mod243 phase collision and cyclic CRT worst-phase checks')
    print('NEW CONDITIONAL CONSERVATIVE UPPER',PREVIOUS-greedy)
if __name__=='__main__':main()
