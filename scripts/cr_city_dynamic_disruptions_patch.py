from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve()
module=root/'src/world/dynamic-logistics-disruptions-pwa12-104-city-candidate-03.js'
module.write_text(r'''if(typeof window!=='undefined'){
(() => {
'use strict';
const VERSION='pwa12.104-city-candidate.03';
const TYPE_MOD={metro:.08,border:.12,freight:.15,security:.22,hidden:-.06};
function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
function hash(...parts){let h=2166136261>>>0;for(const x of parts){const s=String(x??'');for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)}}return h>>>0}
function nowMin(){return Math.round((((Game.day||1)-1)*24+(Game.hour||0))*60)}
function active(){return window.activeInterdistrictDispatchV12104?.()||null}
function world(){return window.currentDistrictV133?.()||null}
function nearestHood(w,p){let best=null,bd=Infinity;for(const n of w?.neighborhoods||[]){const d=Math.hypot((p?.x||0)-n.x,(p?.y||0)-n.y);if(d<bd){bd=d;best=n.id}}return best}
function hoodState(w,id){return window.ensureNeighborhoodStateV134?.(w)?.[id]||null}
function option(a,id=a?.chosenLinkId){return a?.options?.find(x=>x.linkId===id)||null}
function pressureFor(a,w=world()){
  if(!a||!w||!Game.ovPlayer)return null;
  const hid=nearestHood(w,Game.ovPlayer),h=hoodState(w,hid),op=option(a);
  if(!h||!op)return null;
  const heat=(h.localHeat||0)/100,sec=(h.security||0)/5,gang=(h.gangPressure||0)/5,unrest=(h.unrest||0)/5;
  const p=clamp(heat*.28+sec*.24+gang*.27+unrest*.14+(TYPE_MOD[op.linkType]||0)+(a.risk||0)*.12,0,1);
  return{hoodId:hid,hood:h,op,pressure:Number(p.toFixed(3)),roll:(hash(a.id,op.linkId,hid,Game.day||1)%1000)/1000};
}
window.interdistrictDisruptionPressureV12104=pressureFor;
function reasonFor(x){
  const h=x.hood,op=x.op;
  if((h.gangPressure||0)>=4&&(h.gangPressure||0)>=(h.security||0))return{code:'gang_cordon',title:'GANG CORDON',copy:'A local crew has sealed the approach and is shaking down every vehicle and runner.'};
  if(op.linkType==='security'||((h.security||0)>=4&&op.linkType==='border'))return{code:'security_sweep',title:'SECURITY SWEEP',copy:'A security sweep just hardened the crossing. IDs, cargo and faces are being checked.'};
  if(op.linkType==='metro')return{code:'metro_cut',title:'METRO SERVICE CUT',copy:'The selected metro approach is under an unscheduled service shutdown and platform sweep.'};
  if(op.linkType==='freight')return{code:'freight_inspection',title:'FREIGHT INSPECTION',copy:'Cargo control has opened the freight lane for invasive inspection.'};
  if(op.linkType==='hidden')return{code:'covert_burned',title:'COVERT ROUTE BURNED',copy:'The covert approach is compromised; watchers are working the entry corridor.'};
  return{code:'border_lock',title:'BORDER LOCKDOWN',copy:'The crossing tightened without warning and queues are backing into the district.'};
}
function viableAlternative(a){return (a?.options||[]).filter(o=>!o.blocked&&o.linkId!==a.chosenLinkId).sort((x,y)=>x.risk-y.risk||x.windowMin-y.windowMin)[0]||null}
function arm(a=active()){
  if(!a||a.phase!=='to_transit'||!a.chosenLinkId||a.dynamicDisruptionTriggered)return null;
  const remaining=Game.pendingPath?.length||0;
  if(!remaining)return null;
  if(!a.dynamicDisruptionArm||a.dynamicDisruptionArm.linkId!==a.chosenLinkId){a.dynamicDisruptionArm={linkId:a.chosenLinkId,startRemaining:remaining,armedAt:nowMin(),x:Game.ovPlayer?.x,y:Game.ovPlayer?.y};return a.dynamicDisruptionArm}
  return a.dynamicDisruptionArm;
}
function trigger(a,x){
  const reason=reasonFor(x),alt=viableAlternative(a),remaining=Game.pendingPath?.length||0;
  a.dynamicDisruptionTriggered=true;
  a.dynamicDisruption={version:1,status:'alert',reason:reason.code,title:reason.title,copy:reason.copy,pressure:x.pressure,roll:Number(x.roll.toFixed(3)),hoodId:x.hoodId,linkId:a.chosenLinkId,linkName:x.op.linkName,linkType:x.op.linkType,alternativeLinkId:alt?.linkId||null,alternativeLinkName:alt?.linkName||null,triggeredAt:nowMin(),remainingPath:remaining,deadlineAtTrigger:a.deadline};
  Game.pendingPath=null;Game._v133TravelTarget=null;
  window.addJournal?.('side','CITY ROUTE DISRUPTED',`${reason.title} on ${x.op.linkName}. ${alt?'An alternate physical crossing is available: '+alt.linkName+'.':'No alternate direct crossing is currently available.'}`);
  window.streetToastV134?.(`${reason.title} · ROUTE HALTED`);
  window.saveGame?.(0,true);update();return a.dynamicDisruption;
}
function evaluate(w=world()){
  const a=active();if(!a||a.phase!=='to_transit'||a.dynamicDisruptionTriggered||!a.chosenLinkId)return false;
  const ar=arm(a);if(!ar)return false;
  const remaining=Game.pendingPath?.length||0;if(remaining>=ar.startRemaining)return false;
  const x=pressureFor(a,w);if(!x)return false;
  const should=x.pressure>=.92||(x.pressure>=.58&&x.roll<x.pressure);
  if(!should)return false;
  return trigger(a,x);
}
window.evaluateInterdistrictDisruptionV12104=evaluate;
function reroute(){
  const a=active(),d=a?.dynamicDisruption;if(!a||d?.status!=='alert')return false;
  const alt=viableAlternative(a);if(!alt)return false;
  const deadline=a.deadline,from=d.linkId;
  const ok=window.chooseInterdistrictTransitV12104?.(alt.linkId);if(!ok)return false;
  a.deadline=deadline;d.status='rerouted';d.resolvedAt=nowMin();d.resolution='reroute';d.fromLinkId=from;d.toLinkId=alt.linkId;d.toLinkName=alt.linkName;
  window.addJournal?.('side','CITY REROUTE',`${d.title}: abandoned ${d.linkName} and committed a physical route to ${alt.linkName}. Original delivery deadline remains in force.`);
  window.streetToastV134?.(`REROUTED · ${alt.linkName}`);window.saveGame?.(0,true);window.updateInterdistrictDispatchUIV12104?.();update();return true
}
window.rerouteInterdistrictDisruptionV12104=reroute;
function pushThrough(){
  const a=active(),d=a?.dynamicDisruption;if(!a||d?.status!=='alert')return false;
  const oldDeadline=a.deadline,oldRisk=Number(a.risk||0),link=d.linkId,w=world(),hid=nearestHood(w,Game.ovPlayer),h=hoodState(w,hid);
  const ok=window.chooseInterdistrictTransitV12104?.(link);if(!ok)return false;
  a.deadline=oldDeadline;a.risk=Number(clamp(oldRisk+.08+d.pressure*.12,0,1).toFixed(3));
  const heat= d.reason==='security_sweep'||d.reason==='border_lock'?3:d.reason==='covert_burned'?4:d.reason==='gang_cordon'?2:1;
  if(h){h.localHeat=clamp((h.localHeat||0)+heat,0,100);h.events=(h.events||0)+1}
  if(typeof window.advanceTime==='function')window.advanceTime(.25);else if(typeof advanceTime==='function')advanceTime(.25);
  d.status='pushed';d.resolvedAt=nowMin();d.resolution='push';d.heatAdded=heat;d.riskBefore=oldRisk;d.riskAfter=a.risk;
  window.addJournal?.('side','CITY DISRUPTION PUSHED',`${d.title}: pushed through ${d.linkName}. +15 minutes, +${heat} local heat, route risk ${Math.round(oldRisk*100)}% → ${Math.round(a.risk*100)}%. Original deadline remains in force.`);
  window.streetToastV134?.(`${d.title} · PUSHED THROUGH`);window.updateNeighborhoodHUDV134?.();window.saveGame?.(0,true);window.updateInterdistrictDispatchUIV12104?.();update();return true
}
window.pushThroughInterdistrictDisruptionV12104=pushThrough;
function panel(){
  let p=document.getElementById('v12104-disruption-panel'),wrap=document.querySelector('#overworld-screen .wrap');if(!wrap)return null;
  if(!document.getElementById('v12104-disruption-style')){const st=document.createElement('style');st.id='v12104-disruption-style';st.textContent=`#v12104-disruption-panel{position:absolute;left:50%;bottom:82px;transform:translateX(-50%);z-index:31;width:min(380px,calc(100% - 28px));max-height:min(60vh,490px);overflow:auto;padding:12px 13px;background:rgba(20,7,8,.97);border:1px solid rgba(255,83,74,.72);box-shadow:0 12px 36px rgba(0,0,0,.62);font:12px/1.38 monospace;color:#edf3f5;display:none;pointer-events:auto}#v12104-disruption-panel .k{font-size:10px;letter-spacing:.14em;color:#ff665b}#v12104-disruption-panel .alert{margin:6px 0 8px;font-size:15px;color:#fff;font-weight:700}#v12104-disruption-panel .meta{margin:6px 0;color:#c4cdd1}#v12104-disruption-panel .terms{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;margin:8px 0}#v12104-disruption-panel .terms span{padding:5px 3px;background:rgba(255,255,255,.05);text-align:center}#v12104-disruption-panel button{width:100%;min-height:42px;margin-top:6px}@media(max-width:520px){#v12104-disruption-panel{left:8px;right:8px;bottom:74px;transform:none;width:auto;max-height:58vh;padding:10px}#v12104-disruption-panel button{min-height:44px}}`;document.head.appendChild(st)}
  if(!p){p=document.createElement('div');p.id='v12104-disruption-panel';wrap.appendChild(p)}return p
}
function update(){
  const p=panel(),a=active(),d=a?.dynamicDisruption,base=document.getElementById('v12104-interdistrict-panel');
  if(!p||Game.screen!=='overworld-screen'||!a||d?.status!=='alert'){if(p)p.style.display='none';if(base){base.style.opacity='';base.style.pointerEvents=''}return}
  const alt=viableAlternative(a),remain=a.deadline===null?null:a.deadline-nowMin();p.style.display='block';if(base){base.style.opacity='.28';base.style.pointerEvents='none'};
  p.innerHTML=`<div class="k">LIVE ROUTE DISRUPTION</div><div class="alert">${d.title}</div><div class="meta">${d.copy}<br><b>${d.linkName}</b> is no longer a clean approach. Your crew is stopped in ${d.hoodId||'the district'}; no transit has occurred.</div><div class="terms"><span>${Math.round(d.pressure*100)}%<br>PRESSURE</span><span>${remain===null?'—':remain}<br>MIN LEFT</span><span>${alt?alt.linkType.toUpperCase():'NONE'}<br>ALT</span></div>${alt?`<button class="btn small" id="v12104-disrupt-reroute">REROUTE VIA ${alt.linkName}</button>`:''}<button class="btn small" id="v12104-disrupt-push">PUSH THROUGH ${d.linkName}</button><div class="meta">Rerouting preserves the original deadline and sends you physically to another transit node. Pushing through preserves the deadline but costs 15 minutes and raises local heat/risk.</div>`;
  p.querySelector('#v12104-disrupt-reroute')?.addEventListener('click',reroute);p.querySelector('#v12104-disrupt-push')?.addEventListener('click',pushThrough)
}
window.updateInterdistrictDisruptionUIV12104=update;
const prevStep=window.onStreetStepV134;window.onStreetStepV134=function(w){const r=prevStep?.apply(this,arguments);evaluate(w||world());update();return r};
const prevInit=window.initOverworldV133;if(prevInit){const wrapped=function(){const r=prevInit.apply(this,arguments);update();return r};window.initOverworldV133=wrapped;if(window.initOverworld===prevInit)window.initOverworld=wrapped}
setTimeout(update,0);window.CR_CITY_DYNAMIC_DISRUPTIONS={version:VERSION,evaluate,reroute,pushThrough,update};
})();
}''',encoding='utf-8')

