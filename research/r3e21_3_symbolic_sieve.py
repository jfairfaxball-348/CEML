"""R3E21-3 mathematical sieve fixtures. NO frontier science."""
from fractions import Fraction
from itertools import product

B=2175982616*2**40
E=3*10**21

def T(n):
    return n//2 if n%2==0 else (3*n+1)//2

def forward_dp(K):
    c={0:1}
    for j in range(1,K+1):
        c={s:c.get(s,0)+c.get(s-1,0) for s in range(j+1) if 3**s>=2**j}
    return sum(c.values())

def forward_residues(K):
    # Independent low-bit lift via actual T states, not the counting DP.
    states=[(0,0,0)]
    for j in range(K):
        nxt=[]
        for r,t,s in states:
            for bit in (0,1):
                x=t+bit*3**s
                odd=s+x%2
                if 3**odd>=2**(j+1):
                    nxt.append((r+bit*2**j,T(x),odd))
        states=nxt
    return {r for r,t,s in states}

def reverse_sieve(A=6):
    m=3**A
    covered=set()
    words=[]
    for j in range(1,10):
        for bits in product((0,1),repeat=j):
            a=sum(bits)
            if not (1<=a<=A and 2**j<3**a):
                continue
            num=0
            for i,e in enumerate(bits):
                if e:
                    num=3*num+2**i
            md=3**a
            r=num*pow(2**j,-1,md)%md
            words.append((j,a,num,r,bits))
            covered.update(range(r,m,md))
    return words,covered

def check():
    assert B>=2**70
    for k in range(1,13):
        residues=forward_residues(k)
        assert len(residues)==forward_dp(k)
        for r in range(2**k):
            n=2**(2*k)+r
            x=n
            descended=False
            for j in range(1,k+1):
                x=T(x)
                descended |= x<n
            assert descended==(r not in residues),(k,r)
    words,covered=reverse_sieve()
    assert len(words)==179 and len(covered)==335
    assert {r for r in range(729) if r%9 in (2,4,5,8)}<=covered
    for r in covered:
        n=729+r
        found=False
        for j,a,num,res,bits in words:
            if n%(3**a)!=res:
                continue
            p=(2**j*n-num)//3**a
            if not 0<p<n:
                continue
            v=p
            for bit in bits:
                assert v%2==bit
                v=T(v)
            assert v==n
            found=True
        assert found
    counts={5:4,16:2114,24:286581,27:1762293,
            30:12771274,32:41347483,34:151917636,35:263841377}
    for k,v in counts.items():
        assert forward_dp(k)==v
        c=v*(729-len(covered))
        m=2**k*729
        q,rem=divmod(E-B,m)
        print(k,"forward",v,"density",Fraction(c,m),
              "pct",100*float(Fraction(c,m)),
              "finite_candidates_in",[q*c,(q+1)*c],"remainder",rem)
    # Exact independent CRT count for K=24 with only the proven mod-9 reverse mask.
    inverse=pow(2**24,-1,9)
    total=0
    for r in forward_residues(24):
        for t in (0,1,3,6,7):
            res=r+2**24*((t-r)*inverse%9)
            mod=9*2**24
            total+=(E-1-res)//mod-(B-1-res)//mod
    assert total==5764853461828189824
    print("K24+mod9 exact candidates",total,"reverse templates",len(words),
          "reverse covered classes",len(covered))

if __name__=="__main__":
    check()
