from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve()
module=root/'src/world/transit-incidents-pwa12-104-city-candidate-06.js'
module.write_text(r'''if(typeof window!=='undefined'){
(() => {
'use strict';
const VERSION='pwa12.104-city-candidate.06';
const QUIET=new Set(['OPEN ACCESS','FRIENDLY CORRIDOR','FRIENDLY FREIGHT','PRIORITY CLEARANCE','COVERT BYPASS','CONTACT COVER','INCIDENT CLEARED']);
function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
function copy(v){return JSON.parse(JSON.stringify(v))}
function nowMin(){return Math.round((((Game.day||1)-1)*24+(Game.hour||0))*60)}
function active(){return window.activeInterdistrictDispatchV12104?.()||null}
function world(){return window.currentDistrictV133?.()||null}
function state(){
 const s=window.ensureLivingStreetsStateV134?.()||(Game.livingStreetsV134=Game.livingStreetsV134||{});
 s.transitIncidents=s.transitIncidents||{version:1,active:null,history:[],stats:{created:0,cleared:0,complied:0,spoofed:0,contacts:0,fights:0,retreated:0,crossed:0}};
 const x=s.transitIncidents;x.history=x.history||[];x.stats=x.stats||{};for(const k of ['created','cleared','complied','spoofed','contacts','fights','retreated','crossed'])x.stats[k]=x.stats[k]||0;return x
}
function defs(d){return window.V13_DISTRICT_LOCATIONS?.[d]||[]}
function def(d,id){return defs(d).find(x=>x.id===id)||null}
function classes(){return new Set((window.activeCrewV135?.()||Game.roster||[]).map(u=>u.className))}
function currentIncident(){return state().active}
function option(a,id){return a?.options?.find(x=>x.linkId===id)||null}
function ecology(a,id){return window.evaluateTransitAccessEcologyV12104?.(id,a?.sourceDistrict,a?.kind)||null}
function clearance(a,id){const c=a?.transitIncidentClearances?.[id];return c&&!c.consumed?c:null}
function needsIncident(e){return !!e&&!QUIET.has(e.label)&&(!!e.blocked||e.costDelta>0||e.minutesDelta>0||e.riskDelta>=.05)}
function sourceContact(a){
 const d=def(a?.sourceDistrict,a?.sourceId),id=d?.contact,rel=id&&Game.contactRelations?.[id];if(!id||!rel?.known)return null;return{id,name:d.name||id,trust:Number(rel.trust||0)}
}
function nodeFor(a,op,w=world()){return w&&w.id===a?.sourceDistrict?w.transit?.find(t=>t.id===op?.sourceNodeId)||null:null}
function hoodIdAt(w,p){let best=null,bd=Infinity;for(const n of w?.neighborhoods||[]){const d=Math.hypot((p?.x||0)-n.x,(p?.y||0)-n.y);if(d<bd){bd=d;best=n.id}}return best}
function hoodFor(inc,w=window.generateDistrictV133?.(inc?.district)){if(!inc||!w)return null;return window.ensureNeighborhoodStateV134?.(w)?.[inc.neighborhood]||null}
function actorFor(e){if(e?.linkType==='security'||e?.label?.includes('SCREEN')||e?.label?.includes('METRO')||e?.label?.includes('LOCKDOWN'))return'security';if(e?.label==='CARGO TOLL'||e?.label==='STREET LEVY'||(e?.pressure?.gang||0)>(e?.pressure?.security||0))return'gang';if(e?.linkType==='freight')return'contractor';return null}
function profile(e){
 const actor=actorFor(e),blocked=!!e.blocked,toll=Math.max(0,Math.round(Number(e.costDelta||0))),clearanceFee=blocked?Math.max(toll,180+Math.round((e.pressure?.heat||0)*140)):toll;
 const wait=Math.max(1,Math.round(Number(e.minutesDelta||0))||3);
 let copyText='The crossing has hardened in real time. The crew has reached the physical control point; the city will not resolve this from a menu.';
 if(e.label==='METRO ID SWEEP'||e.label==='PLATFORM SCREENING')copyText='Transit security has turned the platform approach into a live ID sweep. Scanners and armed staff are checking every face before the gates.';
 else if(e.label==='CARGO TOLL'||e.label==='FREIGHT INSPECTION')copyText='Cargo control has built a temporary inspection lane across the freight approach. Every runner is being stopped before the loading gate.';
 else if(e.label==='STREET LEVY')copyText='A local crew has barricaded the crossing and is collecting a street levy from anything that wants through.';
 else if(e.label==='STREET LOCKDOWN'||e.label==='FACTION LOCKDOWN'||e.label==='INTENSIVE SCREENING')copyText='A hard checkpoint now occupies the transit approach. Credentials, cargo and affiliations are being checked under weapons.';
 else if(e.label==='CROWD DELAY')copyText='The approach is physically jammed by a crowd surge and improvised barriers. The crew must wait, work a gap, or back away.';
 return{actor,blocked,toll,clearanceFee,wait,text:copyText}
}
function createIncident(a,op,e){
 const w=world(),n=nodeFor(a,op,w);if(!a||!op||!e||!w||!n)return null;
 const st=state(),old=st.active;if(old&&old.dispatchId===a.id&&old.linkId===op.linkId&&['approach','engaged','cleared','combat'].includes(old.status))return old;
 const p=profile(e),inc={version:1,id:`ti_${a.id}_${op.linkId}_${Game.day||1}_${nowMin()}`,dispatchId:a.id,linkId:op.linkId,linkName:op.linkName,linkType:op.linkType,nodeId:op.sourceNodeId,district:w.id,x:n.x,y:n.y,neighborhood:hoodIdAt(w,n),status:'approach',createdAt:nowMin(),ecology:copy(e),profile:p,sourceContact:sourceContact(a),deadlineAtCreation:a.deadline??null};
 st.active=inc;st.stats.created++;a.transitIncidentId=inc.id;a.transitIncidentLinkId=op.linkId;a.transitIncidentDeadline=a.deadline??(nowMin()+Math.max(30,op.windowMin||45));if(a.deadline==null)a.deadline=a.transitIncidentDeadline;a.phase='to_incident';window.addJournal?.('side','PHYSICAL TRANSIT INCIDENT',`${e.label} now occupies ${op.linkName}. The crew must physically reach the ${op.linkType} approach before deciding how to clear it.`);window.streetToastV134?.(`${e.label} · PHYSICAL CHECKPOINT`);window.saveGame?.(0,true);return inc
}
function routeIncident(inc=currentIncident()){
 const a=active(),w=world();if(!a||!inc||w?.id!==inc.district||!Game.ovPlayer)return false;
 if(Math.hypot(Game.ovPlayer.x-inc.x,Game.ovPlayer.y-inc.y)<=1.45)return engageIncident(inc);
 const ok=window.routeToTransitNodeV133?.(inc.nodeId);if(!ok)return false;Game._v133TravelTarget={kind:'v12104incident',id:inc.id,label:`TRANSIT INCIDENT // ${inc.ecology.label}`};Game.ovCamera&&(Game.ovCamera.follow=true);return true
}
window.routeTransitIncidentV12104=routeIncident;
function begin(linkId){
 const a=active();if(!a||a.phase!=='choose_transit')return false;const op=option(a,linkId),e=ecology(a,linkId);if(!op||!needsIncident(e)||clearance(a,linkId))return false;
 const inc=createIncident(a,op,e);if(!inc)return false;const ok=routeIncident(inc);update();return !!ok
}
window.beginTransitIncidentV12104=begin;
function engageIncident(inc=currentIncident()){
 const a=active(),w=world();if(!a||!inc||inc.dispatchId!==a.id||w?.id!==inc.district||!Game.ovPlayer||Math.hypot(Game.ovPlayer.x-inc.x,Game.ovPlayer.y-inc.y)>1.65)return false;
 Game.pendingPath=null;Game._v133TravelTarget=null;inc.status='engaged';inc.engagedAt=inc.engagedAt||nowMin();a.phase='incident';window.saveGame?.(0,true);update();return true
}
window.engageTransitIncidentV12104=engageIncident;
function detect(){const inc=currentIncident();if(!inc||inc.status!=='approach')return false;const w=world();if(w?.id!==inc.district||!Game.ovPlayer)return false;if(Math.hypot(Game.ovPlayer.x-inc.x,Game.ovPlayer.y-inc.y)<=1.65)return engageIncident(inc);return false}
function mutateHeat(inc,delta){const h=hoodFor(inc);if(!h)return;h.localHeat=clamp(Number(h.localHeat||0)+delta,0,100);h.events=(h.events||0)+1}
function factionHeat(inc,delta){const f=inc?.ecology?.faction||inc?.ecology?.controller;if(!f)return;Game.heat=Game.heat||{};Game.heat[f]=clamp(Number(Game.heat[f]||0)+delta,0,100)}
function grant(method,detail={}){
 const a=active(),inc=currentIncident();if(!a||!inc||inc.dispatchId!==a.id||!['engaged','combat'].includes(inc.status))return false;
 a.transitIncidentClearances=a.transitIncidentClearances||{};const c={linkId:inc.linkId,incidentId:inc.id,method,at:nowMin(),day:Game.day||1,consumed:false,label:'INCIDENT CLEARED',...detail};a.transitIncidentClearances[inc.linkId]=c;inc.status='cleared';inc.resolution=method;inc.resolvedAt=nowMin();inc.clearance=copy(c);a.phase='incident_cleared';const st=state();st.stats.cleared++;if(method==='comply')st.stats.complied++;if(method==='agentex'||method==='hacker')st.stats.spoofed++;if(method==='contact')st.stats.contacts++;window.addJournal?.('side','TRANSIT INCIDENT CLEARED',`${inc.ecology.label} at ${inc.linkName} cleared via ${String(method).toUpperCase()}. The crew still must use the physical transit node; ordinary transit/security rules remain authoritative.`);window.streetToastV134?.(`${inc.ecology.label} · CLEARED`);window.updateNeighborhoodHUDV134?.();window.saveGame?.(0,true);update();return c
}
function comply(){
 const a=active(),inc=currentIncident();if(!a||inc?.status!=='engaged')return false;const fee=inc.profile.clearanceFee||0;if(fee>0&&Number(Game.credits||0)<fee){window.streetToastV134?.('INSUFFICIENT CREDITS');return false}if(fee)Game.credits=Math.max(0,Number(Game.credits||0)-fee);window.advanceTime?.(inc.profile.wait||3);mutateHeat(inc,-Math.min(2,inc.ecology.blocked?1:2));if(inc.ecology.heatDelta)mutateHeat(inc,inc.ecology.heatDelta);return !!grant('comply',{fee,minutes:inc.profile.wait||3})
}
window.complyTransitIncidentV12104=comply;
function spoof(kind){
 const inc=currentIncident();if(inc?.status!=='engaged'||!['agentex','hacker'].includes(kind))return false;const need=kind==='agentex'?'AgentEX':'Hacker';if(!classes().has(need))return false;const minutes=kind==='agentex'?2:3;window.advanceTime?.(minutes);if(kind==='agentex')mutateHeat(inc,-2);else{mutateHeat(inc,1);factionHeat(inc,2)}return !!grant(kind,{minutes})
}
window.spoofTransitIncidentV12104=spoof;
function contactCover(){
 const a=active(),inc=currentIncident(),c=inc?.sourceContact,rel=c&&Game.contactRelations?.[c.id];if(!a||inc?.status!=='engaged'||!c||!rel?.known||Number(rel.trust||0)<30)return false;window.changeContactTrustV13?.(c.id,-3,'Cleared a physical transit incident');window.advanceTime?.(1);mutateHeat(inc,-1);return !!grant('contact',{contactId:c.id,contactName:c.name,trustSpent:3,minutes:1})
}
window.contactCoverTransitIncidentV12104=contactCover;
function fight(){
 const a=active(),inc=currentIncident(),w=world();if(!a||inc?.status!=='engaged'||!inc.profile.actor||w?.id!==inc.district)return false;inc.status='combat';inc.combatStartedAt=nowMin();inc.pendingCombat=true;a.phase='incident_combat';state().stats.fights++;window.saveGame?.(0,true);hide();const ok=window.launchStreetCombatV134?.(inc.profile.actor,w);if(!ok){inc.status='engaged';inc.pendingCombat=false;a.phase='incident';update();return false}return true
}
window.fightTransitIncidentV12104=fight;
function archive(inc,status=inc?.status){if(!inc)return;const st=state();st.history.unshift({...copy(inc),status});st.history=st.history.slice(0,36)}
function retreat(){
 const a=active(),inc=currentIncident();if(!a||!inc||!['engaged','cleared'].includes(inc.status))return false;const deadline=a.deadline;a.transitIncidentCarryDeadline=deadline;inc.status='retreated';inc.resolvedAt=nowMin();archive(inc,'retreated');state().stats.retreated++;state().active=null;a.phase='choose_transit';a.chosenLinkId=null;a.chosenOption=null;a.transitIncidentId=null;a.transitIncidentLinkId=null;Game.pendingPath=null;Game._v133TravelTarget=null;window.addJournal?.('side','TRANSIT INCIDENT ABANDONED',`${inc.linkName}: the crew backed away from the physical checkpoint. Original delivery deadline remains in force.`);window.streetToastV134?.('CHECKPOINT ABANDONED · REPLAN');window.saveGame?.(0,true);window.updateInterdistrictDispatchUIV12104?.();update();return true
}
window.retreatTransitIncidentV12104=retreat;
function selectCleared(){
 const a=active(),inc=currentIncident(),op=a&&option(a,inc?.linkId),c=a&&clearance(a,inc?.linkId);if(!a||!inc||inc.status!=='cleared'||!op||!c)return false;
 a.chosenLinkId=op.linkId;a.chosenOption=copy(op);a.payout=op.payout;a.risk=op.risk;a.phase='to_transit';if(a.deadline==null)a.deadline=a.transitIncidentDeadline||nowMin()+Math.max(30,op.windowMin||45);
 if(a.multiHop&&a.multiHopPlan){const p=a.multiHopPlan,chosen=copy(op);if(p.stage===1)p.selectedLeg1=chosen;else if(p.stage===2)p.selectedLeg2=chosen;a.deadline=p.deadline}
 inc.status='cleared_waiting_crossing';inc.proceededAt=nowMin();window.saveGame?.(0,true);update();const w=world(),n=nodeFor(a,op,w);if(w&&n&&Game.ovPlayer&&Math.hypot(Game.ovPlayer.x-n.x,Game.ovPlayer.y-n.y)<=1.6){window.routeToTransitNodeV133?.(op.sourceNodeId);return true}return !!window.routeToTransitNodeV133?.(op.sourceNodeId)
}
window.continueTransitIncidentV12104=selectCleared;
function combatSettled(m,success){
 const a=active(),inc=currentIncident();if(!a||!inc||inc.status!=='combat'||!inc.pendingCombat||!m?.v134StreetEncounter)return false;inc.pendingCombat=false;inc.combatMissionId=m.id;inc.combatSuccess=!!success;
 if(success){grant('fight',{missionId:m.id});return true}
 inc.status='failed';inc.resolution='fight_failed';inc.resolvedAt=nowMin();archive(inc,'fight_failed');state().active=null;a.transitIncidentCarryDeadline=a.deadline;a.phase='choose_transit';a.chosenLinkId=null;a.chosenOption=null;a.transitIncidentId=null;a.transitIncidentLinkId=null;window.addJournal?.('side','TRANSIT INCIDENT LOST',`${inc.linkName}: the crew failed to break the physical checkpoint. The route remains closed; replan from the current district.`);window.saveGame?.(0,true);return true
}
window.onTransitIncidentStreetCombatSettledV12104=combatSettled;

/* Candidate 05 owns live access evaluation. Candidate 06 adds a one-crossing clearance
   only after the crew physically resolves the incident at the transit approach. */
const prevPrepare=window.prepareTransitAccessEcologyV12104;
if(prevPrepare)window.prepareTransitAccessEcologyV12104=function(l,current,mode){const e=prevPrepare.apply(this,arguments),a=active(),c=clearance(a,l?.id);if(!c)return e;return{...(e||{}),allowed:true,blocked:false,label:'INCIDENT CLEARED',reason:'',costDelta:0,minutesDelta:0,heatDelta:0,incidentClearance:copy(c),mode}}
const prevCommit=window.commitTransitAccessEcologyV12104;
if(prevCommit)window.commitTransitAccessEcologyV12104=function(e,ctx){const a=active(),c=clearance(a,ctx?.linkId),inc=currentIncident();const effective=c?{...(e||{}),allowed:true,blocked:false,label:'INCIDENT CLEARED',costDelta:0,minutesDelta:0,heatDelta:0}:e;const r=prevCommit.call(this,effective,ctx);if(c){c.consumed=true;c.crossedAt=nowMin();state().stats.crossed++;if(inc&&inc.id===c.incidentId){inc.status='crossed';inc.crossedAt=nowMin();archive(inc,'crossed');state().active=null}a.transitIncidentId=null;a.transitIncidentLinkId=null;window.saveGame?.(0,true)}return r}
const prevChoose=window.chooseInterdistrictTransitV12104;
if(prevChoose)window.chooseInterdistrictTransitV12104=function(linkId){const a=active(),carry=a?.transitIncidentCarryDeadline,e=a?.phase==='choose_transit'?ecology(a,linkId):null;if(a?.phase==='choose_transit'&&needsIncident(e)&&!clearance(a,linkId))return begin(linkId);const ok=prevChoose.apply(this,arguments);if(ok&&carry){a.deadline=carry;delete a.transitIncidentCarryDeadline;window.saveGame?.(0,true)}return ok}

function ensureUI(){
 const wrap=document.querySelector('#overworld-screen .wrap');if(!wrap)return null;
 if(!document.getElementById('v12104-transit-incident-style')){const st=document.createElement('style');st.id='v12104-transit-incident-style';st.textContent=`#v12104-transit-incident-panel{position:absolute;left:50%;bottom:82px;transform:translateX(-50%);z-index:34;width:min(390px,calc(100% - 28px));max-height:min(68vh,560px);overflow:auto;padding:12px 13px;background:rgba(12,10,8,.98);border:1px solid rgba(238,176,76,.78);box-shadow:0 14px 42px rgba(0,0,0,.68);font:12px/1.42 monospace;color:#edf3f5;display:none;pointer-events:auto}#v12104-transit-incident-panel .k{font-size:10px;letter-spacing:.14em;color:#eeb04c}#v12104-transit-incident-panel h2{margin:5px 0 7px;font:700 17px/1.2 Orbitron,sans-serif;color:#fff}#v12104-transit-incident-panel .meta{margin:7px 0;color:#c7ced2}#v12104-transit-incident-panel .terms{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;margin:8px 0}#v12104-transit-incident-panel .terms span{padding:6px 3px;background:rgba(255,255,255,.055);text-align:center}#v12104-transit-incident-panel button{width:100%;min-height:44px;margin-top:6px}#v12104-transit-incident-panel .danger{border-color:rgba(255,90,77,.7);color:#ffc0ba}@media(max-width:520px){#v12104-transit-incident-panel{left:8px;right:8px;bottom:74px;transform:none;width:auto;max-height:62vh;padding:10px}#v12104-transit-incident-panel button{min-height:44px}}`;document.head.appendChild(st)}
 let p=document.getElementById('v12104-transit-incident-panel');if(!p){p=document.createElement('div');p.id='v12104-transit-incident-panel';wrap.appendChild(p)}return p
}
function hide(){const p=document.getElementById('v12104-transit-incident-panel');if(p)p.style.display='none'}
function action(btn,id,label,fn,klass=''){btn.insertAdjacentHTML('beforeend',`<button class="btn small ${klass}" id="${id}">${label}</button>`);btn.querySelector('#'+id).onclick=fn}
function update(){
 const p=ensureUI(),a=active(),inc=currentIncident();if(!p||Game.screen!=='overworld-screen'||!a||!inc||inc.dispatchId!==a.id||!['engaged','cleared','cleared_waiting_crossing'].includes(inc.status)){if(p)p.style.display='none';return}
 const e=inc.ecology,prof=inc.profile,c=inc.sourceContact,cl=classes(),fee=prof.clearanceFee||0,remain=a.deadline==null?'—':Math.max(0,a.deadline-nowMin());p.style.display='block';
 p.innerHTML=`<div class="k">PHYSICAL TRANSIT INCIDENT // ${inc.linkType.toUpperCase()}</div><h2>${e.label}</h2><div class="meta">${prof.text}<br><b>${inc.linkName}</b> · ${inc.neighborhood||inc.district}</div><div class="terms"><span>${Math.round((e.pressure?.heat||0)*100)}<br>HEAT</span><span>${Math.round((e.pressure?.security||0)*5)}/5<br>SEC</span><span>${remain}<br>MIN LEFT</span></div><div id="v12104-transit-incident-actions"></div>`;
 const box=p.querySelector('#v12104-transit-incident-actions');if(inc.status==='cleared'||inc.status==='cleared_waiting_crossing'){action(box,'v12104-ti-enter',`ENTER ${inc.linkName.toUpperCase()}`,selectCleared);action(box,'v12104-ti-retreat','BACK OFF & REPLAN',retreat);return}
 action(box,'v12104-ti-comply',fee?`PROCESS CLEARANCE · ¢${fee} · ${prof.wait} MIN`:`SUBMIT / WAIT · ${prof.wait} MIN`,comply);
 if(cl.has('AgentEX'))action(box,'v12104-ti-agentex','[AGENTEX] SPOOF CREDENTIALS',()=>spoof('agentex'));
 if(cl.has('Hacker'))action(box,'v12104-ti-hacker','[HACKER] SPOOF CHECKPOINT SYSTEMS',()=>spoof('hacker'));
 if(c&&Number(Game.contactRelations?.[c.id]?.trust||0)>=30)action(box,'v12104-ti-contact',`CALL ${c.name.toUpperCase()} · 3 TRUST`,contactCover);
 if(prof.actor)action(box,'v12104-ti-fight','FIGHT THROUGH · TACTICAL COMBAT',fight,'danger');
 action(box,'v12104-ti-retreat','BACK OFF & REPLAN',retreat)
}
window.updateTransitIncidentUIV12104=update;
function draw(ctx,w,W,H,t){const inc=currentIncident();if(!inc||w?.id!==inc.district||['crossed','retreated','failed'].includes(inc.status))return;const s=window.worldToScreen?.(inc.x+.5,inc.y+.5);if(!s||s.x<-36||s.y<-36||s.x>W+36||s.y>H+36)return;ctx.save();ctx.translate(s.x,s.y);ctx.shadowColor=inc.status.startsWith('cleared')?'#72e39a':'#eeb04c';ctx.shadowBlur=13;ctx.strokeStyle=inc.status.startsWith('cleared')?'#72e39a':'#eeb04c';ctx.fillStyle='rgba(10,8,6,.9)';ctx.lineWidth=2;ctx.fillRect(-10,-7,20,14);ctx.strokeRect(-10,-7,20,14);ctx.beginPath();ctx.moveTo(-8,-3);ctx.lineTo(8,3);ctx.moveTo(-8,3);ctx.lineTo(8,-3);ctx.stroke();ctx.shadowBlur=0;ctx.fillStyle='#fff0cb';ctx.font=`800 ${Math.max(7,t*.18)}px Orbitron`;ctx.textAlign='center';ctx.fillText('!',0,3);ctx.restore()}
function tap(q){const inc=currentIncident();if(!inc||world()?.id!==inc.district||Math.hypot(q.x-inc.x,q.y-inc.y)>1.4)return false;if(inc.status==='approach')return routeIncident(inc);if(['engaged','cleared','cleared_waiting_crossing'].includes(inc.status)){update();return true}return false}
const prevDraw=window.drawLivingStreetsV134;window.drawLivingStreetsV134=function(ctx,w,W,H,t,hover){prevDraw?.apply(this,arguments);draw(ctx,w,W,H,t)};
const prevTap=window.handleLivingStreetTapV134;window.handleLivingStreetTapV134=function(q){if(tap(q))return true;return prevTap?.apply(this,arguments)||false};
const prevStep=window.onStreetStepV134;window.onStreetStepV134=function(w){const r=prevStep?.apply(this,arguments);detect();update();return r};
const prevInit=window.initOverworldV133;if(prevInit){const wrapped=function(){const r=prevInit.apply(this,arguments);setTimeout(()=>{detect();update()},0);return r};window.initOverworldV133=wrapped;if(window.initOverworld===prevInit)window.initOverworld=wrapped}
const prevIU=window.updateInterdistrictDispatchUIV12104;if(prevIU)window.updateInterdistrictDispatchUIV12104=function(){const r=prevIU.apply(this,arguments);setTimeout(decorateChoices,0);return r};
const prevMU=window.updateMultiHopDispatchUIV12104;if(prevMU)window.updateMultiHopDispatchUIV12104=function(){const r=prevMU.apply(this,arguments);setTimeout(decorateChoices,0);return r};
function decorateChoices(){const a=active();if(!a||a.phase!=='choose_transit')return;for(const panel of [document.getElementById('v12104-interdistrict-panel'),document.getElementById('v12104-multihop-panel')]){if(!panel)continue;for(const b of panel.querySelectorAll('[data-cross-link],[data-multi-link]')){const id=b.dataset.crossLink||b.dataset.multiLink,e=ecology(a,id),box=b.closest('.choice');if(!box||!needsIncident(e)||clearance(a,id))continue;box.querySelector(`.v12104-ti-approach[data-link="${id}"]`)?.remove();const x=document.createElement('button');x.className='btn small v12104-ti-approach';x.dataset.link=id;x.style.minHeight='44px';x.textContent=`APPROACH ${e.label} PHYSICALLY`;x.onclick=()=>begin(id);box.appendChild(x)}}}
setTimeout(()=>{decorateChoices();update()},0);
window.CR_CITY_TRANSIT_INCIDENTS={version:VERSION,state,needsIncident,begin,routeIncident,engageIncident,comply,spoof,contactCover,fight,retreat,continueTransit:selectCleared,combatSettled,update,draw};
})();
}''',encoding='utf-8')

