from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve()
module=root/'src/world/patrol-corridors-pwa12-104-city-candidate-08.js'
module.write_text(r'''if(typeof window!=='undefined'){
(() => {
'use strict';
const VERSION='pwa12.104-city-candidate.08';
const MODES={
 fast:{id:'fast',label:'FAST',desc:'Shortest physical street route. Time first; exposure accepted.'},
 low:{id:'low',label:'LOW PROFILE',desc:'Avoids security pressure, local heat and known control infrastructure.'},
 back:{id:'back',label:'BACK ALLEY',desc:'Maximum surveillance avoidance; accepts longer streets and rougher territory.'}
};
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const copy=v=>v==null?v:JSON.parse(JSON.stringify(v));
const world=()=>window.currentDistrictV133?.()||null;
const canonical=(a,b,w=world())=>window.findDistrictPathV133?.(a,b,w)||null;
function state(){
 const s=window.ensureLivingStreetsStateV134?.()||(Game.livingStreetsV134=Game.livingStreetsV134||{});
 s.patrolCorridors=s.patrolCorridors||{version:1,preference:'fast',familiarity:{},history:[],stats:{planned:0,switched:0,steps:0}};
 const p=s.patrolCorridors;p.version=1;if(!MODES[p.preference])p.preference='fast';p.familiarity=p.familiarity||{};p.history=p.history||[];p.stats=p.stats||{};
 for(const k of ['planned','switched','steps'])p.stats[k]=Number(p.stats[k]||0);return p
}
function nearestHood(w,p){let best=null,bd=Infinity;for(const n of w?.neighborhoods||[]){const d=Math.hypot(Number(p?.x||0)-n.x,Number(p?.y||0)-n.y);if(d<bd){bd=d;best=n}}return best}
function hoodState(w,n){return n?window.ensureNeighborhoodStateV134?.(w)?.[n.id]||null:null}
function familiarity(w,n){return Number(state().familiarity?.[w?.id]?.[n?.id]||0)}
function markFamiliar(w,p){if(!w||!p)return 0;const n=nearestHood(w,p);if(!n)return 0;const st=state();st.familiarity[w.id]=st.familiarity[w.id]||{};const v=clamp(Number(st.familiarity[w.id][n.id]||0)+1,0,18);st.familiarity[w.id][n.id]=v;st.stats.steps++;return v}
function actorSide(a){const t=String(a?.type||'').toLowerCase();if(/security|patrol|corp|meridian|guard|cop|drone/.test(t))return'security';if(/gang|iron|raider|thug|jack|wraith/.test(t))return'gang';return null}
function patrolSources(w=world()){
 if(!w)return[];const out=[];
 for(const p of window.controlPostsForWorldV12104?.(w)||[])out.push({kind:'post',side:p.profile?.actor==='gang'?'gang':'security',x:p.x,y:p.y,radius:11,power:1,label:p.profile?.title||'CONTROL POST'});
 for(const a of window.ensureStreetActorsV134?.(w)||[]){const side=actorSide(a);if(side)out.push({kind:'actor',side,x:a.x,y:a.y,radius:6,power:.55,label:String(a.type||side).toUpperCase()})}
 return out
}
function exposureAt(w,p,sources=patrolSources(w)){
 const n=nearestHood(w,p),h=hoodState(w,n)||{},security=clamp(Number(h.security||0)/5,0,1),heat=clamp(Number(h.localHeat||0)/100,0,1),gang=clamp(Number(h.gangPressure||0)/5,0,1),unrest=clamp(Number(h.unrest||0)/5,0,1);let patrol=0,post=0;
 for(const s of sources){const d=Math.hypot(p.x-s.x,p.y-s.y);if(d>=s.radius)continue;const v=(1-d/s.radius)*s.power;patrol+=v*(s.side==='security'?1:.55);if(s.kind==='post')post+=v}
 return{hood:n?.id||null,security,heat,gang,unrest,patrol:clamp(patrol,0,1.5),post:clamp(post,0,1.5)}
}
function pathMetrics(path,w=world()){
 const sources=patrolSources(w);if(!path?.length)return{steps:0,minutes:0,security:0,heat:0,gang:0,unrest:0,patrol:0,post:0,exposure:0,intel:0,hoods:[]};
 let sec=0,heat=0,gang=0,unrest=0,patrol=0,post=0,intel=0;const hoods=new Set();
 for(const p of path){const e=exposureAt(w,p,sources);sec+=e.security;heat+=e.heat;gang+=e.gang;unrest+=e.unrest;patrol+=e.patrol;post+=e.post;if(e.hood){hoods.add(e.hood);const n=(w.neighborhoods||[]).find(x=>x.id===e.hood);intel+=clamp(familiarity(w,n)/8,0,1)}}
 const n=path.length,security=sec/n,localHeat=heat/n,gangP=gang/n,unrestP=unrest/n,pat=patrol/n,posts=post/n;
 return{steps:Math.max(0,n-1),minutes:Math.max(0,n-1)*.25,security,heat:localHeat,gang:gangP,unrest:unrestP,patrol:pat,post:posts,exposure:clamp(security*.28+localHeat*.30+pat*.25+posts*.12+gangP*.04+unrestP*.01,0,1.5),intel:clamp(intel/n,0,1),hoods:[...hoods]}
}
function cleanJoin(a,b){if(!a?.length||!b?.length)return null;const joined=a.concat(b.slice(1)),last=new Map();for(let i=0;i<joined.length;i++)last.set(`${joined[i].x},${joined[i].y}`,i);const out=[];for(let i=0;i<joined.length;i++){const p=joined[i],k=`${p.x},${p.y}`;out.push(p);const li=last.get(k);if(li>i)i=li}return out}
function samePath(a,b){if((a?.length||0)!==(b?.length||0))return false;for(let i=0;i<a.length;i++)if(a[i].x!==b[i].x||a[i].y!==b[i].y)return false;return true}
function routeKey(p){return(p||[]).map(q=>`${q.x},${q.y}`).join('|')}
function waypointCandidates(start,goal,w){
 const pts=[];const seen=new Set(),add=p=>{if(!p)return;const q={x:Math.round(p.x),y:Math.round(p.y)},k=`${q.x},${q.y}`;if(k===`${start.x},${start.y}`||k===`${goal.x},${goal.y}`||seen.has(k))return;seen.add(k);pts.push(q)};
 for(const n of w?.neighborhoods||[])add(n);for(const tr of w?.transit||[])add(tr);for(const p of Object.values(w?.locations||{}))add(p);
 const dx=goal.x-start.x,dy=goal.y-start.y,len=Math.max(1,Math.hypot(dx,dy)),nx=-dy/len,ny=dx/len;
 for(const t of [.25,.5,.75])for(const off of [-18,-11,11,18])add({x:start.x+dx*t+nx*off,y:start.y+dy*t+ny*off});
 return pts.slice(0,34)
}
function alternatives(start,goal,w=world()){
 const fast=canonical(start,goal,w);if(!fast?.length)return[];const paths=[fast],keys=new Set([routeKey(fast)]),limit=Math.max(20,fast.length*2);
 for(const via of waypointCandidates(start,goal,w)){
   const a=canonical(start,via,w);if(!a?.length)continue;const b=canonical(via,goal,w);if(!b?.length)continue;const p=cleanJoin(a,b);if(!p?.length||p.length>limit)continue;const k=routeKey(p);if(keys.has(k))continue;keys.add(k);paths.push(p);if(paths.length>=28)break
 }
 return paths
}
function score(mode,m,fastSteps){const detour=m.steps/Math.max(1,fastSteps);if(mode==='low')return m.steps+55*m.security+62*m.heat+82*m.patrol+95*m.post+9*m.gang+Math.max(0,detour-1)*28;if(mode==='back')return m.steps*1.08+76*m.security+70*m.heat+98*m.patrol+125*m.post+3*m.gang+2*m.unrest+Math.max(0,detour-1)*20;return m.steps}
function makeOption(mode,path,w,fastSteps){const metrics=pathMetrics(path,w);return{mode,label:MODES[mode].label,desc:MODES[mode].desc,path,metrics,score:score(mode,metrics,fastSteps)}}
function preview(goal,target=null,w=world(),start=Game.ovPlayer){
 if(!w||!start||!goal)return null;const paths=alternatives(start,goal,w);if(!paths.length)return null;const fast=makeOption('fast',paths[0],w,paths[0].length-1),maxLow=Math.max(fast.metrics.steps+5,Math.floor(fast.metrics.steps*1.58)),maxBack=Math.max(fast.metrics.steps+8,Math.floor(fast.metrics.steps*1.95));
 const pick=(mode,max)=>{let best=fast;for(const p of paths){const o=makeOption(mode,p,w,fast.metrics.steps);if(o.metrics.steps>max)continue;if(best===fast||o.score<best.score)best=o}return best.mode===mode?best:makeOption(mode,best.path,w,fast.metrics.steps)};
 const low=pick('low',maxLow),back=pick('back',maxBack);return{worldId:w.id,start:{x:start.x,y:start.y},goal:{x:goal.x,y:goal.y},target:copy(target),options:{fast,low,back}}
}
window.previewPatrolRoutesV12104=preview;
function band(v){return v<.28?'LOW':v<.52?'MODERATE':v<.78?'HIGH':'SEVERE'}
function intelText(m){const cov=Math.round(m.intel*100);return m.intel>=.55?`EXPOSURE ${Math.round(m.exposure*100)} · INTEL ${cov}%`:`EXPOSURE ${band(m.exposure)} · INTEL ${cov<20?'THIN':cov<55?'PARTIAL':'GOOD'}`}
function ensureStyle(){if(document.getElementById('v12104-patrol-route-style'))return;const s=document.createElement('style');s.id='v12104-patrol-route-style';s.textContent=`#v12104-patrol-route-panel{position:fixed;z-index:10044;left:50%;bottom:14px;transform:translateX(-50%);width:min(430px,calc(100vw - 24px));max-height:min(78vh,660px);overflow:auto;background:rgba(3,8,12,.975);border:1px solid rgba(67,215,232,.65);box-shadow:0 14px 48px rgba(0,0,0,.68),0 0 28px rgba(67,215,232,.11);padding:12px;color:#d8e5e9;font:12px/1.42 Share Tech Mono,monospace}#v12104-patrol-route-panel[hidden]{display:none!important}#v12104-patrol-route-panel h3{margin:0 0 4px;color:#67e4ee;font:800 14px/1.2 Orbitron,sans-serif;letter-spacing:.06em}#v12104-patrol-route-panel .pr-sub{color:#91a7b0;margin-bottom:8px}.pr-options{display:grid;gap:8px}.pr-choice{display:block;width:100%;min-height:58px;text-align:left;white-space:normal}.pr-choice b{display:block;color:#e6f5f7;font:800 12px Orbitron,sans-serif}.pr-choice small{display:block;margin-top:3px;color:#91a7b0;line-height:1.35}.pr-choice[data-best='1']{outline:1px solid rgba(93,232,175,.58)}.v12104-route-intel{margin-top:5px;padding-top:5px;border-top:1px solid rgba(67,215,232,.2);font-size:10px;color:#9bb2ba}.v12104-route-switch{display:flex;gap:5px;flex-wrap:wrap;margin-top:5px}.v12104-route-switch button{min-height:34px;padding:4px 7px;font-size:9px}@media(max-width:520px){#v12104-patrol-route-panel{bottom:8px;width:calc(100vw - 20px);padding:10px;max-height:74vh}.pr-choice{min-height:62px}.v12104-route-switch button{min-height:44px;flex:1 1 30%}}`;document.head.appendChild(s)}
function ensurePanel(){ensureStyle();let p=document.getElementById('v12104-patrol-route-panel');if(!p){p=document.createElement('section');p.id='v12104-patrol-route-panel';p.hidden=true;document.body.appendChild(p)}return p}
function hidePlanner(){const p=document.getElementById('v12104-patrol-route-panel');if(p)p.hidden=true}
let ACTIVE_PLAN=null;
function goalForTarget(t,w=world()){if(!t)return null;if(t.kind==='location')return w?.locations?.[t.id]||null;if(t.kind==='transit')return w?.transit?.find(x=>x.id===t.id)||null;if(Number.isFinite(t.x)&&Number.isFinite(t.y))return{x:t.x,y:t.y};return null}
function optimizeActive(mode,target,goal){const w=world(),p=preview(goal,target,w,Game.ovPlayer),o=p?.options?.[mode];if(!o?.path?.length)return false;Game.pendingPath=o.path;Game._v133TravelTarget=target;ACTIVE_PLAN={worldId:w.id,goal:{x:goal.x,y:goal.y},target:copy(target),mode,metrics:o.metrics};state().preference=mode;window.requestOverworldRenderV133?.();window.updateOverworldHUD?.();return true}
const BASE={point:null,location:null,transit:null};
function wrapBase(kind,base,resolver){return function(){const args=[...arguments],ok=base?.apply(this,args);if(!ok||!Game.pendingPath?.length)return ok;const w=world(),target=Game._v133TravelTarget,goal=resolver(args,w,target);if(!goal)return ok;const mode=state().preference||'fast';optimizeActive(mode,target,goal);return ok}}
function installRouteWrappers(){
 if(BASE.point)return;BASE.point=window.routeToPointV133;BASE.location=window.routeToLocationV133;BASE.transit=window.routeToTransitNodeV133;if(!BASE.point||!BASE.location||!BASE.transit)return false;
 window.routeToPointV133=wrapBase('point',BASE.point,(a,w)=>a[0]);
 window.routeToLocationV133=wrapBase('location',BASE.location,(a,w)=>w?.locations?.[a[0]]||null);
 window.routeToTransitNodeV133=wrapBase('transit',BASE.transit,(a,w)=>w?.transit?.find(x=>x.id===a[0])||null);return true
}
function launch(target,goal,mode){const st=state();st.preference=mode;hidePlanner();let ok=false;if(target?.kind==='location')ok=window.routeToLocationV133?.(target.id);else if(target?.kind==='transit')ok=window.routeToTransitNodeV133?.(target.id);else ok=window.routeToPointV133?.(goal,target||{kind:'point',x:goal.x,y:goal.y,label:`${goal.x},${goal.y}`});if(ok){st.stats.planned++;st.history.unshift({type:'plan',world:world()?.id,mode,goal:{x:goal.x,y:goal.y},atStep:window.ensureLivingStreetsStateV134?.().stepCount||0});st.history=st.history.slice(0,40);window.saveGame?.(0,true)}return !!ok}
function openPlanner(spec){
 const w=world(),goal=spec?.point||goalForTarget(spec?.target,w),target=spec?.target||{kind:'point',x:goal?.x,y:goal?.y,label:goal?`${goal.x},${goal.y}`:'STREET'};if(!w||!goal||!Game.ovPlayer)return false;installRouteWrappers();const p=preview(goal,target,w,Game.ovPlayer);if(!p)return false;const box=ensurePanel(),opts=['fast','low','back'].map(k=>p.options[k]);box.hidden=false;box.innerHTML=`<h3>STREET ROUTE // ${String(target.label||target.id||'DESTINATION').toUpperCase()}</h3><div class="pr-sub">Choose how the crew crosses ${w.cfg?.name||w.id}. All options use the physical street graph.</div><div class="pr-options"></div>`;const list=box.querySelector('.pr-options');
 const minExp=Math.min(...opts.map(x=>x.metrics.exposure));for(const o of opts){const b=document.createElement('button');b.className='btn pr-choice';b.dataset.mode=o.mode;b.dataset.best=o.metrics.exposure===minExp?'1':'0';b.innerHTML=`<b>${o.label}</b><small>${o.metrics.steps} BLOCKS · ${o.metrics.minutes.toFixed(1)} MIN · ${intelText(o.metrics)}<br>${o.desc}</small>`;b.onclick=()=>launch(target,goal,o.mode);list.appendChild(b)}return true
}
window.openPatrolRoutePlannerV12104=openPlanner;
function switchMode(mode){if(!MODES[mode]||!ACTIVE_PLAN||ACTIVE_PLAN.worldId!==world()?.id||!Game.pendingPath?.length)return false;const target=Game._v133TravelTarget||ACTIVE_PLAN.target,goal=ACTIVE_PLAN.goal,before={x:Game.ovPlayer.x,y:Game.ovPlayer.y};if(!optimizeActive(mode,target,goal))return false;const st=state();st.stats.switched++;st.history.unshift({type:'switch',world:world().id,mode,at:{x:before.x,y:before.y},atStep:window.ensureLivingStreetsStateV134?.().stepCount||0});st.history=st.history.slice(0,40);window.saveGame?.(0,true);return true}
window.switchPatrolRouteProfileV12104=switchMode;
function decorate(card,target){if(!card||!Game.pendingPath?.length)return;const mode=ACTIVE_PLAN?.mode||state().preference||'fast',m=pathMetrics(Game.pendingPath,world()),d=document.createElement('div');d.className='v12104-route-intel';d.innerHTML=`<b>${MODES[mode].label}</b> · ${intelText(m)}<div class="v12104-route-switch"></div>`;const row=d.querySelector('.v12104-route-switch');for(const k of ['fast','low','back']){const b=document.createElement('button');b.className='btn small';b.textContent=MODES[k].label;b.disabled=k===mode;b.onclick=e=>{e.preventDefault();e.stopPropagation();switchMode(k)};row.appendChild(b)}card.appendChild(d)}
window.decoratePatrolRouteCardV12104=decorate;
function drawCorridors(ctx,w,W,H,t){if(!ctx||!w)return;const src=patrolSources(w),here=Game.ovPlayer||{x:-999,y:-999};for(const s of src){const n=nearestHood(w,s),known=familiarity(w,n)>=3||Math.hypot(here.x-s.x,here.y-s.y)<=9;if(!known)continue;const p=window.worldToScreen?.(s.x+.5,s.y+.5);if(!p)continue;const r=Math.max(14,Math.min(70,s.radius*t*.68));ctx.save();ctx.strokeStyle=s.side==='security'?'rgba(94,200,255,.25)':'rgba(255,111,88,.22)';ctx.fillStyle=s.side==='security'?'rgba(94,200,255,.035)':'rgba(255,111,88,.032)';ctx.setLineDash([5,7]);ctx.lineWidth=1.2;ctx.beginPath();ctx.arc(p.x,p.y,r,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.setLineDash([]);ctx.restore()}}
function stepHook(w){markFamiliar(w,Game.ovPlayer)}
function initHook(){installRouteWrappers();ensureStyle();state();ACTIVE_PLAN=null;hidePlanner()}
function currentPlan(){return ACTIVE_PLAN?copy(ACTIVE_PLAN):null}
window.currentPatrolRoutePlanV12104=currentPlan;
installRouteWrappers();
const prevDraw=window.drawLivingStreetsV134;if(prevDraw)window.drawLivingStreetsV134=function(ctx,w,W,H,t,hover){const r=prevDraw.apply(this,arguments);drawCorridors(ctx,w,W,H,t);return r};
const prevStep=window.onStreetStepV134;if(prevStep)window.onStreetStepV134=function(w){const r=prevStep.apply(this,arguments);stepHook(w||world());return r};
const prevInit=window.initOverworldV133;if(prevInit){const wrapped=function(){const r=prevInit.apply(this,arguments);initHook();return r};window.initOverworldV133=wrapped;if(window.initOverworld===prevInit)window.initOverworld=wrapped}
ensureStyle();state();window.CR_CITY_PATROL_CORRIDORS={version:VERSION,state,preview,openPlanner,switchMode,pathMetrics,patrolSources,markFamiliar};
})();
}''',encoding='utf-8')

