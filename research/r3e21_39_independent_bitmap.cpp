// R39 source-distinct positive-lift exact T and mod3 bitmap check; RESEARCH ONLY.
// Build: g++ -O3 -std=c++17 -Wall -Wextra -o /tmp/r39-bmp research/r3e21_39_independent_bitmap.cpp
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <vector>
using U=unsigned __int128;
static constexpr uint32_t LIM=1u<<24, MASK=LIM-1, WORDS=LIM/64;
static U T(U z){return (z&1)?(3*z+1)/2:z/2;}
static bool port_de(uint32_t w,int i){
 uint32_t q=(w>>i)+1u;int a=q?__builtin_ctz(q):32;
 return i+a+2<24 && ((w>>(i+a))&3u)==0;
}
static bool scan_de(uint32_t w,int i){
 int j=i;while(j<24 && ((w>>j)&1u))j++;
 return j+2<24 && ((w>>j)&3u)==0u;
}
static uint32_t inv_odd(uint32_t a){
 uint32_t x=1;for(int t=0;t<5;t++)x*=2-a*x;
 assert(((uint64_t)x*a&MASK)==1u);return x&MASK;
}
int main(){
 const uint64_t old[8]={333343,1590275,3837929,6750160,9809263,12495505,14479396,15712298};
 const uint64_t odd[8]={333343,1650277,3837929,6738759,9809263,12498034,14479880,15712298};
 const uint64_t over[8]={0,60002,0,0,0,2529,484,0};
 const uint64_t under[8]={0,0,0,11401,0,0,0,0};
 uint64_t counts[2][8]={},gaps[2][8]={},mismatched=0;
 const uint32_t inv3=inv_odd(3);
 uint32_t inverse[8],forward[8];
 forward[0]=1;for(int t=0;t<42;t++)forward[0]=(uint64_t)forward[0]*3&MASK;
 for(int a=0;a<8;a++){
  forward[a]=a?((uint64_t)forward[a-1]*3&MASK):forward[0];
  inverse[a]=inv_odd(forward[a]);
  uint32_t invpow=1;
  for(int t=0;t<42+a;t++)invpow=(uint64_t)invpow*inv3&MASK;
  assert(inverse[a]==invpow);
 }
 // 1=LIVE; two incoming parity classes; trailing 64-bit wrap cell.
 std::vector<uint64_t> bits[2][8];
 for(int q=0;q<2;q++)for(int a=0;a<8;a++)bits[q][a].resize(WORDS+1);
 for(uint32_t r=0;r<LIM;r++){
  uint32_t w[2]={};int score[2]={};
  for(int q=0;q<2;q++){
   // Select positive high lift so z0%3 equals the class's real incoming residue.
   const int target=q?1:2;
   const uint32_t h=1+(3+(target-(int)(r%3)))%3;
   U z=(U)h*LIM+r-1;
   assert((uint32_t)(z%3)==(uint32_t)target && z>0);
   int run=q,cur=0,peak=0;U path[25];path[0]=z;
   for(int i=0;i<24;i++){
    if(path[i]&1)w[q]|=1u<<i;
    path[i+1]=T(path[i]);
    if(path[i]&1){run=0;assert(path[i+1]%3==2);}
    else{
     run++;
     bool valid=(2*path[i+1]-1)%3==0;
     assert(valid==(run%2==0));
    }
   }
   run=q;
   for(int i=0;i<24;i++){
    bool de0=port_de(w[q],i),de1=scan_de(w[q],i);
    assert(de0==de1);
    if(w[q]>>i&1u){
     if(de1)peak=std::max(peak,cur+306);
     cur-=179;run=0;
    }else{
     cur+=306;run++;
     bool actual_predecessor=(2*path[i+1]-1)%3==0;
     assert(actual_predecessor==(run%2==0));
     if(actual_predecessor)peak=std::max(peak,cur+179);
    }
    peak=std::max(peak,cur);
   }
   score[q]=peak;
  }
  assert(w[0]==w[1]);
  if(score[0]!=score[1])mismatched++;
  for(int a=0;a<8;a++){
   uint32_t index=(uint64_t)r*inverse[a]&MASK;
   assert(((uint64_t)index*forward[a]&MASK)==r);
   for(int q=0;q<2;q++)if(score[q]<=174+485*a){
    counts[q][a]++;bits[q][a][index/64]|=1ull<<(index%64);
   }
   if(score[0]>174+485*a && score[1]<=174+485*a)gaps[0][a]++;
   if(score[1]>174+485*a && score[0]<=174+485*a)gaps[1][a]++;
  }
 }
 assert(mismatched==399426);
 uint64_t oc=0,uc=0;
 for(int a=0;a<8;a++)for(int q=0;q<2;q++){
  auto &v=bits[q][a];v[WORDS]=v[0];uint64_t total=0;
  for(uint32_t j=0;j<WORDS;j++)total+=__builtin_popcountll(v[j]);
  assert(total==counts[q][a] && v[WORDS]==v[0]);
  assert(counts[q][a]==(q?odd:old)[a]);
  assert(gaps[q][a]==(q?under:over)[a]);
 }
 for(int a=0;a<8;a++){oc+=gaps[0][a];uc+=gaps[1][a];}
 assert(oc==63015 && uc==11401);
 for(uint32_t r: {0u,1u,109u,13704093u,MASK})for(int a=0;a<8;a++){
  uint32_t p=(uint64_t)r*inverse[a]&MASK;
  for(uint32_t lift=0;lift<64;lift++){
   uint32_t expected=(p+lift)&MASK;
   uint32_t shifted=((uint64_t)((r+(uint64_t)lift*forward[a])&MASK)*inverse[a])&MASK;
   assert(expected==shifted);
   uint64_t w0=bits[0][a][p/64],w1=bits[0][a][p/64+1];
   bool via_window=((lift+(p%64)<64?w0:w1)>>((lift+p%64)%64))&1u;
   bool via_direct=(bits[0][a][expected/64]>>(expected%64))&1u;
   assert(via_window==via_direct);
  }
 }
 std::printf("R39_INDEPENDENT_BITMAP_PASS residues=%u parity_states=2 mismatched=%llu source_clear_corrected_live=%llu source_live_corrected_clear=%llu padded_lifts=64\n",
  LIM,(unsigned long long)mismatched,(unsigned long long)oc,(unsigned long long)uc);
}
