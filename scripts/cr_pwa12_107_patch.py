#!/usr/bin/env python3
from pathlib import Path
import sys

root=Path(sys.argv[1])
p=root/'src/runtime/legacy-save-bridge.js'
old=p.read_text()
assert 'function installLegacySaveBridge' in old
assert 'let pending=Promise.resolve();' in old
assert 'return !!legacyLoad(Number(slot));' in old

new=r'''function installLegacySaveBridge({target=globalThis,persistence,storage=target.localStorage,gameVersion='14.0.0-alpha.1'}={}){
 if(!persistence)throw new TypeError('persistence required');
 if(!storage)throw new TypeError('storage required');
 const legacySave=target.saveGame?.bind(target);
 const legacyLoad=(target.loadGame||target.loadGameV135)?.bind(target);
 const serialize=target.serializeGame?.bind(target);
 if(!legacySave||!legacyLoad||!serialize)throw new TypeError('legacy save/load/serialize functions required');
 let pending=Promise.resolve(),loadTail=Promise.resolve(),loadTransaction=null;
 const queue=(fn)=>{pending=pending.then(fn,fn);return pending};
 function mirrorKey(slot){return `chrome_requiem_v13_${Number(slot)}`}
 async function persistSnapshot(slot,payload){
   const envelope=await createSaveEnvelope(payload,{gameVersion,slot:Number(slot)});
   await persistence.saveSlot(Number(slot),envelope);
   return envelope;
 }
 function capturePayload(){return JSON.parse(serialize())}
 function save(slot=0,quiet=true){
   // Compatibility reconstruction may autosave while hydration is incomplete.
   // Buffer those writes until transaction commit; discard them on rollback.
   if(loadTransaction){loadTransaction.saves.push({slot:Number(slot),quiet:!!quiet});return true}
   const n=Number(slot),ok=legacySave(n,quiet);
   if(ok!==false){
     let payload;
     try{payload=JSON.parse(serialize())}catch(err){
       console.warn('[CR14] save snapshot capture failed:',err?.message||err);
       return ok;
     }
     queue(()=>persistSnapshot(n,payload));
   }
   return ok;
 }
 target.saveGame=save;

 function cloneRollbackValue(value,seen=new WeakMap()){
   if(value===null||typeof value!=='object')return value;
   if(seen.has(value))return seen.get(value);
   if(Array.isArray(value)){const out=[];seen.set(value,out);for(const v of value)out.push(cloneRollbackValue(v,seen));return out}
   if(typeof Map!=='undefined'&&value instanceof Map){const out=new Map();seen.set(value,out);for(const [k,v] of value)out.set(cloneRollbackValue(k,seen),cloneRollbackValue(v,seen));return out}
   if(typeof Set!=='undefined'&&value instanceof Set){const out=new Set();seen.set(value,out);for(const v of value)out.add(cloneRollbackValue(v,seen));return out}
   if(typeof Date!=='undefined'&&value instanceof Date)return new Date(value.getTime());
   if(typeof ArrayBuffer!=='undefined'&&ArrayBuffer.isView?.(value)){try{return value.slice?value.slice():new value.constructor(value)}catch{return value}}
   const proto=Object.getPrototypeOf(value);
   // Preserve host objects/class instances by identity; clone plain gameplay graphs.
   if(proto!==Object.prototype&&proto!==null)return value;
   const out=Object.create(proto);seen.set(value,out);
   for(const key of Object.keys(value)){try{out[key]=cloneRollbackValue(value[key],seen)}catch{out[key]=value[key]}}
   return out;
 }
 function gameRoot(){return target.Game||target.ChromeRequiemCoreV5?.state||null}
 function captureRuntimeState(){const game=gameRoot();return game&&typeof game==='object'?{game,state:cloneRollbackValue(game)}:null}
 function restoreRuntimeState(snapshot){
   if(!snapshot?.game||!snapshot.state)return false;
   const game=snapshot.game,state=snapshot.state;
   for(const key of Object.keys(game))if(!Object.prototype.hasOwnProperty.call(state,key))try{delete game[key]}catch{}
   for(const key of Object.keys(state))try{game[key]=state[key]}catch{}
   return true;
 }
 function captureSurface(){
   const doc=target.document;if(!doc?.getElementById)return null;
   const attributeIds=['intro','charcreate','load-menu','overworld-screen','combat','board','objective-hud'];
   const childIds=['grid','units','actions','init-strip','objective-hud'];
   const attrs=[],children=[];
   for(const id of attributeIds){const node=doc.getElementById(id);if(node)attrs.push({id,node,values:[...node.attributes].map(a=>[a.name,a.value])})}
   for(const id of childIds){const node=doc.getElementById(id);if(node)children.push({id,node,values:[...node.childNodes]})}
   return {attrs,children};
 }
 function restoreAttributes(node,values){
   try{for(const a of [...node.attributes])node.removeAttribute(a.name);for(const [k,v] of values)node.setAttribute(k,v)}catch{}
 }
 function restoreSurface(snapshot){
   if(!snapshot)return;
   const doc=target.document;
   for(const item of snapshot.children){
     try{const current=doc?.getElementById?.(item.id);if(current&&current!==item.node)current.replaceWith(item.node);item.node.replaceChildren(...item.values)}catch{}
   }
   for(const item of snapshot.attrs){
     try{const current=doc?.getElementById?.(item.id);const node=current||item.node;restoreAttributes(node,item.values)}catch{}
   }
 }
 function restorePresentation(runtime){
   const screen=runtime?.state?.screen;
   try{if(screen&&typeof target.showScreen==='function')target.showScreen(screen)}catch{}
   try{if(screen==='combat'&&typeof target.updateCombat==='function')target.updateCombat()}catch{}
   try{if(screen!=='combat'&&typeof target.updateOverworldHUD==='function')target.updateOverworldHUD()}catch{}
 }
 async function resolveEnvelope(slot=0){
   try{await pending}catch(err){
     console.warn('[CR14] pending save failed before load; attempting last valid recovery point:',err?.message||err);
   }
   const n=Number(slot),live=await persistence.loadSlot(n);
   if(live&&await validateSaveEnvelope(live))return live;
   if(typeof persistence.loadBackup!=='function')return null;
   const backup=await persistence.loadBackup(n);
   if(!backup||!(await validateSaveEnvelope(backup)))return null;
   if(typeof persistence.restoreBackup==='function')await persistence.restoreBackup(n);
   return backup;
 }
 function commitBufferedSaves(requests){
   // Every reconstruction autosave observes only the committed hydrated state.
   const slots=new Map();for(const r of requests)slots.set(Number(r.slot),r);
   for(const [slot] of slots){
     let payload;try{payload=capturePayload()}catch(err){console.warn('[CR14] post-load save snapshot failed:',err?.message||err);continue}
     try{storage.setItem(mirrorKey(slot),JSON.stringify(payload))}catch(err){console.warn('[CR14] post-load mirror write failed:',err?.message||err)}
     queue(()=>persistSnapshot(slot,payload));
   }
 }
 async function runLoad(slot=0){
   const n=Number(slot),envelope=await resolveEnvelope(n);if(!envelope)return false;
   const key=mirrorKey(n),previousMirror=storage.getItem(key),runtime=captureRuntimeState(),surface=captureSurface();
   const txn={slot:n,saves:[]};loadTransaction=txn;
   try{
     storage.setItem(key,JSON.stringify(envelope.payload));
     let ok=false;
     try{ok=!!legacyLoad(n)}catch(err){throw new Error(`legacy hydration threw: ${err?.message||err}`)}
     if(!ok)throw new Error('legacy hydration returned false');
     loadTransaction=null;
     commitBufferedSaves(txn.saves);
     return true;
   }catch(err){
     restoreRuntimeState(runtime);restoreSurface(surface);
     try{if(previousMirror===null)storage.removeItem(key);else storage.setItem(key,previousMirror)}catch{}
     restorePresentation(runtime);
     console.warn('[CR14] load transaction rolled back:',err?.message||err);
     return false;
   }finally{if(loadTransaction===txn)loadTransaction=null}
 }
 function load(slot=0){
   // Serialize hydration so two compatibility loaders can never interleave mutations.
   const run=()=>runLoad(Number(slot));
   const result=loadTail.then(run,run);
   loadTail=result.then(()=>undefined,()=>undefined);
   return result;
 }
 async function hydrateSlot(slot=0){
   const envelope=await resolveEnvelope(slot);if(!envelope)return false;
   storage.setItem(mirrorKey(slot),JSON.stringify(envelope.payload));return true;
 }
 async function hydrateAll(slots=[0,1,2]){const out=[];for(const slot of slots)if(await hydrateSlot(slot))out.push(slot);return out}
 async function flush(){await loadTail;return pending}
 const api={backendName:persistence.backendName,save,load,hydrateSlot,hydrateAll,resolveEnvelope,flush,persistence};
 return Object.freeze(api);
}
'''
p.write_text(new)
print('PATCHED',p)
