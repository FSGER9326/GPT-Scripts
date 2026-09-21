// PWA12.71: saves requested immediately before Load must be durable before the
// load attempts primary/backup recovery. This is a deterministic bridge test;
// it does not claim to replace real-browser IndexedDB recovery validation.
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const rootUrl=new URL('../src/runtime/',import.meta.url);
const read=name=>readFileSync(new URL(name,rootUrl),'utf8');
const backing=new Map();
const storage={getItem:key=>backing.get(key)??null,setItem:(key,value)=>backing.set(key,String(value)),removeItem:key=>backing.delete(key)};
let live={credits:100,day:1},restoreCalls=0;
let releaseWrite;
const gate=new Promise(resolve=>releaseWrite=resolve);
const primary=new Map(),backups=new Map();
let wrote=false;
const persistence={
 backendName:'indexeddb',
 async saveSlot(slot,envelope){await gate;const previous=primary.get(slot);if(previous)backups.set(slot,previous);primary.set(slot,envelope);wrote=true;return true},
 async loadSlot(slot){return primary.get(slot)||null},
 async loadBackup(slot){return backups.get(slot)||null},
 async restoreBackup(slot){const b=backups.get(slot);if(!b)return false;primary.set(slot,b);restoreCalls++;return true},
};
const target={localStorage:storage,
 saveGame(slot){storage.setItem(`chrome_requiem_v13_${slot}`,JSON.stringify(live));return true},
 loadGame(slot){const data=storage.getItem(`chrome_requiem_v13_${slot}`);if(!data)return false;live=JSON.parse(data);return true},
 serializeGame(){return JSON.stringify(live)},
};
const env={globalThis:null,structuredClone,TextEncoder,BigInt,Uint8Array,Uint32Array,Date,console,Promise};env.globalThis=env;
vm.createContext(env);vm.runInContext(read('save-envelope.js')+ '\n'+read('legacy-save-bridge.js')+'\nthis.makeBridge=installLegacySaveBridge;',env,{timeout:5000});
const bridge=env.makeBridge({target,persistence,storage,gameVersion:'14.0.0-pwa.12.71-qa'});
live={credits:43210,day:9,missionHistory:[{id:'first',success:true}]};bridge.save(1,true);
live={credits:0,day:1};
let settled=false;
const pendingLoad=bridge.load(1).then(value=>{settled=true;return value});
// Force async scheduling and prove the load does not proceed past the in-flight save.
await Promise.resolve();await Promise.resolve();await Promise.resolve();
assert.equal(settled,false,'load returned before the asynchronous primary write completed');
releaseWrite();
assert.equal(await pendingLoad,true,'load failed after pending save completed');
assert.equal(wrote,true);assert.equal(live.credits,43210);assert.equal(live.day,9);
assert.deepEqual(live.missionHistory,[{id:'first',success:true}]);
// A subsequent valid save rotates known-good A into the backup. Corrupted B
// must load A and repair the primary before another load.
live={credits:9731,day:12};bridge.save(1,true);await bridge.flush();
assert.equal(primary.get(1).payload.credits,9731);
assert.equal(backups.get(1).payload.credits,43210);
primary.set(1,{...primary.get(1),checksum:'corrupted'});
live={credits:-1,day:0};assert.equal(await bridge.load(1),true);
assert.equal(live.credits,43210);assert.equal(restoreCalls,1);
assert.equal(primary.get(1).payload.credits,43210);
console.log('PASS PWA12.71 in-flight save/load atomicity and primary corruption recovery: latest save wins only after durability, known-good backup restores without data loss');
