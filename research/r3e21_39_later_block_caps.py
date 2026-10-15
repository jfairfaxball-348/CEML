#!/usr/bin/env python3
"""R39 exact capped j=114,130 sparse parity certificates, NOT full hazard safety."""
from itertools import combinations
from math import comb
D=518059092085797269936906884792713216
START_LIMIT=1<<72
CAP_PROBES=5_000_000
CAP_MATERIALIZE=250_000
def test_small():
 for j in (4,6,8):
  w=j+4;mod=1<<w;inv3=pow(3,-1,mod);ratio=2*inv3%mod
  for n in range(1,1<<10):
   x=n+1;es=[]
   for i in range(w):
    if x&1:
     if i<j:es.append(i)
     else:break
     x=(x+1)//2
    else:x=3*x//2
   else:
    residue=(-sum(pow(3,k,mod)*pow(ratio,p,mod) for k,p in enumerate(es)))%mod
    assert residue==(n+1)%mod
def run(j):
 w=j+16;mod=1<<w;inv3=pow(3,-1,mod);ratio=2*inv3%mod
 terms=[[pow(3,k,mod)*pow(ratio,p,mod)%mod for p in range(j)] for k in range(3)]
 checked=0
 for m in range(4):
  c=comb(j,m)
  assert c<CAP_PROBES
  found=0
  for es in combinations(range(j),m):
   x=(-sum(terms[k][p] for k,p in enumerate(es)))%mod
   if 2<=x<=START_LIMIT:found+=1
   checked+=1
  assert found==0,(j,m,found)
  print(f'j={j} m={m} complete={c} compatible_start_classes=0')
 assert checked==sum(comb(j,m) for m in range(4))
 maxm={114:14,130:21}[j]
 total=sum(comb(j,m) for m in range(maxm+1))
 remaining=total-checked
 assert comb(j,4)>CAP_PROBES
 assert comb(j,7)>CAP_MATERIALIZE
 print(f'R39_LATER_STRATUM_PASS j={j} checked={checked} zero_hits=1 unexamined={remaining} max_m={maxm} next_class_count={comb(j,4)} cap_probes={CAP_PROBES}')
if __name__=='__main__':
 test_small()
 run(114)
 run(130)