# Candidate 08 needs one narrow export from canonical routing so arbitrary map points can
# still wake the established overworld scheduler before the selected route replaces pendingPath.
p=root/'src/world/district-worlds-v13-3.js'
s=p.read_text(encoding='utf-8')
needle="function routeToLocationV133(id){const p=currentDistrictV133().locations[id];if(!p)return false;"
if 'window.routeToPointV133=routeToPointV133;' not in s:
    if needle not in s: raise SystemExit('routeToLocationV133 seam missing')
    s=s.replace(needle,"window.routeToPointV133=routeToPointV133;\n"+needle,1)

# Manual map taps get a route-choice surface. Programmatic callers retain the route APIs and
# therefore preserve logistics/control-post architecture.
old="else{mark.kind==='transit'?routeToTransitNodeV133(mark.id):routeToLocationV133(mark.id)}return}"
new="else{const spec={point:{x:mark.x,y:mark.y},target:{kind:mark.kind==='transit'?'transit':'location',id:mark.id,label:mark.label||mark.id}};if(!window.openPatrolRoutePlannerV12104?.(spec))mark.kind==='transit'?routeToTransitNodeV133(mark.id):routeToLocationV133(mark.id)}return}"
if 'openPatrolRoutePlannerV12104?.(spec)' not in s:
    if old not in s: raise SystemExit('marker tap route seam missing')
    s=s.replace(old,new,1)
