from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve()
module=root/'src/world/patrol-routing-pwa12-104-city-candidate-08.js'
module.write_text(r'''if(typeof window!=='undefined'){
(() => {
'use strict';
const VERSION='pwa12.104-city-candidate.08';
const T={PARCEL:0,ART:1,SEC:2,ALLEY:3,PLAZA:4,YARD:5,ROUGH:6,WATER:7,RAIL:8,BRIDGE:9,TUNNEL:10,PARK:11,INDUSTRIAL:12,PED:13,TRANSIT:14,BUILDING:15,WALL:16};
const BASE={[T.ART]:1,[T.SEC]:1.10,[T.ALLEY]:1.28,[T.PLAZA]:1.16,[T.YARD]:1.55,[T.ROUGH]:3.40,[T.RAIL]:1.72,[T.BRIDGE]:1.05,[T.TUNNEL]:1.18,[T.PARK]:1.75,[T.INDUSTRIAL]:1.85,[T.PED]:1.08,[T.TRANSIT]:1.0};
const PROFILES={
 fast:{id:'fast',name:'FAST',tag:'SHORTEST STREET LINE',desc:'Prioritizes distance and normal street speed. Accepts patrol and territorial exposure.'},
 low:{id:'low',name:'LOW PROFILE',tag:'MINIMIZE EXPOSURE',desc:'Trades distance for streets with less security, gang and local-heat pressure.'},
 back:{id:'back',name:'BACK ALLEY',tag:'ALLEYS · TUNNELS · SERVICE WAYS',desc:'Prefers alleys, tunnels, pedestrian cuts and industrial/service terrain even when the route is longer.'}
};
const FACTORS={
 low:{[T.ART]:1.08,[T.SEC]:1.24,[T.ALLEY]:.92,[T.PLAZA]:1.18,[T.YARD]:.98,[T.ROUGH]:1.05,[T.RAIL]:.98,[T.BRIDGE]:1.08,[T.TUNNEL]:.84,[T.PARK]:.92,[T.INDUSTRIAL]:.92,[T.PED]:.90,[T.TRANSIT]:1.20},
 back:{[T.ART]:1.54,[T.SEC]:1.82,[T.ALLEY]:.58,[T.PLAZA]:1.62,[T.YARD]:.68,[T.ROUGH]:.94,[T.RAIL]:.82,[T.BRIDGE]:1.20,[T.TUNNEL]:.58,[T.PARK]:.80,[T.INDUSTRIAL]:.70,[T.PED]:.72,[T.TRANSIT]:1.70}
};
const WEIGHTS={low:{security:5.2,gang:3.5},back:{security:4.0,gang:2.45}};
function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
function copy(v){return v==null?v:JSON.parse(JSON.stringify(v))}
function nowMin(){return Math.round((((Game.day||1)-1)*24+(Game.hour||0))*60)}
function world(){return window.currentDistrictV133?.()||null}
function state(){
 const s=window.ensureLivingStreetsStateV134?.()||(Game.livingStreetsV134=Game.livingStreetsV134||{});
 s.patrolRouting=s.patrolRouting||{version:1,activeRoute:null,history:[],stats:{planned:0,committed:0,resumed:0,completed:0,exposureSteps:0}};
 const x=s.patrolRouting;x.history=x.history||[];x.stats=x.stats||{};for(const k of ['planned','committed','resumed','completed','exposureSteps'])x.stats[k]=Number(x.stats[k]||0);return x
}
let PREVIEW=null,OVERRIDE=null,CORRIDOR_CACHE=null,RISK_CACHE=null;
function terrain(world,x,y){return x>=0&&y>=0&&x<world.w&&y<world.h?world.terrain[y*world.w+x]:T.WALL}
function walkable(world,x,y){return BASE[terrain(world,x,y)]!==undefined}
function neighborhoodState(world){return window.ensureNeighborhoodStateV134?.(world)||{}}
function nearestNeighborhood(world,p){let best=null,bd=Infinity;for(const n of world?.neighborhoods||[]){const d=Math.hypot((p?.x||0)-n.x,(p?.y||0)-n.y);if(d<bd){bd=d;best=n}}return best}
function nearestPoint(points,n){let best=null,bd=Infinity;for(const p of points||[]){const d=Math.hypot(p.x-n.x,p.y-n.y);if(d<bd&&d>1){bd=d;best=p}}return best}
function corridorSignature(world){
 const ns=neighborhoodState(world);let k=world.id;for(const n of world.neighborhoods||[]){const h=ns[n.id]||{};k+=`|${n.id}:${Math.round(h.localHeat||0)}:${h.security||0}:${h.gangPressure||0}:${h.unrest||0}:${h.controller||''}`}
 const posts=window.controlPostsForWorldV12104?.(world)||[];for(const p of posts)k+=`|cp:${p.linkId}:${p.profile?.actor||''}`;return k
}
function patrolCorridors(world=window.currentDistrictV133?.()){
 if(!world)return[];const key=corridorSignature(world);if(CORRIDOR_CACHE?.key===key)return CORRIDOR_CACHE.value;
 const ns=neighborhoodState(world),out=[],transit=(world.transit||[]).map(x=>({x:x.x,y:x.y,id:x.id})),locs=Object.values(world.locations||{}).map(x=>({x:x.x,y:x.y,id:x.id}));
 for(const n of world.neighborhoods||[]){const h=ns[n.id]||{},sec=clamp(Math.max(0,(Number(h.security||0)-2)/3)*.58+Number(h.localHeat||0)/100*.68,0,1),gang=clamp(Math.max(0,(Number(h.gangPressure||0)-2)/3)*.68+Number(h.unrest||0)/5*.34,0,1);
   if(sec>=.34){const a=nearestPoint(transit.length?transit:locs,n);if(a)out.push({id:`sec:${n.id}`,actor:'security',neighborhood:n.id,ax:n.x,ay:n.y,bx:a.x,by:a.y,width:5.5+sec*8,strength:sec})}
   if(gang>=.38){const a=nearestPoint(locs.length?locs:transit,n);if(a)out.push({id:`gang:${n.id}`,actor:'gang',neighborhood:n.id,ax:n.x,ay:n.y,bx:a.x,by:a.y,width:4.8+gang*7,strength:gang})}
 }
 for(const p of window.controlPostsForWorldV12104?.(world)||[]){const n=nearestNeighborhood(world,p),actor=p.profile?.actor==='gang'?'gang':'security';if(n)out.push({id:`post:${p.linkId}`,actor,neighborhood:n.id,ax:p.x,ay:p.y,bx:n.x,by:n.y,width:8.5,strength:1,controlPost:true})}
 CORRIDOR_CACHE={key,value:out};RISK_CACHE=null;return out
}
window.patrolCorridorsForWorldV12104=patrolCorridors;
function pointSegDist(px,py,a){const vx=a.bx-a.ax,vy=a.by-a.ay,wx=px-a.ax,wy=py-a.ay,d=vx*vx+vy*vy;if(!d)return Math.hypot(wx,wy);const t=clamp((wx*vx+wy*vy)/d,0,1),x=a.ax+vx*t,y=a.ay+vy*t;return Math.hypot(px-x,py-y)}
function riskGrid(world=window.currentDistrictV133?.()){
 if(!world)return null;const corridors=patrolCorridors(world),key=(CORRIDOR_CACHE?.key||corridorSignature(world))+':risk';if(RISK_CACHE?.key===key)return RISK_CACHE.value;
 const N=world.w*world.h,security=new Float32Array(N),gang=new Float32Array(N),ns=neighborhoodState(world);
 for(let y=0;y<world.h;y++)for(let x=0;x<world.w;x++){const idx=y*world.w+x;if(BASE[world.terrain[idx]]===undefined)continue;const n=nearestNeighborhood(world,{x,y}),h=n?ns[n.id]||{}:{},baseSec=Math.max(0,(Number(h.security||0)-2)/3)*.18+Number(h.localHeat||0)/100*.24,baseGang=Math.max(0,(Number(h.gangPressure||0)-2)/3)*.18+Number(h.unrest||0)/5*.14;let se=baseSec,ga=baseGang;for(const c of corridors){const d=pointSegDist(x,y,c);if(d>=c.width)continue;const v=c.strength*(1-d/c.width);if(c.actor==='security')se=Math.max(se,v);else ga=Math.max(ga,v)}security[idx]=clamp(se,0,1);gang[idx]=clamp(ga,0,1)}
 const value={security,gang,corridors};RISK_CACHE={key,value};return value
}
window.patrolRiskGridV12104=riskGrid;
class Heap{constructor(){this.a=[]}get size(){return this.a.length}push(n){const a=this.a;a.push(n);let i=a.length-1;while(i>0){const p=(i-1)>>1;if(a[p].s<=n.s)break;a[i]=a[p];i=p}a[i]=n}pop(){const a=this.a;if(!a.length)return null;const r=a[0],last=a.pop();if(a.length){let i=0;a[0]=last;for(;;){let l=i*2+1,rr=l+1,s=i;if(l<a.length&&a[l].s<a[s].s)s=l;if(rr<a.length&&a[rr].s<a[s].s)s=rr;if(s===i)break;[a[i],a[s]]=[a[s],a[i]];i=s}}return r}}
function findRiskPath(start,goal,profile='low',w=window.currentDistrictV133?.()){
 if(!w||!start||!goal||!walkable(w,goal.x,goal.y)||!walkable(w,start.x,start.y))return null;if(profile==='fast')return window.findDistrictPathV133?.(start,goal,w)||null;
 const factors=FACTORS[profile]||FACTORS.low,weights=WEIGHTS[profile]||WEIGHTS.low,rg=riskGrid(w),W=w.w,H=w.h,N=W*H,INF=1e20,g=new Float64Array(N),parent=new Int32Array(N),closed=new Uint8Array(N);g.fill(INF);parent.fill(-1);
 const si=start.y*W+start.x,gi=goal.y*W+goal.x,hp=new Heap(),heur=(x,y)=>Math.hypot(goal.x-x,goal.y-y)*.52;g[si]=0;hp.push({i:si,s:heur(start.x,start.y)});const dirs=[[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]];let guard=0;
 while(hp.size&&guard++<N*4){const q=hp.pop(),cur=q.i;if(closed[cur])continue;closed[cur]=1;if(cur===gi)break;const cx=cur%W,cy=(cur/W)|0;for(const[dx,dy]of dirs){const nx=cx+dx,ny=cy+dy;if(nx<0||ny<0||nx>=W||ny>=H||!walkable(w,nx,ny))continue;if(dx&&dy&&(!walkable(w,cx+dx,cy)||!walkable(w,cx,cy+dy)))continue;const ni=ny*W+nx;if(closed[ni])continue;const tv=terrain(w,nx,ny),diag=dx&&dy?1.414:1,base=BASE[tv]*(factors[tv]??1),ex=rg.security[ni]*weights.security+rg.gang[ni]*weights.gang,ng=g[cur]+(base+ex)*diag;if(ng>=g[ni])continue;g[ni]=ng;parent[ni]=cur;hp.push({i:ni,s:ng+heur(nx,ny)})}}
 if(si!==gi&&parent[gi]===-1)return null;const path=[];let cur=gi;while(cur!==-1){path.push({x:cur%W,y:(cur/W)|0});if(cur===si)break;cur=parent[cur]}return path.reverse()
}
window.findRiskAwareDistrictPathV12104=findRiskPath;
function analyze(path,w=window.currentDistrictV133?.()){
 if(!path?.length||!w)return null;const rg=riskGrid(w);let se=0,ga=0,max=0,hot=0;for(const p of path){const i=p.y*w.w+p.x,s=rg.security[i]||0,g=rg.gang[i]||0;se+=s;ga+=g;const v=Math.max(s,g);max=Math.max(max,v);if(v>=.58)hot++}const n=path.length;return{cells:Math.max(0,n-1),security:Math.round(se/n*100),gang:Math.round(ga/n*100),exposure:Math.round((se*.62+ga*.38)/n*100),peak:Math.round(max*100),hotCells:hot}}
function planRoutes(goal,target={kind:'point',label:'STREET DESTINATION'},w=window.currentDistrictV133?.()){
 if(!w||!Game.ovPlayer||!goal)return null;const fast=findRiskPath(Game.ovPlayer,goal,'fast',w),low=findRiskPath(Game.ovPlayer,goal,'low',w),back=findRiskPath(Game.ovPlayer,goal,'back',w);if(!fast?.length)return null;const plans={};for(const[id,p]of Object.entries({fast,low,back}))if(p?.length){const a=analyze(p,w);plans[id]={profile:id,path:p,analysis:{...a,detour:id==='fast'?0:Math.round((a.cells-Math.max(1,fast.length-1))/Math.max(1,fast.length-1)*100)}}}return{worldId:w.id,goal:{x:goal.x,y:goal.y},target:copy(target),plans,corridors:patrolCorridors(w).length}
}
window.planPatrolRoutesV12104=planRoutes;
function ensureStyle(){if(document.getElementById('v12104-patrol-routing-style'))return;const s=document.createElement('style');s.id='v12104-patrol-routing-style';s.textContent=`#v12104-route-planner{position:fixed;z-index:10055;left:50%;bottom:14px;transform:translateX(-50%);width:min(430px,calc(100vw - 24px));max-height:min(80vh,690px);overflow:auto;background:rgba(3,7,11,.98);border:1px solid rgba(75,194,230,.72);box-shadow:0 16px 52px rgba(0,0,0,.72),0 0 30px rgba(75,194,230,.12);padding:12px;color:#dce7eb;font:12px/1.42 Share Tech Mono,monospace}#v12104-route-planner[hidden]{display:none!important}#v12104-route-planner h3{margin:0 0 4px;color:#8fe3ff;font:800 14px/1.2 Orbitron,sans-serif;letter-spacing:.06em}#v12104-route-planner .rp-sub{color:#91a5ad;margin-bottom:9px}#v12104-route-planner .rp-card{display:block;width:100%;text-align:left;margin:7px 0;padding:9px;border:1px solid rgba(143,227,255,.26);background:rgba(143,227,255,.055);min-height:64px;white-space:normal}#v12104-route-planner .rp-card b{display:block;color:#f0f7f9;font:800 12px Orbitron,sans-serif}#v12104-route-planner .rp-card small{display:block;color:#91a5ad;margin-top:3px;font:10px/1.35 Share Tech Mono,monospace}#v12104-route-planner .rp-metrics{display:block;margin-top:5px;color:#c8d8de}#v12104-route-planner .rp-close{width:100%;min-height:44px;margin-top:6px}#v12104-route-planner .rp-intel{padding:7px 8px;border-left:2px solid #5ec8ff;background:rgba(94,200,255,.06);font-size:10px;color:#9eb4bd}@media(max-width:520px){#v12104-route-planner{bottom:8px;width:calc(100vw - 20px);padding:10px;max-height:74vh}#v12104-route-planner .rp-card{min-height:68px}#v12104-route-planner .rp-close{min-height:46px}}`;document.head.appendChild(s)}
function ensurePanel(){ensureStyle();let p=document.getElementById('v12104-route-planner');if(!p){p=document.createElement('section');p.id='v12104-route-planner';p.hidden=true;document.body.appendChild(p)}return p}
function hidePlanner(){const p=document.getElementById('v12104-route-planner');if(p)p.hidden=true;PREVIEW=null;Game.ovStaticDirty=true}
window.closePatrolRoutePlannerV12104=hidePlanner;
function routeMetric(p){const a=p.analysis,d=a.detour>0?` · +${a.detour}% detour`:a.detour<0?` · ${a.detour}% distance`:'';return`${a.cells} cells${d} · exposure ${a.exposure} · SEC ${a.security} · GANG ${a.gang}`}
function openPlanner(goal,target={kind:'point',label:'STREET DESTINATION'}){
 const p=planRoutes(goal,target);if(!p||p.plans.fast?.path?.length<2)return false;PREVIEW=p;state().stats.planned++;const box=ensurePanel();box.hidden=false;box.innerHTML=`<h3>ROUTE TACTICS</h3><div class="rp-sub">${target?.label||'STREET DESTINATION'} · ${p.corridors} ACTIVE PATROL CORRIDORS</div><div class="rp-intel">Live route intelligence combines Local Heat, Security, Gang Pressure, Unrest and physical control-post pressure. Route choice changes the streets the crew actually walks.</div>`;for(const id of ['fast','low','back']){const q=p.plans[id];if(!q)continue;const prof=PROFILES[id],b=document.createElement('button');b.className='btn rp-card';b.id=`v12104-route-${id}`;b.innerHTML=`<b>${prof.name} · ${prof.tag}</b><span class="rp-metrics">${routeMetric(q)}</span><small>${prof.desc}</small>`;b.onclick=()=>commitRoute(id);box.appendChild(b)}const x=document.createElement('button');x.className='btn small rp-close';x.id='v12104-route-cancel';x.textContent='CANCEL ROUTE';x.onclick=hidePlanner;box.appendChild(x);Game.ovStaticDirty=true;return true
}
window.openPatrolRoutePlannerV12104=openPlanner;
function takeOverride(p,target,w){if(!OVERRIDE||OVERRIDE.worldId!==w?.id||OVERRIDE.goal.x!==p?.x||OVERRIDE.goal.y!==p?.y)return null;const x=OVERRIDE;OVERRIDE=null;return x}
window.takePatrolRouteOverrideV12104=takeOverride;
function commitRoute(profile,{resume=false}={}){
 const p=PREVIEW?.plans?.[profile];if(!PREVIEW||!p||!window.routeToPointV133)return false;const snap=PREVIEW;OVERRIDE={owner:'patrolRouting',worldId:snap.worldId,goal:copy(snap.goal),target:copy(snap.target),profile,path:p.path.map(q=>({x:q.x,y:q.y})),analysis:copy(p.analysis),resume:!!resume};const goal=copy(snap.goal),target=copy(snap.target);hidePlanner();const ok=window.routeToPointV133(goal,target);if(!ok)OVERRIDE=null;return !!ok
}
window.commitPatrolRouteV12104=commitRoute;
const prevCommitted=window.onPhysicalRouteCommittedV12104;window.onPhysicalRouteCommittedV12104=function(ctx){const r=prevCommitted?.apply(this,arguments);const st=state(),o=ctx?.override;if(o?.owner==='patrolRouting'){st.activeRoute={district:ctx.worldId,goal:copy(o.goal),target:copy(o.target),profile:o.profile,analysis:copy(o.analysis),startedAt:o.resume?(st.activeRoute?.startedAt||nowMin()):nowMin(),lastExposure:0,maxExposure:st.activeRoute?.maxExposure||0};if(o.resume)st.stats.resumed++;else{st.stats.committed++;st.history.unshift({type:'route',district:ctx.worldId,profile:o.profile,goal:copy(o.goal),analysis:copy(o.analysis),at:nowMin()});st.history=st.history.slice(0,48);window.streetToastV134?.(`${PROFILES[o.profile]?.name||o.profile} · ${o.analysis?.cells||ctx.path?.length||0} CELLS · EXPOSURE ${o.analysis?.exposure??'—'}`);window.saveGame?.(0,true)}}else if(st.activeRoute&&st.activeRoute.district===ctx?.worldId){st.activeRoute=null}return r};
function resumeActive(){const st=state(),a=st.activeRoute,w=world();if(!a||!w||a.district!==w.id||!Game.ovPlayer)return false;if(Game.livingStreetsV134?.controlPosts?.approach||Game.livingStreetsV134?.transitIncidents?.active)return false;if(Math.hypot(Game.ovPlayer.x-a.goal.x,Game.ovPlayer.y-a.goal.y)<=1.2){st.activeRoute=null;return false}const plan=planRoutes(a.goal,a.target,w),p=plan?.plans?.[a.profile];if(!p)return false;PREVIEW=plan;return commitRoute(a.profile,{resume:true})}
window.resumePatrolRouteV12104=resumeActive;
function routeStep(w=world()){const st=state(),a=st.activeRoute;if(!a||!w||a.district!==w.id||!Game.ovPlayer)return;const rg=riskGrid(w),i=Game.ovPlayer.y*w.w+Game.ovPlayer.x,se=rg?.security?.[i]||0,ga=rg?.gang?.[i]||0,ex=clamp(se*.62+ga*.38,0,1);a.lastExposure=Math.round(ex*100);a.maxExposure=Math.max(Number(a.maxExposure||0),a.lastExposure);if(ex>=.55)st.stats.exposureSteps++;if(Math.hypot(Game.ovPlayer.x-a.goal.x,Game.ovPlayer.y-a.goal.y)<=1.2){st.history.unshift({type:'complete',district:w.id,profile:a.profile,maxExposure:a.maxExposure,at:nowMin()});st.history=st.history.slice(0,48);st.stats.completed++;st.activeRoute=null}}
function screen(p){return window.worldToScreen?.(p.x,p.y)||null}
function drawLine(ctx,pts,stroke,width,dash=[]){if(!pts?.length)return;ctx.save();ctx.strokeStyle=stroke;ctx.lineWidth=width;ctx.setLineDash(dash);ctx.beginPath();let started=false;for(let i=0;i<pts.length;i+=Math.max(1,Math.floor(pts.length/80))){const s=screen({x:pts[i].x+.5,y:pts[i].y+.5});if(!s)continue;if(!started){ctx.moveTo(s.x,s.y);started=true}else ctx.lineTo(s.x,s.y)}ctx.stroke();ctx.restore()}
function drawOverlay(ctx,w,W,H,t){if(!ctx||!w)return;const cs=patrolCorridors(w);for(const c of cs){const a=screen({x:c.ax+.5,y:c.ay+.5}),b=screen({x:c.bx+.5,y:c.by+.5});if(!a||!b)continue;ctx.save();ctx.globalAlpha=.18+.15*c.strength;ctx.strokeStyle=c.actor==='security'?'#5ec8ff':'#ff755e';ctx.lineWidth=Math.max(4,(c.width||6)*Math.max(.45,t*.06));ctx.setLineDash(c.actor==='security'?[9,7]:[4,6]);ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();ctx.restore()}
 if(PREVIEW?.worldId===w.id){drawLine(ctx,PREVIEW.plans.fast?.path,'rgba(255,210,93,.72)',2,[8,5]);drawLine(ctx,PREVIEW.plans.low?.path,'rgba(94,200,255,.82)',2.4,[4,4]);drawLine(ctx,PREVIEW.plans.back?.path,'rgba(178,118,255,.82)',2.4,[2,5])}}
window.drawPatrolRoutingV12104=drawOverlay;
const prevDraw=window.drawLivingStreetsV134;if(prevDraw)window.drawLivingStreetsV134=function(ctx,w,W,H,t,hover){const r=prevDraw.apply(this,arguments);drawOverlay(ctx,w,W,H,t);return r};
const prevStep=window.onStreetStepV134;if(prevStep)window.onStreetStepV134=function(w){const r=prevStep.apply(this,arguments);routeStep(w);return r};
const prevInit=window.initOverworldV133;if(prevInit){const wrapped=function(){const r=prevInit.apply(this,arguments);setTimeout(()=>resumeActive(),0);return r};window.initOverworldV133=wrapped;if(window.initOverworld===prevInit)window.initOverworld=wrapped}
ensureStyle();window.CR_CITY_PATROL_ROUTING={version:VERSION,state,patrolCorridors,riskGrid,findRiskPath,planRoutes,openPlanner,commitRoute,resumeActive};
})();
}''',encoding='utf-8')

