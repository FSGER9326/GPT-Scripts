from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve()
module=root/'src/world/district-dispatches-pwa12-104-city-candidate-01.js'
module.write_text(r'''if(typeof window!=='undefined'){
(() => {
'use strict';
const DISPATCH_VERSION='pwa12.104-city-candidate.01';
const DISPATCH_KIND={
 courier:{label:'COURIER RELAY',verb:'sealed courier package',base:220,heat:-1,prosperity:1},
 medical:{label:'MEDICAL RUN',verb:'temperature-locked medical case',base:280,heat:-2,prosperity:1},
 data:{label:'DATA DROP',verb:'air-gapped data shard',base:320,heat:2,prosperity:0},
 contraband:{label:'CONTRABAND HANDOFF',verb:'unregistered cargo case',base:410,heat:6,prosperity:0}
};
function clampD(v,a,b){return Math.max(a,Math.min(b,v))}
function hashD(...parts){let h=2166136261>>>0;for(const s0 of parts){const s=String(s0??'');for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)}}return h>>>0}
function nowMinutesD(){return Math.round((((Game.day||1)-1)*24+(Game.hour||0))*60)}
function ensureDispatchStateD(){
 const street=window.ensureLivingStreetsStateV134?.()||(Game.livingStreetsV134=Game.livingStreetsV134||{});
 street.districtDispatches=street.districtDispatches||{};const s=street.districtDispatches;
 s.version=1;s.active=s.active||null;s.offers=s.offers||{};s.history=Array.isArray(s.history)?s.history:[];s.stats=s.stats||{accepted:0,delivered:0,late:0,abandoned:0};return s
}
window.ensureDistrictDispatchStateV12104=ensureDispatchStateD;
function worldD(){return window.currentDistrictV133?.()||null}
function defsD(world=worldD()){return world?(window.V13_DISTRICT_LOCATIONS?.[world.id]||[]):[]}
function defD(id,world=worldD()){return defsD(world).find(x=>x.id===id)||null}
function knownD(d){return !!d&&(!!Game.cityLife?.discovered?.[d.id]||!!(d.contact&&Game.contactRelations?.[d.contact]?.known))}
function locationNameD(id,world=worldD()){return defD(id,world)?.name||id.replaceAll('_',' ').toUpperCase()}
function nearLocationD(world=worldD(),max=2.2){
 if(!world||!Game.ovPlayer)return null;let best=null;
 for(const d of defsD(world)){const p=world.locations?.[d.id];if(!p||!knownD(d))continue;const dist=Math.hypot(Game.ovPlayer.x-p.x,Game.ovPlayer.y-p.y);if(dist<=max&&(!best||dist<best.dist))best={id:d.id,def:d,point:p,dist}}
 return best
}
window.nearDistrictDispatchLocationV12104=nearLocationD;
function nearestHoodIdD(world,p){let best=null,bd=Infinity;for(const n of world.neighborhoods||[]){const d=Math.hypot((p.x||0)-n.x,(p.y||0)-n.y);if(d<bd){bd=d;best=n.id}}return best}
function hoodStateD(world,id){return window.ensureNeighborhoodStateV134?.(world)?.[id]||null}
function hoodRiskD(h,kind){if(!h)return .35;const heat=(h.localHeat||0)/100,gang=(h.gangPressure||0)/5,unrest=(h.unrest||0)/5,security=(h.security||0)/5;const secWeight=(kind==='contraband'||kind==='data')?.30:.12;return clampD(heat*.34+gang*.28+unrest*.18+security*secWeight,0,1)}
function routeMetricsD(sourceId,targetId,world=worldD(),kind='courier'){
 const a=world?.locations?.[sourceId],b=world?.locations?.[targetId];if(!a||!b)return null;
 const path=window.findDistrictPathV133?.(a,b,world);if(!path?.length)return null;let risk=0,count=0,last=null;
 for(let i=0;i<path.length;i+=Math.max(1,Math.floor(path.length/12))){const hid=nearestHoodIdD(world,path[i]);if(hid===last)continue;last=hid;risk+=hoodRiskD(hoodStateD(world,hid),kind);count++}
 const targetH=world.locations[targetId]?.neighborhood;if(targetH&&targetH!==last){risk+=hoodRiskD(hoodStateD(world,targetH),kind);count++}
 return{blocks:Math.max(0,path.length-1),risk:clampD(count?risk/count:.3,0,1),path}
}
window.routeMetricsDistrictDispatchV12104=routeMetricsD;
function typeForSourceD(src,seed){let kinds;if(src?.shop){const shop=(window.V13_SHOPS||[]).find(s=>s.id===src.shop);kinds=shop?.type==='clinic'?['medical','courier','data']:['courier','contraband','data']}else if(src?.contact){const c=(window.V13_CONTACTS||[]).find(x=>x.id===src.contact),services=c?.services||[];kinds=services.includes('clinic')?['medical','data','courier']:services.includes('smuggling')?['contraband','courier','data']:['data','courier','contraband']}else kinds=['courier','data'];return kinds[seed%kinds.length]}
function quoteDispatchD(sourceId,targetId,world=worldD(),forcedKind=null){
 const src=defD(sourceId,world),dst=defD(targetId,world);if(!src||!dst||sourceId===targetId)return null;const seed=hashD(world.id,sourceId,targetId,Game.day||1),kind=forcedKind||typeForSourceD(src,seed),metrics=routeMetricsD(sourceId,targetId,world,kind);if(!metrics||metrics.blocks<4)return null;
 const spec=DISPATCH_KIND[kind],payout=Math.round((spec.base+metrics.blocks*4+metrics.risk*230)/10)*10,windowMin=Math.max(28,Math.ceil(18+metrics.blocks*.46+metrics.risk*14));
 return{kind,label:spec.label,verb:spec.verb,sourceId,targetId,sourceName:src.name,targetName:dst.name,blocks:metrics.blocks,risk:Number(metrics.risk.toFixed(3)),payout,windowMin}
}
window.quoteDistrictDispatchV12104=quoteDispatchD;
function offerDispatchD(sourceId,world=worldD()){
 if(!world||!world.locations?.[sourceId])return null;const src=defD(sourceId,world);if(!src||!knownD(src))return null;const state=ensureDispatchStateD(),key=`${world.id}:${sourceId}:${Game.day||1}`;if(state.offers[key])return state.offers[key];
 const ids=defsD(world).map(x=>x.id).filter(id=>id!==sourceId&&world.locations?.[id]);const scored=[];
 for(const id of ids){const q=quoteDispatchD(sourceId,id,world);if(q&&q.blocks>=10)scored.push(q)}
 if(!scored.length)return null;scored.sort((a,b)=>((hashD(key,a.targetId)%100000)-(hashD(key,b.targetId)%100000))||b.blocks-a.blocks);const pick=scored[0];
 const offer={id:`dispatch_${world.id}_${Game.day||1}_${sourceId}`,district:world.id,day:Game.day||1,createdAt:nowMinutesD(),...pick};state.offers[key]=offer;return offer
}
window.offerDistrictDispatchV12104=offerDispatchD;
function activeDispatchD(){return ensureDispatchStateD().active}
window.activeDistrictDispatchV12104=activeDispatchD;
function sourceIsPhysicalD(offer,world=worldD()){const near=nearLocationD(world);return !!near&&near.id===offer?.sourceId&&world?.id===offer?.district}
function revealTargetD(offer){Game.cityLife=Game.cityLife||{};Game.cityLife.discovered=Game.cityLife.discovered||{};Game.cityLife.discovered[offer.targetId]=true}
function acceptDispatchD(id){
 const world=worldD(),near=nearLocationD(world),offer=near?offerDispatchD(near.id,world):null,state=ensureDispatchStateD();if(!offer||offer.id!==id||state.active||!sourceIsPhysicalD(offer,world))return false;
 revealTargetD(offer);if(!window.routeToLocationV133?.(offer.targetId))return false;const start=nowMinutesD();state.active={...offer,acceptedAt:start,deadline:start+offer.windowMin,status:'active'};state.stats.accepted++;window.streetToastV134?.(`${offer.label} · ROUTE COMMITTED`);window.addJournal?.('side',offer.label,`${offer.sourceName} → ${offer.targetName}. Physical delivery route committed; ¢${offer.payout} on-time.`);window.saveGame?.(0,true);updateDispatchUID();return true
}
window.acceptDistrictDispatchV12104=acceptDispatchD;
function mutateHoodD(h,field,delta){if(!h)return;if(field==='localHeat')h[field]=clampD((h[field]||0)+delta,0,100);else h[field]=clampD((h[field]||0)+delta,0,5);h.events=(h.events||0)+1}
function completeDispatchD(world=worldD()){
 const state=ensureDispatchStateD(),a=state.active;if(!a||!world||a.district!==world.id)return false;const p=world.locations?.[a.targetId];if(!p||!Game.ovPlayer||Math.hypot(Game.ovPlayer.x-p.x,Game.ovPlayer.y-p.y)>2.15)return false;
 const spec=DISPATCH_KIND[a.kind]||DISPATCH_KIND.courier,now=nowMinutesD(),late=Math.max(0,now-a.deadline),mult=late?Math.max(.45,1-Math.min(1,late/90)*.55):1,reward=Math.max(0,Math.round(a.payout*mult/10)*10),targetH=hoodStateD(world,p.neighborhood),sourceH=hoodStateD(world,world.locations?.[a.sourceId]?.neighborhood);
 Game.credits=(Game.credits||0)+reward;mutateHoodD(targetH,'localHeat',spec.heat);if(spec.prosperity)mutateHoodD(targetH,'prosperity',spec.prosperity);if(a.kind==='medical')mutateHoodD(targetH,'unrest',-1);if(a.kind==='contraband')mutateHoodD(sourceH,'localHeat',2);
 const src=defD(a.sourceId,world);if(src?.contact&&Game.contactRelations?.[src.contact]?.known&&typeof window.changeContactTrustV13==='function')window.changeContactTrustV13(src.contact,late?-1:1,late?'Late street dispatch':'Completed street dispatch');
 const record={...a,status:'delivered',deliveredAt:now,lateMinutes:late,reward};state.history.unshift(record);state.history=state.history.slice(0,24);state.active=null;state.stats.delivered++;if(late)state.stats.late++;
 window.addJournal?.('side',`${a.label} ${late?'LATE':'DELIVERED'}`,`${a.targetName}: ${late?`${late} minutes late; `:''}received ${a.verb}. Paid ¢${reward}.`);window.streetToastV134?.(`${a.label} ${late?'LATE':'DELIVERED'} · ¢${reward}`);window.updateNeighborhoodHUDV134?.();window.updateOverworldHUD?.();window.saveGame?.(0,true);updateDispatchUID();return record
}
window.tryCompleteDistrictDispatchV12104=completeDispatchD;
function abandonDispatchD(){const state=ensureDispatchStateD(),a=state.active,world=worldD();if(!a)return false;const src=defD(a.sourceId,world);if(src?.contact&&Game.contactRelations?.[src.contact]?.known&&typeof window.changeContactTrustV13==='function')window.changeContactTrustV13(src.contact,-1,'Abandoned street dispatch');const h=world?.locations?.[a.sourceId]?hoodStateD(world,world.locations[a.sourceId].neighborhood):null;mutateHoodD(h,'localHeat',2);state.history.unshift({...a,status:'abandoned',endedAt:nowMinutesD()});state.history=state.history.slice(0,24);state.active=null;state.stats.abandoned++;Game.pendingPath=null;Game._v133TravelTarget=null;window.streetToastV134?.('DISPATCH ABANDONED');window.saveGame?.(0,true);updateDispatchUID();return true}
window.abandonDistrictDispatchV12104=abandonDispatchD;
function fmtTimeD(min){const d=Math.floor(min/1440)+1,m=((min%1440)+1440)%1440,h=Math.floor(m/60),mm=Math.floor(m%60);return `D${d} ${String(h).padStart(2,'0')}:${String(mm).padStart(2,'0')}`}
function riskLabelD(r){return r>=.72?'SEVERE':r>=.52?'HIGH':r>=.32?'ELEVATED':'MANAGEABLE'}
function ensureDispatchUID(){
 let panel=document.getElementById('v12104-dispatch-panel');const wrap=document.querySelector('#overworld-screen .wrap');if(!wrap)return null;if(!document.getElementById('v12104-dispatch-style')){const st=document.createElement('style');st.id='v12104-dispatch-style';st.textContent=`#v12104-dispatch-panel{position:absolute;right:14px;bottom:84px;z-index:24;width:min(340px,calc(100% - 28px));padding:11px 12px;background:rgba(5,11,15,.94);border:1px solid rgba(67,215,232,.38);box-shadow:0 9px 28px rgba(0,0,0,.44);font:12px/1.35 monospace;color:#d8edf2;display:none;pointer-events:auto}#v12104-dispatch-panel b{color:#fff}#v12104-dispatch-panel .k{font-size:10px;letter-spacing:.13em;color:#43d7e8}#v12104-dispatch-panel .meta{margin:6px 0;color:#9db5bd}#v12104-dispatch-panel .terms{display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin:8px 0}#v12104-dispatch-panel .terms span{padding:5px;background:rgba(255,255,255,.04);text-align:center}#v12104-dispatch-panel .actions{display:flex;gap:6px;flex-wrap:wrap}#v12104-dispatch-panel button{min-height:38px;flex:1 1 120px}@media(max-width:520px){#v12104-dispatch-panel{left:8px;right:8px;bottom:76px;width:auto;padding:9px 10px}#v12104-dispatch-panel .terms{gap:3px}#v12104-dispatch-panel button{min-height:42px}}`;document.head.appendChild(st)}if(!panel){panel=document.createElement('div');panel.id='v12104-dispatch-panel';wrap.appendChild(panel)}return panel
}
function updateDispatchUID(){
 const panel=ensureDispatchUID();if(!panel)return;const world=worldD();if(Game.screen!=='overworld-screen'||!world){panel.style.display='none';return}const state=ensureDispatchStateD(),a=state.active;
 if(a){const now=nowMinutesD(),remain=a.deadline-now,here=world.id===a.district,target=world.locations?.[a.targetId],dist=here&&target&&Game.ovPlayer?Math.round(Math.hypot(Game.ovPlayer.x-target.x,Game.ovPlayer.y-target.y)):null;panel.style.display='block';panel.innerHTML=`<div class="k">ACTIVE LOCAL DISPATCH</div><b>${a.label}</b><div class="meta">${a.sourceName} → ${a.targetName}<br>${a.verb} · ${remain>=0?`${remain} MIN TO WINDOW`:`${Math.abs(remain)} MIN LATE`}</div><div class="terms"><span>¢${a.payout}<br>BASE</span><span>${riskLabelD(a.risk)}<br>RISK</span><span>${dist===null?'—':dist}<br>CELLS</span></div><div class="actions"><button class="btn small" id="v12104-route-dispatch">ROUTE TO DROP</button><button class="btn small" id="v12104-abandon-dispatch">ABANDON</button></div>`;panel.querySelector('#v12104-route-dispatch').onclick=()=>{if(!here){window.openStrategicCityMapV133?.();return}window.routeToLocationV133?.(a.targetId)};panel.querySelector('#v12104-abandon-dispatch').onclick=()=>abandonDispatchD();return}
 const near=nearLocationD(world);if(!near){panel.style.display='none';return}const offer=offerDispatchD(near.id,world);if(!offer){panel.style.display='none';return}panel.style.display='block';panel.innerHTML=`<div class="k">${world.cfg.name.toUpperCase()} // STREET DISPATCH</div><b>${offer.label}</b><div class="meta">Pickup confirmed at ${offer.sourceName}. Deliver a ${offer.verb} to <b>${offer.targetName}</b>. The destination coordinates enter your street map only when you take the job.</div><div class="terms"><span>¢${offer.payout}<br>PAYOUT</span><span>${offer.blocks}<br>BLOCKS</span><span>${riskLabelD(offer.risk)}<br>RISK</span></div><div class="actions"><button class="btn small" id="v12104-accept-dispatch">ACCEPT & ROUTE · ${offer.windowMin} MIN</button></div>`;panel.querySelector('#v12104-accept-dispatch').onclick=()=>acceptDispatchD(offer.id)
}
window.updateDistrictDispatchUIV12104=updateDispatchUID;
const prevStreetStep=window.onStreetStepV134;
window.onStreetStepV134=function(world){const r=prevStreetStep?.apply(this,arguments);completeDispatchD(world||worldD());updateDispatchUID();return r};
const prevInit=window.initOverworldV133;
if(prevInit){const wrapped=function(){const r=prevInit.apply(this,arguments);completeDispatchD(worldD());updateDispatchUID();return r};window.initOverworldV133=wrapped;if(window.initOverworld===prevInit)window.initOverworld=wrapped}
window.CR_CITY_DISTRICT_DISPATCHES={version:DISPATCH_VERSION,update:updateDispatchUID};
})();
}
''',encoding='utf-8')

manifest=root/'src/bootstrap/module-manifest.js'
s=manifest.read_text(encoding='utf-8')
entry="  'world.districtDispatches':{path:'./src/world/district-dispatches-pwa12-104-city-candidate-01.js',kind:'module'},\n"
if 'world.districtDispatches' not in s:
    needle="  'world.livingStreets':{path:'./src/world/living-streets-v13-4a.js',kind:'module'},\n"
    if needle not in s: raise SystemExit('manifest module seam missing')
    s=s.replace(needle,needle+entry,1)
    order="  'world.livingStreets','missions.approaches','company','visuals','runtime'"
    if order not in s: raise SystemExit('manifest order seam missing')
    s=s.replace(order,"  'world.livingStreets','world.districtDispatches','missions.approaches','company','visuals','runtime'",1)
manifest.write_text(s,encoding='utf-8')
print('patched district dispatches candidate',root)