old2="if(!isWalkableV133(q.x,q.y)){toast('Blocked.');return}routeToPointV133(q,{kind:'point',label:`${q.x},${q.y}`})"
new2="if(!isWalkableV133(q.x,q.y)){toast('Blocked.');return}const pt={kind:'point',x:q.x,y:q.y,label:`${q.x},${q.y}`};if(!window.openPatrolRoutePlannerV12104?.({point:q,target:pt}))routeToPointV133(q,pt)"
if 'openPatrolRoutePlannerV12104?.({point:q,target:pt})' not in s:
    if old2 not in s: raise SystemExit('point tap route seam missing')
    s=s.replace(old2,new2,1)

# Preserve the canonical route card and let Candidate 08 append live route intelligence.
old3="e.innerHTML=`<b>ACTIVE ROUTE</b>${t?.label||'Street route'} · ${Math.max(0,Game.pendingPath.length-1)} blocks remaining`"
new3=old3+";window.decoratePatrolRouteCardV12104?.(e,t)"
if 'decoratePatrolRouteCardV12104?.(e,t)' not in s:
    if old3 not in s: raise SystemExit('route card seam missing')
    s=s.replace(old3,new3,1)
p.write_text(s,encoding='utf-8')

manifest=root/'src/bootstrap/module-manifest.js'
s=manifest.read_text(encoding='utf-8')
entry="  'world.patrolCorridors':{path:'./src/world/patrol-corridors-pwa12-104-city-candidate-08.js',kind:'module'},\n"
if 'world.patrolCorridors' not in s:
    needle="  'world.controlPosts':{path:'./src/world/district-control-posts-pwa12-104-city-candidate-07.js',kind:'module'},\n"
    if needle not in s: raise SystemExit('Candidate 07 manifest seam missing')
    s=s.replace(needle,needle+entry,1)
    order="'world.accessEcology','world.transitIncidents','world.controlPosts','missions.approaches'"
    if order not in s: raise SystemExit('Candidate 07 manifest order seam missing')
    s=s.replace(order,"'world.accessEcology','world.transitIncidents','world.controlPosts','world.patrolCorridors','missions.approaches'",1)
manifest.write_text(s,encoding='utf-8')

# rebundle_runtime.py derives ordering from SOURCE markers in runtime-bundle.js.
bundle=root/'src/runtime/runtime-bundle.js'
s=bundle.read_text(encoding='utf-8')
marker='/* SOURCE: src/world/patrol-corridors-pwa12-104-city-candidate-08.js */'
if marker not in s:
    prev='/* SOURCE: src/world/district-control-posts-pwa12-104-city-candidate-07.js */'
    nxt='/* SOURCE: src/missions/contract-approaches-v13-4b.js */'
    a=s.find(prev);b=s.find(nxt)
    if a<0 or b<0 or a>b: raise SystemExit('Candidate 07 runtime marker seam missing')
    s=s[:b]+marker+'\n'+s[b:]
bundle.write_text(s,encoding='utf-8')
print('applied Candidate 08 Patrol Corridors + Risk-Aware Physical Route Choice')
