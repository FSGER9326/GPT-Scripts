// PWA12.107: deterministic load transaction coverage for the v14 compatibility bridge.
// This test exercises quarantine/commit/discard semantics and the exclusive load barrier
// without claiming browser/IndexedDB coverage.
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import path from 'node:path';

const root=path.resolve(process.argv[2]||'.');
const read=name=>readFileSync(path.join(root,'src/runtime',name),'utf8');
const env={globalThis:null,structuredClone,TextEncoder,BigInt,Uint8Array,Uint32Array,Date,console,Promise};
env.globalThis=env;
vm.createContext(env);
vm.runInContext(read('save-envelope.js')+'\n'+read('legacy-save-bridge.js')+'\nthis.makeBridge=installLegacySaveBridge;this.makeEnvelope=createSaveEnvelope;',env,{timeout:5000});

function makeStorage(){
 const backing=new Map();
 return {
  backing,
  api:{
   getItem:key=>backing.has(key)?backing.get(key):null,
   setItem:(key,value)=>backing.set(key,String(value)),
   removeItem:key=>backing.delete(key),
  }
 };
}
function makePersistence(){
 const primary=new Map(),backup=new Map(),writes=[];
 return {
  primary,backup,writes,
  api:{
   backendName:'memory-test',
   async saveSlot(slot,envelope){const n=Number(slot),old=primary.get(n);if(old)backup.set(n,old);primary.set(n,envelope);writes.push({slot:n,envelope});return true},
   async loadSlot(slot){return primary.get(Number(slot))||null},
   async loadBackup(slot){return backup.get(Number(slot))||null},
   async restoreBackup(slot){const n=Number(slot),b=backup.get(n);if(!b)return false;primary.set(n,b);return true},
  }
 };
}

// Successful legacy reconstruction autosaves are quarantined during hydration and
// committed only after the legacy loader has returned true.
{
 const {api:storage}=makeStorage(),p=makePersistence();
 let live={name:'BEFORE',credits:100,day:1},legacyWrites=0;
 const target={localStorage:storage,
  saveGame(slot){legacyWrites++;storage.setItem(`chrome_requiem_v13_${slot}`,JSON.stringify(live));return true},
  loadGame(slot){
   live=JSON.parse(storage.getItem(`chrome_requiem_v13_${slot}`));
   live.cityRebuilt=true;live.day+=1;
   assert.equal(target.saveGame(slot,true),true,'compatibility autosave should be buffered during hydration');
   live.afterBufferedSave='not-part-of-buffered-snapshot';
   return true;
  },
  serializeGame(){return JSON.stringify(live)},
 };
 p.primary.set(0,await env.makeEnvelope({name:'TARGET',credits:900,day:7},{gameVersion:'14.0.0-pwa.12.107-test',slot:0,now:100}));
 const bridge=env.makeBridge({target,persistence:p.api,storage,gameVersion:'14.0.0-pwa.12.107-test'});
 assert.equal(await bridge.load(0),true);
 assert.equal(legacyWrites,0,'underlying legacy save must not write during hydration');
 await bridge.flush();
 assert.equal(p.writes.length,1,'successful hydration should commit one deferred autosave');
 assert.equal(p.primary.get(0).payload.name,'TARGET');
 assert.equal(p.primary.get(0).payload.day,8);
 assert.equal(p.primary.get(0).payload.cityRebuilt,true);
 assert.equal(p.primary.get(0).payload.afterBufferedSave,undefined,'snapshot must remain tied to original autosave boundary');
 assert.equal(JSON.parse(storage.getItem('chrome_requiem_v13_0')).day,8);
 assert.equal(bridge.loadInProgress,false);
}

// A late exception must discard every reconstruction autosave and restore the exact
// pre-load compatibility mirror. This prevents a half-hydrated state from becoming
// durable primary/backup data. Runtime object rollback is intentionally the next target.
{
 const {api:storage}=makeStorage(),p=makePersistence();
 let live={name:'LIVE_BEFORE',credits:321,day:4},legacyWrites=0;
 const priorRaw=JSON.stringify(live);
 storage.setItem('chrome_requiem_v13_0',priorRaw);
 const target={localStorage:storage,
  saveGame(slot){legacyWrites++;storage.setItem(`chrome_requiem_v13_${slot}`,JSON.stringify(live));return true},
  loadGame(slot){
   live=JSON.parse(storage.getItem(`chrome_requiem_v13_${slot}`));
   live.partialHydration=true;
   assert.equal(target.saveGame(slot,true),true);
   throw new Error('late hydration boom');
  },
  serializeGame(){return JSON.stringify(live)},
 };
 const durable=await env.makeEnvelope({name:'TARGET',credits:999,day:10},{gameVersion:'14.0.0-pwa.12.107-test',slot:0,now:200});
 p.primary.set(0,durable);
 const bridge=env.makeBridge({target,persistence:p.api,storage,gameVersion:'14.0.0-pwa.12.107-test'});
 await assert.rejects(bridge.load(0),/late hydration boom/);
 assert.equal(storage.getItem('chrome_requiem_v13_0'),priorRaw,'failed load must restore prior compatibility mirror byte-for-byte');
 assert.equal(p.writes.length,0,'failed hydration must commit zero autosaves');
 assert.equal(p.primary.get(0),durable,'failed hydration must not replace durable primary');
 assert.equal(legacyWrites,0,'buffered compatibility save must never reach legacy writer');
 assert.equal(bridge.loadInProgress,false);
}

