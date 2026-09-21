const V14_VERSION=globalThis.CR14_BUILD_VERSION||'14.0.0-dev';

function diagnosticsFor(target){
 const names=['runDiagnosticsV136','runDiagnosticsV135','runDiagnosticsV134B','runDiagnosticsV134','runDiagnosticsV133','runDiagnosticsV131','runDiagnosticsV13'];
 const results={};let passed=0,total=0;
 for(const name of names){if(typeof target[name]!=='function')continue;const r=target[name]();results[name]=r;passed+=r?.passed||0;total+=r?.total||0}
 return{version:V14_VERSION,passed,total,results};
}

function installSafeLoadMenuRouting({target,bridge}){
 const render=target.renderLoadMenu;
 if(typeof render!=='function'||!bridge?.load)return;
 target.renderLoadMenu=function(){
  const result=render.apply(this,arguments),host=target.document?.getElementById('load-slots');
  if(!host)return result;
  [...host.querySelectorAll('button')].forEach((button,slot)=>{
   if(button.disabled)return;
   button.onclick=async()=>{
    if(button.dataset.loading==='1')return;
    button.dataset.loading='1';const label=button.innerHTML;button.disabled=true;
    try{
     const ok=await bridge.load(slot);
     if(!ok){button.disabled=false;button.innerHTML=label;target.logMsg?.('SAVE RECOVERY // No valid primary or backup save found.','bad');}
    }catch(err){
     button.disabled=false;button.innerHTML=label;
     console.warn('[CR14] safe load failed:',err?.message||err);
     target.logMsg?.('SAVE RECOVERY // Load failed; stored data was left untouched.','bad');
    }finally{delete button.dataset.loading;}
   };
  });
  return result;
 };
}

async function bootChromeRequiemV14({target=globalThis,storage,persistence=null,slots=[0,1,2],registerPwa=true}={}){
 if(!target.CRAssets?.ready)throw new Error('PWA asset loader is not available');
 await target.CRAssets.ready;
 if(!target.CRAssets?.state?.manifest)throw new Error('PWA asset manifest unavailable');
 const local=storage ?? target.localStorage;
 const db=persistence ?? await openPersistence({storage:local});
 const migrations=[];
 for(const slot of slots)migrations.push(await migrateSlotIfNeeded({slot,persistence:db,storage:local}));
 const bridge=installLegacySaveBridge({target,persistence:db,storage:local,gameVersion:V14_VERSION});
 const persistenceLifecycle=installPersistenceLifecycle({target,bridge});
 await bridge.hydrateAll(slots);
 // Route visible save-slot clicks through checksum validation and known-good backup
 // recovery instead of the historical localStorage-only loadGame path.
 installSafeLoadMenuRouting({target,bridge});
 const legacy=target.CRRuntime;
 if(!legacy)throw new Error('v13.6 CRRuntime is not available');
 const runtime=createRuntime({
   save:(slot=0,quiet=true)=>bridge.save(slot,quiet),
   load:(slot=0)=>bridge.load(slot),
   newGame:(name,className,background)=>{const r=legacy.newGame(name,className,background);bridge.save(0,true);return r},
   advanceTime:(minutes)=>legacy.advanceTime(minutes),
   startMission:(m)=>legacy.startMission(m),
   buildGrid:(m)=>legacy.buildGrid(m),
   createCombatUnits:(m)=>legacy.createCombatUnits(m),
   showScreen:(id)=>target.showScreen(id),
   diagnostics:()=>diagnosticsFor(target)
 },{version:V14_VERSION});
 installCompatibility(runtime,target);
 target.ChromeRequiem.version=V14_VERSION;
 const transfer=Object.freeze({
   exportSave:(slot=0,exportedAt=Date.now())=>exportSaveText({persistence:db,slot,exportedAt}),
   importSave:async(text,{slotOverride=null,now=Date.now()}={})=>{const result=await importSaveText({persistence:db,text,slotOverride,now});await bridge.hydrateSlot(result.slot);return result}
 });
 const architecture=Object.freeze({moduleOrder:MODULE_ORDER,modules:MODULES,compatibility:COMPATIBILITY_EXPORTS});
 const install=installPWAControls({target});
 const connectivity=installConnectivity({target});
 const boot=Object.freeze({ready:true,version:V14_VERSION,backend:db.backendName,migrations,runtime,bridge,persistenceLifecycle,transfer,architecture,install,connectivity});
 target.ChromeRequiemV14Boot=boot;
 if(registerPwa&&target.navigator?.serviceWorker){
   Promise.resolve(registerPWA({target})).catch(err=>console.warn('[CR14] PWA registration skipped:',err?.message||err));
 }
 target.dispatchEvent?.(new CustomEvent('cr14-ready',{detail:{version:V14_VERSION,backend:db.backendName}}));
 return boot;
}

if(typeof window!=='undefined'&&window.document){
 const start=()=>bootChromeRequiemV14({registerPwa:true}).then(()=>document.getElementById('cr14-boot-overlay')?.remove()).catch(err=>{
   console.error('[CR14] Boot failed',err);const el=document.getElementById('cr14-boot-overlay');if(el){el.classList.add('error');el.textContent=`V14 BOOT FAILURE // ${err.message}`}
 });
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
}
