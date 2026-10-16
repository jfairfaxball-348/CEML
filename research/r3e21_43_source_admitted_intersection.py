#!/usr/bin/env python3
"""R43 complete disjoint root cylinders: source mod9/flag ∩ literal-T descent.
No LUT50, binary, native or interval verification is asserted.
"""
from collections import Counter
from hashlib import sha256
import r3e21_40_source_reachable_cylinder as src

L, P, B, E = src.L, 3**43, src.B, src.E
STRATA = (
    (148957342012655,2416,547,10409,1194),
    (146557399178687,15884,3780,70550,8357),
    (130677744459943,15884,3647,70460,8298),
    (21359721993575,7006,1621,30405,3487),
    (236955905271263,4910,1144,21314,2467),
    (53319191503839,15884,3739,70639,8301),
    (202396992200703,12401,2894,54461,6348),
    (35120119522751,7006,1622,30383,3485),
)
DIGEST='fa2add371b8e778e793adfaa84d57a72b6f7d103a74c2528435640100e8bcc24'

def digest(a):
    assert len(a)==len(set(a))
    return sha256(('\n'.join(map(str,sorted(a)))+'\n').encode()).hexdigest()

def count_leaf(s, tally, admitted, trace):
    i,r,f,number,flag,q=s
    if not(i==66 and f==43 and q%2 and src.eligible(*s)):return
    assert flag in (0,2)
    tally['roots']+=1;tally['flag'+str(flag)]+=1
    lo=max(0,(B-r+L-1)//L);hi=min(63,(E-1-r)//L)
    assert hi-lo in (7,8)
    tally['ninth']+=int(hi-lo==8)
    choices=[a for a in range(lo,lo+8) if (number-1+a*P)%8==0]
    assert len(choices)==1
    for a in range(lo,hi+1):
        n=r+a*L; assert B<=n<E
        ok=src.gate(n,number,43,flag,a)
        tally['lifts']+=1;tally['gates']+=int(ok)
        if a==choices[0]:
            tally['canonical']+=1;tally['intersection']+=int(ok)
            if ok:admitted.append(n)
            if trace:
                z=n;odd=0;run=0
                for k in range(1,70):
                    odd+=int(z&1 and k<=66)
                    run=0 if z&1 else run+1
                    z=src.T(z)
                    if k==66:
                        assert z==number-1+a*P and z%8==0
                        assert odd==43 and run==q
                assert z<n

def prefix(low):
    s=(2,3,2,9,0,0)
    for i in range(2,48):
        assert s and s[0]==i and src.eligible(*s)
        s=src.source_child(*s,(low>>i)&1)
    assert s and src.eligible(*s) and s[1]==low
    return s

def exhaustive(low,p):
    tally=Counter();a=[]
    for j in range(1<<18):
        r=low+(j<<48);s=p
        while s and src.eligible(*s) and s[0]<66:
            s=src.source_child(*s,(r>>s[0])&1)
        tally['probes']+=1
        if s and s[0]==66:count_leaf(s,tally,a,True)
    return tally,a

def recursive(p):
    tally=Counter();a=[]
    def dfs(s):
        if not s or not src.eligible(*s):return
        if s[0]==66:
            count_leaf(s,tally,a,False);return
        dfs(src.source_child(*s,0));dfs(src.source_child(*s,1))
    dfs(p)
    return tally,a

def main():
    assert len({s[0] for s in STRATA})==8
    assert src.LOW not in {s[0] for s in STRATA}
    total=Counter();family=[]
    for idx,(low,roots,ninth,gates,overlap) in enumerate(STRATA):
        assert low%4==3 and low < (1<<48)
        p=prefix(low);c,a=exhaustive(low,p);d,b=recursive(p)
        assert {k:v for k,v in c.items() if k!='probes'}==dict(d)
        assert digest(a)==digest(b)
        assert (c['probes'],c['roots'],c['ninth'],c['gates'],c['intersection'])==(1<<18,roots,ninth,gates,overlap)
        assert c['lifts']==8*roots+ninth and c['canonical']==roots
        assert c['flag0']+c['flag2']==roots
        total.update(c);family.extend(a)
        print(f'R43_CLASS_PASS index={idx} low48={low} roots={roots} ninth={ninth} admitted={gates} intersection={overlap}')
    assert (total['probes'],total['roots'],total['ninth'],total['lifts'],total['gates'],total['intersection'])==(2097152,81391,18994,670122,358621,41937)
    assert (total['flag0'],total['flag2'])==(75446,5945)
    assert digest(family)==DIGEST
    print('R43_INTERSECTION_PASS probes=2097152 eligible_roots=81391 ninth=18994 source_gated=358621 canonical_admitted=41937 nonadmitted_canonical=39454 union_R41=96375 sha256='+DIGEST)

if __name__=='__main__':main()
