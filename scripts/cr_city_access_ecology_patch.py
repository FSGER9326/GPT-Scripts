from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve()
module=root/'src/world/access-ecology-pwa12-104-city-candidate-05.js'
module.write_text(r'''if(typeof window!=='undefined'){
(() => {
'use strict';
const VERSION='pwa12.104-city-candidate.05';
function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
function copy(v){return JSON.parse(JSON.stringify(v))}
function nowMin(){return Math.round((((Game.day||1)-1)*24+(Game.hour||0))*60)}
function link(id){return (window.V133_TRANSIT_LINKS||[]).find(x=>x.id===id)||null}
function world(id){return window.generateDistrictV133?.(id)||null}
function endpoint(l,d){return l?.from?.district===d?l.from:l?.to?.district===d?l.to:null}
function other(l,d){return l?.from?.district===d?l.to:l?.to?.district===d?l.from:null}
function nearestHood(w,p){let best=null,bd=Infinity;for(const n of w?.neighborhoods||[]){const d=Math.hypot((p?.x||0)-n.x,(p?.y||0)-n.y);if(d<bd){bd=d;best=n.id}}return best}
function hoodAtTransit(d,node){const w=world(d),tr=w?.transit?.find(x=>x.id===node);if(!w||!tr)return null;const id=nearestHood(w,tr);return id?window.ensureNeighborhoodStateV134?.(w)?.[id]||null:null}
function factionId(v){return v&&v!=='local'&&window.FACTIONS?.[v]?v:null}
function defs(d){return window.V13_DISTRICT_LOCATIONS?.[d]||[]}
function def(d,id){return defs(d).find(x=>x.id===id)||null}
function active(){return window.activeInterdistrictDispatchV12104?.()||null}
function state(){const s=window.ensureLivingStreetsStateV134?.()||(Game.livingStreetsV134=Game.livingStreetsV134||{});s.accessEcology=s.accessEcology||{version:1,history:[],stats:{sponsors:0,lockouts:0,tolls:0,crossings:0}};s.accessEcology.history=s.accessEcology.history||[];s.accessEcology.stats=s.accessEcology.stats||{sponsors:0,lockouts:0,tolls:0,crossings:0};return s.accessEcology}
function sourceContact(a=active()){
 if(!a)return null;const d=def(a.sourceDistrict,a.sourceId);if(!d?.contact)return null;const rel=Game.contactRelations?.[d.contact];if(!rel?.known)return null;const w=window.currentDistrictV133?.(),p=w?.locations?.[a.sourceId];if(!w||w.id!==a.sourceDistrict||!p||!Game.ovPlayer||Math.hypot(Game.ovPlayer.x-p.x,Game.ovPlayer.y-p.y)>2.25)return null;return{id:d.contact,name:d.name||d.contact,trust:Number(rel.trust||0)}
}
function pressure(l,from){const ep=endpoint(l,from),to=other(l,from);if(!ep||!to)return null;const a=hoodAtTransit(from,ep.node),b=hoodAtTransit(to.district,to.node);const avg=(k,scale=1)=>((Number(a?.[k]||0)+Number(b?.[k]||0))/2)/scale;return{fromHood:a,toHood:b,heat:avg('localHeat',100),security:avg('security',5),gang:avg('gangPressure',5),unrest:avg('unrest',5),toDistrict:to.district,sourceController:factionId(a?.controller),destController:factionId(b?.controller)}}
function sponsorRecord(a,lid){return a?.accessEcologySponsors?.[lid]||null}
function evaluate(linkId,fromDistrict,kind='courier'){
 const l=typeof linkId==='string'?link(linkId):linkId;if(!l)return null;const from=fromDistrict||window.currentDistrictV133?.()?.id,ctx=pressure(l,from);if(!ctx)return null;
 const faction=l.faction||ctx.sourceController||ctx.destController||null,rep=Number(Game.rep?.[faction]||0),fheat=Number(Game.heat?.[faction]||0),notoriety=Number(Game.notoriety||0),a=active(),sponsor=sponsorRecord(a,l.id);
 const friendly=!!faction&&(rep>=30||((ctx.sourceController===faction||ctx.destController===faction)&&rep>=15)),hostile=!!faction&&(rep<=-15||fheat>=55),highHeat=ctx.heat>=.62,highSec=ctx.security>=.68,gangHeavy=ctx.gang>=.68,unrestHigh=ctx.unrest>=.66;
 let blocked=false,label='OPEN ACCESS',reason='',costDelta=0,minutesDelta=0,riskDelta=0,heatDelta=0;
 if(l.type==='hidden'){
   label='COVERT BYPASS';riskDelta=-.07;minutesDelta=ctx.heat>.72?2:0;
 }else if(l.type==='security'){
   if(friendly){label='PRIORITY CLEARANCE';costDelta=-20;minutesDelta=-2;riskDelta=-.10}
   else if((hostile&&(highHeat||notoriety>=55))||(highSec&&ctx.heat>=.72)){blocked=true;label='FACTION LOCKDOWN';reason='Controller pressure has hardened this checkpoint.';riskDelta=.18;minutesDelta=5}
   else if(highHeat||fheat>=40){label='INTENSIVE SCREENING';minutesDelta=5;riskDelta=.11}
 }else if(l.type==='metro'){
   if((highSec&&highHeat)||notoriety>=88){blocked=true;label='METRO ID SWEEP';reason='Transit security is actively screening this corridor.';riskDelta=.16;minutesDelta=4}
   else if(ctx.heat>=.45){label='PLATFORM SCREENING';minutesDelta=3;riskDelta=.06}
 }else if(l.type==='freight'){
   if(friendly){label='FRIENDLY FREIGHT';costDelta=-30;minutesDelta=-1;riskDelta=-.06}
   else if(gangHeavy||unrestHigh){label='CARGO TOLL';costDelta=80+Math.round(ctx.gang*70);minutesDelta=4;riskDelta=.10;heatDelta=1}
   else if(highSec&&kind==='contraband'){label='FREIGHT INSPECTION';minutesDelta=5;riskDelta=.12}
 }else if(l.type==='border'){
   if(highSec&&ctx.heat>=.72){blocked=true;label='STREET LOCKDOWN';reason='Security and local heat have closed this crossing.';minutesDelta=4;riskDelta=.14}
   else if(gangHeavy&&ctx.heat>=.38){label='STREET LEVY';costDelta=55+Math.round(ctx.gang*55);minutesDelta=3;riskDelta=.09;heatDelta=1}
   else if(unrestHigh){label='CROWD DELAY';minutesDelta=4;riskDelta=.05}
 }
 if(friendly&&!blocked&&l.type!=='hidden'&&l.type!=='freight'&&l.type!=='security'){label='FRIENDLY CORRIDOR';costDelta-=15;riskDelta-=.05}
 if(sponsor){blocked=false;label='CONTACT COVER';reason='';minutesDelta=Math.max(0,minutesDelta-2);riskDelta-=.06}
 const c=sourceContact(a),sponsorAvailable=blocked&&!sponsor&&!!c&&c.trust>=30&&a?.phase==='choose_transit';
 return{version:1,linkId:l.id,linkName:l.name,linkType:l.type,fromDistrict:from,toDistrict:ctx.toDistrict,faction,controller:ctx.sourceController||ctx.destController||null,pressure:{heat:Number(ctx.heat.toFixed(3)),security:Number(ctx.security.toFixed(3)),gang:Number(ctx.gang.toFixed(3)),unrest:Number(ctx.unrest.toFixed(3))},rep,factionHeat:fheat,notoriety,friendly,hostile,blocked,label,reason,costDelta,minutesDelta,riskDelta:Number(riskDelta.toFixed(3)),heatDelta,sponsor:!!sponsor,sponsorAvailable,sponsorContact:c};
}
window.evaluateTransitAccessEcologyV12104=evaluate;
function applyOption(op,eco){if(!op||!eco)return op;op.baseEcology=op.baseEcology||{cost:Number(op.cost||0),risk:Number(op.risk||0),transitMinutes:Number(op.transitMinutes||0),payout:Number(op.payout||0),windowMin:Number(op.windowMin||0),accessLabel:op.accessLabel,blocked:!!op.blocked};const b=op.baseEcology;op.cost=Math.max(0,b.cost+eco.costDelta);op.risk=Number(clamp(b.risk+eco.riskDelta,0,1).toFixed(3));op.transitMinutes=Math.max(1,b.transitMinutes+eco.minutesDelta);op.payout=Math.max(0,Math.round((b.payout+Math.max(0,eco.riskDelta)*260+Math.max(0,eco.costDelta)*.45)/10)*10);op.windowMin=Math.max(30,b.windowMin+Math.max(0,eco.minutesDelta));op.accessLabel=eco.label;op.ecologyBlocked=!!eco.blocked;op.blocked=!!b.blocked||!!eco.blocked;op.accessEcology=copy(eco);return op}
window.applyTransitAccessEcologyToOptionV12104=applyOption;
function refreshOptions(a=active()){if(!a?.options)return a;for(const op of a.options){const eco=evaluate(op.linkId,a.sourceDistrict,a.kind);applyOption(op,eco)}return a}
window.refreshTransitAccessEcologyV12104=refreshOptions;
function sponsor(linkId){const a=active(),eco=evaluate(linkId,a?.sourceDistrict,a?.kind);if(!a||!eco?.sponsorAvailable||a.phase!=='choose_transit')return false;const c=eco.sponsorContact;if(!c||c.trust<30)return false;a.accessEcologySponsors=a.accessEcologySponsors||{};if(a.accessEcologySponsors[linkId])return true;const rec={linkId,contactId:c.id,contactName:c.name,spentTrust:3,day:Game.day||1,at:nowMin()};a.accessEcologySponsors[linkId]=rec;window.changeContactTrustV13?.(c.id,-3,'Sponsored city transit access');const s=state();s.stats.sponsors=(s.stats.sponsors||0)+1;s.history.unshift({type:'sponsor',...rec});s.history=s.history.slice(0,30);refreshOptions(a);window.addJournal?.('side','Transit Cover',`${c.name} burns local influence to reopen ${eco.linkName}. This clears the live district-access lock; ordinary checkpoint rules still apply.`);window.streetToastV134?.(`${c.name.toUpperCase()} · TRANSIT COVER`);window.saveGame?.(0,true);window.updateInterdistrictDispatchUIV12104?.();return true}
window.sponsorTransitAccessV12104=sponsor;
const baseChoose=window.chooseInterdistrictTransitV12104;
if(baseChoose){window.chooseInterdistrictTransitV12104=function(linkId){const a=active();if(a){refreshOptions(a);const op=a.options?.find(x=>x.linkId===linkId),eco=evaluate(linkId,a.sourceDistrict,a.kind);if(!op||eco?.blocked){window.streetToastV134?.(`${eco?.label||'ROUTE CLOSED'} · ${eco?.reason||'Choose another physical crossing.'}`);state().stats.lockouts=(state().stats.lockouts||0)+1;return false}applyOption(op,eco)}const ok=baseChoose.apply(this,arguments);if(ok){const cur=active(),op=cur?.chosenOption;if(op){const eco=evaluate(op.linkId,cur.sourceDistrict,cur.kind);op.accessEcology=copy(eco);cur.accessEcologyCommitted=copy(eco);window.saveGame?.(0,true)}}decorate();return ok}}
function prepare(l,current,mode){const a=active(),eco=evaluate(l,current,a?.kind||'courier');if(!eco)return null;if(eco.blocked)return{...eco,allowed:false};return{...eco,allowed:true,mode}}
window.prepareTransitAccessEcologyV12104=prepare;
function commit(eco,ctx){if(!eco||!ctx)return;const s=state(),h=eco.heatDelta?hoodAtTransit(ctx.fromDistrict,endpoint(link(ctx.linkId),ctx.fromDistrict)?.node):null;if(h&&eco.heatDelta){h.localHeat=clamp(Number(h.localHeat||0)+eco.heatDelta,0,100);h.events=(h.events||0)+1}s.stats.crossings=(s.stats.crossings||0)+1;if(eco.costDelta>0)s.stats.tolls=(s.stats.tolls||0)+1;s.history.unshift({type:'crossing',at:nowMin(),day:Game.day||1,linkId:ctx.linkId,fromDistrict:ctx.fromDistrict,toDistrict:ctx.toDistrict,label:eco.label,costDelta:eco.costDelta,minutesDelta:eco.minutesDelta,sponsor:eco.sponsor});s.history=s.history.slice(0,30);const a=active();if(a?.chosenOption?.linkId===ctx.linkId){a.accessEcologyCommitted=copy(eco);a.chosenOption.accessEcology=copy(eco)}window.saveGame?.(0,true)}
window.commitTransitAccessEcologyV12104=commit;
function style(){if(document.getElementById('v12104-access-ecology-style'))return;const s=document.createElement('style');s.id='v12104-access-ecology-style';s.textContent=`.v12104-eco{margin:6px 0 3px;padding:5px 6px;border-left:2px solid rgba(124,229,159,.6);background:rgba(70,160,108,.08);font:10px/1.35 monospace;color:#bfe7ce}.v12104-eco.blocked{border-left-color:#ff685f;background:rgba(255,70,60,.08);color:#ffc3bf}.v12104-eco b{color:#e6fff0}.v12104-eco-sponsor{border-color:rgba(110,230,180,.45)!important;color:#c8ffe4!important}@media(max-width:520px){.v12104-eco{font-size:10px}.v12104-eco-sponsor{min-height:44px!important}}`;document.head.appendChild(s)}
function decorate(){style();const a=active();if(!a||a.phase!=='choose_transit')return;refreshOptions(a);for(const p of [document.getElementById('v12104-interdistrict-panel'),document.getElementById('v12104-multihop-panel')]){if(!p)continue;for(const b of p.querySelectorAll('[data-cross-link],[data-multi-link]')){const id=b.dataset.crossLink||b.dataset.multiLink,eco=evaluate(id,a.sourceDistrict,a.kind),box=b.closest('.choice');if(!eco||!box)continue;box.querySelector('.v12104-eco')?.remove();box.querySelector('.v12104-eco-sponsor')?.remove();const d=document.createElement('div');d.className='v12104-eco'+(eco.blocked?' blocked':'');const fare=eco.costDelta===0?'FARE UNCHANGED':eco.costDelta>0?`+¢${eco.costDelta} LOCAL COST`:`-¢${Math.abs(eco.costDelta)} LOCAL COST`,delay=eco.minutesDelta>0?`+${eco.minutesDelta} MIN`:(eco.minutesDelta<0?`${eco.minutesDelta} MIN`:'NO DELAY');d.innerHTML=`<b>${eco.label}</b> · ${fare} · ${delay}<br>HEAT ${Math.round(eco.pressure.heat*100)} · SEC ${Math.round(eco.pressure.security*5)}/5 · GANG ${Math.round(eco.pressure.gang*5)}/5${eco.faction?` · ${window.FACTIONS?.[eco.faction]?.short||eco.faction} REP ${eco.rep}`:''}`;box.insertBefore(d,b);b.disabled=!!eco.blocked||!!a.options?.find(x=>x.linkId===id)?.baseEcology?.blocked;if(eco.blocked&&eco.sponsorAvailable){const sb=document.createElement('button');sb.className='btn small v12104-eco-sponsor';sb.textContent=`CALL ${eco.sponsorContact.name.toUpperCase()} · 3 TRUST`;sb.onclick=()=>sponsor(id);box.appendChild(sb)}}}}
window.decorateTransitAccessEcologyV12104=decorate;
const baseUI=window.updateInterdistrictDispatchUIV12104;if(baseUI)window.updateInterdistrictDispatchUIV12104=function(){const r=baseUI.apply(this,arguments);decorate();return r};
const baseMulti=window.updateMultiHopDispatchUIV12104;if(baseMulti)window.updateMultiHopDispatchUIV12104=function(){const r=baseMulti.apply(this,arguments);decorate();return r};
const prevInit=window.initOverworldV133;if(prevInit){const wrapped=function(){const r=prevInit.apply(this,arguments);setTimeout(decorate,0);return r};window.initOverworldV133=wrapped;if(window.initOverworld===prevInit)window.initOverworld=wrapped}
setTimeout(decorate,0);window.CR_CITY_ACCESS_ECOLOGY={version:VERSION,evaluate,refreshOptions,sponsor,prepare,commit,decorate};
})();
}''',encoding='utf-8')

