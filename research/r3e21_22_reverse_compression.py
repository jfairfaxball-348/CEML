#!/usr/bin/env python3
"""CEML R3E21-22 bounded, research-only exact symbolic certificate tests.
No orbit-to-one science or native verification. E is EXCLUSIVE.
"""
B=2392518188130438742016
E=3000000000000000000000
OFFICIAL=326865589733606241
def T(n): return (3*n+1)//2 if n&1 else n//2
def cd(a,b): return -(-a//b)
def ct(lo,hi,r,M): return max(0,cd(hi-r,M)-cd(lo-r,M))
def cone(k):
    ell=1
    while (1<<(k+ell))<=3**k:ell+=1
    M=1<<(k+ell)
    r=((1<<k)*pow(3**k,-1,1<<ell)-1)%M
    return ell,r,M
def path(n,j):
    s=0;x=n
    for _ in range(j):s+=x&1;x=T(x)
    return x,s
def certified(k,m):
    ell,r,M=cone(k);n=(1<<k)*m-1
    assert n%M==r and m&1
    assert (3**k*m-1)%(1<<ell)==0
    assert ((1<<(k+ell))-3**k)*m>(1<<ell)-1
    x=n
    for i in range(k):
        assert x&1;x=T(x)
        assert x==3**(i+1)*(1<<(k-i-1))*m-1
    for _ in range(ell):
        assert x%2==0;x=T(x)
    assert x==(3**k*m-1)//(1<<ell)<n
def lift(a,j,b,t,q):
    z,s=path(a,j);w,u=path(b,t);assert z==w
    h=max(s,u)
    n=a+(1<<j)*3**(h-s)*q
    m=b+(1<<t)*3**(h-u)*q
    assert path(n,j)[0]==path(m,t)[0]==z+3**h*q
    return n,m
def odd_witness(K,m):
    n=(1<<K)*m-1;x=n
    for i in range(1,K+1):
        assert x&1;x=T(x)
        assert x==3**i*(1<<(K-i))*m-1 and x>n
    return n
def main():
    assert ct(3,200,1,4)==49
    for lo in range(0,31,3):
        for hi in range(lo,lo+61,13):
            for M in (2,3,7,16,72):
                for r in range(M):
                    assert ct(lo,hi,r,M)==sum(n%M==r for n in range(lo,hi))
    total=0; nonempty=0;depth=0
    for k in range(1,73):
        ell,r,M=cone(k)
        N=ct(B,E,r,M)
        total+=N
        if N:
            nonempty+=1;depth=max(depth,k+ell)
            first=r+M*cd(B-r,M)
            assert B<=first<E
            certified(k,(first+1)//(1<<k))
            assert ct(B,E,r,M)>0
    assert total==216787629252827377045
    assert nonempty==43 and depth==69
    assert [cone(k) for k in (1,2,3,4)]==[(1,1,4),(2,3,16),(2,23,32),(3,15,128)]
    # Bounded actual truncated T and signed examples; no orbit-to-one.
    for n in range(3,3000,2):
        k=0;m=n+1
        while m%2==0:k+=1;m//=2
        ell,r,M=cone(k)
        if n%M==r and ((1<<(k+ell))-3**k)*m>(1<<ell)-1:
            assert path(n,k+ell)[0]<n
    assert path(11,3)[0]==13>11
    for q in (0,1,2,7,31,1234):
        n,m=lift(31,3,27,6,q)
        assert (n,m)==(31+72*q,27+64*q) and 0<m<n
        assert all(path(n,j)[0]>n for j in (1,2,3))
        assert n%9==4 and (8*n-5)//9==m # already known P2!
    assert ct(B,E,31,72)==8437247387077239694
    assert odd_witness(69,5)==2951479051793528258559
    assert ct(B,E,(1<<69)-1,1<<69)==1
    assert ct(B,E,(1<<68)-1,1<<68)==2
    # Exact affine transfer: authentically check multiple signed high-bit lifts.
    for a,j in ((15,6),(31,3),(17,5),(7,4)):
        y,s=path(a,j)
        for q in (0,1,2,7,1000):
            assert path(a+(1<<j)*q,j)[0]==y+3**s*q
    print('PASS bounded research-only R3E21-22')
    print('RUN_CONES',total,'classes',nonempty,'max descent depth',depth,'fresh',0)
    print('TAIL_MERGE_P2',ct(B,E,31,72),'fresh',0)
    print('K69_ALL_ODD',odd_witness(69,5),'not a survivor claim')
    print('OFFICIAL_CONDITIONAL_UPPER_UNCHANGED',OFFICIAL)
if __name__=='__main__':main()
