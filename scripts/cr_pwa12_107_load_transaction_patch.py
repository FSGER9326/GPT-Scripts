from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / 'src/runtime/legacy-save-bridge.js'
source = path.read_text(encoding='utf-8')

required = [
    "function installLegacySaveBridge(",
    "let pending=Promise.resolve();",
    "const queue=(fn)=>{pending=pending.then(fn,fn);return pending};",
    "async function load(slot=0){",
    "return !!legacyLoad(Number(slot));",
]
for marker in required:
    if marker not in source:
        raise SystemExit(f'canonical bridge anchor missing: {marker}')
if 'load transaction barrier' in source or 'queuedLoads' in source:
    raise SystemExit('load transaction patch appears to be already applied')

candidate = r'''function installLegacySaveBridge({target=globalThis,persistence,storage=target.localStorage,gameVersion='14.0.0-alpha.1'}={}){
 if(!persistence)throw new TypeError('persistence required');
 if(!storage)throw new TypeError('storage required');
 const legacySave=target.saveGame?.bind(target);
 // Capture the currently installed compatibility load entry point first. Future layers
 // (operation checkpoints, migrations, recovery shims) must not be bypassed merely
 // because the historical v13.5 symbol is still present on window.
 const legacyLoad=(target.loadGame||target.loadGameV135)?.bind(target);
 const serialize=target.serializeGame?.bind(target);
 if(!legacySave||!legacyLoad||!serialize)throw new TypeError('legacy save/load/serialize functions required');
 let pending=Promise.resolve();
 let loadTail=Promise.resolve();
 let activeLoad=null;
 let queuedLoads=0;
 const queue=(fn)=>{pending=pending.then(fn,fn);return pending};
 function mirrorKey(slot){return `chrome_requiem_v13_${Number(slot)}`}
 async function persistSnapshot(slot,payload){
   const envelope=await createSaveEnvelope(payload,{gameVersion,slot:Number(slot)});
   await persistence.saveSlot(Number(slot),envelope);
   return envelope;
 }
 function captureSnapshot(){
   try{return JSON.parse(serialize())}
   catch(err){console.warn('[CR14] save snapshot capture failed:',err?.message||err);return null}
 }
 function restoreMirror(tx){
   if(!tx?.mirrorChanged)return;
   const key=mirrorKey(tx.slot);
   if(tx.priorMirror===null||tx.priorMirror===undefined)storage.removeItem?.(key);
   else storage.setItem(key,tx.priorMirror);
   tx.mirrorChanged=false;
 }
 function save(slot=0,quiet=true){
   const n=Number(slot);
   // PWA12.107 load transaction barrier: compatibility loaders are allowed to
   // request migration/checkpoint autosaves while hydrating, but those writes are
   // quarantined until the legacy load returns successfully. A failed load can
   // therefore never rotate a half-hydrated snapshot into primary/backup storage.
   if(activeLoad?.phase==='hydrating'){
     const payload=captureSnapshot();
     if(!payload)return false;
     activeLoad.deferred.set(n,{slot:n,quiet:!!quiet,payload});
     return true;
   }
   // A user/timer save racing an explicitly requested Load is ambiguous: letting
   // it execute can change the very slot the transaction is selecting. Load wins
   // deterministically; the caller receives false instead of silently saving a
   // different campaign state.
   if(activeLoad||queuedLoads>0){
     console.warn('[CR14] save skipped while load transaction is in progress:',n);
     return false;
   }
   const ok=legacySave(n,quiet);
   if(ok!==false){
     // Preserve the canonical exact save-call-boundary snapshot behavior verbatim;
     // inherited regression contracts depend on this ordering as well as its semantics.
     let payload;
     try{payload=JSON.parse(serialize())}catch(err){
       console.warn('[CR14] save snapshot capture failed:',err?.message||err);
       return ok;
     }
     queue(()=>persistSnapshot(n,payload));
   }
   return ok;
 }
 // Route every existing legacy autosave/manual save call through the v14 mirror.
 // The captured legacySave remains the underlying implementation, so this does
 // not recurse and preserves all v13.6 save semantics outside a load transaction.
 target.saveGame=save;
 async function resolveEnvelope(slot=0){
   // An immediate Load may follow a checkpoint/manual save while its v14 mirror
   // is still waiting on checksum generation or the IndexedDB transaction.
   // Read only after writes requested before this load have settled; otherwise
   // the load can report an empty slot or resurrect the previous snapshot.
   // A failed write must not prevent recovery from an older valid backup.
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
 async function loadOnce(slot=0){
   const n=Number(slot),tx={slot:n,phase:'waiting',deferred:new Map(),priorMirror:null,mirrorChanged:false};
   activeLoad=tx;
   try{
     const envelope=await resolveEnvelope(n);
     if(!envelope)return false;
     const key=mirrorKey(n);
     tx.priorMirror=storage.getItem(key);
     storage.setItem(key,JSON.stringify(envelope.payload));
     tx.mirrorChanged=true;
     tx.phase='hydrating';
     let ok=false;
     try{ok=!!legacyLoad(n)}
     catch(err){
       tx.deferred.clear();
       restoreMirror(tx);
       throw err;
     }
     if(!ok){
       tx.deferred.clear();
       restoreMirror(tx);
       return false;
     }
     tx.phase='committing';
     // Each slot keeps only its latest compatibility autosave from this load.
     // The payload was captured synchronously at the original save call boundary.
     for(const entry of tx.deferred.values()){
       storage.setItem(mirrorKey(entry.slot),JSON.stringify(entry.payload));
       queue(()=>persistSnapshot(entry.slot,entry.payload));
     }
     tx.deferred.clear();
     return true;
   }finally{
     activeLoad=null;
   }
 }
 function load(slot=0){
   queuedLoads++;
   const run=loadTail.then(()=>loadOnce(slot),()=>loadOnce(slot));
   const tracked=run.finally(()=>{queuedLoads=Math.max(0,queuedLoads-1)});
   // Keep later loads moving even when this request rejects, while preserving the
   // rejection for the caller that owns this transaction.
   loadTail=tracked.then(()=>undefined,()=>undefined);
   return tracked;
 }
 async function hydrateSlot(slot=0){
   // Import/boot hydration must not rewrite the compatibility mirror in the middle
   // of a live Load transaction.
   await loadTail;
   const envelope=await resolveEnvelope(slot);
   if(!envelope)return false;
   storage.setItem(mirrorKey(slot),JSON.stringify(envelope.payload));
   return true;
 }
 async function hydrateAll(slots=[0,1,2]){const out=[];for(const slot of slots)if(await hydrateSlot(slot))out.push(slot);return out}
 async function flush(){
   // Wait for the load queue first because a successful hydration may enqueue its
   // deferred migration/checkpoint autosaves only at commit time.
   await loadTail;
   await pending;
   return true;
 }
 const api={backendName:persistence.backendName,save,load,hydrateSlot,hydrateAll,resolveEnvelope,flush,persistence,
   get loadInProgress(){return queuedLoads>0||!!activeLoad}};
 return Object.freeze(api);
}
'''

path.write_text(candidate, encoding='utf-8')
print('PATCHED', path)