# Patch the canonical transit authority instead of replacing it. Candidate 05 only
# contributes a live access verdict and local cost/time deltas; canonical security,
# bribe/hack, district activation, arrival-node, save, and transit callbacks remain.
p=root/'src/world/district-worlds-v13-3.js'
s=p.read_text(encoding='utf-8')
needle=" const link=V133_TRANSIT_LINKS.find(x=>x.id===linkId);if(!link)return false;const current=currentDistrictV133().id,ep=endpointForV133(link,current),to=otherEndpointV133(link,current);if(!ep||!to)return false;"
repl=needle+"\n const ecology=window.prepareTransitAccessEcologyV12104?.(link,current,mode)||null;if(ecology&&ecology.allowed===false){toast(ecology.reason||ecology.label||'Route closed by live district conditions.');return false}"
if 'prepareTransitAccessEcologyV12104' not in s:
    if needle not in s: raise SystemExit('travel authority seam missing')
    s=s.replace(needle,repl,1)
needle2="const access=accessForLinkV133(link);let cost=link.cost||0;"
repl2="const access=accessForLinkV133(link);let cost=Math.max(0,(link.cost||0)+(ecology?.costDelta||0));"
if repl2 not in s:
    if needle2 not in s: raise SystemExit('transit fare seam missing')
    s=s.replace(needle2,repl2,1)
