from pathlib import Path
import sys

ROOT=Path(sys.argv[1]).resolve()

JS=r'''if(typeof window!=='undefined'){
((root)=>{
'use strict';
const ARC='reconciliation_window_v14';
const SOURCE_ARC='quiet_census_v14';
const DISTRICT_ID='helix_financial';
const LOCATION_ID='loc_helix_hidden_1';
const CONTRACTOR=Object.freeze({id:'quiet_census',name:'QUIET CENSUS CIVIC ANALYTICS'});
const SOURCE_CLASSES=Object.freeze(['clinic_intake','freight_movement','union_discipline','debt_history']);
const ACCESS=Object.freeze({
  quiet_census_clean_access:Object.freeze({key:'authenticated_ghost',label:'AUTHENTICATED GHOST',evidence:1,minutes:10,followHeat:2,burnHeat:-4,branch:'civic',detail:'A dead municipal vendor identity still authenticates against the Annex. It is quiet access, but the proof it exposes is mostly internal.'}),
  quiet_census_exception_key:Object.freeze({key:'exception_channel',label:'EXCEPTION CHANNEL',evidence:3,minutes:6,followHeat:6,burnHeat:-1,branch:'civic',detail:'The copied exception signature opens a privileged reconciliation rail. It exposes the cleanest ledger evidence and wakes the strongest audit trail.'}),
  quiet_census_chain_of_custody:Object.freeze({key:'custody_claim',label:'CUSTODY CLAIM',evidence:2,minutes:15,followHeat:3,burnHeat:-2,branch:'market',detail:'Broker attestation lets the crew force a neutral-market provenance dispute into the settlement queue. Slow, defensible and hard to quietly erase.'}),
  quiet_census_public_proof:Object.freeze({key:'purge_window',label:'PURGE WINDOW',evidence:2,minutes:5,followHeat:8,burnHeat:2,branch:'market',purge:true,detail:'Quiet Census already knows the settlement nonce is public. The Annex is moving records now; urgency is measured in committed action time, not a wall-clock countdown.'})
});

const state=()=>root.ChromeRequiemCoreV5?.state||(typeof Game!=='undefined'?Game:root.Game);
const clamp=(v,a=0,b=100)=>Math.max(a,Math.min(b,Number(v)||0));
const journal=()=>{const game=state();if(!game)return[];if(!Array.isArray(game.journal))game.journal=[];return game.journal};
const sourceOutcome=()=>journal().find(j=>j?.narrativeKey===SOURCE_ARC&&j.quietCensusStage==='outcome'&&j.nextHook==='quiet_census_reconciliation_window'&&ACCESS[j.nextModifier])||null;
const sourceKey=()=>sourceOutcome()?.sourceMissionId||null;
const leadId=(sourceMissionId)=>`reconciliation_window_lead_${sourceMissionId}`;
const choiceId=(sourceMissionId)=>`reconciliation_window_choice_${sourceMissionId}`;
const outcomeId=(sourceMissionId)=>`reconciliation_window_outcome_${sourceMissionId}`;
const record=(id)=>journal().find(j=>j?.id===id)||null;
const choice=()=>{const key=sourceKey();return key?record(choiceId(key)):null};
const resolution=()=>{const key=sourceKey();return key?record(outcomeId(key)):null};
const accessProfile=()=>ACCESS[sourceOutcome()?.nextModifier]||null;

function revealLocation(id){
  const game=state();if(!game)return false;game.cityLife=game.cityLife||{};game.cityLife.discovered=game.cityLife.discovered||{};
  const was=!!game.cityLife.discovered[id];game.cityLife.discovered[id]=true;return !was;
}
function ensureLead(){
  const game=state(),src=sourceOutcome(),profile=accessProfile();if(!game||!src||!profile)return null;
  const key=src.sourceMissionId;if(!key)return null;
  const existing=record(leadId(key));if(existing){revealLocation(LOCATION_ID);return existing}
  const unlocked=revealLocation(LOCATION_ID);
  const entry={
    id:leadId(key),type:'side',title:'Reconciliation Window',status:'Reach Settlement Vault Annex',
    narrativeKey:ARC,reconciliationStage:'lead',sourceMissionId:key,sourceOutcomeId:src.id,day:game.day,
    branch:src.branch,allyContactId:src.allyContactId,priorLeverage:src.leverage,accessModifier:src.nextModifier,
    accessKey:profile.key,districtId:DISTRICT_ID,locationId:LOCATION_ID,contractorId:CONTRACTOR.id,
    locationUnlocked:unlocked?LOCATION_ID:null,
    desc:'Quiet Census closes its behavioral-identity accounts through a restricted Helix settlement room. The next reconciliation run is the first place the crew can separate the contractor’s payment principal from the live source map feeding it.'
  };
  journal().unshift(entry);
  root.logMsg?.(`RECONCILIATION WINDOW // Settlement Vault Annex exposed through ${profile.label}.`,'sys');
  root.saveGame?.(0,true);
  return entry;
}
function lead(){
  const key=sourceKey();if(!key||choice()||resolution())return null;
  return record(leadId(key))||ensureLead();
}
function locationPoint(){
  const game=state();if(!game)return null;const world=root.generateDistrictV133?.(DISTRICT_ID),p=world?.locations?.[LOCATION_ID];
  return p?{x:p.x,y:p.y,districtId:DISTRICT_ID,locationId:LOCATION_ID}:null;
}
function atTarget(){
  const game=state(),p=locationPoint(),player=game?.ovPlayer;if(!game||!p||!player)return false;
  if(game.districtWorldsV133?.activeId!==DISTRICT_ID)return false;
  if(game.cityLife?.currentLocation!==LOCATION_ID)return false;
  if(!Number.isFinite(player.x)||!Number.isFinite(player.y))return false;
  return Math.abs(player.x-p.x)+Math.abs(player.y-p.y)<=2;
}
function adjustHeat(delta){
  const game=state();if(!game)return 0;game.heat=game.heat&&typeof game.heat==='object'?game.heat:{};
  const before=clamp(game.heat.meridian);game.heat.meridian=clamp(before+delta);return game.heat.meridian-before;
}
function advance(minutes){if(typeof root.advanceTime==='function')root.advanceTime(minutes)}
function decisionAvailable(decision){
  const game=state();return !!game&&['follow_principal','burn_source_map'].includes(decision)&&!game.activeMission&&!!lead()&&atTarget()&&!choice()&&!resolution();
}
function evidenceAfter(profile,decision){
  if(decision==='follow_principal')return profile.evidence;
  if(['custody_claim','purge_window'].includes(profile.key))return profile.evidence;
  return Math.max(1,profile.evidence-1);
}
function outcomeText(profile,decision){
  if(decision==='follow_principal'){
    if(profile.key==='purge_window')return 'The purge queue loses one settlement token before the record movers can close it. The token points past Quiet Census toward a still-blind principal, but the live source map survives the night: clinic intake, freight movement, labor discipline and debt histories remain addressable.';
    if(profile.key==='exception_channel')return 'The exception rail exposes the cleanest settlement token in the room. The crew preserves it instead of touching the source index. Quiet Census now has an audit scar to follow, and the people represented by the index remain legible to the system.';
    if(profile.key==='custody_claim')return 'The broker chain forces a provenance hold long enough to preserve the principal-side settlement token. The evidence can travel outside Helix, but the live source map remains intact while the dispute exists.';
    return 'The municipal ghost passes as a forgotten vendor and lifts one principal-side settlement token without opening the source index. The trace is thin and quiet. So is the decision to leave Quiet Census’s map of people alive.';
  }
  if(profile.key==='purge_window')return 'The crew uses the active purge against its owner, poisoning the live source pointers before the movers can export them. Public broker witnesses still prove Quiet Census existed, but the clean payment trail dies with the map.';
  if(profile.key==='custody_claim')return 'The custody claim keeps the broker-attested evidence package intact while the crew invalidates the source pointers inside Helix. Quiet Census remains provable; the direct route from its settlement token to the principal does not.';
  if(profile.key==='exception_channel')return 'The exception key reaches the source index at privileged depth. The crew burns the addressability layer and leaves the contractor ledger scar behind. The best principal token becomes collateral damage.';
  return 'The dead vendor identity signs one last legitimate-looking correction: the source map is deauthorized from inside its own civic trust chain. Quiet Census keeps a paper shadow, but its mapped people stop resolving cleanly to the system.';
}
function resolve(decision){
  const game=state(),entry=lead(),src=sourceOutcome(),profile=accessProfile();if(!game||!entry||!src||!profile||!decisionAvailable(decision))return false;
  const key=entry.sourceMissionId;if(record(choiceId(key))||record(outcomeId(key)))return false;
  const follow=decision==='follow_principal';
  const picked={
    id:choiceId(key),type:'side',title:'Reconciliation Window — decision',status:follow?'Principal trace preserved':'Source map burned',
    narrativeKey:ARC,reconciliationStage:'choice',decision,sourceMissionId:key,sourceOutcomeId:src.id,day:game.day,
    branch:src.branch,allyContactId:src.allyContactId,accessModifier:src.nextModifier,accessKey:profile.key,districtId:DISTRICT_ID,locationId:LOCATION_ID,
    desc:follow?'Preserved the principal-side settlement token and left the live Quiet Census source map intact.':'Destroyed the live Quiet Census source addressability map and sacrificed the clean principal-side settlement token.'
  };
  journal().unshift(picked);
  const heatDelta=follow?profile.followHeat:profile.burnHeat;
  const minutes=profile.minutes+(follow?2:4);
  const effects={meridianHeat:adjustHeat(heatDelta),minutes};advance(minutes);
  const evidenceQuality=evidenceAfter(profile,decision),desc=outcomeText(profile,decision);
  const out={
    id:outcomeId(key),type:'side',title:follow?'Reconciliation Window — principal trace':'Reconciliation Window — source shelter',
    status:follow?'Principal token retained':'Source map deauthorized',narrativeKey:ARC,reconciliationStage:'outcome',decision,
    sourceMissionId:key,sourceOutcomeId:src.id,day:game.day,branch:src.branch,allyContactId:src.allyContactId,
    districtId:DISTRICT_ID,locationId:LOCATION_ID,contractorId:CONTRACTOR.id,contractorName:CONTRACTOR.name,
    priorLeverage:src.leverage,accessModifier:src.nextModifier,accessKey:profile.key,accessLabel:profile.label,purgeWindow:!!profile.purge,
    evidenceQuality,effects,principalTrace:follow,sourceMapBurned:!follow,sourceProtection:follow?'exposed':'hardened',
    sourceClasses:[...SOURCE_CLASSES],nextHook:follow?'quiet_census_principal_trace':'quiet_census_source_shelter',desc
  };
  journal().unshift(out);
  root.logMsg?.(follow?`RECONCILIATION WINDOW // Principal trace retained. Meridian heat ${effects.meridianHeat>=0?'+':''}${effects.meridianHeat}.`:`RECONCILIATION WINDOW // Source map burned. Meridian heat ${effects.meridianHeat>=0?'+':''}${effects.meridianHeat}.`,'good');
  root.saveGame?.(0,true);renderLocationCase();return true;
}
function accessCopy(profile,local){
  if(!local)return `Quiet Census reconciles through the Settlement Vault Annex in Helix Financial. ${profile.label} is enough to identify the access route remotely, but the crew must stand at the Annex terminal before committing an irreversible settlement action.`;
  if(profile.key==='authenticated_ghost')return 'The Annex is colder than the street and quieter than a clinic after curfew. Settlement racks print identity receipts for people who will never know they were counted. The dead municipal vendor credential turns green. One side of the ledger is a principal token; the other is a live map of clinic visits, freight shifts, labor discipline and debt.';
  if(profile.key==='exception_channel')return 'The exception key opens a privileged reconciliation rail behind the public settlement layer. Quiet Census has normalized clinic intake, freight movement, labor discipline and debt histories into addressable behavioral identities. The cleanest principal token sits beside the same index. The audit daemon is already awake.';
  if(profile.key==='custody_claim')return 'The Annex accepts Comet’s broker chain as a provenance dispute and freezes one reconciliation batch for review. That buys procedural access rather than invisibility. The contractor ledger and the live source map are both visible, but every action becomes part of a defensible chain of custody.';
  return 'The settlement room is in motion. Quiet Census is not deleting the scandal; it is exporting addressable source records before the public broker proof hardens. The purge queue exposes both the principal-side token and the live source map, but only while the crew spends action time inside the queue.';
}
function renderLocationCase(){
  const game=state(),src=sourceOutcome(),profile=accessProfile(),host=root.document?.getElementById('v13-location-panel');if(!game||!src||!profile||!host)return;
  host.querySelector('.v14-reconciliation-window')?.remove();
  if(game.cityLife?.currentLocation!==LOCATION_ID)return;
  const entry=lead(),picked=choice(),done=resolution();if(!entry&&!picked&&!done)return;
  const local=atTarget()&&!game.activeMission,section=root.document.createElement('section');section.className=`v14-reconciliation-window ${profile.branch} ${profile.purge?'purge':''}`;
  if(entry){
    section.innerHTML=`<div class="v14-rw-kicker">QUIET CENSUS // HELIX SETTLEMENT</div><h3>RECONCILIATION WINDOW</h3><p>${accessCopy(profile,local)}</p><div class="v14-rw-facts"><span>ACCESS // ${profile.label}</span><span>EVIDENCE // ${profile.evidence}/3</span><span>ACTION TIME // ${profile.minutes}M+</span><span>${profile.purge?'STATE // PURGE ACTIVE':local?'STATE // RECONCILIATION OPEN':'ACCESS // PHYSICAL'}</span></div>`;
    const actions=root.document.createElement('div');actions.className='v14-rw-actions';
    const options=[
      ['follow_principal','FOLLOW THE PRINCIPAL','Preserve the principal-side settlement token. Gain the cleanest route toward whoever pays Quiet Census, but leave the live source map addressable.'],
      ['burn_source_map','BURN THE SOURCE MAP','Deauthorize the map of patients, workers, debtors and contacts. Protect those sources now, but destroy the cleanest path toward the principal.']
    ];
    for(const [decision,label,detail] of options){const b=root.document.createElement('button');b.type='button';b.className='v14-rw-choice';b.disabled=!local;b.innerHTML=`<strong>${label}</strong><small>${detail}${!local?' · Reach the physical Annex marker first.':''}</small>`;b.addEventListener('click',()=>resolve(decision));actions.appendChild(b)}
    section.appendChild(actions);
  }else if(done){
    section.innerHTML=`<div class="v14-rw-kicker">SETTLEMENT RECORD // CLOSED</div><h3>${done.principalTrace?'PRINCIPAL TRACE RETAINED':'SOURCE MAP BURNED'}</h3><p>${done.desc}</p><div class="v14-rw-facts"><span>ACCESS // ${done.accessLabel}</span><span>EVIDENCE // ${done.evidenceQuality}/3</span><span>SOURCES // ${done.sourceProtection.toUpperCase()}</span><span>NEXT // ${done.principalTrace?'BLIND PRINCIPAL TRACE':'CITY SOURCE SHELTER'}</span></div>`;
  }else{
    section.innerHTML='<div class="v14-rw-kicker">SETTLEMENT RECORD // COMMITTING</div><h3>RECONCILIATION WINDOW</h3><p>The Annex decision is already committed. Reopen the location after city state settles.</p>';
  }
  host.appendChild(section);
}
function bindLocationCard(){
  const card=root.document?.querySelector?.(`#v13-locations [data-l="${LOCATION_ID}"]`);if(!card||card.dataset.rwBound==='1')return;
  card.dataset.rwBound='1';card.addEventListener('click',()=>setTimeout(renderLocationCase,0));
}
function afterDistrictRender(){ensureLead();renderLocationCase();bindLocationCard()}
const previousDistrict=root.renderDistrictHubV13;
if(typeof previousDistrict==='function')root.renderDistrictHubV13=function(){ensureLead();const result=previousDistrict.apply(this,arguments);afterDistrictRender();return result};
const previousOpenCity=root.openCityLifeV13;
if(typeof previousOpenCity==='function')root.openCityLifeV13=function(){ensureLead();const result=previousOpenCity.apply(this,arguments);afterDistrictRender();return result};
const previousDossier=root.renderContactDossierV13;
if(typeof previousDossier==='function')root.renderContactDossierV13=function(){const result=previousDossier.apply(this,arguments);ensureLead();return result};
root.CR14ReconciliationWindowV14=Object.freeze({
  arc:ARC,sourceArc:SOURCE_ARC,districtId:DISTRICT_ID,locationId:LOCATION_ID,contractor:CONTRACTOR,access:ACCESS,sourceClasses:SOURCE_CLASSES,
  sourceOutcome,accessProfile,ensureLead,lead,choice,resolution,locationPoint,atTarget,decisionAvailable,resolve,renderLocationCase,
  ids:Object.freeze({lead:leadId,choice:choiceId,outcome:outcomeId})
});
})(globalThis);
}'''

