(() => {
'use strict';
const VERSION = 2;
if ((window.WorkshopCalibrationV14?.version || 0) >= VERSION) return;
const PROFILE_KEY = 'weaponCalibrationV14';
let timeProcessingFault = false;
const PROFILES = Object.freeze({
  field: Object.freeze({id:'field',name:'FIELD ZERO',workshop:1,credits:80,salvage:0,minutes:60,damage:0,range:0,crit:0,desc:'Return the platform to its neutral factory/field geometry.'}),
  breach: Object.freeze({id:'breach',name:'BREACH PRESSURE',workshop:2,credits:260,salvage:2,minutes:120,damage:2,range:-1,crit:-5,desc:'+2 DMG · -1 RANGE · -5% CRIT. Close-range pressure at the cost of reach and precision.'}),
  precision: Object.freeze({id:'precision',name:'PRECISION BED',workshop:2,credits:260,salvage:2,minutes:120,damage:-1,range:1,crit:6,desc:'-1 DMG · +1 RANGE · +6% CRIT. Extends the engagement envelope at the cost of stopping power.'})
});
const AFFINITY = Object.freeze({
  breach:new Set(['redline','atlas','mako']),
  precision:new Set(['kestrel','helix','sable'])
});
function clampInt(n,lo,hi){n=Number.isFinite(Number(n))?Math.round(Number(n)):lo;return Math.max(lo,Math.min(hi,n))}
function ensureUnit(u){
  if(!u)return null;
  if(!u[PROFILE_KEY]||typeof u[PROFILE_KEY]!=='object'||Array.isArray(u[PROFILE_KEY]))u[PROFILE_KEY]={};
  for(const [weapon,value] of Object.entries(u[PROFILE_KEY]))if(!PROFILES[value]||value==='field')delete u[PROFILE_KEY][weapon];
  return u[PROFILE_KEY];
}
function currentProfileId(u,weaponKey=u?.weapon){if(!u||!weaponKey)return'field';const map=ensureUnit(u),id=map?.[weaponKey];return PROFILES[id]?id:'field'}
function currentProfile(u,weaponKey=u?.weapon){return PROFILES[currentProfileId(u,weaponKey)]}
function manufacturerOf(weaponKey){try{return String(ITEMS?.[weaponKey]?.manufacturer||ITEMS?.[weaponKey]?.mfg||ITEMS?.[weaponKey]?.brand||'').toLowerCase()}catch{return''}}
function workshopLevel(){return Math.max(1,clampInt(Game?.safehouse?.workshop||1,1,99))}
function quote(u,weaponKey,profileId){
  const p=PROFILES[profileId];if(!u||!weaponKey||!p)return null;
  const ws=workshopLevel(),mfg=manufacturerOf(weaponKey),aligned=!!AFFINITY[profileId]?.has(mfg);
  let credits=p.credits,salvage=p.salvage,minutes=p.minutes;
  if(profileId!=='field'&&aligned){credits=Math.round(credits*.85);salvage=Math.max(1,salvage-1)}
  if(ws>=4)credits=Math.round(credits*.85);
  if(ws>=3)minutes=Math.max(60,minutes-30);
  return{profile:p,workshop:ws,manufacturer:mfg,aligned,credits,salvage,minutes};
}
function applyDerived(u){
  if(!u?.weapon)return u;
  const p=currentProfile(u,u.weapon);if(p.id==='field')return u;
  u.damage=Math.max(1,Number(u.damage||1)+p.damage);
  u.range=Math.max(1,Number(u.range||1)+p.range);
  u.critChance=Math.max(0,Math.min(95,Number(u.critChance||0)+p.crit));
  return u;
}
function canRefit(u,weaponKey,profileId){
  const q=quote(u,weaponKey,profileId);if(!q)return{ok:false,reason:'Invalid calibration.'};
  if(timeProcessingFault)return{ok:false,reason:'Refit locked after a world-time processing fault. Reload before using the workshop again.'};
  if(Game?.activeMission)return{ok:false,reason:'Return from the active operation before refitting.'};
  if(currentProfileId(u,weaponKey)===profileId)return{ok:false,reason:'Calibration already installed.'};
  if(q.workshop<q.profile.workshop)return{ok:false,reason:`Workshop LV ${q.profile.workshop} required.`};
  if((Game?.credits||0)<q.credits)return{ok:false,reason:'Not enough credits.'};
  if((Game?.salvage||0)<q.salvage)return{ok:false,reason:'Not enough salvage.'};
  if(typeof advanceTime!=='function')return{ok:false,reason:'Action-time API unavailable.'};
  return{ok:true,quote:q};
}
function writeProfile(map,weaponKey,profileId){if(profileId==='field')delete map[weaponKey];else map[weaponKey]=profileId}
function setProfile(u,weaponKey,profileId){
  const check=canRefit(u,weaponKey,profileId);if(!check.ok){if(typeof toast==='function')toast(check.reason);return false}
  const q=check.quote,map=ensureUnit(u),beforeId=currentProfileId(u,weaponKey),beforeCredits=Number(Game.credits||0),beforeSalvage=Number(Game.salvage||0);
  try{
    Game.credits=beforeCredits-q.credits;Game.salvage=beforeSalvage-q.salvage;writeProfile(map,weaponKey,profileId);applySkillsToUnit(u);
  }catch(err){
    Game.credits=beforeCredits;Game.salvage=beforeSalvage;writeProfile(map,weaponKey,beforeId);try{applySkillsToUnit(u)}catch{}
    if(typeof toast==='function')toast(`Calibration failed before commit: ${err?.message||err}`);return false;
  }
  let timeError=null;
  try{advanceTime(q.minutes)}catch(err){timeError=err;console.error('Workshop calibration time processing failed',err)}
  let saveOk=true;
  try{if(typeof saveGame==='function')saveOk=saveGame(0,true)!==false}catch(err){saveOk=false;console.error('Workshop calibration save failed',err)}
  try{if(typeof updateOverworldHUD==='function')updateOverworldHUD()}catch{}
  if(timeError){timeProcessingFault=true;if(typeof toast==='function')toast(`${q.profile.name} installed; world-time processing reported an error. Workshop refits are locked until reload.`);return true}
  if(typeof toast==='function')toast(`${q.profile.name} calibrated · ¢${q.credits} · ⚙${q.salvage} · ${q.minutes}m${saveOk?'':' · SAVE WARNING'}`);
  return true;
}
function describeDelta(p){const signed=n=>`${n>0?'+':''}${n}`;if(p.id==='field')return'NEUTRAL DERIVED STATS';return`${signed(p.damage)} DMG · ${signed(p.range)} RANGE · ${signed(p.crit)}% CRIT`}
function renderPanel(body){
  if(!body||body.querySelector('.v14-calibration-panel'))return;
  const u=Game?.roster?.[Game.selectedCrewIndex]||Game?.roster?.[0];if(!u?.weapon)return;
  const weaponKey=u.weapon,active=currentProfile(u,weaponKey),panel=document.createElement('section');
  panel.className='v11-bench v14-calibration-panel';
  panel.innerHTML=`<div class="v14-cal-head"><div><b>WORKSHOP CALIBRATION</b><span>${active.name}</span></div><small>LV ${workshopLevel()} · mutually exclusive refit</small></div><div class="v14-cal-grid">${Object.values(PROFILES).map(p=>{const q=quote(u,weaponKey,p.id),c=canRefit(u,weaponKey,p.id),current=p.id===active.id;return`<article class="v14-cal-card ${current?'active':''}"><h5>${p.name}${q.aligned?' · MFG FIT':''}</h5><div class="v14-cal-delta">${describeDelta(p)}</div><p>${p.desc}</p><div class="v14-cal-cost">¢${q.credits} · ⚙${q.salvage} · ${q.minutes}m · WS${p.workshop}</div><button class="btn small" data-cal-profile="${p.id}" ${c.ok?'':'disabled'}>${current?'INSTALLED':'REFIT'}</button></article>`}).join('')}</div>`;
  panel.querySelectorAll('[data-cal-profile]').forEach(btn=>{btn.onclick=()=>{if(setProfile(u,weaponKey,btn.dataset.calProfile)&&typeof renderCrewScreen==='function')renderCrewScreen()}});
  body.appendChild(panel);
}
const previousApply=applySkillsToUnit;
applySkillsToUnit=function workshopCalibrationApply(u){const result=previousApply(u);ensureUnit(u);applyDerived(u);return result};
window.applySkillsToUnit=applySkillsToUnit;
const previousBench=typeof renderWeaponBenchV11==='function'?renderWeaponBenchV11:null;
if(previousBench){renderWeaponBenchV11=function workshopCalibrationBench(body){previousBench(body);renderPanel(body)};window.renderWeaponBenchV11=renderWeaponBenchV11}
for(const u of Game?.roster||[])ensureUnit(u);
function diagnostics(){
  const synthetic={weapon:'test',weaponCalibrationV14:{test:'breach'},damage:10,range:5,critChance:20};
  const itemKey=typeof ITEMS==='object'?Object.keys(ITEMS).find(k=>ITEMS[k]?.type==='weapon'):null,itemBefore=itemKey?JSON.stringify(ITEMS[itemKey]):null;
  applyDerived(synthetic);const itemStable=!itemKey||JSON.stringify(ITEMS[itemKey])===itemBefore;
  const old={weapon:'test'};ensureUnit(old);const malformed={weapon:'test',weaponCalibrationV14:{test:'field',ghost:'invalid'}};ensureUnit(malformed);
  const rows=[
    ['profiles mutually exclusive',Object.keys(PROFILES).length===3],
    ['legacy default is field',currentProfileId(old,'test')==='field'],
    ['field and invalid entries normalize away',Object.keys(malformed.weaponCalibrationV14).length===0],
    ['breach arithmetic',synthetic.damage===12&&synthetic.range===4&&synthetic.critChance===15],
    ['precision is non-dominant',PROFILES.precision.damage<0&&PROFILES.precision.range>0&&PROFILES.precision.crit>0],
    ['base item definition unchanged',itemStable],
    ['single authoritative calibration field',!Object.prototype.hasOwnProperty.call(synthetic,'calibrationProfileV14')],
    ['schema additive roster state',!!old.weaponCalibrationV14&&typeof old.weaponCalibrationV14==='object']
  ].map(([name,ok])=>({name,ok:!!ok}));return rows;
}
window.runDiagnosticsV14Calibration=()=>{const results=diagnostics();return{version:VERSION,passed:results.filter(x=>x.ok).length,total:results.length,results}};
window.WorkshopCalibrationV14=Object.freeze({version:VERSION,profiles:PROFILES,quote,currentProfileId,canRefit,setProfile,applyDerived,renderPanel,ensureUnit,isTimeFaulted:()=>timeProcessingFault});
})();
