"""CEML R3E21-15: small exact research-only tail-cover reproducer. NO scientific batches."""
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import product

B,E,MOD,J,D,K=2392518188130438742016,3*10**21,729,12,72,67
PREV_UPPER=327148848121277240

def T(n):return (3*n+1)//2 if n&1 else n//2

def roots_mask():
    live=[True]
    for j in range(1,J+1):
        nxt=[];seen=set()
        for r in range(1<<j):
            x,s=r,0
            for _ in range(j):s+=x&1;x=T(x)
            key=s,x
            dead=key in seen or (3**s<2**j and 3**s-2**j<r-x)
            seen.add(key)
            nxt.append(live[r%len(live)] and not dead)
        live=nxt
    roots=[r for r in range(1<<J) if live[r]]
    assert len(roots)==182
    byphase=defaultdict(list);ntemplates=0
    for h in range(1,10):
        for bits in product((0,1),repeat=h):
            a=sum(bits)
            if not (1<=a<=6 and 2**h<3**a):continue
            c=0
            for i,b in enumerate(bits):
                if b:c=3*c+2**i
            t0=c*pow(2**h,-1,3**a)%(3**a)
            for t in range(t0,MOD,3**a):byphase[t].append((h,a,c))
            ntemplates+=1
    assert (ntemplates,len(byphase))==(179,335)
    masks={}
    for r in roots:
        x,s,c,prefixes=r,0,0,[]
        for j in range(1,J+1):
            if x&1:s+=1;c=3*c+2**(j-1)
            x=T(x);prefixes.append((j,s,c))
        allowed=set()
        for t in range(MOD):
            if t in byphase:continue
            forbidden=False
            for j,s,c in prefixes:
                y=(3**s*t+c)*pow(2**j,-1,MOD)%MOD
                for h,a,v in byphase.get(y,()):
                    coeff=2**h*3**s-3**a*2**j
                    off=2**h*c-2**j*v
                    if coeff<=0 and coeff*B+off<0 and 2**h*3**s*B+off>0:
                        forbidden=True;break
                if forbidden:break
            if not forbidden:allowed.add(t)
        masks[r]=frozenset(allowed)
    assert Counter(map(len,masks.values()))=={394:144,0:38}
    nonempty={m for m in masks.values() if m}
    assert len(nonempty)==1
    return [r for r in roots if masks[r]],next(iter(nonempty))

def root_state(r):
    x,s,c=r,0,0
    for j in range(1,J+1):
        if x&1:s+=1;c=3*c+2**(j-1)
        x=T(x)
        assert 3**s>=2**j
    return s,c%9

def threshold_gate():
    biggest=(1,None);pos=(0,None)
    for j in range(1,D+1):
        for s in range(1,j+1):
            mx=2**(j-s)*(3**s-2**s)
            delta=9*2**j-4*3**s
            if delta>0:
                bound=max(1,(4*mx-5*2**j)//delta+1)
                if bound>biggest[0]:biggest=bound,(j,s)
            elif delta<0:
                bound=5*2**j//(-delta)
                if bound>pos[0]:pos=bound,(j,s)
            else:assert (j,s)==(2,2)
    assert biggest==(1455237284,(67,43)) and pos==(40,(21,14)) and B>biggest[0]

def weight(k,U):
    N=(E-B)//(1<<k);q,r=divmod(N,MOD)
    stride=pow(2,k,MOD)
    seq=[int(i*stride%MOD in U) for i in range(MOD)]*2
    v=sum(seq[:r]);mn=v
    for i in range(1,MOD):
        v+=seq[i+r-1]-seq[i-1];mn=min(mn,v)
    return q*len(U)+mn

def child(j,s,c,seen2,b):
    jj=j+1;ss=s+b
    if 3**ss<2**jj:return None
    cc=(3*c+pow(2,j,9))%9 if b else c
    y9=cc*pow(2**jj,-1,9)%9
    if y9%3==2 and 2*3**ss<3*2**jj:return None
    return ss,cc,seen2 or (y9==8 and 4*3**ss<9*2**jj)

def cover(roots,U):
    weights=[weight(k,U) for k in range(K+1)]
    assert weights[55:68]==[9110,4554,2277,1138,568,282,139,68,33,15,7,3,1]
    assert 3**46>2**D and 2*3**46>3*2**D
    @lru_cache(None)
    def V(j,s,c,seen2):
        stop=weights[j] if seen2 and s>=46 else 0
        if j==K:return stop
        nxt=[z for b in (0,1) if (z:=child(j,s,c,seen2,b)) is not None]
        return max(stop,sum(V(j+1,*z) for z in nxt))
    total=sum(V(J,*root_state(r),False) for r in roots)
    states=Counter((J,*root_state(r),False) for r in roots)
    hist=Counter()
    while states:
        following=Counter()
        for (j,s,c,seen2),mult in states.items():
            stop=weights[j] if seen2 and s>=46 else 0
            nxt=[z for b in (0,1) if (z:=child(j,s,c,seen2,b)) is not None] if j<K else []
            follow=sum(V(j+1,*z) for z in nxt)
            if (stop and stop>=follow) or j==K:
                if stop:hist[j]+=mult
            else:
                for z in nxt:following[(j+1,*z)]+=mult
        states=following
    assert total==sum(hist[k]*weights[k] for k in hist)==220259463699144
    assert PREV_UPPER-total==326928588657578096
    return total,dict(sorted(hist.items())),V.cache_info().currsize

def bounded_oracle(roots,U):
    roots=set(roots);old=one=two_only=both=0;samples=[]
    for n in range(B,B+350000):
        if n%4096 not in roots or n%729 not in U:continue
        x,s,hit1,hit2=n,0,False,False
        safe=True;first2=None
        for j in range(1,D+1):
            s+=x&1;x=T(x)
            if 3**s<2**j:safe=False;break
            if j>J and x%3==2:
                p=(2*x-1)//3
                if 0<p<n and T(p)==x:hit1=True
            if j>J and x%9==8:
                p=(4*x-5)//9
                if 0<p<n and T(T(p))==x:
                    hit2=True
                    if first2 is None:first2=(j,p,x)
        if safe:
            old+=1;one+=int(hit1);both+=int(hit1 and hit2)
            if hit2 and not hit1:
                two_only+=1;samples.append((n-B,*first2))
    assert (old,one,two_only,both)==(141,25,3,25)
    assert samples==[
      (160511,50,1750060641509827815151,3937636443397112584091),
      (243871,20,1616773298159572124607,3637739920859037280367),
      (298087,26,2046228705483208516575,4604014587337219162295)]
    return old,one,two_only,samples

def main():
    threshold_gate()
    roots,U=roots_mask()
    lower,hist,states=cover(roots,U)
    print('PASS masks 144 common 394/729, high-base threshold, memo states',states)
    print('PASS prefix-free independent forward histogram',hist)
    print('PASS bounded exact 72-prefix oracle',bounded_oracle(roots,U))
    print('Certified disjoint old-predicate lower',lower)
    print('CONDITIONAL CONSERVATIVE UPPER',PREV_UPPER-lower)
    print('No Collatz-to-one science, source-equivalent enhanced competitor match, novelty or frontier')

if __name__=='__main__':main()
