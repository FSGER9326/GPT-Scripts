if(typeof window!=='undefined'){(()=>{
'use strict';
const VERSION='14.0-social.5';
const MIN_BONDED_LOYALTY=2;
const MIN_DUTY_LOYALTY=3;
const STRAIN_LOYALTY_COST=1;

function rosterId(u,i=-1){
  if(!u)return null;
  if(u.v135RosterId)return u.v135RosterId;
  window.migrateCompanyRosterV135?.();
  if(u.v135RosterId)return u.v135RosterId;
  const idx=i>=0?i:(Game.roster||[]).indexOf(u);
  return u.recruitId||`crew:${u.name||'merc'}:${u.className||'class'}:${Math.max(0,idx)}`;
}
function crewById(id){return (Game.roster||[]).find((u,i)=>rosterId(u,i)===id)||null}
function companyState(){
  window.migrateCompanyRosterV135?.();
  return typeof window.ensureCompanyStateV135==='function'?window.ensureCompanyStateV135():(Game.companyV135||(Game.companyV135={}));
}
function state(){
  const company=companyState();
  const s=company.recoverySupportV14||(company.recoverySupportV14={version:1,assignments:{},history:[]});
  s.version=1;
  s.assignments=s.assignments&&typeof s.assignments==='object'?s.assignments:{};
  s.history=Array.isArray(s.history)?s.history:[];
  return s;
}
function recoveryState(){
  if(typeof window.ensureRecoveryNetworkV14==='function')return window.ensureRecoveryNetworkV14();
  return companyState().recoveryV14||{version:1,cases:{},history:[]};
}
function recoveryCaseById(id){return recoveryState()?.cases?.[id]||null}
function seriousInjury(u){
  if(typeof window.seriousInjuryOfV134B==='function')return window.seriousInjuryOfV134B(u);
  return (u?.injuries||[]).find(x=>x==='broken_arm'||x==='concussion')||null;
}
function activeIds(){return companyState().activeIds||[]}
function setReserve(id){
  const c=companyState();
  c.activeIds=(c.activeIds||[]).filter(x=>x!==id);
  c.reserveIds=Array.isArray(c.reserveIds)?c.reserveIds:[];
  if(!c.reserveIds.includes(id))c.reserveIds.push(id);
}
function setActiveIfVacant(id,targetCount){
  const u=crewById(id);if(!u||seriousInjury(u)||recoveryCaseById(id))return false;
  const c=companyState();c.activeIds=Array.isArray(c.activeIds)?c.activeIds:[];c.reserveIds=Array.isArray(c.reserveIds)?c.reserveIds:[];
  if(c.activeIds.includes(id))return true;
  if(c.activeIds.length>=Number(targetCount||0))return false;
  c.reserveIds=c.reserveIds.filter(x=>x!==id);c.activeIds.push(id);return true;
}
function relation(patient,helper){
  const loyalty=Number(helper?.loyalty||0);
  const sameFaction=!!patient?.originFaction&&patient.originFaction===helper?.originFaction;
  const sameContact=!!patient?.originContactId&&patient.originContactId===helper?.originContactId;
  const loyalTrait=(helper?.traits||[]).includes('Loyal');
  const trusted=loyalty>=4;
  const bonded=sameContact||sameFaction||loyalTrait||trusted;
  const eligible=loyalty>=MIN_DUTY_LOYALTY||(loyalty>=MIN_BONDED_LOYALTY&&bonded);
  let reason='professional duty';
  if(sameContact)reason='shared contact history';
  else if(sameFaction)reason='shared faction origin';
  else if(loyalTrait)reason='Loyal trait';
  else if(trusted)reason='trusted veteran';
  return{loyalty,sameFaction,sameContact,loyalTrait,trusted,bonded,eligible,strained:eligible&&!bonded,reason};
}
function supportCandidates(patientOrId){
  const patient=typeof patientOrId==='string'?crewById(patientOrId):patientOrId,id=rosterId(patient);
  const c=recoveryCaseById(id);if(!patient||!c||Number(c.dueDay||0)<=(Game.day||1)+1)return[];
  const s=state(),used=new Set(Object.values(s.assignments).map(a=>a?.helperId).filter(Boolean));
  const lead=Game.roster?.[0];
  const pool=typeof window.deployableActiveCrewV135==='function'?window.deployableActiveCrewV135():(Game.roster||[]).filter(u=>activeIds().includes(rosterId(u)));
  return pool.filter(u=>u&&u!==patient&&u!==lead&&!used.has(rosterId(u))&&!recoveryCaseById(rosterId(u))&&!seriousInjury(u)).map(u=>{
    const r=relation(patient,u);return{u,id:rosterId(u),...r};
  }).filter(x=>x.eligible).sort((a,b)=>Number(b.bonded)-Number(a.bonded)||b.loyalty-a.loyalty||String(a.u.name).localeCompare(String(b.u.name)));
}
function assignmentFor(patientOrId){return state().assignments[typeof patientOrId==='string'?patientOrId:rosterId(patientOrId)]||null}
function addHistory(entry){const s=state();s.history.unshift(entry);s.history=s.history.slice(0,40)}
function assignmentOutcome(a){
  const c=recoveryCaseById(a.patientId);if(c)return null;
  const hist=recoveryState()?.history||[];
  const h=hist.find(x=>x&&x.rosterId===a.patientId&&x.injuryId===a.injuryId&&Number(x.completedDay||x.day||0)>=Number(a.startedDay||0));
  if(h?.outcome==='recovered')return'recovered';
  const patient=crewById(a.patientId);
  if(!patient)return'roster_missing';
  if(!(patient.injuries||[]).includes(a.injuryId))return h?.outcome||'treated_elsewhere';
  return null;
}
function releaseAssignment(patientId,outcome){
  const s=state(),a=s.assignments[patientId];if(!a)return false;
  const helper=crewById(a.helperId),patient=crewById(patientId),completed=outcome==='recovered';
  let loyaltyChange=0;
  if(completed&&a.strained&&helper){
    const before=Number(helper.loyalty||0);helper.loyalty=Math.max(-6,before-STRAIN_LOYALTY_COST);loyaltyChange=helper.loyalty-before;
    window.addJournal?.('story','Recovery Friction',`${helper.name} carried ${patient?.name||a.patientName} through recovery, but the strained pairing cost trust. LOY ${before} → ${helper.loyalty}.`);
  }
  const returned=setActiveIfVacant(a.helperId,a.restoreActiveTargetCount);
  const c=recoveryCaseById(patientId);if(c?.crewSupport)c.crewSupport=null;
  addHistory({...a,outcome,completedDay:Game.day||1,loyaltyChange,helperReturnedActive:returned});
  delete s.assignments[patientId];
  if(helper)window.addJournal?.('main','Recovery Detail Released',`${helper.name} is released from ${patient?.name||a.patientName}'s recovery detail${returned?' and returns to ACTIVE duty':' and remains in RESERVE'}.`);
  return true;
}
function normalizeSupport(){
  const s=state();let changed=false;
  for(const [patientId,a] of Object.entries({...s.assignments})){
    if(!a||!a.helperId){delete s.assignments[patientId];changed=true;continue}
    const helper=crewById(a.helperId),patient=crewById(patientId);
    if(!helper||!patient){if(releaseAssignment(patientId,!patient?'roster_missing':'helper_missing'))changed=true;continue}
    const outcome=assignmentOutcome(a);
    if(outcome){if(releaseAssignment(patientId,outcome))changed=true;continue}
    setReserve(a.helperId);
    const c=recoveryCaseById(patientId);
    if(c)c.crewSupport={version:1,helperId:a.helperId,helperName:a.helperName,strained:!!a.strained,relationship:a.relationship};
  }
  return{state:s,changed};
}
function assignSupport(patientId,helperId){
  normalizeSupport();const s=state();if(s.assignments[patientId])return null;
  const patient=crewById(patientId),c=recoveryCaseById(patientId);if(!patient||!c||Number(c.dueDay||0)<=(Game.day||1)+1)return null;
  const choice=supportCandidates(patient).find(x=>x.id===helperId);if(!choice)return null;
  const beforeDue=Number(c.dueDay),day=Game.day||1,dueDay=Math.max(day+1,beforeDue-1);if(dueDay>=beforeDue)return null;
  const targetActiveCount=activeIds().length;setReserve(helperId);c.dueDay=dueDay;
  const a={version:1,patientId,helperId,patientName:patient.name,helperName:choice.u.name,injuryId:c.injuryId,startedDay:day,originalDueDay:beforeDue,dueDay,restoreActiveTargetCount:targetActiveCount,relationship:choice.reason,bonded:choice.bonded,strained:choice.strained,helperLoyaltyAtStart:choice.loyalty};
  s.assignments[patientId]=a;c.crewSupport={version:1,helperId,helperName:choice.u.name,strained:choice.strained,relationship:choice.reason};
  const consequence=choice.strained?'The pairing is strained: helper LOY -1 when recovery completes.':'The pair is bonded: no loyalty cost on completion.';
  window.addJournal?.('story','Recovery Partner Assigned',`${choice.u.name} takes recovery detail for ${patient.name}. Recovery moves Day ${beforeDue} → ${dueDay}; both operatives are unavailable for deployment. ${consequence}`);
  window.toast?.(`${choice.u.name} assigned · recovery -1 day`);window.saveGame?.(0,true);renderSupport();return a;
}
function activeAssignments(){normalizeSupport();return Object.values(state().assignments).filter(Boolean)}
function decorateBriefing(){
  const body=document.getElementById('v10-brief-body');if(!body)return;body.querySelector('.v14-recovery-support-briefing')?.remove();
  const rows=activeAssignments();if(!rows.length)return;
  const note=document.createElement('div');note.className='v135-team-note v14-recovery-support-briefing';
  note.innerHTML=`RECOVERY DETAIL · ${rows.map(a=>`<b>${a.helperName}</b> supporting <b>${a.patientName}</b> until Day ${a.dueDay}`).join(' · ')} · both unavailable`;
  const recovery=body.querySelector('.v14-recovery-briefing'),actions=body.querySelector('.v10-brief-actions');if(recovery)recovery.insertAdjacentElement('afterend',note);else actions?.insertAdjacentElement('beforebegin',note);
}
function renderSupport(){
  normalizeSupport();const panel=document.getElementById('v14-recovery-panel');if(!panel)return null;panel.querySelector('#v14-recovery-support')?.remove();
  const cases=Object.entries(recoveryState()?.cases||{}).filter(([,c])=>c&&Number(c.dueDay||0)>(Game.day||1));if(!cases.length)return null;
  const host=document.createElement('section');host.id='v14-recovery-support';host.className='v14-recovery-support';
  host.innerHTML='<div class="v14-recovery-support-head"><div><b>CREW RECOVERY BONDS</b><span>Commit a second operative to recovery detail: lose two bodies now to regain the patient sooner.</span></div><em>RELATIONSHIPS COST TIME</em></div><div class="v14-recovery-support-list"></div>';
  const list=host.querySelector('.v14-recovery-support-list');
  for(const [patientId,c] of cases){
    const patient=crewById(patientId);if(!patient)continue;const a=assignmentFor(patientId),row=document.createElement('div');row.className='v14-recovery-support-row';
    if(a){
      row.innerHTML=`<div class="v14-recovery-support-copy"><strong>${patient.name} + ${a.helperName}</strong><span>RECOVERY DETAIL · ${a.bonded?'BONDED':'STRAINED'} · ${a.relationship}</span><small>Patient due Day ${c.dueDay} · helper locked to RESERVE${a.strained?' · helper LOY -1 on successful recovery':''}</small></div>`;
    }else{
      const rem=Math.max(0,Number(c.dueDay)-(Game.day||1)),choices=supportCandidates(patient);
      if(rem<=1){row.innerHTML=`<div class="v14-recovery-support-copy"><strong>${patient.name}</strong><span>FINAL RECOVERY DAY</span><small>No crew assignment can shorten the remaining time.</small></div>`}
      else if(!choices.length){row.innerHTML=`<div class="v14-recovery-support-copy"><strong>${patient.name}</strong><span>NO ELIGIBLE ACTIVE SUPPORTER</span><small>Requires LOY 3+, or LOY 2+ with a shared faction/contact bond, Loyal trait, or veteran trust.</small></div>`}
      else{
        row.innerHTML=`<div class="v14-recovery-support-copy"><strong>${patient.name}</strong><span>ASSIGN RECOVERY PARTNER · CUT 1 DAY</span><small class="v14-recovery-support-consequence"></small></div><div class="v14-recovery-support-actions"><select aria-label="Choose recovery partner for ${patient.name}"></select><button class="btn small">ASSIGN SUPPORT · -1 DAY</button></div>`;
        const sel=row.querySelector('select'),note=row.querySelector('.v14-recovery-support-consequence'),btn=row.querySelector('button');
        choices.forEach(x=>{const op=document.createElement('option');op.value=x.id;op.textContent=`${x.u.name} · LOY ${x.loyalty>=0?'+':''}${x.loyalty} · ${x.bonded?'BONDED':'STRAINED'} · ${x.reason}`;sel.appendChild(op)});
        const update=()=>{const x=choices.find(v=>v.id===sel.value)||choices[0];note.textContent=x.strained?`${x.u.name} also leaves ACTIVE duty · strained pairing costs -1 LOY when recovery completes.`:`${x.u.name} also leaves ACTIVE duty · bonded pairing has no loyalty cost.`};sel.addEventListener('change',update);update();
        btn.addEventListener('click',()=>{if(assignSupport(patientId,sel.value)){renderSupport();window.renderCompanyPanelV135?.();window.updateOverworldHUD?.()}});
      }
    }
    list.appendChild(row);
  }
  const foot=panel.querySelector('.v14-recovery-foot');if(foot)foot.insertAdjacentElement('beforebegin',host);else panel.appendChild(host);return host;
}
function normalizeAndPersist(){const r=normalizeSupport();if(r.changed)window.saveGame?.(0,true);return r}

const priorSafehouse=window.openSafehouse;
if(typeof priorSafehouse==='function'){const wrapped=function(){normalizeAndPersist();const r=priorSafehouse.apply(this,arguments);try{renderSupport()}catch(e){console.warn('[v14 recovery bonds] safehouse',e)}return r};window.openSafehouse=wrapped;try{openSafehouse=wrapped}catch(e){}}
const priorBriefing=window.showMissionBriefingV10;
if(typeof priorBriefing==='function'){const wrapped=function(m){normalizeAndPersist();const r=priorBriefing.apply(this,arguments);try{decorateBriefing()}catch(e){console.warn('[v14 recovery bonds] briefing',e)}return r};window.showMissionBriefingV10=wrapped;try{showMissionBriefingV10=wrapped}catch(e){}}
const priorCombat=window.createCombatUnits;
if(typeof priorCombat==='function'){const wrapped=function(){normalizeAndPersist();return priorCombat.apply(this,arguments)};window.createCombatUnits=wrapped;try{createCombatUnits=wrapped}catch(e){}}
const priorAdvance=window.advanceTime;
if(typeof priorAdvance==='function'){const wrapped=function(){const r=priorAdvance.apply(this,arguments);normalizeAndPersist();return r};window.advanceTime=wrapped;try{advanceTime=wrapped}catch(e){}}
const priorProcess=window.processRecoveryV14;
if(typeof priorProcess==='function'){window.processRecoveryV14=function(){const r=priorProcess.apply(this,arguments);normalizeAndPersist();return r}}
const priorLoad=window.loadGame;
if(typeof priorLoad==='function'){const wrapped=function(){const r=priorLoad.apply(this,arguments);setTimeout(()=>{try{normalizeAndPersist()}catch(e){console.warn('[v14 recovery bonds] load',e)}},0);return r};window.loadGame=wrapped;try{loadGame=wrapped}catch(e){}}
const priorCompany=window.renderCompanyPanelV135;
if(typeof priorCompany==='function'){window.renderCompanyPanelV135=function(){normalizeAndPersist();return priorCompany.apply(this,arguments)}}

function runDiagnosticsRecoverySupportV14(){
  const rows=[],add=(name,ok,details='')=>rows.push({name,ok:!!ok,details});
  try{
    const s=state();add('support state',s.version===1&&!!s.assignments);add('recovery integration',typeof window.ensureRecoveryNetworkV14==='function');add('relationship gate',MIN_BONDED_LOYALTY===2&&MIN_DUTY_LOYALTY===3);add('assignment api',typeof window.assignRecoverySupportV14==='function');add('mission exclusion hook',window.createCombatUnits===createCombatUnits);add('schema nested persistence',!!companyState().recoverySupportV14);
  }catch(e){add('exception',false,e.message)}
  return{version:VERSION,passed:rows.filter(x=>x.ok).length,total:rows.length,results:rows};
}
Object.assign(window,{ensureRecoverySupportV14:state,recoverySupportCandidatesV14:supportCandidates,recoverySupportAssignmentV14:assignmentFor,assignRecoverySupportV14:assignSupport,normalizeRecoverySupportV14:normalizeSupport,renderRecoverySupportV14:renderSupport,runDiagnosticsRecoverySupportV14});
window.ChromeRequiem=window.ChromeRequiem||{};window.ChromeRequiem.modules=Object.assign(window.ChromeRequiem.modules||{},{RecoverySupportV14:{version:VERSION,diagnostics:runDiagnosticsRecoverySupportV14}});
try{normalizeSupport()}catch(e){console.warn('[v14 recovery bonds] init',e)}
})();}
