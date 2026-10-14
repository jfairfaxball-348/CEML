"""CEML-R3E21-14. Exact research-only first-hit cover; NOT production science."""
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import product

B=2392518188130438742016
E=3000000000000000000000
W=E-B
MOD=729
J=12
D=72
K=67
OLD_UPPER=330156319374735841

def T(n):
    return (3*n+1)//2 if n&1 else n//2

def old_roots():
    live=[True]
    for j in range(1,J+1):
        nxt=[]; seen=set()
        for r in range(1<<j):
            x,s=r,0
            for _ in range(j):
                s+=x&1
                x=T(x)
            key=(s,x)
            kill=key in seen or (3**s<2**j and 3**s-2**j<r-x)
            seen.add(key)
            nxt.append(live[r%len(live)] and not kill)
        live=nxt
    roots=[r for r,v in enumerate(live) if v]
    assert len(roots)==182
    return roots

def templates():
    byphase=defaultdict(list)
    total=0
    for h in range(1,10):
        for bits in product((0,1),repeat=h):
            a=sum(bits)
            if not (1<=a<=6 and 2**h<3**a):
                continue
            c=0
            for i,b in enumerate(bits):
                if b: c=3*c+2**i
            residue=c*pow(2**h,-1,3**a)%(3**a)
            for t in range(residue,MOD,3**a):
                byphase[t].append((h,a,c))
            total+=1
    assert (total,len(byphase))==(179,335)
    return byphase

def old_masks(roots):
    byphase=templates()
    inv2=[0]+[pow(2**j,-1,MOD) for j in range(1,J+1)]
    masks={}
    for r in roots:
        x,s,c=r,0,0
        prefixes=[]
        for j in range(1,J+1):
            if x&1:
                s+=1
                c=3*c+2**(j-1)
            x=T(x)
            prefixes.append((j,s,c))
        allowed=set()
        for t in range(MOD):
            if t in byphase:
                continue
            rejected=False
            for j,s,c in prefixes:
                y=(3**s*t+c)*inv2[j]%MOD
                for h,a,d in byphase.get(y,()):
                    slope=2**h*3**s-3**a*2**j
                    const=2**h*c-2**j*d
                    if slope<=0 and slope*B+const<0 and 2**h*3**s*B+const>0:
                        rejected=True
                        break
                if rejected: break
            if not rejected: allowed.add(t)
        masks[r]=frozenset(allowed)
    assert Counter(len(m) for m in masks.values())=={394:144,0:38}
    common={m for m in masks.values() if m}
    assert len(common)==1
    return [r for r in roots if masks[r]],common.pop()

def root_state(r):
    x,s,e=r,0,-1
    for j in range(1,J+1):
        if x&1: s+=1;e=0
        elif e>=0:e^=1
        x=T(x)
        assert 3**s>=2**j
    return s,e

def hit(j,s,e):
    return e==0 and 2*3**s<3*2**j

def step(j,s,e,ever,b):
    s+=b
    if 3**s<2**(j+1):return None
    e=0 if b else (-1 if e<0 else e^1)
    return s,e,ever or (j+1>J and hit(j+1,s,e))

def g(k,U):
    """Strict universal lower: every k-cylinder has >=floor(W/2^k) lifts."""
    N=W//(1<<k)
    q,r=divmod(N,MOD)
    if r==0: return q*len(U)
    stride=pow(2,k,MOD)
    one=[int((i*stride)%MOD in U) for i in range(MOD)]
    two=one+one
    running=sum(two[:r]); minimum=running
    for i in range(1,MOD):
        running+=two[i+r-1]-two[i-1]
        minimum=min(minimum,running)
    result=q*len(U)+minimum
    if k>=60:
        brute=min(sum((t+i*stride)%MOD in U for i in range(N)) for t in range(MOD))
        assert result==brute
    return result

def cover(roots,U):
    weights=[g(j,U) for j in range(K+2)]
    assert weights[55:69]==[9110,4554,2277,1138,568,282,139,68,33,15,7,3,1,0]
    assert 3**45<2**D<=3**46
    @lru_cache(None)
    def V(j,s,e,ever):
        stop=weights[j] if ever and s>=46 else 0
        if j==K:return stop
        children=[step(j,s,e,ever,b) for b in (0,1)]
        return max(stop,sum(V(j+1,*v) for v in children if v is not None))
    # A second forward multiplicity walk verifies the antichain arithmetic.
    states=Counter((J,*root_state(r),False) for r in roots)
    leaves=Counter()
    while states:
        nxt=Counter()
        for (j,s,e,ever),mult in states.items():
            stop=weights[j] if ever and s>=46 else 0
            children=[step(j,s,e,ever,b) for b in (0,1)] if j<K else []
            follow=sum(V(j+1,*v) for v in children if v is not None)
            if (stop and stop>=follow) or j==K:
                if stop:leaves[j]+=mult
            else:
                for child in children:
                    if child is not None:nxt[(j+1,*child)]+=mult
        states=nxt
    answer=sum(n*weights[j] for j,n in leaves.items())
    independent=sum(V(J,*root_state(r),False) for r in roots)
    assert answer==independent==3007471253458601
    assert OLD_UPPER-answer==327148848121277240
    return answer,dict(sorted(leaves.items())),weights