# Register after Candidate 07 and before mission approaches.
manifest=root/'src/bootstrap/module-manifest.js'
s=manifest.read_text(encoding='utf-8')
entry="  'world.patrolRouting':{path:'./src/world/patrol-routing-pwa12-104-city-candidate-08.js',kind:'module'},\n"
if 'world.patrolRouting' not in s:
    needle="  'world.controlPosts':{path:'./src/world/district-control-posts-pwa12-104-city-candidate-07.js',kind:'module'},\n"
    if needle not in s:raise SystemExit('Candidate 07 manifest seam missing')
    s=s.replace(needle,needle+entry,1)
    order="'world.accessEcology','world.transitIncidents','world.controlPosts','missions.approaches'"
    if order not in s:raise SystemExit('Candidate 07 manifest order seam missing')
    s=s.replace(order,"'world.accessEcology','world.transitIncidents','world.controlPosts','world.patrolRouting','missions.approaches'",1)
manifest.write_text(s,encoding='utf-8')

# Runtime bundle markers are the actual ordered-source authority.
bundle=root/'src/runtime/runtime-bundle.js'
s=bundle.read_text(encoding='utf-8')
cp='/* SOURCE: src/world/district-control-posts-pwa12-104-city-candidate-07.js */'
pr='/* SOURCE: src/world/patrol-routing-pwa12-104-city-candidate-08.js */'
mission='/* SOURCE: src/missions/contract-approaches-v13-4b.js */'
if cp not in s or mission not in s:raise SystemExit('Candidate 07 runtime-bundle seam missing')
if pr not in s:s=s.replace(mission,pr+'\n'+mission,1)
pos=[s.index(x) for x in (cp,pr,mission)]
if pos!=sorted(pos):raise SystemExit(f'Candidate 08 runtime order invalid: {pos}')
bundle.write_text(s,encoding='utf-8')

