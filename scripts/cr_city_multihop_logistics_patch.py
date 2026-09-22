from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve()

# Candidate 02 owns normal interdistrict completion. Multi-hop jobs must stop at the
# physical intermediate handoff instead of being mistaken for a final delivery.
c2=root/'src/world/interdistrict-logistics-pwa12-104-city-candidate-02.js'
s=c2.read_text(encoding='utf-8')
needle=" const s=state(),a=active();if(!a||!w||a.phase!=='last_mile'||w.id!==a.targetDistrict)return false;"
replacement=" const s=state(),a=active();if(a?.multiHop&&typeof window.tryCompleteMultiHopDispatchV12104==='function')return window.tryCompleteMultiHopDispatchV12104(w);if(!a||!w||a.phase!=='last_mile'||w.id!==a.targetDistrict)return false;"
if replacement not in s:
    if needle not in s: raise SystemExit('candidate 02 completion seam missing')
    s=s.replace(needle,replacement,1)
c2.write_text(s,encoding='utf-8')

module=root/'src/world/multihop-logistics-pwa12-104-city-candidate-04.js'
module.write_text(r'''if(typeof window!=='undefined'){
(() => {
'use strict';
const VERSION='pwa12.104-city-candidate.04';
const EFFECTS={courier:{heat:-1,prosperity:1,unrest:0},medical:{heat:-2,prosperity:1,unrest:-1},data:{heat:2,prosperity:0,unrest:0},contraband:{heat:6,prosperity:0,unrest:1}};
function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
function copy(v){return JSON.parse(JSON.stringify(v))}
function hash(...parts){let h=2166136261>>>0;for(const x of parts){const s=String(x??'');for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)}}return h>>>0}
function nowMin(){return Math.round((((Game.day||1)-1)*24+(Game.hour||0))*60)}
function state(){const s=window.ensureDistrictDispatchStateV12104?.();if(!s)return null;s.multiHopOffers=s.multiHopOffers||{};s.stats=s.stats||{};s.stats.multiHopAccepted=s.stats.multiHopAccepted||0;s.stats.multiHopHandoffs=s.stats.multiHopHandoffs||0;s.stats.multiHopDelivered=s.stats.multiHopDelivered||0;s.stats.multiHopAbandoned=s.stats.multiHopAbandoned||0;return s}
function world(){return window.currentDistrictV133?.()||null}
function defs(id){return window.V13_DISTRICT_LOCATIONS?.[id]||[]}
function def(d,id){return defs(d).find(x=>x.id===id)||null}
function known(d){return !!d&&(!!Game.cityLife?.discovered?.[d.id]||!!(d.contact&&Game.contactRelations?.[d.contact]?.known))}
function nearSource(w=world(),max=2.2){if(!w||!Game.ovPlayer)return null;let best=null;for(const d of defs(w.id)){const p=w.locations?.[d.id];if(!p||!known(d))continue;const q=Math.hypot(Game.ovPlayer.x-p.x,Game.ovPlayer.y-p.y);if(q<=max&&(!best||q<best.dist))best={id:d.id,def:d,point:p,dist:q}}return best}
function linkVisible(link){if(!link)return false;if(link.type==='hidden')return !!Game.districtWorldsV133?.hiddenLinks?.[link.id];return true}
function directLinks(a,b){return (window.V133_TRANSIT_LINKS||[]).filter(l=>linkVisible(l)&&((l.from.district===a&&l.to.district===b)||(l.to.district===a&&l.from.district===b)))}
function eligibleLocations(id,w){return defs(id).filter(d=>w?.locations?.[d.id]&&(d.contact||d.shop||d.type==='clinic'))}
function best(options){return (options||[]).filter(o=>!o.blocked).sort((a,b)=>a.risk-b.risk||a.windowMin-b.windowMin||a.cost-b.cost)[0]||null}
function routeCount(q){return (q?.options||[]).filter(o=>!o.blocked).length}
function chainPayout(plan){const a=plan.selectedLeg1||best(plan.leg1?.options),b=plan.selectedLeg2||best(plan.leg2?.options);if(!a||!b)return 0;return Math.round(((a.payout+b.payout)*1.12)/10)*10}
function chainRisk(plan){const a=plan.selectedLeg1||best(plan.leg1?.options),b=plan.selectedLeg2||best(plan.leg2?.options);return Number((((a?.risk||0)+(b?.risk||0))/2).toFixed(3))}
function offer(sourceId,w=world()){
 const s=state();if(!s||!w||!w.locations?.[sourceId])return null;const src=def(w.id,sourceId);if(!src||!known(src))return null;
 const key=`${w.id}:${sourceId}:${Game.day||1}:multihop`;if(s.multiHopOffers[key])return s.multiHopOffers[key];
 const seed=hash(key),candidates=[];const mids=Object.keys(window.V133_DISTRICTS||{}).filter(mid=>mid!==w.id&&directLinks(w.id,mid).length);
 for(const mid of mids){const mw=window.generateDistrictV133?.(mid);if(!mw)continue;const handoffs=eligibleLocations(mid,mw).sort((a,b)=>(hash(seed,mid,a.id)%100000)-(hash(seed,mid,b.id)%100000)).slice(0,3);
   for(const fin of Object.keys(window.V133_DISTRICTS||{})){if(fin===w.id||fin===mid||!directLinks(mid,fin).length)continue;const fw=window.generateDistrictV133?.(fin);if(!fw)continue;const finals=eligibleLocations(fin,fw).sort((a,b)=>(hash(seed,fin,a.id)%100000)-(hash(seed,fin,b.id)%100000)).slice(0,3);
     for(const hand of handoffs.slice(0,2)){const q1=window.quoteInterdistrictDispatchV12104?.(sourceId,mid,hand.id,null,w);if(!q1||!routeCount(q1))continue;for(const dest of finals.slice(0,2)){const q2=window.quoteInterdistrictDispatchV12104?.(hand.id,fin,dest.id,q1.kind,mw);if(!q2||!routeCount(q2))continue;const b1=best(q1.options),b2=best(q2.options);if(!b1||!b2)continue;const totalRisk=(b1.risk+b2.risk)/2,windowMin=Math.max(100,b1.windowMin+b2.windowMin+28),payout=Math.round(((b1.payout+b2.payout)*1.12)/10)*10;candidates.push({q1,q2,mid,fin,hand,dest,totalRisk,windowMin,payout,routes:routeCount(q1)+routeCount(q2),tie:hash(seed,mid,hand.id,fin,dest.id)%100000})}}
   }
 }
 if(!candidates.length)return null;candidates.sort((a,b)=>b.routes-a.routes||a.totalRisk-b.totalRisk||a.tie-b.tie);const c=candidates[0];
 const o={id:`multi_${w.id}_${Game.day||1}_${sourceId}`,day:Game.day||1,createdAt:nowMin(),multiHopOffer:true,kind:c.q1.kind,label:`LONG-HAUL ${c.q1.label}`,verb:c.q1.verb,sourceDistrict:w.id,sourceId,sourceName:src.name,handoffDistrict:c.mid,handoffId:c.hand.id,handoffName:c.hand.name,handoffDistrictName:window.V133_DISTRICTS?.[c.mid]?.name||c.mid,finalDistrict:c.fin,finalId:c.dest.id,finalName:c.dest.name,finalDistrictName:window.V133_DISTRICTS?.[c.fin]?.name||c.fin,leg1:copy(c.q1),leg2:copy(c.q2),estimatedPayout:c.payout,estimatedRisk:Number(c.totalRisk.toFixed(3)),windowMin:c.windowMin};s.multiHopOffers[key]=o;return o
}
window.offerMultiHopDispatchV12104=offer;
function active(){const a=window.activeInterdistrictDispatchV12104?.();return a?.multiHop?a:null}
window.activeMultiHopDispatchV12104=active;
function applyLeg(a,leg){a.sourceDistrict=leg.sourceDistrict;a.sourceId=leg.sourceId;a.sourceName=leg.sourceName;a.targetDistrict=leg.targetDistrict;a.targetId=leg.targetId;a.targetName=leg.targetName;a.targetDistrictName=leg.targetDistrictName;a.options=copy(leg.options);a.chosenLinkId=null;a.chosenOption=null;a.phase='choose_transit';a.transitMode=null;a.transitAt=null;a.risk=best(a.options)?.risk||0}
function accept(id){const w=world(),n=nearSource(w),o=n?offer(n.id,w):null,s=state();if(!o||o.id!==id||s.active||!n||n.id!==o.sourceId)return false;const start=nowMin(),deadline=start+o.windowMin,plan={version:1,stage:1,deadline,acceptedAt:start,originalSourceDistrict:o.sourceDistrict,originalSourceId:o.sourceId,originalSourceName:o.sourceName,handoffDistrict:o.handoffDistrict,handoffId:o.handoffId,handoffName:o.handoffName,handoffDistrictName:o.handoffDistrictName,finalDistrict:o.finalDistrict,finalId:o.finalId,finalName:o.finalName,finalDistrictName:o.finalDistrictName,leg1:copy(o.leg1),leg2:copy(o.leg2),disruptions:[]};
 s.active={id:o.id,day:o.day,createdAt:o.createdAt,crossDistrict:true,multiHop:true,status:'active',kind:o.kind,label:o.label,verb:o.verb,acceptedAt:start,deadline,payout:o.estimatedPayout,risk:o.estimatedRisk,multiHopPlan:plan};applyLeg(s.active,plan.leg1);s.active.deadline=deadline;s.active.payout=o.estimatedPayout;s.stats.accepted=(s.stats.accepted||0)+1;s.stats.crossAccepted=(s.stats.crossAccepted||0)+1;s.stats.multiHopAccepted++;
 window.addJournal?.('side',o.label,`${o.sourceName} → ${o.handoffName} (${o.handoffDistrictName}) → ${o.finalName} (${o.finalDistrictName}). Two physical city crossings and an intermediate handoff are required.`);window.streetToastV134?.('LONG-HAUL RUN · LEG 1 READY');window.saveGame?.(0,true);update();return true}
window.acceptMultiHopDispatchV12104=accept;
const baseChoose=window.chooseInterdistrictTransitV12104;
if(baseChoose){window.chooseInterdistrictTransitV12104=function(linkId){const a=active(),plan=a?.multiHopPlan,stage=plan?.stage;const deadline=plan?.deadline;const ok=baseChoose.apply(this,arguments);if(!ok||!a||!plan)return ok;const chosen=a.options.find(o=>o.linkId===a.chosenLinkId);if(stage===1)plan.selectedLeg1=copy(chosen);else if(stage===2)plan.selectedLeg2=copy(chosen);a.deadline=deadline;a.payout=chainPayout(plan);a.risk=chosen?.risk||a.risk;window.saveGame?.(0,true);update();return ok}}
function nearTarget(a,w=world(),max=2.15){const p=w?.locations?.[a?.targetId];return !!p&&!!Game.ovPlayer&&w.id===a.targetDistrict&&Math.hypot(Game.ovPlayer.x-p.x,Game.ovPlayer.y-p.y)<=max}
function archiveDisruption(a){const d=a?.dynamicDisruption,p=a?.multiHopPlan;if(!d||!p)return;if(!p.disruptions.some(x=>x.triggeredAt===d.triggeredAt&&x.linkId===d.linkId))p.disruptions.push(copy(d))}
function handoff(a,w){const s=state(),p=a.multiHopPlan;if(!nearTarget(a,w)||p.stage!==1||a.phase!=='last_mile')return false;archiveDisruption(a);p.stage='handoff';p.handoffAt=nowMin();a.phase='handoff';Game.pendingPath=null;Game._v133TravelTarget=null;s.stats.multiHopHandoffs++;const hd=def(p.handoffDistrict,p.handoffId);if(hd?.contact&&Game.contactRelations?.[hd.contact]?.known&&typeof window.changeContactTrustV13==='function')window.changeContactTrustV13(hd.contact,1,'Completed long-haul handoff');window.addJournal?.('side','LONG-HAUL HANDOFF',`${p.handoffName}: first city leg secured. The cargo must now be transferred and a second physical crossing selected.`);window.streetToastV134?.('HANDOFF COMPLETE · LEG 2 AWAITS');window.saveGame?.(0,true);update();return{handoff:true}}
function mutate(h,field,delta){if(!h)return;if(field==='localHeat')h[field]=clamp((h[field]||0)+delta,0,100);else h[field]=clamp((h[field]||0)+delta,0,5);h.events=(h.events||0)+1}
function hoodAt(w,p){let id=null,bd=Infinity;for(const n of w?.neighborhoods||[]){const d=Math.hypot((p?.x||0)-n.x,(p?.y||0)-n.y);if(d<bd){bd=d;id=n.id}}return id?window.ensureNeighborhoodStateV134?.(w)?.[id]:null}
function finalDelivery(a,w){const s=state(),p=a.multiHopPlan;if(!nearTarget(a,w)||p.stage!==2||a.phase!=='last_mile')return false;archiveDisruption(a);const now=nowMin(),late=Math.max(0,now-(p.deadline||now)),mult=late?Math.max(.4,1-Math.min(1,late/150)*.6):1,total=chainPayout(p),reward=Math.round(total*mult/10)*10,pt=w.locations?.[a.targetId],h=hoodAt(w,pt),fx=EFFECTS[a.kind]||EFFECTS.courier;Game.credits=(Game.credits||0)+reward;mutate(h,'localHeat',fx.heat);if(fx.prosperity)mutate(h,'prosperity',fx.prosperity);if(fx.unrest)mutate(h,'unrest',fx.unrest);
 const src=def(p.originalSourceDistrict,p.originalSourceId),hand=def(p.handoffDistrict,p.handoffId);if(src?.contact&&Game.contactRelations?.[src.contact]?.known&&typeof window.changeContactTrustV13==='function')window.changeContactTrustV13(src.contact,late?-1:2,late?'Late long-haul delivery':'Completed long-haul delivery');if(hand?.contact&&hand.contact!==src?.contact&&Game.contactRelations?.[hand.contact]?.known&&typeof window.changeContactTrustV13==='function')window.changeContactTrustV13(hand.contact,late?0:1,'Long-haul relay completed');
 const rec={...copy(a),status:'delivered',deliveredAt:now,lateMinutes:late,reward,multiHop:true,totalPayout:total};s.history.unshift(rec);s.history=s.history.slice(0,24);s.active=null;s.stats.delivered=(s.stats.delivered||0)+1;s.stats.crossDelivered=(s.stats.crossDelivered||0)+1;s.stats.multiHopDelivered++;if(late)s.stats.late=(s.stats.late||0)+1;Game.pendingPath=null;Game._v133TravelTarget=null;window.streetToastV134?.(`${a.label} ${late?'LATE':'DELIVERED'} · ¢${reward}`);window.addJournal?.('side',`${a.label} ${late?'LATE':'DELIVERED'}`,`${p.originalSourceName} → ${p.handoffName} → ${p.finalName}. Two city crossings completed. Paid ¢${reward}.`);window.updateNeighborhoodHUDV134?.();window.updateOverworldHUD?.();window.saveGame?.(0,true);update();return rec}
function complete(w=world()){const a=active(),p=a?.multiHopPlan;if(!a||!p)return false;if(p.stage===1)return handoff(a,w);if(p.stage===2)return finalDelivery(a,w);return false}
window.tryCompleteMultiHopDispatchV12104=complete;
function beginSecondLeg(){const a=active(),p=a?.multiHopPlan,w=world();if(!a||!p||p.stage!=='handoff'||a.phase!=='handoff'||w?.id!==p.handoffDistrict)return false;const hp=w.locations?.[p.handoffId];if(!hp||!Game.ovPlayer||Math.hypot(Game.ovPlayer.x-hp.x,Game.ovPlayer.y-hp.y)>2.15)return false;archiveDisruption(a);delete a.dynamicDisruption;delete a.dynamicDisruptionTriggered;delete a.dynamicDisruptionArm;p.stage=2;p.secondLegStartedAt=nowMin();applyLeg(a,p.leg2);a.deadline=p.deadline;a.payout=chainPayout(p);Game.cityLife=Game.cityLife||{};Game.cityLife.discovered=Game.cityLife.discovered||{};Game.cityLife.discovered[p.handoffId]=true;window.addJournal?.('side','LONG-HAUL LEG 2',`${p.handoffName} transfer complete. Choose a second physical crossing toward ${p.finalName}, ${p.finalDistrictName}.`);window.streetToastV134?.('LEG 2 · CHOOSE TRANSIT');window.saveGame?.(0,true);update();return true}
window.beginSecondLegMultiHopV12104=beginSecondLeg;
function abandon(){const s=state(),a=active(),p=a?.multiHopPlan;if(!a||!p)return false;archiveDisruption(a);const src=def(p.originalSourceDistrict,p.originalSourceId);if(src?.contact&&Game.contactRelations?.[src.contact]?.known&&typeof window.changeContactTrustV13==='function')window.changeContactTrustV13(src.contact,-2,'Abandoned long-haul dispatch');s.history.unshift({...copy(a),status:'abandoned',endedAt:nowMin(),multiHop:true});s.history=s.history.slice(0,24);s.active=null;s.stats.abandoned=(s.stats.abandoned||0)+1;s.stats.crossAbandoned=(s.stats.crossAbandoned||0)+1;s.stats.multiHopAbandoned++;Game.pendingPath=null;Game._v133TravelTarget=null;window.streetToastV134?.('LONG-HAUL RUN ABANDONED');window.saveGame?.(0,true);update();return true}
window.abandonMultiHopDispatchV12104=abandon;
function riskLabel(r){return r>=.72?'SEVERE':r>=.52?'HIGH':r>=.32?'ELEVATED':'MANAGEABLE'}
function panel(){let p=document.getElementById('v12104-multihop-panel'),wrap=document.querySelector('#overworld-screen .wrap');if(!wrap)return null;if(!document.getElementById('v12104-multihop-style')){const st=document.createElement('style');st.id='v12104-multihop-style';st.textContent=`#v12104-multihop-panel{position:absolute;left:50%;bottom:82px;transform:translateX(-50%);z-index:29;width:min(390px,calc(100% - 28px));max-height:min(62vh,520px);overflow:auto;padding:12px 13px;background:rgba(5,11,15,.98);border:1px solid rgba(85,220,255,.58);box-shadow:0 12px 34px rgba(0,0,0,.58);font:12px/1.38 monospace;color:#e0f4f7;display:none;pointer-events:auto}#v12104-multihop-panel .k{font-size:10px;letter-spacing:.14em;color:#55dcff}#v12104-multihop-panel .meta{margin:6px 0;color:#b8cbd0}#v12104-multihop-panel .chain{padding:7px;margin:7px 0;background:rgba(85,220,255,.06);border-left:2px solid #55dcff}#v12104-multihop-panel .terms{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;margin:7px 0}#v12104-multihop-panel .terms span{padding:5px 3px;background:rgba(255,255,255,.05);text-align:center}#v12104-multihop-panel .choice{margin:7px 0;padding:7px;border:1px solid rgba(255,255,255,.11)}#v12104-multihop-panel button{width:100%;min-height:42px;margin-top:5px}@media(max-width:520px){#v12104-multihop-panel{left:8px;right:8px;bottom:74px;transform:none;width:auto;max-height:58vh;padding:10px}#v12104-multihop-panel button{min-height:44px}}`;document.head.appendChild(st)}if(!p){p=document.createElement('div');p.id='v12104-multihop-panel';wrap.appendChild(p)}return p}
function renderActive(p,a){const plan=a.multiHopPlan,base=document.getElementById('v12104-interdistrict-panel'),d=a.dynamicDisruption;if(base)base.style.display='none';if(d?.status==='alert'){p.style.display='none';return}p.style.display='block';const remain=plan.deadline-nowMin(),stage=plan.stage;let body=`<div class="k">LONG-HAUL MULTI-HOP · ${stage===2?'LEG 2 / 2':stage==='handoff'?'HANDOFF':'LEG 1 / 2'}</div><b>${a.label}</b><div class="chain">${plan.originalSourceName}<br>↓ ${plan.handoffName} · ${plan.handoffDistrictName}<br>↓ ${plan.finalName} · ${plan.finalDistrictName}</div><div class="terms"><span>¢${chainPayout(plan)}<br>PROJECTED</span><span>${riskLabel(chainRisk(plan))}<br>CHAIN RISK</span><span>${remain>=0?remain:Math.abs(remain)}<br>${remain>=0?'MIN LEFT':'MIN LATE'}</span></div>`;
 if(stage==='handoff'){body+=`<div class="choice"><b>PHYSICAL HANDOFF COMPLETE</b><div class="meta">Cargo is secured at ${plan.handoffName}. Confirm the transfer here, then choose the second city crossing.</div><button class="btn small" id="v12104-multi-leg2">PREP SECOND LEG</button></div>`}
 else if(a.phase==='choose_transit'){body+=`<div class="meta">Choose crossing ${stage===2?'2':'1'} of 2. You must physically reach its transit node.</div>`+a.options.map(o=>`<div class="choice"><b>${o.linkName}</b> · ${o.linkType.toUpperCase()}<div class="terms"><span>¢${o.payout}<br>LEG VALUE</span><span>${riskLabel(o.risk)}<br>RISK</span><span>${o.cost?`¢${o.cost}`:'FREE'}<br>FARE</span></div><button class="btn small" data-multi-link="${o.linkId}" ${o.blocked?'disabled':''}>${o.blocked?'UNAVAILABLE':'ROUTE VIA '+o.linkType.toUpperCase()}</button></div>`).join('')}
 else if(a.phase==='to_transit'){body+=`<div class="choice"><b>TO TRANSIT · ${a.chosenOption?.linkName||''}</b><div class="meta">Follow the physical street route to the marked ${a.chosenOption?.linkType||'transit'} node. Live neighborhood pressure can disrupt this leg.</div></div>`}
 else if(a.phase==='last_mile'){const target=world()?.locations?.[a.targetId],dist=target&&Game.ovPlayer?Math.round(Math.hypot(Game.ovPlayer.x-target.x,Game.ovPlayer.y-target.y)):null;body+=`<div class="choice"><b>${stage===1?'HANDOFF APPROACH':'FINAL APPROACH'}</b><div class="meta">Reach ${a.targetName} physically.</div><div class="terms"><span>${dist===null?'—':dist}<br>CELLS</span><span>${stage===1?'TRANSFER':'DELIVER'}<br>OBJECTIVE</span><span>${plan.disruptions.length}<br>PAST DISRUPTIONS</span></div><button class="btn small" id="v12104-multi-route">ROUTE TO ${stage===1?'HANDOFF':'DROP'}</button></div>`}
 body+=`<button class="btn small" id="v12104-multi-abandon">ABANDON LONG-HAUL RUN</button>`;p.innerHTML=body;p.querySelectorAll('[data-multi-link]').forEach(b=>b.onclick=()=>window.chooseInterdistrictTransitV12104?.(b.dataset.multiLink));p.querySelector('#v12104-multi-leg2')?.addEventListener('click',beginSecondLeg);p.querySelector('#v12104-multi-route')?.addEventListener('click',()=>window.routeToLocationV133?.(a.targetId));p.querySelector('#v12104-multi-abandon').onclick=abandon}
function enhanceOffer(){const base=document.getElementById('v12104-interdistrict-panel'),w=world(),n=nearSource(w);if(!base||base.style.display==='none'||!n||base.querySelector('#v12104-multi-accept'))return;const o=offer(n.id,w);if(!o)return;const box=document.createElement('div');box.className='choice';box.id='v12104-multi-offer';box.innerHTML=`<div class="k">LONG-HAUL OPTION</div><div class="meta">${o.sourceName} → ${o.handoffName} → ${o.finalName}<br>2 physical crossings · intermediate handoff · ¢${o.estimatedPayout} est.</div><button class="btn small" id="v12104-multi-accept">ACCEPT MULTI-HOP RUN</button>`;base.appendChild(box);box.querySelector('#v12104-multi-accept').onclick=()=>accept(o.id)}
function update(){const p=panel();if(!p)return;const a=active();if(Game.screen!=='overworld-screen'){p.style.display='none';return}if(a){renderActive(p,a);return}p.style.display='none';enhanceOffer()}
window.updateMultiHopDispatchUIV12104=update;
const baseUI=window.updateInterdistrictDispatchUIV12104;if(baseUI)window.updateInterdistrictDispatchUIV12104=function(){const r=baseUI.apply(this,arguments);update();return r};
const prevStep=window.onStreetStepV134;window.onStreetStepV134=function(w){const r=prevStep?.apply(this,arguments);update();return r};
const prevInit=window.initOverworldV133;if(prevInit){const wrapped=function(){const r=prevInit.apply(this,arguments);update();return r};window.initOverworldV133=wrapped;if(window.initOverworld===prevInit)window.initOverworld=wrapped}
setTimeout(()=>{baseUI?.();update()},0);window.CR_CITY_MULTIHOP_LOGISTICS={version:VERSION,offer,accept,beginSecondLeg,complete,abandon,update};
})();
}''',encoding='utf-8')

