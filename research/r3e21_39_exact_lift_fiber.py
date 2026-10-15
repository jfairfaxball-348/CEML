#!/usr/bin/env python3
"""R39 bounded, original-start exact 66-bit lift fiber. RESEARCH ONLY."""
B,E=2392518188130438742016,3000000000000000000000
N=2736476243348084729115
L,M=1<<66,(1<<24)-1
def T(n):return n//2 if n%2==0 else (3*n+1)//2
def trace(n,k):
 xs=[n]
 for _ in range(k):xs.append(T(xs[-1]))
 return xs
def source_first66(n):
 root,f,num,flag,evens=3,2,9,0,0
 for i in range(2,67):
  assert root==n%(1<<i)
  if num<=root:return ('number_le_base',i)
  if 306*i>=485*f:return ('rational',i)
  if evens>=2 and evens%2==0 and 306*(i-1)>=485*(f-1):return ('predecessor',i)
  if i==66:return root,f,num,flag,evens
  bit=n>>i&1
  dinplay=int(306*(i+1)>=485*f)
  va,vb=num,num+3**f
  odd=((num&1)==0)!=bool(bit)
  if odd:
   v=vb if bit else va
   num=v+v//2;f+=1;flag=(flag|dinplay)&~2;evens=0
  else:
   if flag>=2:return ('doubleeven',i)
   v=vb if bit else va
   num=v//2+1;flag<<=1;evens+=1
  root|=bit<<i
 raise AssertionError('bad leaf')
def de(word,i):
 j=i
 while j<24 and word>>j&1:j+=1
 return j+2<24 and (word>>j)&3==0
def score(word,q):
 cur=peak=0;run=q
 for i in range(24):
  if word>>i&1:
   if de(word,i):peak=max(peak,cur+306)
   cur-=179;run=0
  else:
   cur+=306;run+=1
   if run%2==0:peak=max(peak,cur+179)
  peak=max(peak,cur)
 return peak
def source_gates(n,num,f,flag,a):
 if n%9 not in (0,1,3,6,7):return False
 if flag==2 and (num+a)%2==1:return False
 if flag==1 and (num+(a if f%2==0 else 3*a))%4==1:return False
 return True
def main():
 assert B<=N<E and N<1<<72
 path=trace(N,120)
 root,f,num,flag,run=source_first66(N)
 assert (root,f,run)==(N%L,43,1)
 assert num+(N//L)*3**f==path[66]+1
 interval=[];admitted=[];falseclear=[];no_witness=[]
 for a in range(64):
  n=root+a*L
  if not B<=n<E:continue
  interval.append(n)
  assert source_first66(n)==(root,f,num,flag,run)
  if not source_gates(n,num,f,flag,a):continue
  admitted.append(n)
  xs=trace(n,116)
  x66=xs[66]+1
  assert x66==num+a*3**f
  word=sum((xs[66+j]&1)<<j for j in range(24))
  src,corr=score(word,0),score(word,run&1)
  if src>659>=corr:
   falseclear.append((n,a,x66&M,word,src,corr))
   if all(z>=n for z in xs[1:91]) and all(z%3!=2 or (2*z-1)//3>=n for z in xs[67:91]):
    no_witness.append(n)
 assert N in admitted
 assert next(t for t in falseclear if t[0]==N)==(N,37,13704093,0x9faddc,791,612)
 assert all(z>=N for z in path[1:116]) and path[116]<N
 for k in range(67,91):
  z=path[k]
  assert z>=N
  if z%3==2:assert (2*z-1)//3>=N
  else:assert (2*z-1)%3!=0
 assert path[68]%3==1 and (2*path[68]-1)%3!=0
 assert path[67]%3==2 and (2*path[67]-1)//3>N
 inv=pow(3,-f,1<<24)
 idx=num*inv&M
 for a in range(64):
  assert ((num+a*3**f)*inv)&M==(idx+a)&M
  assert ((idx+a)&M)//64<(1<<18)
 assert (len(interval),len(admitted),len(falseclear),len(no_witness))==(8,4,1,1)
 print('R39_EXACT_FIBER_PASS interval_lifts=8 admitted_lifts=4 false_clear_lifts=1 no_direct_or_predecessor_through90=1')
 print('R39_WITNESS_PASS original_n=2736476243348084729115 lift=37 original_24word=0x9faddc source=791 corrected=612 cutoff=659 first_descent=116')
 print('R39_FIBER_FALSE_CLEAR_LIFTS '+','.join(str(t[1]) for t in falseclear))
if __name__=='__main__':main()

# Independently replay the committed full chronological original-start record.
# A missing, truncated or reordered record is a test failure, not evidence.
if __name__=='__main__':
 import json
 with open('research/r3e21_39_original_witness_trace.json',encoding='utf-8') as fh:
  rec=json.load(fh)
 assert rec['original_n']==str(N) and rec['step_start']==0
 assert rec['step_end']==rec['first_strict_descent_step']==116
 assert len(rec['states_0_to_116'])==117
 xs=trace(N,116)
 assert rec['states_0_to_116']==[str(t) for t in xs]
 assert all(t>=N for t in xs[1:116]) and xs[116]<N
 assert sum(t%2 for t in xs[:66])==43
 assert rec['previous_66_prefix_odd_count']==43
 assert rec['previous_66_trailing_even_count']==1
 print('R39_TRACE_FILE_PASS original_n=2736476243348084729115 chronological_states=117 first_descent=116')
