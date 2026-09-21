if(typeof window!=='undefined'){
(() => {
'use strict';
const V134B_VERSION='13.4B';
const V134B_INJURY_SEVERITY={broken_arm:'serious',concussion:'serious',leg_trauma:'light',burns:'light'};

const V134B_APPROACHES=[
 {id:'v134b_ap_front',name:'FRONT GATE',icon:'FG',desc:'Direct breach through the expected security envelope.',effect:'Alerted entry · +1 security response',mode:'front'},
 {id:'v134b_ap_forged',name:'FORGED ACCESS',icon:'ID',desc:'Walk in under a credential set good enough to survive first contact.',effect:'Clean start · security doors pre-cleared',mode:'forged'},
 {id:'v134b_ap_service',name:'SERVICE ACCESS',icon:'SV',desc:'Maintenance corridors, utility doors and cameras that can be made forgetful.',effect:'Side insertion · one hostile removed',mode:'service'},
 {id:'v134b_ap_rooftop',name:'ROOFTOP',icon:'RT',desc:'Enter above the security plan and begin with elevation advantage.',effect:'High-ground insertion · extended firing lanes',mode:'rooftop'},
 {id:'v134b_ap_undergrid',name:'UNDERGRID',icon:'UG',desc:'Come up from infrastructure nobody wants on the official floorplan.',effect:'Deep flank · reduced initial response',mode:'undergrid'},
 {id:'v134b_ap_inside',name:'INSIDE CONTACT',icon:'IC',desc:'Someone on the inside leaves the right door unlocked at the right time.',effect:'Silent insertion · two security layers bypassed',mode:'inside'}
];
window.V134B_APPROACHES=V134B_APPROACHES;

function ensureApproachStateV134B(){
 Game.contractApproachesV134B=Game.contractApproachesV134B||{};
 const s=Game.contractApproachesV134B;
 s.version=1;s.plan=s.plan||null;s.completed=s.completed||{};s.lastRivalStealDay=Number.isFinite(s.lastRivalStealDay)?s.lastRivalStealDay:0;s.stats=s.stats||{planned:0,staged:0,deployed:0,stolen:0};
 return s
}
window.ensureApproachStateV134B=ensureApproachStateV134B;

function missionDistrictV134B(m){
 if(m?.sectorId&&window.V133_DISTRICTS?.[m.sectorId])return m.sectorId;
 const c=(Game.contacts||[]).find(x=>x.id===m?.contact);if(c?.sectorId&&window.V133_DISTRICTS?.[c.sectorId])return c.sectorId;
 const cd=(window.V13_CONTACTS||[]).find(x=>x.id===m?.contact);if(cd?.sectorId&&window.V133_DISTRICTS?.[cd.sectorId])return cd.sectorId;
 return Game.districtWorldsV133?.activeId||'old_market'
}
window.missionDistrictV134B=missionDistrictV134B;

function seriousInjuryOfV134B(u){return (u?.injuries||[]).find(id=>V134B_INJURY_SEVERITY[id]==='serious')||null}
window.seriousInjuryOfV134B=seriousInjuryOfV134B;
function deployableCrewV134B(){const pool=window.activeCrewV135?window.activeCrewV135():(Game.roster||[]);return pool.filter(u=>!seriousInjuryOfV134B(u))}
function blockedCrewV134B(){const pool=window.activeCrewV135?window.activeCrewV135():(Game.roster||[]);return pool.filter(u=>!!seriousInjuryOfV134B(u))}

function missionIntelV134B(m){
 const district=missionDistrictV134B(m),rumor=(Game.rumors||[]).some(r=>r.heard||r.known),hidden=(window.V133_TRANSIT_LINKS||[]).some(l=>l.type==='hidden'&&(l.from.district===district||l.to.district===district)&&Game.districtWorldsV133?.hiddenLinks?.[l.id]);
 return{server:typeof missionIntelTierV12==='function'?missionIntelTierV12():1,rumor,hidden}
}
function contactTrustForMissionV134B(m){return m?.contact&&typeof contactTrustV13==='function'?contactTrustV13(m.contact):0}
function approachAvailabilityV134B(m,id){
 const a=V134B_APPROACHES.find(x=>x.id===id),intel=missionIntelV134B(m),classes=new Set(deployableCrewV134B().map(u=>u.className)),rep=Game.rep?.[m?.targetFaction]||0,trust=contactTrustForMissionV134B(m);
 if(!a)return{ok:false,reason:'Unknown approach'};
 if(id==='v134b_ap_front')return{ok:true,reason:'Always available'};
 if(id==='v134b_ap_forged'){
   if(classes.has('AgentEX'))return{ok:true,reason:'AgentEX credential work'};
   if(rep>=20)return{ok:true,reason:`Faction standing ${rep}`};
   if(Game.credits>=450)return{ok:true,reason:'Brokered credentials · ¢450',cost:450};
   return{ok:false,reason:'AgentEX, faction rep 20+, or ¢450'};
 }
 if(id==='v134b_ap_service'){
   if(classes.has('Hacker'))return{ok:true,reason:'Hacker access'};
   if(intel.hidden)return{ok:true,reason:'Discovered service route'};
   if(intel.server>=2)return{ok:true,reason:`Safehouse server ${intel.server}`};
   return{ok:false,reason:'Hacker, hidden route, or Server 2+'};
 }
 if(id==='v134b_ap_rooftop'){
   if(classes.has('Sniper'))return{ok:true,reason:'Sniper recon'};
   if(trust>=30)return{ok:true,reason:`Contact trust ${trust}`};
   if(intel.server>=3||intel.rumor)return{ok:true,reason:'Recon intelligence'};
   return{ok:false,reason:'Sniper, trust 30+, rumor, or Server 3+'};
 }
 if(id==='v134b_ap_undergrid'){
   if(intel.hidden)return{ok:true,reason:'Hidden route discovered'};
   if((Game.rep?.wraiths||0)>=20)return{ok:true,reason:'Wraiths rep 20+'};
   if(classes.has('Hacker')&&intel.server>=2)return{ok:true,reason:'Hacker + infrastructure intel'};
   return{ok:false,reason:'Hidden route, Wraiths rep 20+, or Hacker + Server 2+'};
 }
 if(id==='v134b_ap_inside'){
   if(trust>=35)return{ok:true,reason:`Inside contact · trust ${trust}`};
   return{ok:false,reason:'Mission contact trust 35+'};
 }
 return{ok:false,reason:'Unavailable'}
}
window.approachAvailabilityV134B=approachAvailabilityV134B;

function missionAnchorV134B(m,world){
 const defs=Object.entries(world.locations||{});if(!defs.length)return{x:Math.floor(world.w/2),y:Math.floor(world.h/2)};
 if(m?.contact){
   const ld=(window.V13_DISTRICT_LOCATIONS?.[world.id]||[]).find(x=>x.contact===m.contact);
   if(ld&&world.locations[ld.id])return world.locations[ld.id]
 }
 const h=Math.abs(hashString(`${m?.id||m?.name||'mission'}:${world.id}:anchor`));return defs[h%defs.length][1]
}
function missionApproachNodesV134B(m,world=(window.currentDistrictV133?.())){
 if(!m||!world)return[];const district=missionDistrictV134B(m);if(world.id!==district)return[];
 const anchor=missionAnchorV134B(m,world),used=new Set(),spec=[
   ['v134b_ap_front', 8,  5],['v134b_ap_forged', 5,-7],['v134b_ap_service',-9, 2],
   ['v134b_ap_rooftop',-4,-9],['v134b_ap_undergrid',-8, 8],['v134b_ap_inside', 3, 8]
 ];
 return spec.map(([id,dx,dy])=>{
   const p=window.nearestWalkableV134?.(world,anchor.x+dx,anchor.y+dy,used,38,true)||{x:anchor.x,y:anchor.y};
   used.add(`${p.x},${p.y}`);return{id,x:p.x,y:p.y,approach:V134B_APPROACHES.find(a=>a.id===id)}
 })
}
window.missionApproachNodesV134B=missionApproachNodesV134B;

function currentPlanMissionV134B(){
 const p=ensureApproachStateV134B().plan;if(!p)return null;
 for(const c of Game.contacts||[]){const m=(c.missions||[]).find(x=>x.id===p.missionId);if(m)return m}
 return p.mission||null
}
function currentPlannedNodeV134B(){
 const s=ensureApproachStateV134B(),p=s.plan,m=currentPlanMissionV134B(),world=window.currentDistrictV133?.();if(!p||!m||!world||world.id!==p.district)return null;
 return missionApproachNodesV134B(m,world).find(x=>x.id===p.approachId)||null
}
window.currentPlannedNodeV134B=currentPlannedNodeV134B;

function planMissionApproachV134B(m,approachId){
 const av=approachAvailabilityV134B(m,approachId);if(!av.ok){toast(av.reason);return false}
 if(!deployableCrewV134B().length){toast('All crew are blocked by serious injuries.');return false}
 const s=ensureApproachStateV134B();s.plan={missionId:m.id,mission:JSON.parse(JSON.stringify(m)),district:missionDistrictV134B(m),approachId,ready:false,cost:av.cost||0,plannedDay:Game.day};s.stats.planned++;
 showScreen('overworld-screen');window.initOverworldV133?.();
 if(Game.districtWorldsV133?.activeId===s.plan.district){setTimeout(()=>routeMissionApproachV134B(),60)}
 else{setTimeout(()=>{window.openStrategicCityMapV133?.();window.renderStrategicCityMapV133?.(s.plan.district);toast(`Reach ${window.V133_DISTRICTS?.[s.plan.district]?.name||s.plan.district} by physical transit.`)},70)}
 saveGame(0,true);return true
}
window.planMissionApproachV134B=planMissionApproachV134B;

function routeMissionApproachV134B(){
 const p=ensureApproachStateV134B().plan,m=currentPlanMissionV134B(),world=window.currentDistrictV133?.();if(!p||!m||!world)return false;
 if(world.id!==p.district){window.openStrategicCityMapV133?.();window.renderStrategicCityMapV133?.(p.district);return false}
 const node=currentPlannedNodeV134B();if(!node)return false;
 const d=Math.hypot(Game.ovPlayer.x-node.x,Game.ovPlayer.y-node.y);if(d<=1.5)return completeMissionApproachV134B({kind:'v134b',id:node.id});
 const path=window.findDistrictPathV133?.(Game.ovPlayer,{x:node.x,y:node.y},world);if(!path?.length){toast('No physical route to staging point.');return false}
 Game.pendingPath=path;Game._v133TravelTarget={kind:'v134b',id:node.id,label:`MISSION // ${node.approach.name}`};Game.ovCamera.follow=true;toast(`Routing to ${node.approach.name}.`);return true
}
window.routeMissionApproachV134B=routeMissionApproachV134B;

function completeMissionApproachV134B(target){
 const s=ensureApproachStateV134B(),p=s.plan,node=currentPlannedNodeV134B();if(!p||!node||target?.id!==p.approachId)return false;
 p.ready=true;p.stagedAt={x:node.x,y:node.y};s.stats.staged++;Game.pendingPath=null;Game._v133TravelTarget=null;openStageModalV134B();saveGame(0,true);return true
}
window.completeMissionApproachV134B=completeMissionApproachV134B;

function ensureV134BUI(){
 const wrap=document.querySelector('#overworld-screen .wrap');if(!wrap)return;
 if(!document.getElementById('v134b-mission-card')){const e=document.createElement('div');e.id='v134b-mission-card';wrap.appendChild(e)}
 if(!document.getElementById('v134b-stage-modal')){const e=document.createElement('div');e.id='v134b-stage-modal';e.innerHTML='<div class="v134b-stage-box" id="v134b-stage-box"></div>';wrap.appendChild(e)}
}
function updateMissionCardV134B(){
 ensureV134BUI();const e=document.getElementById('v134b-mission-card'),p=ensureApproachStateV134B().plan,m=currentPlanMissionV134B();if(!e||!p||!m){if(e)e.style.display='none';return}
 const a=V134B_APPROACHES.find(x=>x.id===p.approachId),here=Game.districtWorldsV133?.activeId===p.district;
 e.style.display='block';e.innerHTML=`<b>${p.ready?'STAGED':'MISSION APPROACH'} · ${a?.name||''}</b><span>${m.name}<br>${window.V133_DISTRICTS?.[p.district]?.name||p.district}${here?' · approach point in this district':' · physical transit required'}</span><button class="btn small" id="v134b-card-action">${p.ready?'DEPLOY':here?'ROUTE':'CITY ROUTE'}</button><button class="btn small" id="v134b-card-cancel">CANCEL</button>`;
 e.querySelector('#v134b-card-action').onclick=()=>p.ready?openStageModalV134B():here?routeMissionApproachV134B():(window.openStrategicCityMapV133?.(),window.renderStrategicCityMapV133?.(p.district));
 e.querySelector('#v134b-card-cancel').onclick=()=>{ensureApproachStateV134B().plan=null;updateMissionCardV134B();saveGame(0,true)}
}

function openStageModalV134B(){
 ensureV134BUI();const p=ensureApproachStateV134B().plan,m=currentPlanMissionV134B(),a=V134B_APPROACHES.find(x=>x.id===p?.approachId),box=document.getElementById('v134b-stage-box'),modal=document.getElementById('v134b-stage-modal');if(!p||!m||!a||!box||!modal)return false;
 const blocked=blockedCrewV134B();box.innerHTML=`<div class="v134b-approach-title">PHYSICAL STAGING COMPLETE</div><h2>${a.name}</h2><p>${m.name}<br>${a.desc}</p><div class="v134b-stage-tags"><span>${a.effect}</span><span>${deployableCrewV134B().length} DEPLOYABLE</span>${p.cost?`<span>COST ¢${p.cost}</span>`:''}</div>${blocked.length?`<div class="v134b-injury-warning">${blocked.map(u=>`${u.name}: ${INJURY_DEFS[seriousInjuryOfV134B(u)]?.name||seriousInjuryOfV134B(u)} — remains behind`).join('<br>')}</div>`:''}<div class="v134b-stage-actions"><button class="btn" id="v134b-stage-hold">HOLD</button><button class="btn primary" id="v134b-stage-deploy">▶ DEPLOY</button></div>`;
 box.querySelector('#v134b-stage-hold').onclick=()=>modal.classList.remove('open');box.querySelector('#v134b-stage-deploy').onclick=()=>{modal.classList.remove('open');launchMissionV134B()};modal.classList.add('open');return true
}
window.openStageModalV134B=openStageModalV134B;

function launchMissionV134B(){
 const s=ensureApproachStateV134B(),p=s.plan,m=currentPlanMissionV134B();if(!p?.ready||!m)return false;
 const available=deployableCrewV134B();if(!available.length){toast('No deployable crew. Treat serious injuries first.');return false}
 if(p.cost){if(Game.credits<p.cost){toast('Approach cost no longer affordable.');return false}Game.credits-=p.cost;p.cost=0}
 m.v134bApproach=p.approachId;m.v134bApproachDistrict=p.district;m.v134bStaged=true;prepareMissionApproachV134B(m);s.completed[m.id]=p.approachId;s.stats.deployed++;s.plan=null;
 try{if(typeof assignRecoveryModifierV131==='function')assignRecoveryModifierV131(m)}catch(e){}
 saveGame(0,true);
 if(typeof V10PrevStartMission==='function'){V10PrevStartMission(m);return true}
 Game.activeMission=m;setTimeout(()=>{showScreen('combat');initCombat(m)},120);return true
}
window.launchMissionV134B=launchMissionV134B;

function prepareMissionApproachV134B(m){
 if(!m||m._v134bPrepared)return m;m._v134bPrepared=true;const id=m.v134bApproach;
 m._v134bOriginalEnemies=[...(m.enemies||[])];
 if(id==='v134b_ap_front'){m.enemies=[...(m.enemies||[]),'Enforcer'];m._v134bAlert=true}
 else if(['v134b_ap_forged','v134b_ap_service','v134b_ap_undergrid','v134b_ap_inside'].includes(id)){
   if((m.enemies||[]).length>2)m.enemies=m.enemies.slice(0,-1);m._v134bAlert=false
 }else if(id==='v134b_ap_rooftop')m._v134bAlert=false;
 return m
}
window.prepareMissionApproachV134B=prepareMissionApproachV134B;

function clearTacticalCellV134B(x,y,{high=false}={}){
 const c=cellAt(x,y);if(!c)return null;c.obstacle=false;c.cover=false;c.hazard=false;c.coverDir=null;c.coverHp=0;c.coverMax=0;c.rubble=false;c.transparentObstacle=false;c.door=false;c.doorOpen=false;c.doorLocked=false;c.elevation=high?1:0;c.hazardTypeV12=null;c.hazardDamageV12=0;c.hazardStatusV12=null;c.coverTypeV12=null;c.wallTypeV12=null;
 if(c.el){c.el.classList.remove('obstacle','cover','hazard','v12-door','locked','open','v12-wall','rubble');c.el.classList.toggle('v12-high',!!high)}
 return c
}
function applyTacticalApproachV134B(m){
 const id=m?.v134bApproach;if(!id)return false;
 if(id==='v134b_ap_rooftop')[[1,2],[2,2],[1,3],[2,3]].forEach(([x,y])=>clearTacticalCellV134B(x,y,{high:true}));
 if(['v134b_ap_forged','v134b_ap_service','v134b_ap_inside'].includes(id)){
   for(const c of Game.grid||[]){if(c.door){c.doorOpen=true;c.doorLocked=false;c.obstacle=false;if(c.el){c.el.classList.add('open');c.el.classList.remove('locked','obstacle')}}}
 }
 if(id==='v134b_ap_undergrid')[[0,4],[1,4],[1,5],[2,5]].forEach(([x,y])=>clearTacticalCellV134B(x,y));
 return true
}
window.applyTacticalApproachV134B=applyTacticalApproachV134B;

function safeCombatCellV134B(x,y,used){
 for(let r=0;r<5;r++)for(let dy=-r;dy<=r;dy++)for(let dx=-r;dx<=r;dx++){
   const nx=x+dx,ny=y+dy,k=`${nx},${ny}`,c=cellAt(nx,ny);if(!c||used.has(k)||c.obstacle||c.unit)continue;used.add(k);return c
 }return null
}
function applyApproachSpawnV134B(m){
 const id=m?.v134bApproach;if(!id)return false;
 const blocked=new Set(blockedCrewV134B());for(const u of [...(Game.units||[])])if(u.team==='player'&&blocked.has(u.rosterRef)){const c=cellAt(u.x,u.y);if(c?.unit===u)c.unit=null;Game.units.splice(Game.units.indexOf(u),1)}
 const formations={
  v134b_ap_front:[[0,9],[1,9],[2,9]],
  v134b_ap_forged:[[3,9],[4,9],[5,9]],
  v134b_ap_service:[[0,6],[0,7],[1,7]],
  v134b_ap_rooftop:[[1,2],[2,2],[1,3]],
  v134b_ap_undergrid:[[0,4],[1,4],[1,5]],
  v134b_ap_inside:[[3,6],[4,6],[3,7]]
 },form=formations[id]||formations.v134b_ap_front,players=(Game.units||[]).filter(u=>u.team==='player'),used=new Set();
 for(const u of players){const oc=cellAt(u.x,u.y);if(oc?.unit===u)oc.unit=null}
 players.forEach((u,i)=>{const seed=form[i]||form[form.length-1],c=safeCombatCellV134B(seed[0],seed[1],used);if(c){u.x=c.x;u.y=c.y;c.unit=u}});
 return true
}
window.applyApproachSpawnV134B=applyApproachSpawnV134B;

function applyApproachAlertV134B(m){
 const quiet=m?.v134bApproach&&m.v134bApproach!=='v134b_ap_front';Game.alerted=!quiet;
 if(Game.objective&&quiet)Game.objective.quiet=true;
 for(const e of (Game.units||[]).filter(u=>u.team==='enemy')){e.awareness=quiet?0:100;e.alerted=!quiet}
 return quiet
}
window.applyApproachAlertV134B=applyApproachAlertV134B;

/* Tactical wrappers */
const V134BPrevBuildGrid=buildGrid;
buildGrid=function(m){prepareMissionApproachV134B(m);const r=V134BPrevBuildGrid(m);applyTacticalApproachV134B(m);return r};
const V134BPrevCreateCombatUnits=createCombatUnits;
createCombatUnits=function(m){const r=V134BPrevCreateCombatUnits(m);applyApproachSpawnV134B(m);applyApproachAlertV134B(m);return r};

/* Physical map rendering / click integration */
const V134BPrevDrawLiving=window.drawLivingStreetsV134;
window.drawLivingStreetsV134=function(ctx,world,W,H,t,hover){
 V134BPrevDrawLiving?.(ctx,world,W,H,t,hover);drawApproachNodeV134B(ctx,world,W,H,t);updateMissionCardV134B()
};
function drawApproachNodeV134B(ctx,world,W,H,t){
 const p=ensureApproachStateV134B().plan,node=currentPlannedNodeV134B();if(!p||!node||p.ready)return;
 const s=window.worldToScreen(node.x+.5,node.y+.5);if(s.x<-30||s.y<-30||s.x>W+30||s.y>H+30)return;ctx.save();ctx.translate(s.x,s.y);ctx.shadowColor='#e4ad4c';ctx.shadowBlur=14;ctx.strokeStyle='#e4ad4c';ctx.fillStyle='rgba(16,11,4,.88)';ctx.lineWidth=2;ctx.beginPath();ctx.rotate(Math.PI/4);ctx.rect(-7,-7,14,14);ctx.fill();ctx.stroke();ctx.rotate(-Math.PI/4);ctx.shadowBlur=0;ctx.fillStyle='#f2d28c';ctx.font=`800 ${Math.max(7,t*.18)}px Orbitron`;ctx.textAlign='center';ctx.fillText('M',0,3);ctx.restore()
}
function handleMissionApproachTapV134B(q){
 const n=currentPlannedNodeV134B();if(!n||ensureApproachStateV134B().plan?.ready)return false;if(Math.hypot(q.x-n.x,q.y-n.y)>1.2)return false;return routeMissionApproachV134B()
}
window.handleMissionApproachTapV134B=handleMissionApproachTapV134B;

/* Briefing integration */
const V134BPrevBriefing=showMissionBriefingV10;
showMissionBriefingV10=function(m){const r=V134BPrevBriefing(m);try{decorateBriefingV134B(m)}catch(e){console.warn('[v13.4B] briefing decorate',e)}return r};
function decorateBriefingV134B(m){
 const body=document.getElementById('v10-brief-body');if(!body)return;body.querySelector('.v134b-approach-block')?.remove();
 const blocked=blockedCrewV134B(),state=ensureApproachStateV134B(),existing=state.plan?.missionId===m.id?state.plan.approachId:null;
 const block=document.createElement('div');block.className='v134b-approach-block';block.innerHTML=`<div class="v134b-approach-title">PHYSICAL INFILTRATION APPROACH</div><div class="v134b-approach-grid"></div>${blocked.length?`<div class="v134b-injury-warning"><b>SERIOUS INJURY — NOT DEPLOYING</b><br>${blocked.map(u=>`${u.name}: ${INJURY_DEFS[seriousInjuryOfV134B(u)]?.name||seriousInjuryOfV134B(u)}`).join('<br>')}</div>`:''}`;
 const grid=block.querySelector('.v134b-approach-grid');
 V134B_APPROACHES.forEach(a=>{const av=approachAvailabilityV134B(m,a.id),b=document.createElement('button');b.className='v134b-approach'+((existing||'v134b_ap_front')===a.id?' selected':'');b.dataset.id=a.id;b.disabled=!av.ok;b.innerHTML=`<b>${a.icon} · ${a.name}</b><small>${a.desc}</small><small>${a.effect}</small><small class="${av.ok?'ok':'req'}">${av.ok?'AVAILABLE · ':'REQUIRES · '}${av.reason}</small>`;b.onclick=()=>{grid.querySelectorAll('.v134b-approach').forEach(x=>x.classList.remove('selected'));b.classList.add('selected');body.dataset.v134bApproach=a.id};grid.appendChild(b)});
 body.dataset.v134bApproach=existing||'v134b_ap_front';const actions=body.querySelector('.v10-brief-actions');actions?.insertAdjacentElement('beforebegin',block);
 const deploy=body.querySelector('#v10-brief-deploy');if(deploy){deploy.textContent='ROUTE TO APPROACH';deploy.disabled=!deployableCrewV134B().length;deploy.onclick=()=>{const id=body.dataset.v134bApproach||'v134b_ap_front';planMissionApproachV134B(m,id)}}
 const reward=body.querySelector('.v10-brief-reward');if(reward){const s=document.createElement('span'),b=document.createElement('b');s.textContent='Street Heat';b.innerHTML=`${notorietyTierV12?.().key||'SAFE'}${heatVendorPctV134B()?` <span class="v134b-heat-note">MARKET +${heatVendorPctV134B()}%</span>`:''}`;reward.appendChild(s);reward.appendChild(b)}
}
window.decorateBriefingV134B=decorateBriefingV134B;

/* Donor-mined mechanic 1: heat-priced specialist markets */
function heatVendorPctV134B(){const k=typeof notorietyTierV12==='function'?notorietyTierV12().key:'SAFE';return{SAFE:0,WATCHED:4,HUNTED:8,CONTRACT:14,BURNED:22}[k]||0}
function heatVendorMultV134B(){return 1+heatVendorPctV134B()/100}
window.heatVendorPctV134B=heatVendorPctV134B;window.heatVendorMultV134B=heatVendorMultV134B;

/* Donor-mined mechanic 2: safer Black Halo contract theft */
function stealableContractV134B(m){return !!m&&!m.isRival&&!m.isShowdown&&!m.oracleKey&&!m.actKey&&!m.storyKey&&!['rival','boss'].includes(m.type)}
function stealContractDailyV134B(force=false){
 const s=ensureApproachStateV134B();if(!force&&s.lastRivalStealDay===Game.day)return false;s.lastRivalStealDay=Game.day;
 const r=Game.rival,e=Game.rivalEconomy;if(!r||r.defeated||!e)return false;if((e.credits||0)<(Game.credits||0)*.5)return false;if(!force&&seededRandom()>=.25)return false;
 const jobs=[];(Game.contacts||[]).forEach(c=>(c.missions||[]).forEach(m=>{if(stealableContractV134B(m))jobs.push({c,m})}));
 const activeContacts=(Game.contacts||[]).filter(c=>(c.missions||[]).length);let pool=jobs.filter(j=>!(activeContacts.length===1&&j.c.missions.length===1));if(!pool.length)pool=jobs.filter(j=>j.c.missions.length>1);if(!pool.length)return false;
 const j=pool[Math.floor(seededRandom()*pool.length)];j.c.missions=j.c.missions.filter(x=>x.id!==j.m.id);e.credits=(e.credits||0)+Math.round((j.m.reward||500)*.35);r.contracts=(r.contracts||0)+1;e.history=e.history||[];e.history.unshift({d:Game.day,t:`Black Halo took "${j.m.name}" before your crew.`});e.history=e.history.slice(0,24);s.stats.stolen++;toast(`BLACK HALO took ${j.m.name}.`);addJournal('main','Contract Stolen',`Black Halo took "${j.m.name}" from ${j.c.name}.`);return true
}
window.stealContractDailyV134B=stealContractDailyV134B;

const V134BPrevAdvanceTime=advanceTime;
advanceTime=function(minutes){const oldDay=Game.day,r=V134BPrevAdvanceTime(minutes);if(Game.day!==oldDay)stealContractDailyV134B(false);return r};

/* Save/load */
const V134BPrevSerialize=serializeGame;
serializeGame=function(){const d=JSON.parse(V134BPrevSerialize());d.version=V134B_VERSION;d.contractApproachesV134B=JSON.parse(JSON.stringify(ensureApproachStateV134B()));return JSON.stringify(d)};
const V134BPrevLoad=loadGame;
loadGame=function(slot){
 let data=null;for(const p of ['chrome_requiem_v13_'+slot,'chrome_requiem_v12_'+slot,'chrome_requiem_v11_'+slot,'chrome_requiem_v10_'+slot,'chrome_requiem_v9_'+slot,'chrome_requiem_v8_'+slot,'chrome_requiem_v7_'+slot,'chrome_requiem_save_'+slot]){const raw=localStorage.getItem(p);if(raw){try{data=JSON.parse(raw)}catch(e){}break}}
 const ok=V134BPrevLoad(slot);if(ok){restoreContractApproachesV134B(data);ensureV134BUI();updateMissionCardV134B()}return ok
};
function restoreContractApproachesV134B(data){Game.contractApproachesV134B=data?.contractApproachesV134B||null;ensureApproachStateV134B()}
window.restoreContractApproachesV134B=restoreContractApproachesV134B;
const V134BPrevNew=startNewGame;
startNewGame=function(name,className,background){const r=V134BPrevNew(name,className,background);Game.contractApproachesV134B=null;ensureApproachStateV134B();ensureV134BUI();return r};

function runDiagnosticsV134B(){
 const rows=[],add=(n,ok,d='')=>rows.push({name:n,ok:!!ok,details:d});try{
   ensureApproachStateV134B();const m=(Game.contacts||[]).flatMap(c=>c.missions||[])[0]||{id:'diag',name:'Diag',sectorId:Game.districtWorldsV133?.activeId||'old_market',targetFaction:'spine',enemies:['Guard','Enforcer'],diff:1,reward:1,xp:1};
   add('6 approach definitions',V134B_APPROACHES.length===6,V134B_APPROACHES.length);add('physical approach nodes',missionApproachNodesV134B(m,window.generateDistrictV133(missionDistrictV134B(m))).length===6);
   add('approach requirements',typeof approachAvailabilityV134B==='function');add('physical routing',typeof routeMissionApproachV134B==='function');add('tactical effects',typeof applyTacticalApproachV134B==='function'&&typeof applyApproachSpawnV134B==='function');
   add('serious injury filter',typeof seriousInjuryOfV134B==='function');add('heat market pressure',heatVendorMultV134B()>=1);add('rival theft',typeof stealContractDailyV134B==='function');add('save state',!!Game.contractApproachesV134B);
   add('Living Streets retained',!!ChromeRequiem.modules?.LivingStreetsV134);add('District Worlds retained',!!ChromeRequiem.modules?.DistrictWorldsV133);add('v12 tactical retained',!!ChromeRequiem.modules?.TacticalV12)
 }catch(e){add('exception',false,e.message)}return{version:V134B_VERSION,passed:rows.filter(x=>x.ok).length,total:rows.length,results:rows}
}
window.runDiagnosticsV134B=runDiagnosticsV134B;

window.ChromeRequiem.version=V134B_VERSION;
window.ChromeRequiem.modules.ContractApproachesV134B={
 approaches:V134B_APPROACHES,ensure:ensureApproachStateV134B,availability:approachAvailabilityV134B,nodes:missionApproachNodesV134B,diagnostics:runDiagnosticsV134B
};
ensureApproachStateV134B();ensureV134BUI();
})();
}



