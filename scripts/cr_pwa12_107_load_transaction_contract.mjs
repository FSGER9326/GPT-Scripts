import assert from 'node:assert/strict';
import {installLegacySaveBridge} from '../src/runtime/legacy-save-bridge.js';
import {createSaveEnvelope} from '../src/runtime/save-envelope.js';

class HostNode { constructor(id){this.id=id;} }
class MemoryStorage {
  constructor(){this.m=new Map()}
  getItem(k){return this.m.has(k)?this.m.get(k):null}
  setItem(k,v){this.m.set(k,String(v))}
  removeItem(k){this.m.delete(k)}
}

function makeTarget(storage){
  const host=new HostNode('combat-unit-node');
  const unit={id:'live-u1',hp:3,ap:1,el:host};
  const Game={screen:'combat',credits:111,day:9,nested:{value:7},units:[unit],turnQueue:[unit],turnIndex:0,activeMission:{id:'live-mission'},combatCanvas:host};
  const target={Game,localStorage:storage,failLoad:true,showScreenCalls:[],
    serializeGame(){return JSON.stringify({screen:Game.screen,credits:Game.credits,day:Game.day,nested:Game.nested,units:Game.units.map(u=>({id:u.id,hp:u.hp,ap:u.ap})),turnIndex:Game.turnIndex,activeMission:Game.activeMission})},
    saveGame(slot=0){storage.setItem(`chrome_requiem_v13_${Number(slot)}`,this.serializeGame());return true},
    loadGame(slot=0){
      const payload=JSON.parse(storage.getItem(`chrome_requiem_v13_${Number(slot)}`));
      Game.screen=payload.screen;Game.credits=payload.credits;Game.day=payload.day;Game.nested={...payload.nested};
      Game.units=(payload.units||[]).map(u=>({...u}));Game.turnQueue=[...Game.units];Game.turnIndex=payload.turnIndex||0;Game.activeMission=payload.activeMission||null;
      // Simulates compatibility reconstruction autosaves that must never escape a failed load.
      this.saveGame(slot,true);
      if(this.failLoad){
        Game.credits=-999;Game.nested.value=-5;Game.units=[];Game.turnQueue=[];Game.screen='intro';
        this.saveGame(slot,true);
        throw new Error('injected late hydration failure');
      }
      return true;
    },
    showScreen(name){this.showScreenCalls.push(name);Game.screen=name},
    updateCombat(){this.updateCombatCalls=(this.updateCombatCalls||0)+1}
  };
  return {target,host,unit};
}

const storage=new MemoryStorage();
const {target,host}=makeTarget(storage);
const durablePayload={screen:'world',credits:5000,day:12,nested:{value:42},units:[],turnIndex:0,activeMission:null};
let primary=await createSaveEnvelope(durablePayload,{gameVersion:'14.0.0-pwa.12.104-street-contact-support',slot:0});
const persisted=[];
const persistence={backendName:'test',async loadSlot(){return primary},async loadBackup(){return null},async saveSlot(slot,envelope){persisted.push({slot,envelope});primary=envelope}};
const liveMirror=target.serializeGame();storage.setItem('chrome_requiem_v13_0',liveMirror);
const bridge=installLegacySaveBridge({target,persistence,storage,gameVersion:'14.0.0-pwa.12.107-load-transaction-rollback-candidate.01'});

const failed=await bridge.load(0);
assert.equal(failed,false,'late hydration exception must fail transaction');
assert.equal(target.Game.screen,'combat');
assert.equal(target.Game.credits,111);
assert.equal(target.Game.day,9);
assert.equal(target.Game.nested.value,7);
assert.equal(target.Game.units.length,1);
assert.equal(target.Game.units[0].hp,3);
assert.equal(target.Game.units[0],target.Game.turnQueue[0],'shared runtime identity must survive rollback');
assert.equal(target.Game.units[0].el,host,'host/DOM-like identity must survive rollback');
assert.equal(target.Game.combatCanvas,host,'runtime-only host reference must survive rollback');
assert.equal(storage.getItem('chrome_requiem_v13_0'),liveMirror,'compatibility mirror must be restored exactly');
assert.equal(persisted.length,0,'failed-load reconstruction autosaves must be discarded');

// A subsequent healthy load must still work and its reconstruction autosave commits only after hydration.
target.failLoad=false;
const loaded=await bridge.load(0);assert.equal(loaded,true);
await bridge.flush();
assert.equal(target.Game.screen,'world');assert.equal(target.Game.credits,5000);assert.equal(target.Game.day,12);
assert.equal(persisted.length,1,'successful-load reconstruction autosaves are coalesced and committed');
assert.equal(persisted[0].envelope.payload.credits,5000);

// Explicit load mutex: second resolver cannot start until first transaction completes.
let calls=0,release;const gate=new Promise(r=>release=r);let first=true;
const storage2=new MemoryStorage();const made2=makeTarget(storage2);made2.target.failLoad=false;
const env2=await createSaveEnvelope(durablePayload,{gameVersion:'14.0.0-pwa.12.104-street-contact-support',slot:0});
const persistence2={backendName:'test',async loadSlot(){calls++;if(first){first=false;await gate}return env2},async loadBackup(){return null},async saveSlot(){}};
const bridge2=installLegacySaveBridge({target:made2.target,persistence:persistence2,storage:storage2,gameVersion:'14.0.0-pwa.12.107-load-transaction-rollback-candidate.01'});
const p1=bridge2.load(0),p2=bridge2.load(0);
await new Promise(r=>setTimeout(r,10));
assert.equal(calls,1,'queued load must not resolve storage concurrently');
release();assert.equal(await p1,true);assert.equal(await p2,true);assert.equal(calls,2);

console.log('PWA12.107 load transaction rollback contract PASS');
