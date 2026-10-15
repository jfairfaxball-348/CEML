// R38 complete two-incoming-parity 2^24 lookahead certificate; NO SCIENCE.
// Original initial even-run count 0 vs source-search1 inherited odd parity 1.
#include <cstdint>
#include <cstdio>
#include <cassert>
#include <algorithm>
using U=unsigned __int128;
static bool de(uint32_t w,int i){
  uint32_t q=w>>i;int a=__builtin_ctz(q+1u);
  return i+a+2<24 && ((w>>(i+a))&3u)==0u;
}
int main(){
 const uint32_t LIM=1u<<24;
 uint64_t g[2][8]={},live[2][8]={},changed=0;
 for(uint32_t r=0;r<LIM;r++){
  U x=(U)r+LIM;uint32_t w=0;
  for(int i=0;i<24;i++){
   if(!(x&1)){w|=1u<<i;x+=x/2;}
   else x=(x+1)/2;
  }
  int cur=0,score[2]={},ev[2]={0,1};
  for(int i=0;i<24;i++){
   if((w>>i)&1){
    if(de(w,i))for(auto &s:score)s=std::max(s,cur+306);
    cur-=179;ev[0]=ev[1]=0;
   }else{
    cur+=306;
    for(int p=0;p<2;p++){
     ++ev[p];
     if((ev[p]&1)==0)score[p]=std::max(score[p],cur+179);
    }
   }
   for(auto &s:score)s=std::max(s,cur);
  }
  if(score[0]!=score[1])changed++;
  for(int a=0;a<8;a++){
   int cutoff=174+485*a;
   for(int p=0;p<2;p++)if(score[p]<=cutoff)live[p][a]++;
   if(score[0]>cutoff && score[1]<=cutoff)g[0][a]++;
   if(score[1]>cutoff && score[0]<=cutoff)g[1][a]++;
  }
 }
 const uint64_t old[8]={333343,1590275,3837929,6750160,9809263,12495505,14479396,15712298};
 const uint64_t odd[8]={333343,1650277,3837929,6738759,9809263,12498034,14479880,15712298};
 const uint64_t over[8]={0,60002,0,0,0,2529,484,0};
 const uint64_t under[8]={0,0,0,11401,0,0,0,0};
 assert(changed==399426);
 uint64_t o=0,u=0;
 for(int a=0;a<8;a++){
  assert(live[0][a]==old[a] && live[1][a]==odd[a]);
  assert(g[0][a]==over[a] && g[1][a]==under[a]);
  o+=g[0][a];u+=g[1][a];
  printf("a=%d original_live=%llu seeded_odd_live=%llu false_clear=%llu false_keep=%llu\n",a,
    (unsigned long long)live[0][a],(unsigned long long)live[1][a],
    (unsigned long long)g[0][a],(unsigned long long)g[1][a]);
 }
 assert(o==63015 && u==11401);
 printf("R38_TWO_PARITY_SCAN_COMPLETE residues=16777216 mismatched_scores=399426 source_false_clear_pairs=63015 source_false_keep_pairs=11401\n");
}
