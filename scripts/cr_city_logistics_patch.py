from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve()
module=root/'src/world/interdistrict-logistics-pwa12-104-city-candidate-02.js'
module.write_text(r'''if(typeof window!=='undefined'){
(() => {
'use strict';
const LOGISTICS_VERSION='pwa12.104-city-logistics-candidate.02';
const CARGO_L={
 courier:{label:'COURIER RELAY',verb:'sealed courier package',base:360,heat:-1,prosperity:1},
 medical:{label:'CROSS-CITY MEDICAL RUN',verb:'temperature-locked medical case',base:460,heat:-2,prosperity:1},
 data:{label:'AIR-GAPPED DATA TRANSFER',verb:'air-gapped data shard',base:520,heat:2,prosperity:0},
 contraband:{label:'INTERDISTRICT CONTRABAND',verb:'unregistered cargo case',base:640,heat:7,prosperity:0}
};
const LINK_RISK_L={border:.24,metro:.16,freight:.28,security:.46,hidden:.10};
function clampL(v,a,b){return Math.max(a,Math.min(b,v))}
function hashL(...parts){let h=2166136261>>>0;for(const s0 of parts){const s=String(s0??'');for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)}}return h>>>0}
function nowMinutesL(){return Math.round((((Game.day||1)-1)*24+(Game.hour||0))*60)}
function districtNameL(id){return window.V133_DISTRICTS?.[id]?.name||String(id||'UNKNOWN').replaceAll('_',' ').toUpperCase()}
function ensureLogisticsStateL(){
 const street=window.ensureLivingStreetsStateV134?.()||(Game.livingStreetsV134=Game.livingStreetsV134||{});
 street.interdistrictLogistics=street.interdistrictLogistics||{};const s=street.interdistrictLogistics;
 s.version=1;s.active=s.active||null;s.offers=s.offers||{};s.history=Array.isArray(s.history)?s.history:[];s.stats=s.stats||{accepted:0,delivered:0,late:0,abandoned:0,rerouted:0,transfers:0};return s
}
window.ensureInterdistrictLogisticsStateV12104=ensureLogisticsStateL;
function worldL(){return window.currentDistrictV133?.()||null}
function defsL(district){return window.V13_DISTRICT_LOCATIONS?.[district]||[]}
function defL(district,id){return defsL(district).find(x=>x.id===id)||null}
function nearSourceL(world=worldL()){return window.nearDistrictDispatchLocationV12104?.(world)||null}
function linkKnownL(link){return !!link&&(link.type!=='hidden'||!!Game.districtWorldsV133?.hiddenLinks?.[link.id])}
function endpointL(link,district){if(link?.from?.district===district)return link.from;if(link?.to?.district===district)return link.to;return null}
function otherL(link,district){if(link?.from?.district===district)return link.to;if(link?.to?.district===district)return link.from;return null}
function accessL(link){
 if(!linkKnownL(link))return{allowed:false,mode:'locked',reason:'UNDISCOVERED'};
 const n=Number(Game.notoriety||0);
 if(link.type==='security'){
  const rep=Number(Game.rep?.[link.faction]||0);if(n<58||rep>=25)return{allowed:true,mode:'clear',reason:'CLEAR'};
  return{allowed:false,mode:Game.roster?.some(u=>u.className==='Hacker'||u.className==='AgentEX')?'bribe/hack':'bribe',reason:'CHECKPOINT',bribe:Math.round(600+n*16)}
 }
 if(link.type==='metro'&&n>=90)return{allowed:false,mode:'bribe',reason:'WATCHLIST',bribe:850};
 return{allowed:true,mode:'clear',reason:'CLEAR'}
}
window.logisticsTransitAccessV12104=accessL;
function linkRiskL(link){
 const n=Number(Game.notoriety||0),a=accessL(link);let r=LINK_RISK_L[link.type]??.30;
 r+=Math.min(.22,n/500);if(!a.allowed)r+=a.mode==='locked'?.45:.20;
 if(link.type==='security'&&Number(Game.rep?.[link.faction]||0)>=25)r-=.16;
 return clampL(r,.04,.95)
}
function enumeratePathsL(from,to,maxLegs=5){
 const links=(window.V133_TRANSIT_LINKS||[]).filter(linkKnownL),out=[];
 function walk(cur,path,visited){
  if(path.length>maxLegs)return;if(cur===to){out.push(path.slice());return}
  for(const link of links){const next=otherL(link,cur);if(!next||visited.has(next.district))continue;visited.add(next.district);path.push(link);walk(next.district,path,visited);path.pop();visited.delete(next.district);if(out.length>=96)return}
 }
 walk(from,[],new Set([from]));return out
}
function pathMetricsL(path){
 let minutes=0,cost=0,survival=1,restrictions=0;
 for(const link of path){minutes+=Number(link.minutes||12);cost+=Number(link.cost||0);const r=linkRiskL(link);survival*=1-r;if(!accessL(link).allowed)restrictions++}
 const risk=clampL(1-survival,0,1);return{minutes,cost,risk:Number(risk.toFixed(3)),restrictions,legs:path.length,links:path.map(x=>x.id)}
}
function routePlansL(from,to){
 const paths=enumeratePathsL(from,to,5).filter(p=>p.length);if(!paths.length)return[];
 const rows=paths.map(p=>({...pathMetricsL(p),raw:p}));
 const selectors=[
  ['FASTEST',r=>r.minutes+r.risk*7+r.restrictions*5],
  ['CHEAPEST',r=>r.cost+r.minutes*2+r.restrictions*140],
  ['LOW PROFILE',r=>r.risk*1000+r.restrictions*260+r.minutes*3+r.cost*.25]
 ];
 const used=new Set(),plans=[];
 for(const [mode,score] of selectors){const ranked=rows.slice().sort((a,b)=>score(a)-score(b));const pick=ranked.find(r=>!used.has(r.links.join('|')))||ranked[0];if(!pick)continue;const key=pick.links.join('|');if(used.has(key))continue;used.add(key);plans.push({id:mode.toLowerCase().replace(' ','_'),mode,...pick,raw:undefined})}
 return plans
}
window.planInterdistrictLogisticsV12104=routePlansL;
function sourceCargoL(src,seed){
 let kinds;if(src?.shop){const shop=(window.V13_SHOPS||[]).find(s=>s.id===src.shop);kinds=shop?.type==='clinic'?['medical','courier','data']:['courier','contraband','data']}
 else if(src?.contact){const c=(window.V13_CONTACTS||[]).find(x=>x.id===src.contact),services=c?.services||[];kinds=services.includes('clinic')?['medical','data','courier']:services.includes('smuggling')?['contraband','courier','data']:['data','courier','contraband']}
 else kinds=['courier','data'];return kinds[seed%kinds.length]
}
function chooseTargetL(sourceDistrict,sourceId){
 const districts=Object.keys(window.V133_DISTRICTS||{}).filter(d=>d!==sourceDistrict&&defsL(d).length);
 const scored=[];for(const d of districts){const plans=routePlansL(sourceDistrict,d);if(!plans.length)continue;const minLeg=Math.min(...plans.map(p=>p.legs));scored.push({district:d,plans,minLeg})}
 if(!scored.length)return null;const deeper=scored.filter(x=>x.minLeg>=2&&x.minLeg<=4),pool=deeper.length?deeper:scored;pool.sort((a,b)=>(hashL(Game.day||1,sourceDistrict,sourceId,a.district)%100000)-(hashL(Game.day||1,sourceDistrict,sourceId,b.district)%100000));const pick=pool[0];
 const targets=defsL(pick.district).filter(d=>d?.id);if(!targets.length)return null;const target=targets[hashL(sourceId,pick.district,Game.day||1)%targets.length];return{district:pick.district,target,plans:pick.plans}
}
function sourceNeighborhoodRiskL(world,sourceId){const p=world?.locations?.[sourceId],h=p?.neighborhood&&window.ensureNeighborhoodStateV134?.(world)?.[p.neighborhood];if(!h)return .3;return clampL((Number(h.localHeat||0)/100)*.42+(Number(h.gangPressure||0)/5)*.28+(Number(h.unrest||0)/5)*.18+(Number(h.security||0)/5)*.12,0,1)}
function offerLogisticsL(sourceId,world=worldL()){
 if(!world||!world.locations?.[sourceId])return null;const src=defL(world.id,sourceId),near=nearSourceL(world);if(!src||!near||near.id!==sourceId)return null;
 const state=ensureLogisticsStateL(),key=`${world.id}:${sourceId}:${Game.day||1}`;if(state.offers[key])return state.offers[key];const target=chooseTargetL(world.id,sourceId);if(!target)return null;
 const seed=hashL(world.id,sourceId,target.district,Game.day||1),kind=sourceCargoL(src,seed),spec=CARGO_L[kind],best=target.plans[0],sourceRisk=sourceNeighborhoodRiskL(world,sourceId),networkRisk=target.plans.reduce((n,p)=>n+p.risk,0)/target.plans.length;
 const payout=Math.round((spec.base+best.minutes*9+best.legs*135+(sourceRisk*.35+networkRisk*.65)*420)/10)*10;
 const offer={id:`ilog_${world.id}_${Game.day||1}_${sourceId}`,day:Game.day||1,sourceDistrict:world.id,sourceId,sourceName:src.name,sourceContact:src.contact||null,targetDistrict:target.district,targetId:target.target.id,targetName:target.target.name,kind,label:spec.label,verb:spec.verb,payout,plans:target.plans.map(p=>({...p})),createdAt:nowMinutesL()};state.offers[key]=offer;return offer
}
window.offerInterdistrictLogisticsV12104=offerLogisticsL;
function activeL(){return ensureLogisticsStateL().active}
window.activeInterdistrictLogisticsV12104=activeL;
function revealTargetL(a){Game.cityLife=Game.cityLife||{};Game.cityLife.discovered=Game.cityLife.discovered||{};Game.cityLife.discovered[a.targetId]=true}
function currentLegL(a){return a?.links?.[a.legIndex]||null}
function transitNodeForL(linkId,district=worldL()?.id){const link=(window.V133_TRANSIT_LINKS||[]).find(x=>x.id===linkId);return endpointL(link,district)?.node||null}
function routeStageL(a=activeL()){
 const world=worldL();if(!a||!world)return false;
 if(world.id===a.targetDistrict&&a.legIndex>=a.links.length){a.stage='to_drop';const ok=window.routeToLocationV133?.(a.targetId);updateLogisticsUIL();return !!ok}
 const linkId=currentLegL(a),node=transitNodeForL(linkId,world.id);if(!linkId||!node)return replanActiveL('route mismatch');
 a.stage='to_transit';a.currentDistrict=world.id;const ok=window.routeToTransitNodeV133?.(node);if(ok){a.nextNode=node;a.nextLink=linkId}updateLogisticsUIL();return !!ok
}
window.routeActiveInterdistrictLogisticsV12104=routeStageL;
function acceptLogisticsL(offerId,planId){
 const world=worldL(),near=nearSourceL(world),offer=near?offerLogisticsL(near.id,world):null,state=ensureLogisticsStateL();if(!offer||offer.id!==offerId||state.active||window.activeDistrictDispatchV12104?.())return false;
 const plan=offer.plans.find(p=>p.id===planId);if(!plan||near.id!==offer.sourceId||world.id!==offer.sourceDistrict)return false;
 const start=nowMinutesL();state.active={...offer,plans:undefined,planMode:plan.mode,planId:plan.id,links:plan.links.slice(),legIndex:0,stage:'to_transit',acceptedAt:start,deadline:start+Math.max(80,plan.minutes+plan.legs*14+58),routeRisk:plan.risk,transitCost:plan.cost,reroutes:0,transferHistory:[],currentDistrict:world.id};
 revealTargetL(state.active);if(!routeStageL(state.active)){state.active=null;return false}state.stats.accepted++;window.addJournal?.('side','INTERDISTRICT LOGISTICS',`${offer.sourceName} → ${offer.targetName}, ${districtNameL(offer.targetDistrict)}. ${plan.mode} transit chain selected; physical transfers required.`);window.streetToastV134?.(`${offer.label} · ${plan.mode} CHAIN COMMITTED`);window.saveGame?.(0,true);updateLogisticsUIL();return true
}
window.acceptInterdistrictLogisticsV12104=acceptLogisticsL;
function selectPlanByModeL(plans,mode){return plans.find(p=>p.mode===mode)||plans[0]||null}
function replanActiveL(reason='network change'){
 const a=activeL(),world=worldL();if(!a||!world)return false;if(world.id===a.targetDistrict){a.links=[];a.legIndex=0;a.stage='to_drop';a.currentDistrict=world.id;a.reroutes++;ensureLogisticsStateL().stats.rerouted++;window.saveGame?.(0,true);return routeStageL(a)}
 const plans=routePlansL(world.id,a.targetDistrict),plan=selectPlanByModeL(plans,a.planMode);if(!plan)return false;a.links=plan.links.slice();a.legIndex=0;a.stage='to_transit';a.currentDistrict=world.id;a.routeRisk=plan.risk;a.transitCost=plan.cost;a.reroutes++;ensureLogisticsStateL().stats.rerouted++;a.transferHistory.push({at:nowMinutesL(),kind:'reroute',district:world.id,reason,links:a.links.slice()});window.addJournal?.('side','LOGISTICS REROUTE',`${districtNameL(world.id)}: ${reason}. ${a.planMode} network path recalculated.`);window.saveGame?.(0,true);return routeStageL(a)
}
window.replanActiveInterdistrictLogisticsV12104=replanActiveL;
function transitCompleteL(evt){
 const state=ensureLogisticsStateL(),a=state.active;if(!a||!evt)return false;const expected=currentLegL(a);a.transferHistory.push({at:nowMinutesL(),kind:'transit',linkId:evt.linkId,from:evt.from,to:evt.to,expected:expected===evt.linkId});state.stats.transfers++;
 if(evt.linkId===expected){a.legIndex++;a.currentDistrict=evt.to;if(a.legIndex>=a.links.length&&evt.to===a.targetDistrict)a.stage='to_drop';else a.stage='to_transit'}else{a.currentDistrict=evt.to;a.reroutes++;state.stats.rerouted++;const plans=routePlansL(evt.to,a.targetDistrict),plan=selectPlanByModeL(plans,a.planMode);if(!plan){a.stage='stranded';window.saveGame?.(0,true);updateLogisticsUIL();return false}a.links=plan.links.slice();a.legIndex=0;a.routeRisk=plan.risk;a.transitCost=plan.cost;a.stage=evt.to===a.targetDistrict?'to_drop':'to_transit';window.addJournal?.('side','LOGISTICS ROUTE DEVIATION',`${districtNameL(evt.to)}: route deviation detected; remaining ${a.planMode} chain recalculated.`)}
 window.saveGame?.(0,true);setTimeout(()=>routeStageL(a),80);updateLogisticsUIL();return true
}
const priorTransitHookL=window.onDistrictTransitCompleteV12104;
window.onDistrictTransitCompleteV12104=function(evt){priorTransitHookL?.(evt);return transitCompleteL(evt)};
function mutateHoodL(h,field,delta){if(!h)return;if(field==='localHeat')h[field]=clampL(Number(h[field]||0)+delta,0,100);else h[field]=clampL(Number(h[field]||0)+delta,0,5);h.events=Number(h.events||0)+1}
function completeLogisticsL(world=worldL()){
 const state=ensureLogisticsStateL(),a=state.active;if(!a||!world||world.id!==a.targetDistrict||a.legIndex<a.links.length)return false;const p=world.locations?.[a.targetId];if(!p||!Game.ovPlayer||Math.hypot(Game.ovPlayer.x-p.x,Game.ovPlayer.y-p.y)>2.15)return false;
 const spec=CARGO_L[a.kind]||CARGO_L.courier,now=nowMinutesL(),late=Math.max(0,now-a.deadline),mult=late?Math.max(.42,1-Math.min(1,late/120)*.58):1,reward=Math.max(0,Math.round(a.payout*mult/10)*10),h=p.neighborhood&&window.ensureNeighborhoodStateV134?.(world)?.[p.neighborhood];
 Game.credits=Number(Game.credits||0)+reward;mutateHoodL(h,'localHeat',spec.heat+(a.reroutes&&['data','contraband'].includes(a.kind)?1:0));if(spec.prosperity)mutateHoodL(h,'prosperity',spec.prosperity);if(a.kind==='medical')mutateHoodL(h,'unrest',-1);
 if(a.sourceContact&&Game.contactRelations?.[a.sourceContact]?.known&&typeof window.changeContactTrustV13==='function')window.changeContactTrustV13(a.sourceContact,late?-1:1,late?'Late interdistrict logistics':'Completed interdistrict logistics');
 const record={...a,status:'delivered',deliveredAt:now,lateMinutes:late,reward};state.history.unshift(record);state.history=state.history.slice(0,24);state.active=null;state.stats.delivered++;if(late)state.stats.late++;
 window.addJournal?.('side',`${a.label} ${late?'LATE':'DELIVERED'}`,`${a.targetName}, ${districtNameL(a.targetDistrict)} received ${a.verb}. Paid ¢${reward}; ${a.transferHistory.filter(x=>x.kind==='transit').length} physical transfer(s).`);window.streetToastV134?.(`${a.label} ${late?'LATE':'DELIVERED'} · ¢${reward}`);window.updateNeighborhoodHUDV134?.();window.updateOverworldHUD?.();window.saveGame?.(0,true);updateLogisticsUIL();return record
}
window.tryCompleteInterdistrictLogisticsV12104=completeLogisticsL;
function abandonLogisticsL(){const state=ensureLogisticsStateL(),a=state.active;if(!a)return false;if(a.sourceContact&&Game.contactRelations?.[a.sourceContact]?.known&&typeof window.changeContactTrustV13==='function')window.changeContactTrustV13(a.sourceContact,-1,'Abandoned interdistrict logistics');state.history.unshift({...a,status:'abandoned',endedAt:nowMinutesL()});state.history=state.history.slice(0,24);state.active=null;state.stats.abandoned++;Game.pendingPath=null;Game._v133TravelTarget=null;window.streetToastV134?.('INTERDISTRICT LOGISTICS ABANDONED');window.saveGame?.(0,true);updateLogisticsUIL();return true}
window.abandonInterdistrictLogisticsV12104=abandonLogisticsL;
function riskLabelL(r){return r>=.72?'SEVERE':r>=.52?'HIGH':r>=.32?'ELEVATED':'MANAGEABLE'}
function ensureLogisticsUIL(){
 let panel=document.getElementById('v12104-logistics-panel'),wrap=document.querySelector('#overworld-screen .wrap');if(!wrap)return null;
 if(!document.getElementById('v12104-logistics-style')){const st=document.createElement('style');st.id='v12104-logistics-style';st.textContent=`#v12104-logistics-panel{position:absolute;right:14px;bottom:84px;z-index:25;width:min(370px,calc(100% - 28px));max-height:min(72vh,620px);overflow:auto;padding:11px 12px;background:rgba(4,10,15,.96);border:1px solid rgba(78,221,242,.42);box-shadow:0 10px 30px rgba(0,0,0,.48);font:12px/1.35 monospace;color:#d7ecf1;display:none;pointer-events:auto}#v12104-logistics-panel .k{font-size:10px;letter-spacing:.13em;color:#4eddf2}#v12104-logistics-panel b{color:#fff}#v12104-logistics-panel .meta{margin:6px 0;color:#a8bec5}#v12104-logistics-panel .route{margin:7px 0;padding:7px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.035)}#v12104-logistics-panel .route strong{display:block;color:#fff;margin-bottom:3px}#v12104-logistics-panel .actions{display:flex;gap:6px;flex-wrap:wrap;margin-top:7px}#v12104-logistics-panel button{min-height:40px;flex:1 1 135px;white-space:normal}#v12104-logistics-panel .local{border-top:1px solid rgba(255,255,255,.1);margin-top:8px;padding-top:8px}@media(max-width:520px){#v12104-logistics-panel{left:8px;right:8px;bottom:76px;width:auto;max-height:64vh;padding:9px 10px}#v12104-logistics-panel button{min-height:44px;flex-basis:100%}}`;document.head.appendChild(st)}
 if(!panel){panel=document.createElement('div');panel.id='v12104-logistics-panel';wrap.appendChild(panel)}return panel
}
function nearTransitReadyL(a,world){const id=currentLegL(a),node=transitNodeForL(id,world?.id),tr=node&&world?.transit?.find(x=>x.id===node);return !!tr&&!!Game.ovPlayer&&Math.hypot(Game.ovPlayer.x-tr.x,Game.ovPlayer.y-tr.y)<=2.2}
function updateLogisticsUIL(){
 const panel=ensureLogisticsUIL(),localPanel=document.getElementById('v12104-dispatch-panel');if(!panel)return;const world=worldL(),state=ensureLogisticsStateL(),a=state.active;
 if(Game.screen!=='overworld-screen'||!world){panel.style.display='none';return}
 if(a){if(localPanel)localPanel.style.display='none';panel.style.display='block';const remain=a.deadline-nowMinutesL(),atTarget=world.id===a.targetDistrict&&a.legIndex>=a.links.length,ready=!atTarget&&nearTransitReadyL(a,world),linkId=currentLegL(a),link=(window.V133_TRANSIT_LINKS||[]).find(x=>x.id===linkId),wrong=!atTarget&&(!link||!endpointL(link,world.id));
  panel.innerHTML=`<div class="k">ACTIVE INTERDISTRICT LOGISTICS</div><b>${a.label}</b><div class="meta">${a.sourceName} → ${a.targetName} · ${districtNameL(a.targetDistrict)}<br>${a.planMode} · ${a.transferHistory.filter(x=>x.kind==='transit').length}/${a.links.length+a.transferHistory.filter(x=>x.kind==='transit').length-a.legIndex} transfers logged · ${remain>=0?`${remain} MIN TO WINDOW`:`${Math.abs(remain)} MIN LATE`}</div><div class="route"><strong>${wrong?'NETWORK DEVIATION':atTarget?'FINAL STREET LEG':ready?'TRANSFER READY':'NEXT TRANSFER'}</strong>${atTarget?`Deliver to ${a.targetName}.`:wrong?'Current district is off the stored chain. Replan from here.':`${link?.name||linkId} · ${String(link?.type||'route').toUpperCase()} · ${accessL(link).reason}`}</div><div class="actions"><button class="btn small" id="v12104-logistics-route">${wrong?'REPLAN NETWORK':atTarget?'ROUTE TO DROP':ready?'USE TRANSIT MARKER':'ROUTE TO TRANSIT'}</button><button class="btn small" id="v12104-logistics-map">CITY MAP</button><button class="btn small" id="v12104-logistics-abandon">ABANDON</button></div>`;
  panel.querySelector('#v12104-logistics-route').onclick=()=>wrong?replanActiveL('manual deviation'):ready?window.streetToastV134?.('Use the transit marker here to cross physically.'):routeStageL(a);panel.querySelector('#v12104-logistics-map').onclick=()=>window.openStrategicCityMapV133?.();panel.querySelector('#v12104-logistics-abandon').onclick=()=>abandonLogisticsL();return
 }
 if(window.activeDistrictDispatchV12104?.()){panel.style.display='none';return}
 const near=nearSourceL(world);if(!near){panel.style.display='none';return}const offer=offerLogisticsL(near.id,world);if(!offer){panel.style.display='none';return}if(localPanel)localPanel.style.display='none';panel.style.display='block';const local=window.offerDistrictDispatchV12104?.(near.id,world)||null;
 panel.innerHTML=`<div class="k">${world.cfg.name.toUpperCase()} // STREET LOGISTICS</div><b>${offer.label}</b><div class="meta">${offer.sourceName} → <b>${offer.targetName}</b>, ${districtNameL(offer.targetDistrict)}<br>${offer.verb} · ¢${offer.payout} contract value. Choose the network route; every district transfer remains physical.</div>${offer.plans.map(p=>`<div class="route"><strong>${p.mode}</strong>${p.legs} TRANSFER${p.legs===1?'':'S'} · ${p.minutes} MIN NETWORK · ¢${p.cost} BASE TRANSIT · ${riskLabelL(p.risk)}${p.restrictions?` · ${p.restrictions} CHECK`:''}<div class="actions"><button class="btn small" data-logistics-plan="${p.id}">ACCEPT ${p.mode}</button></div></div>`).join('')}${local?`<div class="local"><span class="k">LOCAL ALTERNATIVE</span><div class="meta">${local.label} → ${local.targetName} · ¢${local.payout}</div><div class="actions"><button class="btn small" id="v12104-local-dispatch">TAKE LOCAL JOB</button></div></div>`:''}`;
 panel.querySelectorAll('[data-logistics-plan]').forEach(b=>b.onclick=()=>acceptLogisticsL(offer.id,b.dataset.logisticsPlan));if(local)panel.querySelector('#v12104-local-dispatch').onclick=()=>window.acceptDistrictDispatchV12104?.(local.id)
}
window.updateInterdistrictLogisticsUIV12104=updateLogisticsUIL;
const prevStreetStepL=window.onStreetStepV134;
window.onStreetStepV134=function(world){const r=prevStreetStepL?.apply(this,arguments);completeLogisticsL(world||worldL());updateLogisticsUIL();return r};
const prevInitL=window.initOverworldV133;
if(prevInitL){const wrapped=function(){const r=prevInitL.apply(this,arguments);completeLogisticsL(worldL());updateLogisticsUIL();return r};window.initOverworldV133=wrapped;if(window.initOverworld===prevInitL)window.initOverworld=wrapped}
setInterval(()=>{if(Game?.screen==='overworld-screen')updateLogisticsUIL()},900);
window.CR_CITY_INTERDISTRICT_LOGISTICS={version:LOGISTICS_VERSION,update:updateLogisticsUIL,plans:routePlansL};
})();
}
''',encoding='utf-8')