CSS=r'''#v13-location-panel .v14-reconciliation-window{margin-top:12px;padding:14px;border:1px solid rgba(118,178,199,.3);border-left:3px solid #7cb8cc;background:linear-gradient(135deg,rgba(10,24,31,.95),rgba(5,11,16,.99));box-shadow:0 14px 34px rgba(0,0,0,.28)}
#v13-location-panel .v14-reconciliation-window.market{border-color:rgba(196,183,150,.28);border-left-color:#c3b38d;background:linear-gradient(135deg,rgba(27,25,20,.94),rgba(6,12,16,.99))}
#v13-location-panel .v14-reconciliation-window.purge{box-shadow:inset 0 0 0 1px rgba(211,111,94,.13),0 14px 34px rgba(0,0,0,.3)}
#v13-location-panel .v14-rw-kicker{margin:0 0 7px;color:#86bed1;font:760 8.5px/1.3 system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase}
#v13-location-panel .v14-reconciliation-window.market .v14-rw-kicker{color:#c3b38d}
#v13-location-panel .v14-reconciliation-window h3{margin:0 0 7px;color:#edf4f5;font:800 15px/1.18 Orbitron,system-ui,sans-serif;letter-spacing:.05em;overflow-wrap:anywhere}
#v13-location-panel .v14-reconciliation-window p{margin:0 0 10px;color:#becdd1;font:560 10.7px/1.52 system-ui,sans-serif;overflow-wrap:anywhere}
#v13-location-panel .v14-rw-facts{display:flex;flex-wrap:wrap;gap:5px;margin:0 0 10px}
#v13-location-panel .v14-rw-facts span{padding:4px 6px;border:1px solid rgba(133,181,196,.17);background:rgba(3,10,14,.6);color:#a8bac0;font:720 7.8px/1.25 Orbitron,system-ui,sans-serif;letter-spacing:.04em;overflow-wrap:anywhere}
#v13-location-panel .v14-rw-actions{display:grid;grid-template-columns:1fr;gap:7px}
#v13-location-panel .v14-rw-choice{width:100%;min-width:0;min-height:48px;display:grid;gap:4px;padding:10px 11px;text-align:left;white-space:normal;border:1px solid rgba(132,183,199,.28);background:rgba(7,17,22,.96);color:#edf3f4;cursor:pointer}
#v13-location-panel .v14-rw-choice:hover:not(:disabled){border-color:#9bd2e3;background:rgba(13,31,39,.98)}
#v13-location-panel .v14-rw-choice:disabled{opacity:.48;cursor:not-allowed}
#v13-location-panel .v14-rw-choice strong{font:780 9.4px/1.25 Orbitron,system-ui,sans-serif;letter-spacing:.045em;overflow-wrap:anywhere}
#v13-location-panel .v14-rw-choice small{color:#a9b8bc;font:560 9.6px/1.42 system-ui,sans-serif;overflow-wrap:anywhere}
@media(max-width:520px){
 #v13-location-panel .v14-reconciliation-window{padding:12px 10px}
 #v13-location-panel .v14-reconciliation-window h3{font-size:13.5px}
 #v13-location-panel .v14-reconciliation-window p{font-size:10.15px;line-height:1.47}
 #v13-location-panel .v14-rw-facts{display:grid;grid-template-columns:1fr;gap:4px}
 #v13-location-panel .v14-rw-choice{padding:10px 9px;min-height:48px}
 #v13-location-panel .v14-rw-choice small{font-size:9.35px}
}'''