def collision(U):
    seen={}
    for q in range(256):
        r=2299+q*(1<<J)
        x,s,e,ever=r,0,-1,False
        for j in range(1,21):
            if x&1:s+=1;e=0
            elif e>=0:e^=1
            x=T(x)
            if j>J and hit(j,s,e):ever=True
        tag=(s,e,ever)
        step20=1<<20
        first=r+((B-r+step20-1)//step20)*step20
        N=(E-first+step20-1)//step20
        q729,rest=divmod(N,MOD)
        num=q729*len(U)+sum((first+i*step20)%MOD in U for i in range(rest))
        record=(r,num,N,first)
        if tag in seen and seen[tag][1]!=num:
            a=seen[tag]
            assert tag==(12,0,True)
            assert a==(14587,313113692531675,579339801663934,2392518188130438756603)
            assert record==(26875,313113692531674,579339801663934,2392518188130438768891)
            return tag,a,record
        seen[tag]=record
    raise AssertionError('No genuine numerical carry/phase countermodel')

def word_oracle():
    # Actual 22-prefix n=B+6395, then 2048 distinct genuine 11-bit lifts.
    dp=Counter({(14,0,True):1})
    for j in range(22,33):
        nxt=Counter()
        for (s,e,ever),mult in dp.items():
            for b in (0,1):
                child=step(j,s,e,ever,b)
                if child is not None:nxt[child]+=mult
        dp=nxt
    observed=Counter(); words=set()
    for q in range(1<<11):
        n=B+6395+q*(1<<22)
        x,s,e=n,0,-1
        safe=True
        suffix=[]
        for j in range(1,34):
            b=x&1
            if b:s+=1;e=0
            elif e>=0:e^=1
            if j>=23:
                safe&=3**s>=2**j
                suffix.append(b)
            x=T(x)
            if j==22:
                assert (s,e)==(14,0) and x%3==2
                p=(2*x-1)//3
                assert 0<p<n and T(p)==x
        words.add(tuple(suffix))
        if safe:observed[(s,e,True)]+=1
    assert len(words)==2048 and observed==dp and sum(dp.values())==142

def bounded_oracle(roots,U):
    # [B,B+350000) exact preserved old J12/U and all 72 slope screens.
    roots=set(roots)
    old=new=early=0
    depth=Counter()
    for n in range(B,B+350000):
        if n%(1<<J) not in roots or n%MOD not in U:continue
        x,s,e,evens=n,0,-1,-1
        viable=True; first=None
        for j in range(1,D+1):
            b=x&1
            if b:s+=1;e=0;evens=0
            elif e>=0:e^=1;evens+=1
            x=T(x)
            if 3**s<2**j:
                viable=False;break
            if j>J and first is None and hit(j,s,e):
                assert evens>=2 and evens%2==0 and x%3==2
                p=(2*x-1)//3
                assert 0<p<n and p%2==1 and T(p)==x
                first=(j,s)
        if viable:
            old+=1
            if first:
                new+=1
                j,ss=first
                depth[j]+=1
                if j<=66 and 306*(j-1)>=485*(ss-1):early+=1
    assert (old,new,early)==(141,25,19)
    assert depth[71]==6
    return dict(sorted(depth.items()))

def main():
    roots,U=old_masks(old_roots())
    word_oracle()
    local=bounded_oracle(roots,U)
    L,leaves,weights=cover(roots,U)
    phase_collision=collision(U)
    print('PASS: 144 common 394/729 allowed roots and 38 empty; 179 inverse templates')
    print('PASS: 2048 true lifts, 142 safe word completions')
    print('PASS: [B,B+350000) old=141, first-h1=25; 19 search1 rational gate, 6 j71 untested in search2')
    print('first-hit depths:',local)
    print('g55..68:',weights[55:69])
    print('prefix-free antichain leaves:',leaves)
    print('certified old-predicate overlap lower:',L)
    print('conditional upper:',OLD_UPPER-L)
    print('same language state, different numerical CRT occupancy:',phase_collision)
    print('NO completed trajectory, frontier, production, novelty, complete competitor match')

if __name__=='__main__':main()