# Small canonical seam: keep Living Streets combat aftermath authoritative, but notify
# Candidate 06 after the existing street-combat consequences have been calculated.
streets=root/'src/world/living-streets-v13-4a.js'
s=streets.read_text(encoding='utf-8')
needle=" addJournal?.('side',success?'Street Clash Won':'Street Clash Lost',`${m.name}: ${success?'the crew held the street':'emergency extraction ceded the block'}. Neighborhood pressure shifted.`);updateNeighborhoodHUDV134();saveGame?.(0,true);return true"
repl=" addJournal?.('side',success?'Street Clash Won':'Street Clash Lost',`${m.name}: ${success?'the crew held the street':'emergency extraction ceded the block'}. Neighborhood pressure shifted.`);window.onTransitIncidentStreetCombatSettledV12104?.(m,success);updateNeighborhoodHUDV134();saveGame?.(0,true);return true"
if repl not in s:
    if needle not in s: raise SystemExit('living-streets combat aftermath seam missing')
    s=s.replace(needle,repl,1)
streets.write_text(s,encoding='utf-8')

manifest=root/'src/bootstrap/module-manifest.js'
s=manifest.read_text(encoding='utf-8')
entry="  'world.transitIncidents':{path:'./src/world/transit-incidents-pwa12-104-city-candidate-06.js',kind:'module'},\n"
if 'world.transitIncidents' not in s:
    needle="  'world.accessEcology':{path:'./src/world/access-ecology-pwa12-104-city-candidate-05.js',kind:'module'},\n"
    if needle not in s: raise SystemExit('candidate 05 manifest seam missing')
    s=s.replace(needle,needle+entry,1)
    order="'world.multiHopLogistics','world.accessEcology','missions.approaches'"
    if order not in s: raise SystemExit('candidate 05 manifest order seam missing')
    s=s.replace(order,"'world.multiHopLogistics','world.accessEcology','world.transitIncidents','missions.approaches'",1)
manifest.write_text(s,encoding='utf-8')

bundle=root/'src/runtime/runtime-bundle.js'
s=bundle.read_text(encoding='utf-8')
eco='/* SOURCE: src/world/access-ecology-pwa12-104-city-candidate-05.js */'
inc='/* SOURCE: src/world/transit-incidents-pwa12-104-city-candidate-06.js */'
mission='/* SOURCE: src/missions/contract-approaches-v13-4b.js */'
if eco not in s or mission not in s: raise SystemExit('candidate 05 runtime seam missing')
if inc not in s:s=s.replace(mission,inc+'\n'+mission,1)
pos=[s.index(x) for x in (eco,inc,mission)]
if pos!=sorted(pos):raise SystemExit(f'transit incident runtime order invalid: {pos}')
bundle.write_text(s,encoding='utf-8')
print('patched physical transit incidents candidate 06',root)