# Add a narrow route-override seam to the canonical physical route authority. Existing
# programmatic routes get no override and behave exactly as before; selected patrol routes
# still pass through the canonical scheduler/camera/long-route lifecycle.
p=root/'src/world/district-worlds-v13-3.js'
s=p.read_text(encoding='utf-8')
old=" const world=currentDistrictV133(),path=findDistrictPathV133(Game.ovPlayer,p,world);if(!path||path.length<2){if(path?.length===1&&target?.kind==='location')openDistrictLocationV133(target.id);else if(path?.length===1&&target?.kind==='transit')openTransitNodeV133(target.id);else toast('No route.');return false}"
new=" const world=currentDistrictV133(),routeOverride=window.takePatrolRouteOverrideV12104?.(p,target,world)||null,path=routeOverride?.path||findDistrictPathV133(Game.ovPlayer,p,world);if(!path||path.length<2){if(path?.length===1&&target?.kind==='location')openDistrictLocationV133(target.id);else if(path?.length===1&&target?.kind==='transit')openTransitNodeV133(target.id);else toast('No route.');return false}"
if 'takePatrolRouteOverrideV12104' not in s:
    if old not in s:raise SystemExit('canonical routeToPoint path seam missing')
    s=s.replace(old,new,1)
old2=" Game.pendingPath=path;Game._v133TravelTarget=target;Game.ovCamera.follow=true;scheduleOverworldFrameV133(0);if(path.length>60&&Math.random()<.18)Game.storyFlags._pendingTravelEvent=path.length;updateRouteCardV133();updateCameraModeV133();return true"
new2=" Game.pendingPath=path;Game._v133TravelTarget=target;Game.ovCamera.follow=true;scheduleOverworldFrameV133(0);if(path.length>60&&Math.random()<.18)Game.storyFlags._pendingTravelEvent=path.length;updateRouteCardV133();updateCameraModeV133();window.onPhysicalRouteCommittedV12104?.({point:{x:p.x,y:p.y},target,path,worldId:world.id,override:routeOverride});return true"
if 'onPhysicalRouteCommittedV12104' not in s:
    if old2 not in s:raise SystemExit('canonical routeToPoint commit seam missing')
    s=s.replace(old2,new2,1)
