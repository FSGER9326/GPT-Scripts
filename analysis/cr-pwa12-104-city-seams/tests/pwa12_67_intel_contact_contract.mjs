import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const missionHistory=[
  {id:'mission_a',name:'Blacksite A',contact:'c1',operationIntelRecoveredV14:{bonus:180}},
  {id:'mission_b',name:'Blacksite B',contact:'c1',operationIntelRecoveredV14:{bonus:125}},
  {id:'failed',name:'Blacksite C',contact:'c1'}
];
const game={missionHistory,journal:[],contacts:[{id:'c1',name:'Mira',x:7,y:11,faction:'meridian'}],ovPlayer:{x:7,y:11},activeMission:null,heat:{meridian:10},day:2};
let trust=0,saved=0;
const root={document:{getElementById:()=>null},
  initCombat(){},checkWinLose(){},createCombatUnits(){},serializeGame:()=>JSON.stringify(game),loadGame:()=>true,
  ChromeRequiemCoreV5:{state:game},renderContactDossierV13(){},
  saveGame(){saved++},changeContactTrustV13(_id,amount){trust+=amount},
  logMsg(){},localStorage:{getItem:()=>null}};
root.globalThis=root;
vm.runInNewContext(readFileSync(new URL('../src/missions/multistage-operations-v14.js',import.meta.url),'utf8'),root,{timeout:5000});
const api=root.CR14MultiStageOperations;
assert.equal(api.pendingLeads('c1').length,2);
const [first,second]=api.pendingLeads('c1');
assert.equal(api.resolveLead('c1',first.key,'disclose'),true);
assert.equal(game.heat.meridian,16);assert.equal(trust,8);
assert.equal(api.resolveLead('c1',first.key,'disclose'),false);
assert.equal(api.pendingLeads('c1').length,1);
assert.equal(api.resolveLead('c1',second.key,'erase'),true);
assert.equal(game.heat.meridian,8);assert.equal(trust,8);
assert.equal(api.pendingLeads('c1').length,0);assert.equal(saved,2);
game.missionHistory.push({id:'mission_d',contact:'c1',name:'Blacksite D',operationIntelRecoveredV14:{bonus:140}});
const third=api.pendingLeads('c1')[0];
game.ovPlayer={x:0,y:0};assert.equal(api.nearContact('c1'),false);
assert.equal(api.resolveLead('c1',third.key,'disclose'),false);
assert.equal(api.pendingLeads('c1').length,1);
game.ovPlayer={x:7,y:11};game.activeMission={id:'in_progress'};
assert.equal(api.resolveLead('c1',third.key,'disclose'),false);
game.activeMission=null;assert.equal(api.resolveLead('c1',third.key,'disclose'),true);
assert.equal(saved,3);
const snapshot=JSON.parse(JSON.stringify(game));
assert.equal(snapshot.journal.filter(j=>j.id?.startsWith('intel_debrief_')).length,3);
assert.equal(snapshot.missionHistory.length,4);
console.log('PASS PWA12.67 intel handoff: two choices, exclusive settlement, physical range, no mid-mission handoff, journal persistence payload, no reward duplication');