manifest=root/'src/bootstrap/module-manifest.js'
s=manifest.read_text(encoding='utf-8')
entry="  'world.dynamicLogisticsDisruptions':{path:'./src/world/dynamic-logistics-disruptions-pwa12-104-city-candidate-03.js',kind:'module'},\n"
if 'world.dynamicLogisticsDisruptions' not in s:
    needle="  'world.interdistrictLogistics':{path:'./src/world/interdistrict-logistics-pwa12-104-city-candidate-02.js',kind:'module'},\n"
    if needle not in s: raise SystemExit('interdistrict logistics manifest seam missing')
    s=s.replace(needle,needle+entry,1)
    order="'world.livingStreets','world.districtDispatches','world.interdistrictLogistics','missions.approaches'"
    if order not in s: raise SystemExit('candidate 02 manifest order seam missing')
    s=s.replace(order,"'world.livingStreets','world.districtDispatches','world.interdistrictLogistics','world.dynamicLogisticsDisruptions','missions.approaches'",1)
manifest.write_text(s,encoding='utf-8')

bundle=root/'src/runtime/runtime-bundle.js'
s=bundle.read_text(encoding='utf-8')
cross='/* SOURCE: src/world/interdistrict-logistics-pwa12-104-city-candidate-02.js */'
dyn='/* SOURCE: src/world/dynamic-logistics-disruptions-pwa12-104-city-candidate-03.js */'
mission='/* SOURCE: src/missions/contract-approaches-v13-4b.js */'
if cross not in s or mission not in s: raise SystemExit('candidate 02 runtime seam missing')
if dyn not in s:s=s.replace(mission,dyn+'\n'+mission,1)
pos=[s.index(x) for x in (cross,dyn,mission)]
if pos!=sorted(pos):raise SystemExit(f'dynamic disruption runtime order invalid: {pos}')
bundle.write_text(s,encoding='utf-8')
print('patched dynamic logistics disruptions candidate 03',root)
