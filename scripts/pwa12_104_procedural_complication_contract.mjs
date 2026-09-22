import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';

const modulePath=process.argv[2];
if(!modulePath) throw new Error('usage: node pwa12_104_procedural_complication_contract.mjs <procedural-complications-v14.js>');
const src=fs.readFileSync(modulePath,'utf8');
const profiles={dock_nine:{security:2},undergrid:{security:1},glass_heights:{security:5},old_market:{security:3},civic_circuit:{security:4}};
const Game={day:1,contacts:[],contactRelations:{},credits:10000,rep:{},safehouse:{server:1},serverTier:1,units:[],objective:{quiet:true},contractApproachesV134B:{plan:null}};
const box={console,Game,V12_TACTICAL_PROFILES:profiles,saveCount:0,
  generatedContactContractV137:m=>!!m?.generated,
  multiStageConflictV139:m=>!!m?.multiStage,
  applyApproachAlertV134B:()=>true,
  createCombatUnits:m=>m,
  contactTrustV13:id=>Number(Game.contactRelations?.[id]?.trust||0),
  missionIntelTierV12:()=>Number(Game.serverTier||1),
  saveGame:()=>{box.saveCount++},toast:()=>{},logMsg:()=>{}};
box.window=box;
vm.createContext(box);
vm.runInContext(src,box,{filename:'procedural-complications-v14.js'});
assert.equal(box.ChromeRequiem.modules.ProceduralComplicationsV140.metaVersion,1);

const objectives=['eliminate','bounty','raid','breach','sabotage','steal','secure','rescue','extract','heist'];
const targets=['meridian','wraiths','iron','chrome','spine'];
const sectors=Object.keys(profiles);
const norm=x=>JSON.parse(JSON.stringify(x));
let total=0,enabled=0,disabled=0;const chances=new Set(),kinds=new Set();let sample=null;
for(let si=0;si<sectors.length;si++)for(let oi=0;oi<objectives.length;oi++)for(let ti=0;ti<targets.length;ti++)for(let diff=1;diff<=5;diff++){
  const sector=sectors[si],objective=objectives[oi],target=targets[ti],id=`qa_${si}_${oi}_${ti}_${diff}`;
  const contact={id:`c_${si}`,sectorId:sector,faction:'meridian',missions:[]};
  const base={id,generated:true,contact:contact.id,sectorId:sector,objective,type:objective,targetFaction:target,diff,enemies:['Guard','Enforcer','Guard'],reward:900+diff*100,xp:110+diff*5,v137ContractComposition:{seed:100000+total}};
  const m=norm(base),q=box.assignComplicationV140(m,contact,7,oi);total++;assert(q,'metadata missing');
  const m2=norm(base),q2=box.assignComplicationV140(m2,contact,7,oi);assert.equal(JSON.stringify(norm(q)),JSON.stringify(norm(q2)),'determinism failure');
  assert.equal(m.reward,base.reward);assert.equal(m.xp,base.xp);assert.deepEqual(m.enemies,base.enemies);assert.equal(m.objective,base.objective);assert.equal(m.targetFaction,base.targetFaction);
  assert(q.chance>=28&&q.chance<=52,q);chances.add(q.chance);
  if(q.enabled){enabled++;kinds.add(q.kind);assert(q.mitigationCost>=70&&q.mitigationCost<=180,q);sample??={m,contact};}else disabled++;
}
assert.equal(total,1250);assert(enabled>0&&disabled>0,{enabled,disabled});assert(chances.size>=10,[...chances]);assert.equal(kinds.size,4,[...kinds]);