// A false legacy load result receives the same rollback semantics as an exception.
{
 const {api:storage}=makeStorage(),p=makePersistence();
 let live={name:'FALSE_BEFORE',credits:77};
 const priorRaw=JSON.stringify(live);storage.setItem('chrome_requiem_v13_1',priorRaw);
 const target={localStorage:storage,
  saveGame(){return true},
  loadGame(slot){live=JSON.parse(storage.getItem(`chrome_requiem_v13_${slot}`));live.rebuilt='partial';target.saveGame(slot,true);return false},
  serializeGame(){return JSON.stringify(live)},
 };
 p.primary.set(1,await env.makeEnvelope({name:'FALSE_TARGET',credits:88},{gameVersion:'14.0.0-pwa.12.107-test',slot:1,now:300}));
 const bridge=env.makeBridge({target,persistence:p.api,storage,gameVersion:'14.0.0-pwa.12.107-test'});
 assert.equal(await bridge.load(1),false);
 assert.equal(storage.getItem('chrome_requiem_v13_1'),priorRaw);
 assert.equal(p.writes.length,0);
}

// Two explicit Loads are serialized, and a save racing a queued load is rejected
// deterministically rather than mutating the selected slot beneath the transaction.
{
 const {api:storage}=makeStorage();
 const primary=new Map(),backup=new Map();let releaseFirst;
 const firstGate=new Promise(resolve=>releaseFirst=resolve);const loadCalls=[];let legacyWrites=0,live={name:'initial'};
 const persistence={backendName:'gated-test',
  async saveSlot(slot,envelope){primary.set(Number(slot),envelope);return true},
  async loadSlot(slot){const n=Number(slot);loadCalls.push(n);if(n===0)await firstGate;return primary.get(n)||null},
  async loadBackup(slot){return backup.get(Number(slot))||null},async restoreBackup(){return false},
 };
 primary.set(0,await env.makeEnvelope({name:'FIRST',day:1},{gameVersion:'14.0.0-pwa.12.107-test',slot:0,now:400}));
 primary.set(1,await env.makeEnvelope({name:'SECOND',day:2},{gameVersion:'14.0.0-pwa.12.107-test',slot:1,now:401}));
 const target={localStorage:storage,
  saveGame(slot){legacyWrites++;storage.setItem(`chrome_requiem_v13_${slot}`,JSON.stringify(live));return true},
  loadGame(slot){live=JSON.parse(storage.getItem(`chrome_requiem_v13_${slot}`));return true},
  serializeGame(){return JSON.stringify(live)},
 };
 const bridge=env.makeBridge({target,persistence,storage,gameVersion:'14.0.0-pwa.12.107-test'});
 const first=bridge.load(0),second=bridge.load(1);
 assert.equal(bridge.loadInProgress,true);
 assert.equal(bridge.save(2,true),false,'load request must own the save/load boundary immediately');
 assert.equal(legacyWrites,0);
 for(let i=0;i<20&&loadCalls.length===0;i++)await new Promise(resolve=>setTimeout(resolve,0));
 assert.equal(loadCalls.length,1,'first transaction did not enter persistence or second load entered before release');
 assert.equal(loadCalls[0],0);
 releaseFirst();
 assert.equal(await first,true);assert.equal(await second,true);
 assert.equal(loadCalls.length,2);assert.equal(loadCalls[0],0);assert.equal(loadCalls[1],1);
 assert.equal(live.name,'SECOND');assert.equal(bridge.loadInProgress,false);
 assert.equal(bridge.save(2,true),true,'ordinary saving should resume after load queue drains');
 await bridge.flush();
 assert.equal(legacyWrites,1);
}

console.log('PASS PWA12.107 load transaction: serialized loads, deterministic save/load barrier, success-only hydration autosave commit, failure discard, exact compatibility-mirror rollback');
