function installLegacySaveBridge({target=globalThis,persistence,storage=target.localStorage,gameVersion='14.0.0-alpha.1'}={}){
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
 const queue=(fn)=>{pending=pending.then(fn,fn);return pending};
 function mirrorKey(slot){return `chrome_requiem_v13_${Number(slot)}`}
 async function persistSnapshot(slot,payload){
   const envelope=await createSaveEnvelope(payload,{gameVersion,slot:Number(slot)});
   await persistence.saveSlot(Number(slot),envelope);
   return envelope;
 }
 function save(slot=0,quiet=true){
   const n=Number(slot);
   const ok=legacySave(n,quiet);
   if(ok!==false){
     // Capture the exact durable state at the save call boundary. The v14 mirror
     // writes asynchronously; serializing later inside the persistence queue can
     // otherwise make rapid saves all persist a newer shared Game state and rotate
     // the wrong recovery snapshot into backup.
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
 // not recurse and preserves all v13.6 save semantics.
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
 async function load(slot=0){
   const envelope=await resolveEnvelope(slot);
   if(!envelope)return false;
   storage.setItem(mirrorKey(slot),JSON.stringify(envelope.payload));
   return !!legacyLoad(Number(slot));
 }
 async function hydrateSlot(slot=0){
   const envelope=await resolveEnvelope(slot);
   if(!envelope)return false;
   storage.setItem(mirrorKey(slot),JSON.stringify(envelope.payload));
   return true;
 }
 async function hydrateAll(slots=[0,1,2]){const out=[];for(const slot of slots)if(await hydrateSlot(slot))out.push(slot);return out}
 const api={backendName:persistence.backendName,save,load,hydrateSlot,hydrateAll,resolveEnvelope,flush:()=>pending,persistence};
 return Object.freeze(api);
}
