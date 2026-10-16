// R45: independent 9*2048*256 phase oracle for each of seven new classes.
// Bounded mathematical source model, not native binary or global frontier certification.
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
using std::uint32_t;
using std::uint64_t;
struct Class {int f,flag,q,min,max;uint64_t sum;std::array<uint32_t,18> hist;};
static constexpr Class classes[] = {
 {38,0,0,2,10,116480,{0,0,71,752,1483,3506,4117,3971,3169,861,502}},
 {38,0,1,2,10,116480,{0,0,71,752,1483,3506,4117,3971,3169,861,502}},
 {38,0,2,2,10,116480,{0,0,71,752,1483,3506,4117,3971,3169,861,502}},
 {39,0,1,5,17,206080,{0,0,0,0,0,49,90,485,1844,2509,1677,2914,3744,2627,1269,747,416,61}},
 {40,0,0,7,16,197120,{0,0,0,0,0,0,0,500,1743,2568,4281,3344,2716,1883,1117,219,61}},
 {40,0,1,7,16,197120,{0,0,0,0,0,0,0,500,1743,2568,4281,3344,2716,1883,1117,219,61}},
 {41,0,0,3,9,107520,{0,0,0,899,1860,4590,4538,5161,1378,6}}
};
static uint32_t p3[67];static int p2[67];
struct State {int f,flag,q,r9;uint32_t num;};
static bool eligible(int i,int f,int q){
 return 306*i<485*f&&!(q>=2&&q%2==0&&306*(i-1)>=485*(f-1));
}
static bool admitted(int r){return r==0||r==1||r==3||r==6||r==7;}
static bool step(int i,int bit,State &s){
 const uint32_t mask=(uint32_t(1)<<(66-i+3))-1u;
 const uint32_t x=(s.num+(bit?p3[s.f]:0u))&mask;
 const bool odd=((s.num&1u)==0u)!=bool(bit);
 const int f_old=s.f;
 s.r9=(s.r9+bit*p2[i])%9;
 if(odd){
  s.f++;s.flag=(s.flag|(306*(i+1)>=485*f_old))&~2;s.q=0;
  s.num=(x+x/2u)&(mask>>1);
 }else{
  if(s.flag>=2)return false;
  s.flag<<=1;s.q++;s.num=(x/2u+1u)&(mask>>1);
 }
 return eligible(i+1,s.f,s.q);
}
static int canonical_a(const State &s){
 if(s.f!=43||s.flag!=0||(s.q&1)==0)return -1;
 const int residue=(3*(1-int(s.num)))&7;
 if(!residue)return -1;
 const int a=32+residue;
 // 3^43 == 3 mod8:  T^66(original) = num-1+a*3^43 ==0 mod8.
 if(((int(s.num)-1+3*a)&7)!=0)std::abort();
 return a;
}
int main(){
 p3[0]=1;p2[0]=1;
 for(int i=1;i<67;i++){p3[i]=p3[i-1]*3u;p2[i]=p2[i-1]*2%9;}
 uint64_t all_probes=0,all_phases=0;
 for(const Class &c:classes){
  std::array<uint32_t,257> h{};
  uint64_t probes=0,phases=0,sum=0;
  int min=257,max=0;
  for(int r9=0;r9<9;r9++)for(int num=0;num<2048;num++){
   int hits=0;
   for(int bits=0;bits<256;bits++){
    State s{c.f,c.flag,c.q,r9,uint32_t(num)};
    bool ok=true;
    for(int i=58;i<66;i++)if(!step(i,(bits>>(i-58))&1,s)){ok=false;break;}
    ++probes;
    if(!ok)continue;
    const int a=canonical_a(s);
    if(a>=0&&admitted((s.r9+a)%9))++hits;
   }
   ++h[hits];++phases;sum+=hits;
   if(hits<min)min=hits;
   if(hits>max)max=hits;
  }
  if(probes!=4718592ull||phases!=18432ull||min!=c.min||max!=c.max||sum!=c.sum){
   std::fprintf(stderr,"R45_PHASE_FAIL state=%d,%d,%d probes=%llu phases=%llu min=%d max=%d sum=%llu\n",c.f,c.flag,c.q,(unsigned long long)probes,(unsigned long long)phases,min,max,(unsigned long long)sum);
   return EXIT_FAILURE;
  }
  for(int i=0;i<257;i++)if(h[i]!=(i<18?c.hist[i]:0))return EXIT_FAILURE;
  all_probes+=probes;all_phases+=phases;
  std::printf("R45_INDEPENDENT_CLASS_PASS state=%d,%d,%d probes=4718592 phases=18432 min=%d max=%d sum=%llu\n",c.f,c.flag,c.q,min,max,(unsigned long long)sum);
 }
 if(all_probes!=33030144ull||all_phases!=129024ull)return EXIT_FAILURE;
 std::puts("R45_INDEPENDENT_ALL_PASS classes=7 probes=33030144 phases=129024");
 return EXIT_SUCCESS;
}
