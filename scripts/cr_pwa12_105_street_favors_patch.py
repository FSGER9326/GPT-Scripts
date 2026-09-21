from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'work/cr103')
p=root/'src/world/living-streets-v13-4a.js'
s=p.read_text(encoding='utf-8')

old="s.actorCooldown=s.actorCooldown||{};s.stats=s.stats||{events:0,interactions:0,patrolContacts:0,contracts:0,routes:0};s.streetContracts=s.streetContracts||[];"
new=old+"s.contactFavors=s.contactFavors||{};s.contactFavorHistory=s.contactFavorHistory||{};"
if old not in s:
    raise SystemExit('state seam missing')
s=s.replace(old,new,1)

anchor='window.streetContactSupportV134=streetContactSupportV134;\n'
feature=r'''

// PWA12.105 candidate — a local contact who materially supported a won Street Clash
// now owes one persistent, physical-location Street Favor. The crew must visit the
// contact to choose between suppressing the clash aftermath or converting the favor
// into a same-district countermove contract. No new save root/schema is required.
function streetFavorPresentV134(contactId){
 const near=window.CR14MultiStageOperations?.nearContact;
 return typeof near==='function' ? !!near(contactId) : false
}
window.streetFavorPresentV134=streetFavorPresentV134;

function streetFavorStateV134(contactId){return ensureLivingStreetsStateV134().contactFavors?.[contactId]||null}
window.streetFavorStateV134=streetFavorStateV134;

function contactDefForFavorV134(contactId){return (window.V13_CONTACTS||[]).find(c=>c.id===contactId)||Game.contacts?.find(c=>c.id===contactId)||null}
function favorDistrictLabelV134(id){return districtMetaV134(id)?.name||id||'the district'}

function awardStreetFavorV134(m){
 if(!m?.v134StreetEncounter||!m.v134ContactSupport?.id)return false;
 const s=ensureLivingStreetsStateV134(),contactId=m.v134ContactSupport.id;
 if(s.contactFavorHistory[m.id])return false;
 const rel=Game.contactRelations?.[contactId];
 if(!rel?.known||Number(rel.trust||0)<20){s.contactFavorHistory[m.id]={contactId,status:'ineligible',day:Game.day};return false}
 const record={contactId,sourceMissionId:m.id,district:m.sectorId,neighborhood:m.v134StreetNeighborhood||null,targetFaction:m.targetFaction||null,actorType:m.v134StreetActorType||'gang',sourceDiff:Number(m.diff||1),earnedDay:Game.day};
 if(s.contactFavors[contactId]){
  s.contactFavorHistory[m.id]={contactId,status:'overflow',day:Game.day};
  return false
 }
 s.contactFavors[contactId]=record;
 s.contactFavorHistory[m.id]={contactId,status:'banked',day:Game.day};
 s.stats.streetFavorsEarned=(s.stats.streetFavorsEarned||0)+1;
 const def=contactDefForFavorV134(contactId),target=window.FACTIONS?.[record.targetFaction];
 addJournal?.('side','Street Favor Banked',`${def?.name||contactId} owes the crew a local favor after the clash in ${favorDistrictLabelV134(record.district)}. Visit them in person to call in cover or turn it into a countermove${target?` against ${target.name}`:''}.`);
 return true
}
window.awardStreetFavorV134=awardStreetFavorV134;

function buildStreetFavorMissionV134(contactId,favor){
 const contact=Game.contacts?.find(c=>c.id===contactId),def=contactDefForFavorV134(contactId);
 if(!contact||!def||!favor?.targetFaction||def.faction===favor.targetFaction)return null;
 const enemyMap={security:['Guard','Enforcer'],contractor:['Guard','Enforcer'],gang:['Raider','Enforcer'],hunter:['Enforcer','Sniper'],wraith:['Raider','Hacker']};
 const diff=clampV134(Math.max(2,Number(favor.sourceDiff||1)+1),1,3),enemies=[...(enemyMap[favor.actorType]||['Guard','Enforcer'])];
 if(diff>=3)enemies.push(favor.actorType==='hunter'?'Sniper':'Enforcer');
 const target=window.FACTIONS?.[favor.targetFaction],shape=favor.actorType==='security'||favor.actorType==='contractor'?'checkpoint':favor.actorType==='hunter'?'alley':(['undergrid','floodline','dock_nine'].includes(favor.district)?'underpass':'alley');
 return{id:`v134favor_${favor.sourceMissionId}`,contact:contactId,type:'bounty',objective:'bounty',name:`Countermove · ${favorDistrictLabelV134(favor.district)}`,desc:`${def.name} converts the crew's street favor into actionable work: hit ${target?.name||favor.targetFaction} on the same ground before their response hardens. The job is optional, physical, and carries ordinary faction reputation and heat consequences.`,enemies,diff,reward:360+diff*210,xp:100+diff*55,targetFaction:favor.targetFaction,factionRepGain:4+diff,factionRepLoss:{[favor.targetFaction]:-(4+diff)},sectorId:favor.district,tacticalShape:shape,v134StreetArena:shape,v134StreetFavorFollowUp:true,v134StreetFavorSource:favor.sourceMissionId,v134StreetNeighborhood:favor.neighborhood||null};
}
window.buildStreetFavorMissionV134=buildStreetFavorMissionV134;

function resolveStreetFavorV134(contactId,choice){
 const s=ensureLivingStreetsStateV134(),favor=s.contactFavors?.[contactId];
 if(!favor||Game.activeMission||!streetFavorPresentV134(contactId)||!['cover','countermove'].includes(choice))return false;
 const def=contactDefForFavorV134(contactId),history=s.contactFavorHistory[favor.sourceMissionId]||{contactId};
 if(choice==='countermove'){
  const mission=buildStreetFavorMissionV134(contactId,favor),contact=Game.contacts?.find(c=>c.id===contactId);
  if(!mission||!contact)return false;
  const already=(Game.missionHistory||[]).some(m=>m.id===mission.id)||(Game.contacts||[]).some(c=>(c.missions||[]).some(m=>m.id===mission.id));
  if(!already){contact.missions=contact.missions||[];contact.missions.unshift(mission)}
  delete s.contactFavors[contactId];
  s.contactFavorHistory[favor.sourceMissionId]={...history,status:'resolved',choice:'countermove',resolvedDay:Game.day,followUpMissionId:mission.id};
  s.stats.streetFavorsSpent=(s.stats.streetFavorsSpent||0)+1;
  addJournal?.('side','Street Favor · Countermove',`${def?.name||contactId} turned the favor into ${mission.name}, targeting ${window.FACTIONS?.[mission.targetFaction]?.name||mission.targetFaction} in ${favorDistrictLabelV134(mission.sectorId)}.`)
 }else{
  const world=currentWorldV134(),all=world?ensureNeighborhoodStateV134(world):null,h=(favor.neighborhood&&all?.[favor.neighborhood])||(world?currentNeighborhoodStateV134(world):null);
  const beforeLocal=Number(h?.localHeat||0),beforeFaction=Number(Game.heat?.[favor.targetFaction]||0);
  if(h){h.localHeat=clampV134(beforeLocal-12,0,100);h.events=(h.events||0)+1}
  Game.heat=Game.heat&&typeof Game.heat==='object'?Game.heat:{};
  if(favor.targetFaction)Game.heat[favor.targetFaction]=clampV134(beforeFaction-8,0,100);
  delete s.contactFavors[contactId];
  s.contactFavorHistory[favor.sourceMissionId]={...history,status:'resolved',choice:'cover',resolvedDay:Game.day,localHeatRemoved:beforeLocal-Number(h?.localHeat||0),factionHeatRemoved:beforeFaction-Number(Game.heat?.[favor.targetFaction]||0)};
  s.stats.streetFavorsSpent=(s.stats.streetFavorsSpent||0)+1;
  addJournal?.('side','Street Favor · Cover',`${def?.name||contactId} burned local influence to suppress the aftermath in ${favorDistrictLabelV134(favor.district)}. Street heat and ${window.FACTIONS?.[favor.targetFaction]?.short||favor.targetFaction||'target'} attention dropped.`)
 }
 updateNeighborhoodHUDV134();saveGame?.(0,true);
 window.renderContactDossierV13?.(contactId);
 return true
}
window.resolveStreetFavorV134=resolveStreetFavorV134;

function decorateStreetFavorDossierV134(contactId){
 const host=document.getElementById('v13-contracts');if(!host)return;
 host.querySelector('#v134-street-favor-card')?.remove();
 const favor=streetFavorStateV134(contactId);if(!favor)return;
 const def=contactDefForFavorV134(contactId),target=window.FACTIONS?.[favor.targetFaction],physical=streetFavorPresentV134(contactId),sameSide=!!def&&def.faction===favor.targetFaction;
 const card=document.createElement('div');card.id='v134-street-favor-card';card.className='v13-side-card';card.style.cssText='--accent:#e4ad4c;border-left:3px solid var(--accent);margin-bottom:10px';
 card.innerHTML=`<h4>STREET FAVOR // ${physical?'IN PERSON':'REMOTE LOCK'}</h4><p>${def?.name||contactId} backed the crew during the ${favorDistrictLabelV134(favor.district)} clash. This favor is one-use and tied to that physical district.</p><div class="v13-tagrow"><span>${target?.short||favor.targetFaction||'LOCAL'}</span><span>DAY ${favor.earnedDay}</span><span>${String(favor.actorType||'street').toUpperCase()}</span></div><div class="v13-actions" style="margin-top:8px"><button class="btn small" data-v134-favor="cover" ${physical?'':'disabled'}>CALL IN COVER · -12 LOCAL / -8 ${target?.short||'TARGET'} HEAT</button><button class="btn small" data-v134-favor="countermove" ${physical&&!sameSide?'':'disabled'}>TURN FAVOR INTO COUNTERMOVE</button></div><p style="opacity:.7;margin-top:6px">${!physical?`Travel to ${def?.name||'this contact'} and meet them physically to spend the favor.`:sameSide?`${def?.name||'This contact'} will hide the aftermath but will not openly commission a strike on their own faction.`:'Cover reduces immediate pursuit; countermove creates a real same-district contract with normal reputation and heat consequences.'}</p>`;
 host.prepend(card);
 card.querySelectorAll('[data-v134-favor]').forEach(b=>b.onclick=()=>resolveStreetFavorV134(contactId,b.dataset.v134Favor))
}
window.decorateStreetFavorDossierV134=decorateStreetFavorDossierV134;
'''
if anchor not in s:
    raise SystemExit('support anchor missing')
s=s.replace(anchor,anchor+feature,1)

hook="const relation=m.contact&&Game.contactRelations?.[m.contact];if(success&&relation?.known&&typeof changeContactTrustV13==='function')changeContactTrustV13(m.contact,1,'Won a street clash nearby');"
if hook not in s:
    raise SystemExit('settlement hook missing')
s=s.replace(hook,hook+"if(success)awardStreetFavorV134(m);",1)
p.write_text(s,encoding='utf-8')

cityp=root/'src/legacy/city-life-v13.js'
city=cityp.read_text(encoding='utf-8')
city_hook='\n}\nwindow.renderContactDossierV13=renderContactDossierV13;'
if city.count(city_hook)!=1:
    raise SystemExit(f'contact dossier hook count={city.count(city_hook)}')
city=city.replace(city_hook,'\n window.decorateStreetFavorDossierV134?.(id);'+city_hook,1)
cityp.write_text(city,encoding='utf-8')

print('patched faction Street Favors into',root)
