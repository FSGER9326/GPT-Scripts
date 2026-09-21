if(typeof window!=='undefined'){
(() => {
'use strict';
const V135_VERSION='13.5';
const V135_MAX_ACTIVE=6;
const V135_PROTECTED_TYPES=new Set(['boss','rival','showdown']);
const V135_BASE={
 serializeGame,loadGame,startNewGame,advanceTime,generateMissions,createCombatUnits,
 showMissionBriefingV10,showDebriefV10,openSafehouse,renderRoster,
 renderContactDossierV13:typeof renderContactDossierV13==='function'?renderContactDossierV13:null
};

function hashV135(s){if(typeof hashString==='function')return hashString(String(s));let h=2166136261>>>0;for(const c of String(s)){h^=c.charCodeAt(0);h=Math.imul(h,16777619)}return h>>>0}
function clampV135(v,a,b){return Math.max(a,Math.min(b,v))}
function moneyV135(v){return `¢${Math.round(v||0).toLocaleString()}`}
function rosterIdV135(u,i=0){if(!u)return null;if(!u.v135RosterId)u.v135RosterId=`v135r_${hashV135(`${u.name||'merc'}|${u.className||'class'}|${i}`).toString(36)}`;return u.v135RosterId}
function ensureCompanyStateV135(){
 const day=Number.isFinite(Game.day)?Game.day:1;
 if(!Game.companyV135||typeof Game.companyV135!=='object')Game.companyV135={};
 const s=Game.companyV135;s.version=1;s.reserveIds=Array.isArray(s.reserveIds)?s.reserveIds:[];s.activeIds=Array.isArray(s.activeIds)?s.activeIds:[];
 s.finances=s.finances||{};if(!Number.isFinite(s.finances.lastProcessedDay))s.finances.lastProcessedDay=day;s.finances.ledger=Array.isArray(s.finances.ledger)?s.finances.ledger:[];s.finances.outstanding=Number.isFinite(s.finances.outstanding)?s.finances.outstanding:0;s.finances.missedPayments=Number.isFinite(s.finances.missedPayments)?s.finances.missedPayments:0;
 s.maintenance=s.maintenance||{};s.maintenance.weaponWear=s.maintenance.weaponWear||{};s.maintenance.armorWear=s.maintenance.armorWear||{};s.maintenance.pendingRepairs=Array.isArray(s.maintenance.pendingRepairs)?s.maintenance.pendingRepairs:[];
 s.contracts=s.contracts||{};s.contracts.accepted=s.contracts.accepted||{};s.contracts.deadlines=s.contracts.deadlines||{};
 s.rivalEscalation=s.rivalEscalation||{};s.rivalEscalation.pressure=Number.isFinite(s.rivalEscalation.pressure)?s.rivalEscalation.pressure:0;s.rivalEscalation.milestones=s.rivalEscalation.milestones||{};s.rivalEscalation.lastEventDay=Number.isFinite(s.rivalEscalation.lastEventDay)?s.rivalEscalation.lastEventDay:0;s.rivalEscalation.lastRivalContracts=Number.isFinite(s.rivalEscalation.lastRivalContracts)?s.rivalEscalation.lastRivalContracts:(Game.rival?.contracts||0);
 s.stats=s.stats||{daysProcessed:0,repairs:0,expired:0,wearEvents:0};
 return s
}
window.ensureCompanyStateV135=ensureCompanyStateV135;

function migrateCompanyRosterV135(){
 const s=ensureCompanyStateV135(),roster=Game.roster||[],ids=roster.map((u,i)=>rosterIdV135(u,i)),valid=new Set(ids);
 s.activeIds=s.activeIds.filter(id=>valid.has(id));s.reserveIds=s.reserveIds.filter(id=>valid.has(id)&&!s.activeIds.includes(id));
 for(const id of ids)if(!s.activeIds.includes(id)&&!s.reserveIds.includes(id)){if(s.activeIds.length<V135_MAX_ACTIVE)s.activeIds.push(id);else s.reserveIds.push(id)}
 if(s.activeIds.length>V135_MAX_ACTIVE){s.reserveIds.unshift(...s.activeIds.splice(V135_MAX_ACTIVE))}
 s.reserveIds=[...new Set(s.reserveIds.filter(id=>valid.has(id)&&!s.activeIds.includes(id)))];return s
}
window.migrateCompanyRosterV135=migrateCompanyRosterV135;
function rosterByIdV135(id){return (Game.roster||[]).find((u,i)=>rosterIdV135(u,i)===id)||null}
function activeCrewV135(){const s=migrateCompanyRosterV135();return s.activeIds.map(rosterByIdV135).filter(Boolean)}
function reserveCrewV135(){const s=migrateCompanyRosterV135();return s.reserveIds.map(rosterByIdV135).filter(Boolean)}
function seriousInjuryV135(u){return window.seriousInjuryOfV134B?window.seriousInjuryOfV134B(u):((u?.injuries||[]).find(x=>x==='broken_arm'||x==='concussion')||null)}
function isDeployableV135(u){return !!u&&!seriousInjuryV135(u)&&activeCrewV135().includes(u)}
function deployableActiveCrewV135(){return activeCrewV135().filter(u=>!seriousInjuryV135(u))}
function setActiveCrewV135(ids){const s=ensureCompanyStateV135(),valid=new Set((Game.roster||[]).map((u,i)=>rosterIdV135(u,i))),next=[...new Set(ids)].filter(id=>valid.has(id));if(next.length>V135_MAX_ACTIVE)return false;s.activeIds=next;s.reserveIds=[...(Game.roster||[]).map((u,i)=>rosterIdV135(u,i)).filter(id=>!next.includes(id))];return true}
Object.assign(window,{activeCrewV135,reserveCrewV135,isDeployableV135,deployableActiveCrewV135,setActiveCrewV135});

function mercWageV135(u){const base={'Cyber Sword':42,'Gunslinger':38,'Hacker':44,'AgentEX':46,'Sniper':43}[u?.className]??36;const level=Math.max(1,u?.level||1),load=Math.max(0,u?.neuralLoad||0),trait=(u?.traits||[]).includes('Hotshot')?4:(u?.traits||[]).includes('Loyal')?-2:0;return Math.max(24,Math.round(base+level*7+load*1.5+trait))}
window.mercWageV135=mercWageV135;
function companyDailyCostV135(){const safe=Game.safehouse||{},upgradeTotal=['workshop','infirmary','bar','server'].reduce((n,k)=>n+Math.max(0,(safe[k]||1)-1),0),safehouse=80+25*upgradeTotal,wages=(Game.roster||[]).reduce((n,u)=>n+mercWageV135(u),0),medical=8*(Game.roster||[]).filter(u=>(u.injuries||[]).length||u.hp<u.maxHp).length,maintenance=6*activeCrewV135().length,base=safehouse+wages+medical+maintenance,pct=window.heatVendorPctV134B?window.heatVendorPctV134B():0,heat=Math.floor(base*pct/100);return{safehouse,wages,medical,maintenance,heat,total:base+heat}}
window.companyDailyCostV135=companyDailyCostV135;

function moraleDeltaV135(delta){for(const u of Game.roster||[])u.morale=clampV135((u.morale??70)+delta,0,100)}
function rivalPressureTierV135(){const p=ensureCompanyStateV135().rivalEscalation.pressure;return p>=100?'SHOWDOWN READY':p>=75?'WAR FOOTING':p>=50?'HUNTING':p>=25?'WATCHING':'QUIET'}
function checkRivalMilestonesV135(){const s=ensureCompanyStateV135(),r=s.rivalEscalation,out=[],milestones=[[25,'WATCHING'],[50,'HUNTING'],[75,'WAR_FOOTING'],[100,'SHOWDOWN_READY']];for(const [at,key] of milestones)if(r.pressure>=at&&!r.milestones[key]){r.milestones[key]={day:Game.day,pressure:r.pressure};out.push(key);if(typeof addJournal==='function')addJournal('main',`Black Halo · ${key.replaceAll('_',' ')}`,`Rival pressure reached ${r.pressure}.`)}return out}
function adjustRivalPressureV135(delta,reason=''){const r=ensureCompanyStateV135().rivalEscalation;r.pressure=clampV135((r.pressure||0)+delta,0,100);r.lastEventDay=Game.day||r.lastEventDay;if(reason){r.history=r.history||[];r.history.unshift({day:Game.day,delta,reason});r.history=r.history.slice(0,30)}checkRivalMilestonesV135();return r.pressure}
Object.assign(window,{adjustRivalPressureV135,rivalPressureTierV135,checkRivalMilestonesV135});

function contractDeadlineEligibleV135(m){if(!m||!m.id)return false;if(m.storyKey||m.oracleKey||m.actKey||m.isRival||m.isShowdown||m.v134bShowdown||m.v13Chain||String(m.id).startsWith('chain_'))return false;if(V135_PROTECTED_TYPES.has(m.type))return false;return true}
function assignContractDeadlineV135(m){if(!contractDeadlineEligibleV135(m))return null;const d=ensureCompanyStateV135().contracts.deadlines;if(d[m.id])return d[m.id];const h=hashV135(`${m.id}|deadline`)%100,created=m.generatedDay||Game.day||1;let urgency,days;if(h<25){urgency='URGENT';days=1+(hashV135(m.id+'u')%2)}else if(h<70){urgency='STANDARD';days=3+(hashV135(m.id+'s')%2)}else{urgency='RELAXED';days=5+(hashV135(m.id+'r')%3)}return d[m.id]={missionId:m.id,createdDay:created,dueDay:created+Math.max(1,days),urgency,expired:false}}
function contractDeadlineStateV135(m){const d=assignContractDeadlineV135(m);if(!d)return{eligible:false,label:'OPEN',days:null,expired:false};const days=d.dueDay-(Game.day||1),expired=days<0||d.expired;return{eligible:true,label:expired?'EXPIRED':days<=1?'URGENT':`${days} DAYS`,days,expired,urgency:d.urgency,dueDay:d.dueDay}}
function assignAllDeadlinesV135(){for(const c of Game.contacts||[])for(const m of c.missions||[])assignContractDeadlineV135(m)}
function expireContractsV135(day=Game.day){const s=ensureCompanyStateV135(),expired=[];for(const c of Game.contacts||[]){const keep=[];for(const m of c.missions||[]){const d=s.contracts.deadlines[m.id]||assignContractDeadlineV135(m);if(d&&contractDeadlineEligibleV135(m)&&day>d.dueDay){d.expired=true;expired.push(m.id);s.stats.expired++;if(window.changeContactTrustV13)window.changeContactTrustV13(c.id,-2,'Expired contract');if(c.faction&&Game.rep?.[c.faction]!=null)Game.rep[c.faction]-=1;adjustRivalPressureV135(2,`Expired contract: ${m.name}`)}else keep.push(m)}c.missions=keep}return expired}
Object.assign(window,{contractDeadlineEligibleV135,assignContractDeadlineV135,contractDeadlineStateV135,expireContractsV135});


const V135_MISSION_TEMPLATES=[
 {type:'eliminate',name:'Sweep & Clear',desc:'Neutralize a hostile cell before it relocates.',enemies:['Guard','Guard','Heavy'],base:560},
 {type:'extract',name:'Hot Extraction',desc:'Secure the target and open an exit corridor.',enemies:['Guard','Drone','Enforcer'],base:650},
 {type:'sabotage',name:'Sabotage Grid',desc:'Break protected infrastructure and disappear before response teams close.',enemies:['Enforcer','Guard','Heavy','Drone'],base:780},
 {type:'bounty',name:'Priority Bounty',desc:'Find and neutralize a protected high-value target.',enemies:['Enforcer','Enforcer','Heavy'],base:940},
 {type:'steal',name:'Data Extraction',desc:'Acquire protected data from a hostile network node.',enemies:['Guard','Drone','Enforcer'],base:720}
];
function generateContactMissionV135(c,day,slot){
 const seed=hashV135(`${c.id}|${day}|${slot}|v135job`),tpl=V135_MISSION_TEMPLATES[seed%V135_MISSION_TEMPLATES.length],factions=Object.keys(FACTIONS),targetFaction=factions[(seed>>>5)%factions.length],diff=1+((seed>>>9)%3),pool={meridian:['Guard','Enforcer','Drone'],wraiths:['Drone','Enforcer','Guard'],iron:['Guard','Heavy','Brute'],chrome:['Enforcer','Brute','Heavy'],spine:['Guard','Drone','Enforcer']}[targetFaction]||tpl.enemies;
 const m={id:`v135_${c.id}_${day}_${slot}_${(seed%46656).toString(36)}`,contact:c.id,type:tpl.type,objective:tpl.type,name:tpl.name,desc:tpl.desc,enemies:[...pool],diff,reward:tpl.base+diff*160+((seed>>>13)%180),xp:70+diff*35,targetFaction,factionRepGain:5+diff*2,factionRepLoss:{[targetFaction]:-(5+diff*2)},sectorId:c.sectorId||null,v135Generated:true,generatedDay:day};
 if(typeof assignMissionTacticalV12==='function')assignMissionTacticalV12(m);assignContractDeadlineV135(m);return m
}
function replenishContractsV135(day=Game.day){let added=0;for(const c of Game.contacts||[]){c.missions=Array.isArray(c.missions)?c.missions:[];const ordinary=c.missions.filter(contractDeadlineEligibleV135);const target=2+((hashV135(`${c.id}|${day}|board`)%100)<28?1:0);for(let slot=ordinary.length;slot<target;slot++){c.missions.push(generateContactMissionV135(c,day,slot));added++}}return added}
window.replenishContractsV135=replenishContractsV135;

function processCompanyDayV135(day){const s=ensureCompanyStateV135(),entries=[];if(day<=s.finances.lastProcessedDay)return entries;for(let d=s.finances.lastProcessedDay+1;d<=day;d++){const cost=companyDailyCostV135(),prior=s.finances.outstanding||0,due=prior+cost.total,paid=Math.min(Math.max(0,Game.credits||0),due);Game.credits-=paid;s.finances.outstanding=Math.max(0,due-paid);const missed=s.finances.outstanding>0;if(missed){s.finances.missedPayments++;moraleDeltaV135(-3);adjustRivalPressureV135(5,'Unpaid operating costs')}else if(prior>0){moraleDeltaV135(1)}const rc=Game.rival?.contracts||0,delta=Math.max(0,rc-(s.rivalEscalation.lastRivalContracts||0));if(delta)adjustRivalPressureV135(delta*5,'Black Halo contract activity');s.rivalEscalation.lastRivalContracts=rc;if((Game.notoriety||0)>=90)adjustRivalPressureV135(3,'BURNED Notoriety');const expired=expireContractsV135(d),replenished=replenishContractsV135(d);const entry={day:d,cost,priorOutstanding:prior,paid,outstanding:s.finances.outstanding,missed,expired:[...expired],replenished};s.finances.ledger.unshift(entry);s.finances.ledger=s.finances.ledger.slice(0,90);s.finances.lastProcessedDay=d;s.stats.daysProcessed++ ;entries.push(entry)}return entries}
window.processCompanyDayV135=processCompanyDayV135;

function equipmentKeyV135(item,owner,slot){const id=typeof item==='string'?item:(item?.id||'none'),oid=owner?rosterIdV135(owner,(Game.roster||[]).indexOf(owner)):'stash';return `${oid}:${slot}:${id}`}
function wearMapV135(slot){return slot==='weapon'?ensureCompanyStateV135().maintenance.weaponWear:ensureCompanyStateV135().maintenance.armorWear}
function equipmentWearV135(u,slot){const id=slot==='weapon'?u?.weapon:u?.armor_item;if(!id)return 0;return wearMapV135(slot)[equipmentKeyV135(id,u,slot)]||0}
function applyMissionWearV135({success=true,mission=null}={}){if(!mission||mission._v135WearApplied)return false;mission._v135WearApplied=true;const diff=Math.max(1,mission.diff||1),base=success?4+diff:10+diff*2;for(const u of activeCrewV135()){for(const slot of ['weapon','armor']){const id=slot==='weapon'?u.weapon:u.armor_item;if(!id)continue;const map=wearMapV135(slot),key=equipmentKeyV135(id,u,slot),extra=slot==='armor'&&((u.injuries||[]).length||u._v131WasDowned)?3:0;map[key]=clampV135((map[key]||0)+base+extra,0,100)}}ensureCompanyStateV135().stats.wearEvents++;if(mission.isRival&&success)adjustRivalPressureV135(-8,'Successful anti-rival operation');return true}
function repairQuoteV135(keys){const s=ensureCompanyStateV135(),all=[...Object.entries(s.maintenance.weaponWear).map(([key,wear])=>({slot:'weapon',key,wear})),...Object.entries(s.maintenance.armorWear).map(([key,wear])=>({slot:'armor',key,wear}))],sel=all.filter(x=>keys.includes(x.key)&&x.wear>0),wear=sel.reduce((n,x)=>n+x.wear,0);return{credits:Math.ceil(wear*2.2),salvage:Math.ceil(wear/18),wear,items:sel.length}}
function repairEquipmentV135(keys){const q=repairQuoteV135(keys);if(!q.items)return false;if((Game.credits||0)<q.credits||(Game.salvage||0)<q.salvage)return false;Game.credits-=q.credits;Game.salvage-=q.salvage;const s=ensureCompanyStateV135();for(const key of keys){if(key in s.maintenance.weaponWear)s.maintenance.weaponWear[key]=0;if(key in s.maintenance.armorWear)s.maintenance.armorWear[key]=0}s.stats.repairs++;saveGame(0,true);return true}
Object.assign(window,{equipmentKeyV135,equipmentWearV135,applyMissionWearV135,repairQuoteV135,repairEquipmentV135});

function mercStatusV135(u){if(seriousInjuryV135(u))return{label:'INJURED',cls:'injured'};return activeCrewV135().includes(u)?{label:'ACTIVE',cls:'active'}:{label:'RESERVE',cls:'reserve'}}
function itemLabelV135(id){if(!id)return'—';if(typeof ITEMS==='object'&&ITEMS[id])return ITEMS[id].name||id;for(const pool of [window.V13_WEAPONS,window.V13_ARMOR,window.V13_ARMORS]){if(Array.isArray(pool)){const x=pool.find(v=>v.id===id);if(x)return x.name||id}}return id}
function allWearEntriesV135(){const s=ensureCompanyStateV135(),out=[];for(const u of Game.roster||[])for(const slot of ['weapon','armor']){const id=slot==='weapon'?u.weapon:u.armor_item;if(!id)continue;const key=equipmentKeyV135(id,u,slot),wear=wearMapV135(slot)[key]||0;if(wear>0)out.push({key,wear,u,slot,id,label:`${u.name} · ${itemLabelV135(id)}`})}return out.sort((a,b)=>b.wear-a.wear)}

function renderCompanyPanelV135(){const inner=document.getElementById('modal-inner');if(!inner)return;inner.querySelector('#v135-company-panel')?.remove();const s=migrateCompanyRosterV135(),cost=companyDailyCostV135(),active=activeCrewV135(),reserve=reserveCrewV135(),injured=(Game.roster||[]).filter(seriousInjuryV135),wear=allWearEntriesV135(),known=new Set((Game.contacts||[]).filter(c=>Game.contactRelations?.[c.id]?.known!==false).map(c=>c.id)),deadlines=(Game.contacts||[]).filter(c=>known.has(c.id)).flatMap(c=>c.missions||[]).map(m=>({m,d:contractDeadlineStateV135(m)})).filter(x=>x.d.eligible&&!x.d.expired).sort((a,b)=>a.d.dueDay-b.d.dueDay),dueSoon=deadlines.filter(x=>x.d.days<=2).length,pressure=s.rivalEscalation.pressure,tier=rivalPressureTierV135();const host=document.createElement('div');host.id='v135-company-panel';host.innerHTML=`<div class="v135-company-head"><b>COMPANY OPERATIONS</b><div class="v135-head-actions"><span>${tier} · PRESSURE ${pressure}</span><button class="btn small" id="v135-company-leave">LEAVE</button></div></div><div class="v135-pressure"><i style="width:${pressure}%"></i></div><div class="v135-metrics"><div class="v135-metric"><span>CASH</span><b>${moneyV135(Game.credits)}</b></div><div class="v135-metric"><span>OUTSTANDING</span><b>${moneyV135(s.finances.outstanding)}</b></div><div class="v135-metric"><span>NEXT BURN</span><b>${moneyV135(cost.total)}</b></div><div class="v135-metric"><span>PAYROLL</span><b>${moneyV135(cost.wages)}</b></div><div class="v135-metric"><span>ACTIVE</span><b>${active.length}/${V135_MAX_ACTIVE}</b></div><div class="v135-metric"><span>RESERVE</span><b>${reserve.length}</b></div><div class="v135-metric"><span>INJURED</span><b>${injured.length}</b></div><div class="v135-metric"><span>DUE ≤2D</span><b>${dueSoon}</b></div></div><div class="v135-maint-title">DEPLOYMENT ROSTER</div><div class="v135-roster-grid">${(Game.roster||[]).map((u,i)=>{const id=rosterIdV135(u,i),st=mercStatusV135(u),w=mercWageV135(u),isAct=st.cls==='active',disable=st.cls==='injured'||(isAct&&active.length<=1)||(!isAct&&active.length>=V135_MAX_ACTIVE);return`<div class="v135-roster-row"><div><strong>${u.name}</strong> <span class="v135-chip ${st.cls}">${st.label}</span><small>${u.className} · LV ${u.level||1} · ${moneyV135(w)}/day${seriousInjuryV135(u)?` · ${INJURY_DEFS[seriousInjuryV135(u)]?.name||seriousInjuryV135(u)}`:''}</small></div><button class="btn small" data-v135-roster="${id}" ${disable?'disabled':''}>${isAct?'RESERVE':'ACTIVATE'}</button></div>`}).join('')}</div><div class="v135-maint"><div class="v135-maint-title">EQUIPMENT MAINTENANCE</div>${wear.length?wear.slice(0,8).map(x=>`<div class="v135-wear-row"><div>${x.label}<div class="v135-wearbar"><i style="width:${x.wear}%"></i></div></div><b>${Math.round(x.wear)}%</b></div>`).join(''):'<div style="font-size:7px;color:#627680">No accumulated mission wear.</div>'}${wear.length?(()=>{const q=repairQuoteV135(wear.map(x=>x.key));return`<button class="btn small" id="v135-repair-all" style="width:100%;margin-top:6px" ${Game.credits<q.credits||Game.salvage<q.salvage?'disabled':''}>REPAIR ALL · ${moneyV135(q.credits)} · ⚙ ${q.salvage}</button>`})():''}</div>${deadlines[0]?`<div class="v135-deadline-note">NEXT DEADLINE · <b>${deadlines[0].m.name}</b> · DAY ${deadlines[0].d.dueDay} · ${deadlines[0].d.label}</div>`:''}`;
 const grid=inner.querySelector('.safe-grid');if(grid)grid.insertAdjacentElement('beforebegin',host);else{const close=inner.querySelector('#safe-close');if(close)close.insertAdjacentElement('beforebegin',host);else inner.appendChild(host)};const quickLeave=host.querySelector('#v135-company-leave');if(quickLeave)quickLeave.onclick=()=>document.getElementById('modal')?.classList.remove('open');host.querySelectorAll('[data-v135-roster]').forEach(b=>b.onclick=()=>{const id=b.dataset.v135Roster,s=ensureCompanyStateV135(),is=s.activeIds.includes(id);if(is){if(s.activeIds.length<=1)return;s.activeIds=s.activeIds.filter(x=>x!==id);if(!s.reserveIds.includes(id))s.reserveIds.push(id)}else if(s.activeIds.length<V135_MAX_ACTIVE){s.reserveIds=s.reserveIds.filter(x=>x!==id);s.activeIds.push(id)}saveGame(0,true);openSafehouse()});const repair=host.querySelector('#v135-repair-all');if(repair)repair.onclick=()=>{if(repairEquipmentV135(wear.map(x=>x.key)))openSafehouse()};return host}
window.renderCompanyPanelV135=renderCompanyPanelV135;

function decorateBriefingV135(m){assignContractDeadlineV135(m);const body=document.getElementById('v10-brief-body');if(!body)return;body.querySelectorAll('.v135-deadline-note,.v135-team-note').forEach(x=>x.remove());const actions=body.querySelector('.v10-brief-actions')||body.lastElementChild,d=contractDeadlineStateV135(m),team=deployableActiveCrewV135(),reserve=reserveCrewV135(),blocked=activeCrewV135().filter(seriousInjuryV135);const dn=document.createElement('div');dn.className='v135-deadline-note';dn.innerHTML=d.eligible?`CONTRACT WINDOW · <b>${d.urgency}</b> · DUE DAY ${d.dueDay} · <span class="v135-chip ${d.days<=1?'urgent':'deadline'}">${d.label}</span>`:'CONTRACT WINDOW · STORY/PRIORITY JOB — NO GENERATED EXPIRY';actions?.insertAdjacentElement('beforebegin',dn);const tn=document.createElement('div');tn.className='v135-team-note';tn.innerHTML=`FIELD TEAM · <b>${team.length}</b> deployable / ${activeCrewV135().length} active · ${reserve.length} reserve${blocked.length?` · unavailable: ${blocked.map(u=>u.name).join(', ')}`:''}`;dn.insertAdjacentElement('afterend',tn)}
function decorateContactDeadlinesV135(id){const c=(Game.contacts||[]).find(x=>x.id===id);if(!c)return;for(const m of c.missions||[])assignContractDeadlineV135(m);document.querySelectorAll('#v13-contracts .v13-mission[data-m]').forEach(el=>{el.querySelector('.v135-chip.deadline,.v135-chip.urgent')?.remove();const m=c.missions.find(x=>x.id===el.dataset.m);if(!m)return;const d=contractDeadlineStateV135(m);if(!d.eligible)return;const chip=document.createElement('span');chip.className=`v135-chip ${d.days<=1?'urgent':'deadline'}`;chip.textContent=d.label;el.appendChild(chip)})}

function annotateRosterV135(body){if(!body)return;const cards=[...body.querySelectorAll('.v13-crew-card,.crew-card')];cards.forEach((card,i)=>{const u=Game.roster?.[i];if(!u)return;card.querySelector('.v135-crew-badge')?.remove();const st=mercStatusV135(u),b=document.createElement('span');b.className=`v135-chip v135-crew-badge ${st.cls}`;b.textContent=st.label;if(getComputedStyle(card).position==='static')card.style.position='relative';card.appendChild(b)})}

function createCombatUnitsV135(m){const r=V135_BASE.createCombatUnits(m);const active=new Set(activeCrewV135()),remove=(Game.units||[]).filter(u=>u.team==='player'&&(!active.has(u.rosterRef)||seriousInjuryV135(u.rosterRef)));for(const u of remove){const c=typeof cellAt==='function'?cellAt(u.x,u.y):null;if(c?.unit===u)c.unit=null;Game.units.splice(Game.units.indexOf(u),1)}if(window.applyApproachSpawnV134B)window.applyApproachSpawnV134B(m);for(const u of (Game.units||[]).filter(x=>x.team==='player'&&x.rosterRef)){const ww=equipmentWearV135(u.rosterRef,'weapon'),aw=equipmentWearV135(u.rosterRef,'armor');u.v135WeaponWear=ww;u.v135ArmorWear=aw;if(ww>=80)u.critChance=Math.max(0,(u.critChance||0)-8);if(aw>=80)u.armor=Math.max(0,(u.armor||0)-1)}return r}
function showDebriefV135(success,m,salvage){applyMissionWearV135({success,mission:m});return V135_BASE.showDebriefV10(success,m,salvage)}
function openSafehouseV135(){const r=V135_BASE.openSafehouse();migrateCompanyRosterV135();assignAllDeadlinesV135();renderCompanyPanelV135();return r}
function showMissionBriefingV135(m){assignContractDeadlineV135(m);const r=V135_BASE.showMissionBriefingV10(m);decorateBriefingV135(m);return r}
function renderRosterV135(body){const r=V135_BASE.renderRoster(body);annotateRosterV135(body);return r}
function renderContactDossierV135(id){const r=V135_BASE.renderContactDossierV13?V135_BASE.renderContactDossierV13(id):undefined;decorateContactDeadlinesV135(id);return r}
function generateMissionsV135(){const r=V135_BASE.generateMissions();assignAllDeadlinesV135();return r}
function advanceTimeV135(minutes){const before=Game.day||1,r=V135_BASE.advanceTime(minutes),after=Game.day||before;if(after>before)processCompanyDayV135(after);return r}
function startNewGameV135(name,className,background){const r=V135_BASE.startNewGame(name,className,background);Game.companyV135=null;ensureCompanyStateV135().finances.lastProcessedDay=Game.day||1;migrateCompanyRosterV135();assignAllDeadlinesV135();return r}

function serializeGameV135(){const d=JSON.parse(V135_BASE.serializeGame());d.version=V135_VERSION;d.companyV135=JSON.parse(JSON.stringify(ensureCompanyStateV135()));return JSON.stringify(d)}
function readSavePayloadV135(slot){for(const key of [`chrome_requiem_v13_${slot}`,`chrome_requiem_v12_${slot}`,`chrome_requiem_v11_${slot}`,`chrome_requiem_v10_${slot}`,`chrome_requiem_v9_${slot}`,`chrome_requiem_v8_${slot}`,`chrome_requiem_v7_${slot}`,`chrome_requiem_save_${slot}`]){const raw=localStorage.getItem(key);if(raw){try{return JSON.parse(raw)}catch(e){}}}return null}
function restoreCompanyV135(data){Game.companyV135=data?.companyV135?JSON.parse(JSON.stringify(data.companyV135)):null;const s=ensureCompanyStateV135();if(!data?.companyV135)s.finances.lastProcessedDay=Game.day||1;migrateCompanyRosterV135();assignAllDeadlinesV135();return s}
function loadGameV135(slot){const data=readSavePayloadV135(slot),ok=V135_BASE.loadGame(slot);if(ok){restoreCompanyV135(data);saveGame(0,true)}return ok}
Object.assign(window,{serializeGameV135,loadGameV135,startNewGameV135,advanceTimeV135,createCombatUnitsV135,restoreCompanyV135});

// Explicit final compatibility assignments: one named v13.5 layer, no anonymous wrapper chain.
serializeGame=serializeGameV135;loadGame=loadGameV135;startNewGame=startNewGameV135;advanceTime=advanceTimeV135;generateMissions=generateMissionsV135;createCombatUnits=createCombatUnitsV135;showDebriefV10=showDebriefV135;openSafehouse=openSafehouseV135;showMissionBriefingV10=showMissionBriefingV135;renderRoster=renderRosterV135;if(V135_BASE.renderContactDossierV13){renderContactDossierV13=renderContactDossierV135;window.renderContactDossierV13=renderContactDossierV135}

window.CRRuntime=Object.freeze({
 save:(slot=0,quiet=true)=>saveGame(slot,quiet),
 load:slot=>loadGameV135(slot),
 newGame:(name,className,background)=>startNewGameV135(name,className,background),
 advanceTime:minutes=>advanceTimeV135(minutes),
 startMission:m=>typeof startMission==='function'?startMission(m):false,
 buildGrid:m=>buildGrid(m),
 createCombatUnits:m=>createCombatUnitsV135(m)
});


function retireRedundantUIV135(){
 document.getElementById('ov-city-v11')?.remove();document.querySelector('[data-v11-city]')?.remove();document.getElementById('v11-city-screen')?.remove();
 const oldTag=document.querySelector('#intro-tag');if(oldTag&&!oldTag.dataset.v135Clean){oldTag.dataset.v135Clean='1';oldTag.textContent=oldTag.textContent.replace(/\s*·\s*V11\b/g,'')}
}
window.retireRedundantUIV135=retireRedundantUIV135;

function runDiagnosticsV135(){const rows=[],add=(name,ok,details='')=>rows.push({name,ok:!!ok,details});try{const s=migrateCompanyRosterV135(),cost=companyDailyCostV135();add('company state',!!s&&s.version===1);add('active cap',s.activeIds.length<=V135_MAX_ACTIVE,s.activeIds.length);add('roster partition',s.activeIds.length+s.reserveIds.length===(Game.roster||[]).length);add('deterministic wage',(Game.roster||[]).every(u=>mercWageV135(u)===mercWageV135(u)));add('daily cost',cost.total===cost.safehouse+cost.wages+cost.medical+cost.maintenance+cost.heat,cost.total);add('wear maps',!!s.maintenance.weaponWear&&!!s.maintenance.armorWear);add('deadline state',!!s.contracts.deadlines);add('rival pressure',s.rivalEscalation.pressure>=0&&s.rivalEscalation.pressure<=100,s.rivalEscalation.pressure);add('runtime facade',!!window.CRRuntime);add('v13.4B retained',!!ChromeRequiem.modules?.ContractApproachesV134B);add('v13.4A retained',!!ChromeRequiem.modules?.LivingStreetsV134);add('v12 tactical retained',!!ChromeRequiem.modules?.TacticalV12)}catch(e){add('exception',false,e.message)}return{version:V135_VERSION,passed:rows.filter(x=>x.ok).length,total:rows.length,results:rows}}
window.runDiagnosticsV135=runDiagnosticsV135;

window.ChromeRequiem.version=V135_VERSION;window.ChromeRequiem.modules.FoundationV135={ensure:ensureCompanyStateV135,active:activeCrewV135,reserve:reserveCrewV135,wage:mercWageV135,cost:companyDailyCostV135,deadlines:contractDeadlineStateV135,pressure:rivalPressureTierV135,diagnostics:runDiagnosticsV135};
ensureCompanyStateV135();migrateCompanyRosterV135();assignAllDeadlinesV135();retireRedundantUIV135();
})();
}



const companyCallV14=(name,...args)=>{
 const fn=globalThis[name];
 if(typeof fn!=='function')throw new Error(`CompanyV14 missing legacy implementation: ${name}`);
 return fn(...args);
};
const CompanyV14=Object.freeze({
 version:'13.5',
 ensureState:(...args)=>companyCallV14('ensureCompanyStateV135',...args),
 migrateRoster:(...args)=>companyCallV14('migrateCompanyRosterV135',...args),
 dailyCost:(...args)=>companyCallV14('companyDailyCostV135',...args),
 processDay:(...args)=>companyCallV14('processCompanyDayV135',...args),
 wage:(...args)=>companyCallV14('mercWageV135',...args),
 renderPanel:(...args)=>companyCallV14('renderCompanyPanelV135',...args),
 diagnostics:(...args)=>companyCallV14('runDiagnosticsV135',...args)
});
globalThis.ChromeRequiemV14Domains ||= {};
globalThis.ChromeRequiemV14Domains.company=CompanyV14;
