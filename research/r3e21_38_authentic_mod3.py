#!/usr/bin/env python3
"""R38 source-path counterexample fixture; research-only, not frontier science."""
B,E=2392518188130438742016,3000000000000000000000
N=2736476243348084729115
def T(n):
    assert n>=1
    return n//2 if n%2==0 else (3*n+1)//2
def trace(n,k):
    a=[n]
    for _ in range(k): a.append(T(a[-1]))
    return a
def doubleeven(w,i):
    q=(w>>i)+1
    a=(q&-q).bit_length()-1
    return i+a+2<24 and ((w>>(i+a))&3)==0
def score(w,prior_even):
    cur=0;s=[0,0];e=[0,prior_even]
    for i in range(24):
        if (w>>i)&1:
            if doubleeven(w,i):
                for p in range(2):s[p]=max(s[p],cur+306)
            cur-=179;e=[0,0]
        else:
            cur+=306
            for p in range(2):
                e[p]+=1
                if e[p]%2==0:s[p]=max(s[p],cur+179)
        for p in range(2):s[p]=max(s[p],cur)
    return s
def prefix(n):
    base,f,num,flag,evens=3,2,9,0,0
    for i in range(2,67):
        assert base==n%(1<<i)
        assert num>base,('number<=base',i)
        assert 306*i<485*f,('ratio',i)
        assert not (evens>=2 and evens%2==0 and 306*(i-1)>=485*(f-1)),('reverse',i)
        if i==66:return base,f,num,flag,evens
        bit=(n>>i)&1
        dinplay=int(306*(i+1)>=485*f)
        na,nb=num,num+3**f
        odd=(num%2==0)!=bool(bit)
        if odd:
            v=nb if bit else na
            num=v+v//2
            f+=1
            flag=(flag|dinplay)&~2
            evens=0
        else:
            assert flag<2,('doubleeven',i)
            v=nb if bit else na
            num=v//2+1
            flag<<=1
            evens+=1
        base|=bit<<i
    raise AssertionError('no leaf')
def check_base():
    longest=(0,0);peak=0
    for n in range(1,99782):
        z=n;k=0
        while z!=1 and k<10000:
            peak=max(peak,z)
            z=T(z);k+=1
        assert z==1
        longest=max(longest,(k,n))
    assert longest==(221,77031) and peak==785412368,(longest,peak)
    print('R38_BOUNDED_BASE_PASS starts=99781 max_steps=221 max_peak=785412368')
def main():
    assert B<=N<E and N<2**72 and N%4==3
    root,f,num,flag,evens=prefix(N)
    path=trace(N,116)
    a=N>>66
    assert a==37 and root==N%(2**66)
    assert f==43 and f==sum(v%2 for v in path[:66])
    assert num+a*3**f==path[66]+1
    assert evens==1 and path[66]%3==1 and path[67]%3==2 and path[68]%3==1
    assert N%9==6
    assert flag!=2 or (num+a)%2!=1
    assert flag!=1 or (num+(a if f%2==0 else 3*a))%4!=1
    x=path[66]+1
    idx=(num*pow(3,-f,1<<24))% (1<<24)
    assert ((x*pow(3,-f,1<<24))%(1<<24))==(idx+a)%(1<<24)
    w=sum((path[66+j]%2)<<j for j in range(24))
    src,corrected=score(w,evens)
    assert (x%(1<<24),w,src,corrected,174+485*(f-42))==(13704093,0x9faddc,791,612,659)
    assert (w&3)==0 and src>659>=corrected
    assert (2*path[68]-1)%3!=0
    assert (2*path[67]-1)%3==0 and (2*path[67]-1)//3>N
    assert all(z>=N for z in path[:116]) and path[116]<N
    assert all(z>=99781 for z in path[:91])
    # Low24 parity transport valid even for zero residue with positive high lift.
    for r in (0,1,109,13704093):
        x=(1<<24)+r;w1=0
        for i in range(24):
            if not (x&1):w1|=1<<i;x=x+x//2
            else:x=x//2+1
        lo=r;w2=0
        for i in range(24):
            if not (lo&1):w2|=1<<i;lo=lo+lo//2
            else:lo=lo//2+1
        assert w1==w2
    print('R38_AUTHENTIC_MISMATCH_PASS original_n=2736476243348084729115 f=43 lift=37 low24=13704093 source_score=791 corrected_score=612 cutoff=659 first_descent_step=116')
    check_base()
if __name__=='__main__':main()