const authored={id:'authored',generated:false,objective:'raid',type:'raid',enemies:['a','b'],reward:900,xp:100};
assert.equal(box.assignComplicationV140(authored,{id:'c'},1,0),null);assert(!authored.v140Complication);
const multi={id:'multi',generated:true,multiStage:true,objective:'heist',type:'heist',enemies:['a','b','c'],reward:1200,xp:100,targetFaction:'spine',sectorId:'glass_heights'};
const mq=box.assignComplicationV140(multi,{id:'c',sectorId:'glass_heights'},1,0);assert.equal(mq.enabled,false);assert.equal(mq.reason,'INELIGIBLE');
const unsupported={id:'unsupported',generated:true,objective:'escort',type:'escort',enemies:['a','b'],reward:800,xp:90,targetFaction:'iron',sectorId:'old_market'};
assert.equal(box.assignComplicationV140(unsupported,{id:'c',sectorId:'old_market'},1,0).enabled,false);
assert(sample,'no enabled sample');

const persisted=norm(sample.m);persisted.v140Complication.runtimeTriggered=true;persisted.v140Complication.runtimeApproach='v134b_ap_service';persisted.v140Complication.runtimeDay=9;
Game.contacts=[{...sample.contact,missions:[persisted]}];const durable=norm(persisted.v140Complication);box.resetComplicationRuntimeV140();const after=persisted.v140Complication;
assert.equal(after.seed,durable.seed);assert.equal(after.kind,durable.kind);assert.equal(after.enabled,durable.enabled);assert(!('runtimeTriggered'in after)&&!('runtimeApproach'in after)&&!('runtimeDay'in after));
const serialized=JSON.parse(JSON.stringify(persisted));const replay=box.assignComplicationV140(serialized,sample.contact,99,99);assert.equal(replay.seed,after.seed);assert.equal(replay.kind,after.kind);

const mit=norm(sample.m);mit.v140Complication.mitigated=false;mit.v140Complication.mitigationPaid=0;Game.contractApproachesV134B.plan=null;Game.activeMission=null;Game.credits=10000;
const cost=mit.v140Complication.mitigationCost,beforeCredits=Game.credits;assert.equal(box.mitigateComplicationV140(mit),true);assert.equal(Game.credits,beforeCredits-cost);const once=Game.credits;assert.equal(box.mitigateComplicationV140(mit),true);assert.equal(Game.credits,once);
const locked=norm(sample.m);locked.v140Complication.mitigated=false;locked.v140Complication.mitigationPaid=0;locked.v134bStaged=true;Game.credits=10000;const lockedCash=Game.credits;assert.equal(box.mitigateComplicationV140(locked),false);assert.equal(Game.credits,lockedCash);

const quiet=norm(sample.m);quiet.v140Complication.mitigated=false;quiet.v134bApproach='v134b_ap_service';Game.activeMission=quiet;Game.alerted=false;Game.objective={quiet:true};Game.units=[{team:'enemy',awareness:0,alerted:false},{team:'enemy',awareness:0,alerted:false}];
assert.equal(box.applyComplicationRuntimeV140(quiet),true);assert.equal(Game.alerted,true);assert.equal(Game.objective.quiet,false);assert(Game.units.every(x=>x.awareness===100&&x.alerted));assert.equal(quiet.v140Complication.runtimeTriggered,true);
const front=norm(sample.m);front.v140Complication.mitigated=false;front.v134bApproach='v134b_ap_front';Game.activeMission=front;Game.alerted=false;Game.objective={quiet:false};Game.units=[{team:'enemy',awareness:100,alerted:true}];
assert.equal(box.applyComplicationRuntimeV140(front),false);assert.equal(Game.alerted,false);

const intel=norm(sample.m);Game.contacts=[{...sample.contact,missions:[intel]}];Game.contactRelations[sample.contact.id]={trust:0};Game.serverTier=1;assert.equal(box.complicationIntelV140(intel,sample.contact).tier,0);Game.serverTier=2;Game.contactRelations[sample.contact.id].trust=20;assert.equal(box.complicationIntelV140(intel,sample.contact).tier,1);Game.serverTier=3;assert.equal(box.complicationIntelV140(intel,sample.contact).tier,2);
console.log('PASS procedural complication deterministic contract',JSON.stringify({total,enabled,disabled,chances:[Math.min(...chances),Math.max(...chances)],kinds:[...kinds].sort(),sample:{kind:sample.m.v140Complication.kind,cost:sample.m.v140Complication.mitigationCost}}));