# A minimal transit-completion integration hook: it observes a transit only after
# canonical travelDistrictV133 has accepted access/cost, advanced time, and
# activated the destination district. It never replaces transit authority.
core=root/'src/world/district-worlds-v13-3.js'
s=core.read_text(encoding='utf-8')
old="activateDistrictV133(to.district,to.node);showScreen('overworld-screen');initOverworldV133();toast(`${V133_DISTRICTS[current].name} → ${V133_DISTRICTS[to.district].name}`);saveGame(0,true);return true"
new="activateDistrictV133(to.district,to.node);showScreen('overworld-screen');initOverworldV133();window.onDistrictTransitCompleteV12104?.({linkId:link.id,from:current,to:to.district,node:to.node,mode});toast(`${V133_DISTRICTS[current].name} → ${V133_DISTRICTS[to.district].name}`);saveGame(0,true);return true"
if s.count(old)!=1: raise SystemExit(f'transit hook seam count={s.count(old)}')
s=s.replace(old,new,1);core.write_text(s,encoding='utf-8')

manifest=root/'src/bootstrap/module-manifest.js'
s=manifest.read_text(encoding='utf-8')
entry="  'world.interdistrictLogistics':{path:'./src/world/interdistrict-logistics-pwa12-104-city-candidate-02.js',kind:'module'},\n"
if 'world.interdistrictLogistics' not in s:
    needle="  'world.districtDispatches':{path:'./src/world/district-dispatches-pwa12-104-city-candidate-01.js',kind:'module'},\n"
    if needle not in s: raise SystemExit('district dispatch manifest seam missing')
    s=s.replace(needle,needle+entry,1)
    order="  'world.livingStreets','world.districtDispatches','missions.approaches','company','visuals','runtime'"
    if order not in s: raise SystemExit('manifest order seam missing')
    s=s.replace(order,"  'world.livingStreets','world.districtDispatches','world.interdistrictLogistics','missions.approaches','company','visuals','runtime'",1)
manifest.write_text(s,encoding='utf-8')
print('patched interdistrict logistics candidate',root)
