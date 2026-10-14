"""Research only: small-k semantic port of pinned Barina fsieve.c v2/v3.
No high-base residue-class certificate or full k34 binary map claim.
"""
from functools import lru_cache
from r3e21_4_certificates import barina_core

def tz(n):
    return (n & -n).bit_length()-1 if n else 100

@lru_cache(None)
def pred(L, a):
    p = L
    if a == 0:
        return p
    if L % 3 == 2:
        p = min(p, pred((L-2)//3*2+1,a-1))
    if a >= 2 and L % 9 == 4:
        p = min(p, pred((L-4)//9*8+3,a-2))
    if a >= 4 and L % 81 == 10:
        p = min(p, pred((L-10)//81*64+7,a-4))
    if a >= 5 and L % 243 == 182:
        p = min(p, pred((L-182)//243*128+95,a-5))
    return p

def v2(k,n):
    R=k;L=n;last=n
    while R>0:
        L+=1;a=min(tz(L),R);R-=a;L=(L>>a)*3**a-1
        b=min(tz(L),R);R-=b;L>>=b
        if L<n or (b>=2 and (last-1)//2<n):
            return False
        last=L
    return True

def v3(k,n):
    R=k;L=n;last=n;salpha=0
    while R>0:
        L+=1;a=min(tz(L),R);salpha+=a;R-=a;L=(L>>a)*3**a-1
        b=min(tz(L),R);R-=b;L>>=b
        p=pred(L,salpha)
        if b>=2:
            p=min(p,pred((last-1)//2,salpha-a))
        if p<n:
            return False
        last=L
    return True

def main():
    expected={8:(17,17,17,16),10:(49,47,47,52),
              12:(155,145,145,182),14:(494,437,437,593)}
    for k,target in expected.items():
        ns=range(1,1<<k)
        got=(sum(v2(k,n) for n in ns),sum(v3(k,n) for n in ns),
             sum(v2(k,n) and v3(k,n) for n in ns),sum(barina_core(k)[1:]))
        assert got==target,(k,got)
    print("PASS: enhanced v2/v3 positive low-residue k8/10/12/14 source semantic probe")

if __name__=="__main__":
    main()