js_path=ROOT/'src/narrative/reconciliation-window-v14.js'
css_path=ROOT/'src/styles/37-v14-reconciliation-window.css'
js_path.write_text(JS+'\n',encoding='utf-8')
css_path.write_text(CSS+'\n',encoding='utf-8')

manifest=ROOT/'src/bootstrap/module-manifest.js'
text=manifest.read_text(encoding='utf-8')
entry="  'narrative.reconciliationWindow':{path:'./src/narrative/reconciliation-window-v14.js',kind:'module'},"
if entry not in text:
    needle="  'narrative.quietCensus':{path:'./src/narrative/quiet-census-v14.js',kind:'module'},"
    if needle not in text: raise RuntimeError('quiet census manifest entry not found')
    text=text.replace(needle,needle+'\n'+entry,1)
order_old="'narrative.marketEyes','narrative.paperGhosts','narrative.quietCensus','visuals','runtime'"
order_new="'narrative.marketEyes','narrative.paperGhosts','narrative.quietCensus','narrative.reconciliationWindow','visuals','runtime'"
if order_new not in text:
    if order_old not in text: raise RuntimeError('narrative module order not found')
    text=text.replace(order_old,order_new,1)
manifest.write_text(text,encoding='utf-8')

build=ROOT/'tools/build_pwa11.py'
text=build.read_text(encoding='utf-8')
if "'src/narrative/reconciliation-window-v14.js'," not in text:
    needle="    'src/narrative/quiet-census-v14.js',"
    if needle not in text: raise RuntimeError('quiet census precache exclusion not found')
    text=text.replace(needle,needle+"\n    'src/narrative/reconciliation-window-v14.js',",1)
