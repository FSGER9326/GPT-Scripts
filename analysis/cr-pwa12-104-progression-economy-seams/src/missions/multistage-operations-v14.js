/* Chrome Requiem PWA12.61 — continuous three-area tactical operations.
 * Only a completed-area checkpoint is durable: the current room is reconstructed
 * at its entrance, never from a half-completed initiative/grid snapshot. This
 * preserves campaign save schema 14 and does not advance game time on resume.
 */
(function installMultiStageOperations(root){
  'use strict';
  if(!root.document || typeof root.initCombat!=='function' || typeof root.checkWinLose!=='function') return;
  const state=()=>root.ChromeRequiemCoreV5?.state;
  const eligible=m=>!!m && ['heist','extract'].includes(m.type) &&
    ['heist','extract'].includes(m.objective||m.type) && (m.diff||1)>=2 &&
    (m.enemies?.length||0)>=2 && (m.enemies?.length||0)<=6 &&
    !m.oracleKey && !m.worldLocation && !m.multiStageDisabled && m.tacticalShape!=='open';
  const STEPS=Object.freeze([
    {name:'OUTER PERIMETER',shape:'corridor',brief:'Breach the access bulkhead and disable the exterior security nodes.'},
    {name:'SECURED INTERIOR',shape:'rooms',brief:'Complete the original contract objective inside the target site.'},
    {name:'EXTRACTION ROUTE',shape:'entrance',brief:'Fight through the exit vestibule. Reach the marked extraction point.'}
  ]);
  let operation=null;
  const oldInit=root.initCombat;
  const oldUnits=root.createCombatUnits;
  const oldCheck=root.checkWinLose;
  const oldObjectiveAction=root.objectiveActionAvailable;
  const oldSerialize=root.serializeGame;
  const oldLoad=root.loadGame;
  const oldNewGame=root.startNewGame;
  const checkpointKey='operationCheckpointV14';
  // A completed blacksite theft pays only on final successful extraction.
  const intelBonus=m=>Math.min(450,Math.max(125,Math.round((Number(m?.reward)||0)*.30)));
  const openCells=game=>game.grid.filter(c=>!c.arenaVoid&&!c.obstacle&&!c.door&&!c.cover&&!c.unit&&c.objectiveIndex==null);
  const rosterKey=u=>{
    const roster=u?.rosterRef;
    const index=state()?.roster?.indexOf(roster)??-1;
    return index>=0?`roster:${index}`:`name:${u?.name||''}`;
  };

  function stageMission(){
    const m=operation.mission,step=operation.index;
    const type=step===0?'breach':step===2?'extract':(m.objective||m.type);
    let enemies=step===1?m.enemies.slice():step===0?m.enemies.slice(0,2):m.enemies.slice(operation.extractionRerouted?-1:-2);
    const tacticalShape=step===2&&operation.extractionRerouted?'corridor':STEPS[step].shape;
    // A loud perimeter breach has a concrete downstream cost: the site mobilizes
    // one additional response unit for each remaining area. Quiet entry preserves
    // the baseline composition rather than granting a synthetic reward.
    if(step>0 && operation.carry?.alerted && !operation.securitySuppressed) enemies=[...enemies, step===1?'Drone':'Guard'];
    return {...m,id:`${m.id}:area:${step}`,type,objective:type,tacticalShape,
      enemies,name:`${m.name} // ${STEPS[step].name}`,desc:STEPS[step].brief,
      _v12ObjectiveAssigned:true,operationStageV14:step};
  }
  function snapshot(){
    const game=state();
    return {alerted:!!game.alerted,crew:new Map((game.units||[]).filter(u=>u.team==='player').map(u=>[
      rosterKey(u),{hp:u.hp,dead:!!u.dead,statuses:{...u.statuses},
        inventory:{...u.inventory},disabledTurns:u.disabledTurns||0,wasDowned:!!u.rosterRef?.wasDowned}
    ]))};
  }
  function restoreCrew(){
    if(!operation?.carry)return;
    const game=state();
    for(const u of game.units.filter(u=>u.team==='player')){
      const prior=operation.carry.crew.get(rosterKey(u));
      if(!prior)continue;
      u.hp=Math.max(0,Math.min(u.maxHp,prior.hp));u.dead=prior.dead||u.hp<=0;
      u.statuses={...prior.statuses};u.inventory={...prior.inventory};
      u.disabledTurns=prior.disabledTurns;
      if(u.rosterRef && prior.wasDowned)u.rosterRef.wasDowned=true;
      if(u.dead){const c=game.grid.find(c=>c.unit===u);if(c)c.unit=null;}
    }
    if(operation.carry.alerted){
      game.alerted=true;
      for(const u of game.units.filter(u=>u.team==='enemy')){u.alerted=true;u.awareness=100;}
    }
  }
  root.createCombatUnits=function(mission){
    const result=oldUnits.apply(this,arguments);
    if(operation && mission.operationStageV14===operation.index && operation.index>0)restoreCrew();
    return result;
  };
  function drawStage(){
    const game=state(),board=document.getElementById('board');
    if(!board || !operation)return;
    let strip=document.getElementById('operation-stage-strip');
    if(!strip){strip=document.createElement('div');strip.id='operation-stage-strip';strip.setAttribute('aria-live','polite');
      document.getElementById('combat')?.insertBefore(strip,board);}
    const response=operation.index>0?(operation.carry?.alerted?(operation.securitySuppressed?' // SECURITY RESPONSE: SUPPRESSED':' // SECURITY RESPONSE: ESCALATED'):' // SECURITY RESPONSE: CONTAINED'):'';
    const route=operation.extractionRerouted?' // EXFIL: MAINTENANCE ROUTE':operation.intelExtracted?' // BLACKSITE INTEL: SECURED':'';
    strip.textContent=`OPERATION ${String(operation.index+1).padStart(2,'0')}/03 // ${STEPS[operation.index].name}${response}${route}`;
    const hint=document.getElementById('arena-shape-hint');
    if(hint)hint.textContent=STEPS[operation.index].brief;
    if(game?.objective && operation.index===1){
      // The extraction for this operation happens in its own third area.
      const old=game.objective.exfil;
      if(old){const c=game.grid.find(c=>c.x===old.x&&c.y===old.y);
        c?.el.classList.remove('v14-exfil-cell');if(c?.el)delete c.el.dataset.exfil;}
      game.objective.exfil=null;game.objective.exfilReady=false;
      root.updateObjectiveHud();
    }
    if(game?.objective && operation.index===2){
      // Alarm state now changes the extraction space, not just enemy awareness.
      // Electrified containment lanes are transient combat cells and never enter saves.
      if(operation.carry?.alerted && !operation.securitySuppressed){
        let armed=0;
        for(const [x,y] of [[2,5],[6,5],[4,6],[1,6]]){
          const c=game.grid.find(v=>v.x===x&&v.y===y);
          if(!c||c.arenaVoid||c.obstacle||c.door||c.cover||c.unit||c.objectiveIndex!=null)continue;
          c.hazard=true;c.hazardTypeV12='livewire';c.hazardDamageV12=8;
          c.el.classList.add('hazard','v12-hazard');c.el.dataset.hazard='livewire';
          if(++armed>=2)break;
        }
        root.logMsg?.('ALARM CONSEQUENCE // Containment grid energized on the extraction route.','sys');
      }
      // A real extraction objective replaces a redundant second upload.
      for(const c of game.grid){if(c.objectiveIndex!=null){c.objectiveIndex=null;
        c.el.classList.remove('objective-cell','v12-objective');delete c.el.dataset.kind;}}
      const old=game.objective.exfil;
      if(old){const c=game.grid.find(c=>c.x===old.x&&c.y===old.y);
        c?.el.classList.remove('v14-exfil-cell');if(c?.el)delete c.el.dataset.exfil;}
      const exit=game.grid.find(c=>c.x===4&&c.y===0);
      if(!exit||exit.obstacle||exit.arenaVoid)throw new Error('Operation extraction tile must be traversable');
      game.objective.cells=[];game.objective.progress=1;game.objective.required=1;
      game.objective.completed=true;game.objective.exfil={x:4,y:0};game.objective.exfilReady=false;
      exit.el.classList.add('v14-exfil-cell');exit.el.dataset.exfil='1';
      root.updateObjectiveHud();root.updateCombat();
    }
    if(operation.index===1){
      // Two physical, mutually exclusive opportunities. Both are deliberately on
      // the existing traversable room grid rather than creating an abstract menu.
      const available=openCells(game);
      if(!operation.intelExtracted){
        const c=available.slice().sort((a,b)=>Math.abs(a.x-4)+Math.abs(a.y-4)-(Math.abs(b.x-4)+Math.abs(b.y-4)))[0];
        if(c){c.operationRouteConsoleV14=true;c.el.classList.add('v14-security-console');
          c.el.dataset.operationConsole=operation.extractionRerouted?'rerouted':'route';
          if(operation.extractionRerouted)c.el.classList.add('objective-done');
          operation.routeConsole={x:c.x,y:c.y};}
      }
      if(!operation.extractionRerouted){
        const candidates=available.filter(c=>!c.operationRouteConsoleV14);
        // Place the intel port away from the route port so both actions remain
        // independently reachable through the original action-deck interaction.
        const route=operation.routeConsole;
        const eligible=c=>!route||Math.abs(c.x-route.x)+Math.abs(c.y-route.y)>=3;
        const c=candidates.filter(eligible).sort((a,b)=>
          Math.abs(a.x-3)+Math.abs(a.y-7)-Math.abs(b.x-3)-Math.abs(b.y-7))[0]||candidates[0];
        if(c){c.operationIntelConsoleV14=true;c.el.classList.add('v14-intel-console');
          c.el.dataset.operationConsole=operation.intelExtracted?'secured-intel':'intel';
          if(operation.intelExtracted)c.el.classList.add('objective-done');
          operation.intelConsole={x:c.x,y:c.y};}
      }
    }
    if(operation.index===0 && !operation.securitySuppressed){
      const c=game.grid.filter(v=>!v.arenaVoid&&!v.obstacle&&!v.door&&!v.cover&&!v.unit&&v.objectiveIndex==null)
        .sort((a,b)=>(b.y-a.y)||Math.abs(a.x-4)-Math.abs(b.x-4))[0];
      if(c){c.operationSecurityConsoleV14=true;c.el.classList.add('v14-security-console');c.el.dataset.operationConsole='security';operation.console={x:c.x,y:c.y};}
    }
  }
  function launch(){
    operation.changing=true;
    try{oldInit.call(root,stageMission());drawStage();}
    finally{operation.changing=false;}
  }
  function clear(){document.getElementById('operation-stage-strip')?.remove();operation=null;}
  root.initCombat=function(mission){
    if(operation && state()?.activeMission!==operation.mission)clear();
    if(!operation && eligible(mission) && state()?.activeMission===mission){
      operation={mission,index:0,carry:null,changing:false,securitySuppressed:false,extractionRerouted:false,intelExtracted:false,console:null,routeConsole:null,intelConsole:null};
      try{return launch();}catch(e){clear();throw e;}
    }
    if(!operation)document.getElementById('operation-stage-strip')?.remove();
    return oldInit.apply(this,arguments);
  };
  root.objectiveActionAvailable=function(u){
    // Mandatory mission objectives always take precedence when a tile happens to
    // overlap an optional operation console.  Earlier builds let REROUTE/OVERRIDE
    // shadow BREACH/HEIST actions, which could make progression appear blocked.
    const mandatory=oldObjectiveAction?.apply(this,arguments)||null;
    if(mandatory)return mandatory;
    if(operation && operation.index===1 && !operation.extractionRerouted && !operation.intelExtracted && operation.routeConsole && u?.team==='player' && state()?.turn==='player'){
      const d=Math.abs(u.x-operation.routeConsole.x)+Math.abs(u.y-operation.routeConsole.y);
      if(d<=1){const cost=['Hacker','AgentEX'].includes(u.className)?1:2;return{label:`REROUTE EXFIL · ${cost} AP`,run:()=>{
        if(u.ap<cost){root.logMsg?.(`Need ${cost} AP to reroute extraction.`,'sys');return false;}
        if(operation.intelExtracted||operation.extractionRerouted||operation.index!==1)return false;
        u.ap-=cost;operation.extractionRerouted=true;const c=state().grid.find(v=>v.operationRouteConsoleV14);
        if(c){c.el.classList.add('objective-done');c.el.dataset.operationConsole='rerouted';}
        const intel=state().grid.find(v=>v.operationIntelConsoleV14);
        if(intel){intel.el.classList.add('objective-done');intel.el.dataset.operationConsole='locked';}
        root.logMsg?.('EXFIL REROUTED // Maintenance corridor unlocked. Blacksite intel opportunity forfeited.','good');
        root.floatText?.(u.x,u.y,'MAINTENANCE EXFIL','#79f4b6');drawStage();root.updateCombat?.();return true;}};
      }
    }
    if(operation && operation.index===1 && !operation.extractionRerouted && !operation.intelExtracted && operation.intelConsole && u?.team==='player' && state()?.turn==='player'){
      const d=Math.abs(u.x-operation.intelConsole.x)+Math.abs(u.y-operation.intelConsole.y);
      if(d<=1){const cost=['Hacker','AgentEX'].includes(u.className)?1:2;
        return{label:`STEAL BLACKSITE INTEL · ${cost} AP / +¢${intelBonus(operation.mission)} ON EXFIL`,run:()=>{
          if(u.ap<cost){root.logMsg?.(`Need ${cost} AP to extract blacksite intelligence.`,'sys');return false;}
          if(operation.extractionRerouted||operation.intelExtracted||operation.index!==1)return false;
          u.ap-=cost;operation.intelExtracted=true;
          const c=state().grid.find(v=>v.operationIntelConsoleV14);
          if(c){c.el.classList.add('objective-done');c.el.dataset.operationConsole='secured-intel';}
          const route=state().grid.find(v=>v.operationRouteConsoleV14);
          if(route){route.el.classList.add('objective-done');route.el.dataset.operationConsole='locked';}
          root.logMsg?.(`INTEL SECURED // +¢${intelBonus(operation.mission)} on successful extraction. Maintenance exfil is now unavailable.`,'good');
          root.floatText?.(u.x,u.y,'BLACKSITE INTEL','#efc16d');drawStage();root.updateCombat?.();return true;
        }};
      }
    }
    if(operation && operation.index===0 && !operation.securitySuppressed && operation.console && u?.team==='player' && state()?.turn==='player'){
      const d=Math.abs(u.x-operation.console.x)+Math.abs(u.y-operation.console.y);
      if(d<=1){const cost=['Hacker','AgentEX'].includes(u.className)?1:2;return{label:`OVERRIDE SECURITY · ${cost} AP`,run:()=>{
        if(u.ap<cost){root.logMsg?.(`Need ${cost} AP to override site security.`,'sys');return false;}
        u.ap-=cost;operation.securitySuppressed=true;const c=state().grid.find(v=>v.operationSecurityConsoleV14);
        if(c){c.el.classList.add('objective-done');c.el.dataset.operationConsole='suppressed';}
        root.logMsg?.('SECURITY OVERRIDE // Response dispatch and extraction containment disabled.','good');
        root.floatText?.(u.x,u.y,'RESPONSE SUPPRESSED','#79f4b6');root.updateCombat?.();return true;}};
      }
    }
    return null;
  };
  function nextArea(){
    if(!operation||operation.changing||operation.index>=2)return false;
    const game=state();operation.carry=snapshot();
    operation.index++;
    root.logMsg?.(`AREA SECURED // ${STEPS[operation.index].name}`, 'good');
    launch();
    // A stage boundary is a safe durable checkpoint. Never capture unfinished
    // combat-grid state, and never award a payout or advance campaign time here.
    root.saveGame?.(0,true);
    return true;
  }
  root.checkWinLose=function(){
    const game=state();
    if(operation&&!operation.changing&&!game.gameOver && game.activeMission===operation.mission){
      const survivors=game.units.filter(u=>u.team==='player'&&u.hp>0);
      if(survivors.length && game.objective?.completed && operation.index<2 &&
         (operation.index===0 || !game.objective.exfil || game.objective.exfilReady)){
        nextArea();return;
      }
      if(!survivors.length || (operation.index===2 && game.objective?.exfilReady)){
        // Only a surviving squad reaching final extraction can cash in the intel.
        // The existing success handler owns the ONE payout, journal save and
        // mission-history entry; stage boundaries never grant resources.
        if(operation.index===2&&survivors.length&&game.objective?.exfilReady&&operation.intelExtracted&&!operation.intelSettled){
          operation.intelSettled=true;
          const bonus=intelBonus(operation.mission);
          operation.mission.reward=(Number(operation.mission.reward)||0)+bonus;
          operation.mission.operationIntelRecoveredV14={bonus,route:'security'};
          game.journal?.unshift({type:'contract',title:'Blacksite intelligence recovered',
            desc:`Recovered classified site intelligence during ${operation.mission.name}. Added ¢${bonus} to the completed contract payout.${operation.mission.contact?' A separate intelligence lead can be resolved in person with the commissioning contact.':''}`,
            status:operation.mission.contact?'Visit the commissioning contact to resolve the intelligence lead':'Recovered intelligence settled',
            day:game.day,id:`intel_${operation.mission.id}`});
          root.logMsg?.(`BLACKSITE INTEL // ¢${bonus} added to final contract payout.`,'good');
        }
        const result=oldCheck.apply(this,arguments);
        if(game.gameOver)clear();
        return result;
      }
      // Intermediate areas cannot accidentally award victory on enemy elimination.
      return;
    }
    return oldCheck.apply(this,arguments);
  };
  // Emergency extraction must never leave a stale operation attached to a later contract.
  const prevReturn=root.returnToOverworld;
  if(typeof prevReturn==='function')root.returnToOverworld=function(){clear();return prevReturn.apply(this,arguments);};
  function exportCheckpoint(){
    if(!operation||operation.changing||operation.index<1||operation.index>2 ||
       state()?.activeMission!==operation.mission||state()?.gameOver||!operation.carry)return null;
    return {version:1,index:operation.index,mission:JSON.parse(JSON.stringify(operation.mission)),
      alerted:!!operation.carry.alerted,securitySuppressed:!!operation.securitySuppressed,
      extractionRerouted:!!operation.extractionRerouted,intelExtracted:!!operation.intelExtracted,
      crew:Object.fromEntries(operation.carry.crew)};
  }
  root.serializeGame=function(){
    const raw=oldSerialize.apply(this,arguments),data=JSON.parse(raw),checkpoint=exportCheckpoint();
    if(checkpoint)data[checkpointKey]=checkpoint;
    return JSON.stringify(data);
  };
  function readCheckpoint(slot){
    // The v14 persistence bridge hydrates this same compatibility key before
    // calling the legacy loader, including on checksum-validated backup restore.
    try{
      const data=JSON.parse(root.localStorage?.getItem(`chrome_requiem_v13_${Number(slot)}`)||'null');
      return data?.[checkpointKey]||null;
    }catch{return null;}
  }
  function validCheckpoint(cp){
    return !!cp&&cp.version===1&&Number.isInteger(cp.index)&&cp.index>=1&&cp.index<=2&&
      cp.mission&&typeof cp.mission.id==='string'&&eligible(cp.mission)&&
      !(cp.intelExtracted&&cp.extractionRerouted)&&
      cp.crew&&typeof cp.crew==='object'&&!Array.isArray(cp.crew);
  }
  root.loadGame=function(slot=0){
    // Read before the v13 migration loaders run; some of those loaders autosave
    // their reconstructed city state as part of a successful load.
    const cp=readCheckpoint(slot);
    clear();
    const ok=oldLoad.apply(this,arguments);
    if(!ok||!validCheckpoint(cp))return ok;
    try{
      const game=state();
      operation={mission:cp.mission,index:cp.index,changing:false,
        carry:{alerted:!!cp.alerted,crew:new Map(Object.entries(cp.crew))},
        securitySuppressed:!!cp.securitySuppressed,
        extractionRerouted:!!cp.extractionRerouted,intelExtracted:!!cp.intelExtracted,
        console:null,routeConsole:null,intelConsole:null};
      game.activeMission=operation.mission;
      root.showScreen('combat');
      launch();
      root.logMsg?.('OPERATION CHECKPOINT // Re-entered current area at its entrance.','good');
      // Recommit a fully restored state after legacy migration/autosave writes.
      root.saveGame?.(Number(slot),true);
    }catch(err){
      console.warn('[CR14] operation checkpoint resume skipped:',err?.message||err);
      clear();state().activeMission=null;root.showScreen('overworld-screen');
    }
    return ok;
  };
  if(typeof oldNewGame==='function')root.startNewGame=function(){clear();return oldNewGame.apply(this,arguments);};
  // PWA12.67 — Intel remains useful after extraction: the commissioning contact
  // has a physical location, so the squad must visit them to resolve the lead.
  // The mission-history record is the acquisition source of truth, and a journal
  // entry is the durable one-time resolution marker (both survive schema-14 saves).
  const leadKey=(m,index)=>`intel_debrief_${index}_${m.id}`;
  const pendingLeads=(contactId)=>{
    const game=state();
    return (game?.missionHistory||[]).flatMap((m,index)=>
      m?.operationIntelRecoveredV14 && m.contact===contactId &&
      !(game.journal||[]).some(j=>j.id===leadKey(m,index))
        ? [{mission:m,index,key:leadKey(m,index)}] : []);
  };
  const nearContact=(contactId)=>{
    const game=state(),contact=game?.contacts?.find(c=>c.id===contactId);
    const player=game?.ovPlayer;
    // District maps can reuse local coordinates. A matching (x,y) in another
    // district is NOT a physical meeting with this contact.
    const district=game?.districtWorldsV133?.activeId;
    if(district&&contact?.sectorId&&district!==contact.sectorId)return false;
    return !!contact&&!!player&&Number.isFinite(player.x)&&Number.isFinite(player.y)&&
      Math.abs(player.x-contact.x)<=4&&Math.abs(player.y-contact.y)<=4;
  };
  function resolveLead(contactId,leadKeyId,decision){
    const game=state();
    if(!game||game.activeMission||!nearContact(contactId)||!['disclose','erase'].includes(decision))return false;
    const lead=pendingLeads(contactId).find(item=>item.key===leadKeyId);
    const contact=game.contacts.find(c=>c.id===contactId);
    if(!lead||!contact)return false;
    const faction=contact.faction;
    // Consume the lead BEFORE modifying relationship/heat, so repeat clicks or
    // reentrant dossier redraws cannot apply the benefit twice.
    game.journal.unshift({id:lead.key,type:'contract',title:'Blacksite intelligence resolved',
      desc:decision==='disclose'
        ?`Disclosed the recovered ${lead.mission.name} dossier to ${contact.name}. Trust increased by 8; ${faction} security heat increased by 6.`
        :`Erased the recovered ${lead.mission.name} dossier in the presence of ${contact.name}. ${faction} security heat reduced by 8; no intelligence was disclosed.`,
      status:decision==='disclose'?'Shared with contact':'Destroyed in person',decision,sourceMissionId:lead.mission.id,day:game.day});
    game.heat=game.heat&&typeof game.heat==='object'?game.heat:{};
    game.heat[faction]=Math.max(0,Math.min(100,(Number(game.heat[faction])||0)+(decision==='disclose'?6:-8)));
    if(decision==='disclose')root.changeContactTrustV13?.(contactId,8,'Shared recovered blacksite intelligence in person.');
    // Expose a single authored follow-up contract that is tied to this dossier.
    // Only completed mission-history entries close it; no duplicate payout or
    // persistent schema extension is needed. Rehydrate it after daily job refresh.
    ensureFollowUp(contactId);
    root.logMsg?.(decision==='disclose'
      ?`INTEL TRADED // ${contact.name}: trust +8; ${faction} heat +6.`
      :`INTEL ERASED // ${faction} heat -8; contact trust unchanged.`, 'good');
    root.saveGame?.(0,true);
    root.renderContactDossierV13?.(contactId);
    return true;
  }
  // A dossier is not merely a heat/trust trade. Resolving it creates a distinct
  // city-linked operation; the original blacksite payout has already settled.
  // Follow-up IDs derive from the durable source mission id and resolved choice.
  const followUpId=(sourceMissionId,decision)=>`intel_followup_${sourceMissionId}_${decision}`;
  function followUpFor(record){
    const game=state();
    // A pre-12.68 saved journal entry has the original lead key and human-readable
    // choice but lacks structured fields. Recover it without replaying the choice.
    const source=(game?.missionHistory||[]).find((m,i)=>m.id===record.sourceMissionId || leadKey(m,i)===record.id);
    const decision=record.decision || (record.desc?.startsWith('Disclosed the recovered ')?'disclose':record.desc?.startsWith('Erased the recovered ')?'erase':null);
    if(!source?.operationIntelRecoveredV14||!['disclose','erase'].includes(decision))return null;
    const contact=game.contacts?.find(c=>c.id===source.contact);
    if(!contact)return null;
    const target=source.targetFaction||contact.faction;
    const diff=Math.min(3,Math.max(1,Number(source.diff)||2));
    const disclose=decision==='disclose';
    return{id:followUpId(source.id,decision),contact:contact.id,
      // Preserve the actual district of the compromised site, independent of
      // where its commissioning contact is currently standing.
      sectorId:source.sectorId||contact.sectorId,
      type:disclose?'sabotage':'extract',objective:disclose?'sabotage':'extract',
      name:disclose?'CUT THE AUDIT':'GHOST THE TRAIL',
      desc:disclose
        ?`The ${source.name} files exposed a live audit relay. Disable the relay before ${target} traces the leak back to your contact.`
        :`The ${source.name} dossier is ash, but ${target} still holds a mirrored access trace. Recover and wipe its remaining ledger.`,
      enemies:disclose?['Guard','Drone','Enforcer']:['Guard','Drone','Guard'],
      diff,reward:(disclose?440:370)+diff*130,xp:85+diff*35,
      targetFaction:target,factionRepGain:4+diff,
      factionRepLoss:{[target]:-(4+diff)},
      multiStageDisabled:true,intelFollowUpV14:{sourceMissionId:source.id,decision}};
  }
  function ensureFollowUp(contactId){
    const game=state(),contact=game?.contacts?.find(c=>c.id===contactId);
    if(!contact)return [];
    if(!Array.isArray(contact.missions))contact.missions=[];
    // An already-open dossier can outlive an operation's completion. Remove only
    // finished intel jobs; leave normal contact work and uncompleted intel intact.
    const finished=new Set((game.missionHistory||[]).map(done=>done?.id));
    contact.missions=contact.missions.filter(offered=>!offered?.intelFollowUpV14 || !finished.has(offered.id));
    const jobs=[];
    for(const entry of game.journal||[]){
      if(!entry?.id?.startsWith('intel_debrief_'))continue;
      const m=followUpFor(entry);
      if(!m||m.contact!==contactId)continue;
      if(!entry.sourceMissionId){entry.sourceMissionId=m.intelFollowUpV14.sourceMissionId;entry.decision=m.intelFollowUpV14.decision;}
      if((game.missionHistory||[]).some(done=>done.id===m.id))continue;
      const existing=contact.missions.find(offered=>offered.id===m.id);
      if(existing){
        // Older schema-14 saves may already hold this job without its site;
        // repair only the missing location, never reset an accepted mission.
        if(!existing.sectorId)existing.sectorId=m.sectorId;
      }else contact.missions.push(m);
      jobs.push(existing||m);
    }
    return jobs;
  }
  // City dossiers can be read from remote city menus; the actual follow-up
  // operation must be commissioned in person like the original intel handoff.
  const previousStartMission=root.startMission;
  if(typeof previousStartMission==='function')root.startMission=function(mission){
    if(mission?.intelFollowUpV14){
      const game=state();
      // Never trust a stale DOM card or an old mission object: only a still-open
      // history-backed job on this contact's current board may be commissioned.
      const offered=ensureFollowUp(mission.contact).some(job=>job.id===mission.id);
      const completed=(game?.missionHistory||[]).some(done=>done?.id===mission.id);
      if(completed||!offered){
        root.logMsg?.('INTEL ARCHIVED // This intelligence operation is no longer available.','sys');
        return false;
      }
      if(!nearContact(mission.contact)||game?.activeMission){
        root.logMsg?.('CONTACT REQUIRED // Visit the commissioning contact in the city before accepting this intelligence operation.','sys');
        return false;
      }
    }
    return previousStartMission.apply(this,arguments);
  };
  // PWA12.71: Close the intelligence loop at the actual mission-success event.
  // The core has already committed base reward, XP, reputation, and mission history
  // when this event fires; apply only the authored secondary world consequence.
  // The outcome journal id is the idempotency barrier across duplicate events,
  // resumed saves, and stale UI calls, and requires no save-schema migration.
  function settleFollowUp(mission){
    if(!mission?.intelFollowUpV14||!['disclose','erase'].includes(mission.intelFollowUpV14.decision))return false;
    const game=state();if(!game)return false;
    const done=(game.missionHistory||[]).find(m=>m?.id===mission.id);
    const contact=game.contacts?.find(c=>c.id===mission.contact);
    const origin=(game.missionHistory||[]).find(m=>m?.id===mission.intelFollowUpV14.sourceMissionId);
    const debrief=(game.journal||[]).find(j=>j?.id?.startsWith('intel_debrief_') &&
      (j.sourceMissionId===origin?.id || (origin && j.id.endsWith('_'+origin.id))));
    const id=`intel_outcome_${mission.id}`;
    if(!done||!origin?.operationIntelRecoveredV14||!contact||!debrief||
       debrief.decision!==mission.intelFollowUpV14.decision||
       (game.journal||[]).some(j=>j?.id===id))return false;
    const disclosed=debrief.decision==='disclose';
    const faction=mission.targetFaction||origin.targetFaction||contact.faction;
    if(!faction)return false;
    game.heat=game.heat&&typeof game.heat==='object'?game.heat:{};
    const before=Math.max(0,Math.min(100,Number(game.heat[faction])||0));
    // Core mission success already increased target heat by twice the target's
    // reputation penalty. Neutralize that exposure AND actually lower the city's
    // security pressure, rather than advertising a reduction whose net is zero.
    const ordinaryExposure=Math.max(0,-(Number(mission.factionRepLoss?.[faction])||0))*2;
    const after=Math.max(0,before-ordinaryExposure-(disclosed?8:14));
    const delta=after-before;
    game.heat[faction]=after;
    // This contact's own files were disclosed; completing the cover-up builds a
    // small additional relationship. Erasing evidence never grants that benefit.
    if(disclosed)root.changeContactTrustV13?.(contact.id,3,'The squad severed the audit trail after delivering recovered blacksite intelligence.');
    done.intelAftermathV14={decision:debrief.decision,heatReduced:-delta,contactTrustGained:disclosed?3:0};
    if(!Array.isArray(game.journal))game.journal=[];
    game.journal.push({id,type:'contract',title:disclosed?'Audit relay silenced':'Access mirror erased',
      desc:disclosed
        ?`${contact.name}'s audit relay is offline. ${faction} heat ${delta}; contact trust +3.`
        :`The mirrored access ledger was wiped. ${faction} heat ${delta}; no contact intelligence was shared.`,
      status:'Closed',sourceMissionId:origin.id,missionId:mission.id,decision:debrief.decision,
      // The physical aftermath belongs to the raided site, not to the contact's
      // district. Derive street pressure from this durable entry after loading.
      districtId:mission.sectorId||origin.sectorId||null,day:game.day});
    root.logMsg?.(disclosed
      ?`INTEL AFTERMATH // Audit relay disabled; ${faction} heat ${delta}; contact trust +3.`
      :`INTEL AFTERMATH // Mirror wiped; ${faction} heat ${delta}.`,'good');
    return true;
  }
  // In the ordered classic runtime bundle, Events is the canonical core event
  // bus. Do not wrap finalizeMissionSuccess or alter the underlying rewards.
  if(typeof Events!=='undefined'&&typeof Events.on==='function')Events.on('mission:success',settleFollowUp);
  const priorDossier=root.renderContactDossierV13;
  if(typeof priorDossier==='function'){
    root.renderContactDossierV13=function(contactId){
      // Rebuild persistent intelligence work after ordinary mission-board refresh.
      ensureFollowUp(contactId);
      const result=priorDossier.apply(this,arguments);
      const game=state(),host=root.document?.getElementById('v13-contracts');
      if(host && !nearContact(contactId))for(const card of host.querySelectorAll?.('[data-m]')||[]){
        const mission=game?.contacts?.find(c=>c.id===contactId)?.missions?.find(m=>m.id===card.dataset.m);
        if(mission?.intelFollowUpV14){card.classList.add('v14-intel-remote');card.setAttribute('aria-label',mission.name+' — visit contact in person to accept');}
      }
      if(host)for(const card of host.querySelectorAll?.('[data-m]')||[]){
        const mission=game?.contacts?.find(c=>c.id===contactId)?.missions?.find(m=>m.id===card.dataset.m);
        if(mission?.intelFollowUpV14){
          card.classList.add('v14-intel-followup-card');
          const heading=card.querySelector('h4');if(heading)heading.textContent=`INTEL AFTERMATH // ${mission.name}`;
        }
      }
      if(!host||!game?.contacts?.some(c=>c.id===contactId))return result;
      const leads=pendingLeads(contactId);
      // The same durable journal entries drive the readable casefile history.
      // This presentation is read-only: opening it never advances time or alters
      // relationships, heat, mission state, or the save schema.
      const resolved=(game.journal||[]).filter(entry=>entry?.id?.startsWith('intel_debrief_'))
        .map(entry=>({entry,mission:followUpFor(entry)}))
        .filter(item=>item.mission?.contact===contactId);
      if(resolved.length){
        const ledger=root.document.createElement('details');ledger.className='v14-intel-ledger';
        const summary=root.document.createElement('summary');
        const finished=resolved.filter(({mission})=>(game.missionHistory||[]).some(done=>done?.id===mission.id)).length;
        summary.textContent=`INTEL CASEFILES // ${resolved.length} RESOLVED · ${finished} CLOSED`;
        ledger.appendChild(summary);
        const list=root.document.createElement('div');list.className='v14-intel-ledger-list';
        for(const {entry,mission} of resolved.slice(0,6)){
          const closed=(game.missionHistory||[]).some(done=>done?.id===mission.id);
          const active=game.activeMission?.id===mission.id;
          const row=root.document.createElement('div');row.className='v14-intel-ledger-row';
          const heading=root.document.createElement('strong');heading.textContent=`${mission.name} // ${closed?'CLOSED':active?'IN PROGRESS':'AVAILABLE'}`;
          const caption=root.document.createElement('span');
          const outcome=game.journal.find(j=>j?.id===`intel_outcome_${mission.id}`);
          caption.textContent=`${entry.decision==='erase'?'ERASED':'DISCLOSED'} · ${mission.targetFaction} · ${closed?(outcome?.desc||'Contract complete; historical outcome archived'):'Return to this contact to commission follow-up'}`;
          row.append(heading,caption);list.appendChild(row);
        }
        ledger.appendChild(list);
        host.insertBefore(ledger,host.firstChild);
      }
      if(!leads.length)return result;
      const physicallyPresent=nearContact(contactId)&&!game.activeMission;
      const section=root.document.createElement('section');
      section.className='v14-intel-leads';
      const title=root.document.createElement('div');
      title.className='v13-section-title';title.textContent=`RECOVERED INTELLIGENCE // ${leads.length} UNRESOLVED`;
      section.appendChild(title);
      for(const lead of leads){
        const card=root.document.createElement('div');card.className='v14-intel-lead';
        const heading=root.document.createElement('h4');heading.textContent=`${lead.mission.name} // BLACKSITE DOSSIER`;
        const copy=root.document.createElement('p');copy.textContent=physicallyPresent
          ?'The contact can use the stolen files, but distribution alerts the target faction. Destroying them reduces its active security pressure.'
          :'IN-PERSON HANDOFF REQUIRED // Reach this contact on the city map to resolve the dossier.';
        card.append(heading,copy);
        // Read-only briefing before a one-way choice: show the two distinct
        // operation outcomes without modifying state or charging action time.
        const difficulty=Math.min(3,Math.max(1,Number(lead.mission.diff)||2));
        const preview=root.document.createElement('div');preview.className='v14-intel-choice-preview';
        for(const [choice,name,objective,payout,trust,heat] of [
          ['DISCLOSE','CUT THE AUDIT','Sabotage the live audit relay',440+difficulty*130,'+8 now, +3 after success','+6 now; up to -8 net after success'],
          ['ERASE','GHOST THE TRAIL','Extract and wipe the mirrored access ledger',370+difficulty*130,'No intelligence trust bonus','-8 now; up to -14 net after success']]){
          const option=root.document.createElement('div');option.className='v14-intel-choice-option';
          const nameNode=root.document.createElement('strong');nameNode.textContent=`${choice} → ${name}`;
          const detail=root.document.createElement('span');detail.textContent=`${objective} · ${payout}₡ · ${trust} · Faction heat ${heat}`;
          option.append(nameNode,detail);preview.appendChild(option);
        }
        card.appendChild(preview);
        if(physicallyPresent){
          const actions=root.document.createElement('div');actions.className='v14-intel-lead-actions';
          for(const [choice,label] of [['disclose','DISCLOSE // TRUST +8 · HEAT +6'],['erase','ERASE // FACTION HEAT -8']]){
            const button=root.document.createElement('button');button.type='button';
            button.className='btn small';button.textContent=label;
            button.addEventListener('click',()=>resolveLead(contactId,lead.key,choice));
            actions.appendChild(button);
          }
          card.appendChild(actions);
        }
        section.appendChild(card);
      }
      host.insertBefore(section,host.firstChild);
      return result;
    };
  }
  root.CR14MultiStageOperations=Object.freeze({eligible,steps:STEPS,
    exportCheckpoint,pendingLeads,nearContact,resolveLead,followUpFor,ensureFollowUp,settleFollowUp,
    get active(){return operation?{id:operation.mission.id,index:operation.index,count:STEPS.length,securitySuppressed:operation.securitySuppressed,extractionRerouted:operation.extractionRerouted,intelExtracted:operation.intelExtracted,console:operation.console,routeConsole:operation.routeConsole,intelConsole:operation.intelConsole}:null;}});
})(globalThis);