if 'window.routeToPointV133=routeToPointV133' not in s:
    needle="function routeToLocationV133(id){"
    if needle not in s:raise SystemExit('routeToLocation export seam missing')
    s=s.replace(needle,"window.routeToPointV133=routeToPointV133;\n"+needle,1)

# Only direct map taps get the new planner. Existing dispatch/control-post/service code that
# calls routeToLocationV133/routeToTransitNodeV133 remains deterministic and unchanged.
old3="else{mark.kind==='transit'?routeToTransitNodeV133(mark.id):routeToLocationV133(mark.id)}return}"
new3="else{const rt={kind:mark.kind==='transit'?'transit':'location',id:mark.id,label:mark.label||mark.id};if(window.openPatrolRoutePlannerV12104?.({x:mark.x,y:mark.y},rt))return;mark.kind==='transit'?routeToTransitNodeV133(mark.id):routeToLocationV133(mark.id)}return}"
if 'openPatrolRoutePlannerV12104?.({x:mark.x' not in s:
    if old3 not in s:raise SystemExit('manual marker routing seam missing')
    s=s.replace(old3,new3,1)
old4="if(!isWalkableV133(q.x,q.y)){toast('Blocked.');return}routeToPointV133(q,{kind:'point',label:`${q.x},${q.y}`})"
new4="if(!isWalkableV133(q.x,q.y)){toast('Blocked.');return}const rt={kind:'point',label:`${q.x},${q.y}`};if(window.openPatrolRoutePlannerV12104?.(q,rt))return;routeToPointV133(q,rt)"
if "openPatrolRoutePlannerV12104?.(q,rt)" not in s:
    if old4 not in s:raise SystemExit('manual free-point routing seam missing')
    s=s.replace(old4,new4,1)
p.write_text(s,encoding='utf-8')
print('applied Candidate 08 Patrol Corridors + Risk-Aware Physical Route Choice')