if "'src/styles/37-v14-reconciliation-window.css'," not in text:
    needle="    'src/styles/36-v14-quiet-census.css',"
    if needle not in text: raise RuntimeError('quiet census css exclusion not found')
    text=text.replace(needle,needle+"\n    'src/styles/37-v14-reconciliation-window.css',",1)
build.write_text(text,encoding='utf-8')

def insert_bundle_marker(path,after_source,new_source):
    text=path.read_text(encoding='utf-8')
    new_marker=f'/* SOURCE: {new_source} */'
    if new_marker in text:return
    marker=f'/* SOURCE: {after_source} */'
    start=text.find(marker)
    if start<0:raise RuntimeError(f'{after_source} marker not found in {path}')
    nxt=text.find('/* SOURCE:',start+len(marker))
    if nxt<0:raise RuntimeError(f'next marker after {after_source} not found')
    text=text[:nxt]+new_marker+'\n\n'+text[nxt:]
    path.write_text(text,encoding='utf-8')

insert_bundle_marker(ROOT/'src/runtime/runtime-bundle.js','src/narrative/quiet-census-v14.js','src/narrative/reconciliation-window-v14.js')
insert_bundle_marker(ROOT/'src/styles/runtime-bundle.css','src/styles/36-v14-quiet-census.css','src/styles/37-v14-reconciliation-window.css')
print('PATCHED Reconciliation Window narrative slice',ROOT)