needle3="advanceTime(link.minutes||12);Game.districtWorldsV133.unlockedLinks[link.id]=true;"
repl3="advanceTime(Math.max(1,(link.minutes||12)+(ecology?.minutesDelta||0)));Game.districtWorldsV133.unlockedLinks[link.id]=true;"
if repl3 not in s:
    if needle3 not in s: raise SystemExit('transit time seam missing')
    s=s.replace(needle3,repl3,1)
needle4="window.onDistrictTransitCompleteV12104?.({linkId:link.id,fromDistrict:current,toDistrict:to.district,mode});saveGame(0,true);return true"
repl4="window.onDistrictTransitCompleteV12104?.({linkId:link.id,fromDistrict:current,toDistrict:to.district,mode});window.commitTransitAccessEcologyV12104?.(ecology,{linkId:link.id,fromDistrict:current,toDistrict:to.district,mode});saveGame(0,true);return true"
if repl4 not in s:
    if needle4 not in s: raise SystemExit('transit completion seam missing')
    s=s.replace(needle4,repl4,1)
p.write_text(s,encoding='utf-8')

manifest=root/'src/bootstrap/module-manifest.js'
s=manifest.read_text(encoding='utf-8')
entry="  'world.accessEcology':{path:'./src/world/access-ecology-pwa12-104-city-candidate-05.js',kind:'module'},\n"
if 'world.accessEcology' not in s:
    needle="  'world.multiHopLogistics':{path:'./src/world/multihop-logistics-pwa12-104-city-candidate-04.js',kind:'module'},\n"
    if needle not in s: raise SystemExit('candidate 04 manifest seam missing')
    s=s.replace(needle,needle+entry,1)
    order="'world.livingStreets','world.districtDispatches','world.interdistrictLogistics','world.dynamicLogisticsDisruptions','world.multiHopLogistics','missions.approaches'"
    if order not in s: raise SystemExit('candidate 04 manifest order seam missing')
    s=s.replace(order,"'world.livingStreets','world.districtDispatches','world.interdistrictLogistics','world.dynamicLogisticsDisruptions','world.multiHopLogistics','world.accessEcology','missions.approaches'",1)
manifest.write_text(s,encoding='utf-8')

bundle=root/'src/runtime/runtime-bundle.js'
s=bundle.read_text(encoding='utf-8')
multi='/* SOURCE: src/world/multihop-logistics-pwa12-104-city-candidate-04.js */'
eco='/* SOURCE: src/world/access-ecology-pwa12-104-city-candidate-05.js */'
mission='/* SOURCE: src/missions/contract-approaches-v13-4b.js */'
if multi not in s or mission not in s: raise SystemExit('candidate 04 runtime seam missing')
if eco not in s:s=s.replace(mission,eco+'\n'+mission,1)
pos=[s.index(x) for x in (multi,eco,mission)]
if pos!=sorted(pos):raise SystemExit(f'access ecology runtime order invalid: {pos}')
bundle.write_text(s,encoding='utf-8')
print('patched city access ecology candidate 05',root)