manifest=root/'src/bootstrap/module-manifest.js'
s=manifest.read_text(encoding='utf-8')
entry="  'world.multiHopLogistics':{path:'./src/world/multihop-logistics-pwa12-104-city-candidate-04.js',kind:'module'},\n"
if 'world.multiHopLogistics' not in s:
    needle="  'world.dynamicLogisticsDisruptions':{path:'./src/world/dynamic-logistics-disruptions-pwa12-104-city-candidate-03.js',kind:'module'},\n"
    if needle not in s: raise SystemExit('candidate 03 manifest seam missing')
    s=s.replace(needle,needle+entry,1)
    order="'world.livingStreets','world.districtDispatches','world.interdistrictLogistics','world.dynamicLogisticsDisruptions','missions.approaches'"
    if order not in s: raise SystemExit('candidate 03 manifest order seam missing')
    s=s.replace(order,"'world.livingStreets','world.districtDispatches','world.interdistrictLogistics','world.dynamicLogisticsDisruptions','world.multiHopLogistics','missions.approaches'",1)
manifest.write_text(s,encoding='utf-8')

bundle=root/'src/runtime/runtime-bundle.js'
s=bundle.read_text(encoding='utf-8')
dyn='/* SOURCE: src/world/dynamic-logistics-disruptions-pwa12-104-city-candidate-03.js */'
multi='/* SOURCE: src/world/multihop-logistics-pwa12-104-city-candidate-04.js */'
mission='/* SOURCE: src/missions/contract-approaches-v13-4b.js */'
if dyn not in s or mission not in s: raise SystemExit('candidate 03 runtime seam missing')
if multi not in s:s=s.replace(mission,multi+'\n'+mission,1)
pos=[s.index(x) for x in (dyn,multi,mission)]
if pos!=sorted(pos):raise SystemExit(f'multi-hop runtime order invalid: {pos}')
bundle.write_text(s,encoding='utf-8')
print('patched multi-hop logistics candidate 04',root)