const approachesCallV14=(name,...args)=>{
 const fn=globalThis[name];
 if(typeof fn!=='function')throw new Error(`ContractApproachesV14 missing legacy implementation: ${name}`);
 return fn(...args);
};
const ContractApproachesV14=Object.freeze({
 version:'13.4B',
 get approaches(){return globalThis.V134B_APPROACHES},
 ensureState:(...args)=>approachesCallV14('ensureApproachStateV134B',...args),
 availability:(...args)=>approachesCallV14('approachAvailabilityV134B',...args),
 nodes:(...args)=>approachesCallV14('missionApproachNodesV134B',...args),
 plan:(...args)=>approachesCallV14('planMissionApproachV134B',...args),
 prepare:(...args)=>approachesCallV14('prepareMissionApproachV134B',...args),
 route:(...args)=>approachesCallV14('routeMissionApproachV134B',...args),
 complete:(...args)=>approachesCallV14('completeMissionApproachV134B',...args),
 applyTactical:(...args)=>approachesCallV14('applyTacticalApproachV134B',...args),
 diagnostics:(...args)=>approachesCallV14('runDiagnosticsV134B',...args)
});
globalThis.ChromeRequiemV14Domains ||= {};
globalThis.ChromeRequiemV14Domains.missions ||= {};
globalThis.ChromeRequiemV14Domains.missions.approaches=ContractApproachesV14;
