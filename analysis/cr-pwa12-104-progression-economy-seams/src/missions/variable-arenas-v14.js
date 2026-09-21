/* Chrome Requiem PWA12.41 — mission-specific physical tactical footprints.
 * A ten-by-ten backing grid is deliberately retained for legacy combat, saves,
 * animation coordinates and touch geometry. Void cells are impassable and opaque.
 * Shape, objectives and squad deployment change together; only combat state changes.
 */
(function installVariableArenasV14(root) {
  'use strict';
  if (!root.document || typeof root.buildGrid !== 'function' || typeof root.createCombatUnits !== 'function') return;

  const state=()=>root.ChromeRequiemCoreV5?.state;
  const LAYOUTS = Object.freeze({
    corridor: {
      name: 'SERVICE CORRIDOR', kind: 'SINGLE BREACH',
      rows: [
        '  ......  ',
        '  ......  ',
        '  ##D###  ',
        '   ....   ',
        '   ....   ',
        '   ....   ',
        '   ....   ',
        '   ....   ',
        '  ......  ',
        '  ......  '
      ],
      covers: [[2,1],[7,1],[3,5],[6,7]],
      objectivePoints: [[4,1],[3,1],[6,1]],
      playerPoints: [[3,9],[4,9],[5,9],[3,8],[5,8]],
      enemyPoints: [[3,0],[6,0],[2,1],[7,1],[3,1],[6,1],[4,0],[5,0],[2,0],[7,0],[4,1],[5,1]]
    },
    entrance: {
      name: 'BUILDING ENTRANCE', kind: 'SECURITY VESTIBULE',
      rows: [
        '  ......  ',
        ' ........ ',
        ' ........ ',
        ' ###DD### ',
        ' ........ ',
        ' ........ ',
        '  ......  ',
        '  ......  ',
        '   ....   ',
        '   ....   '
      ],
      covers: [[2,1],[7,1],[2,5],[7,5],[3,7],[6,7]],
      objectivePoints: [[4,1],[3,1],[6,1]],
      playerPoints: [[3,9],[4,9],[5,9],[6,9],[3,8]],
      enemyPoints: [[2,0],[7,0],[2,1],[7,1],[3,0],[6,0],[3,1],[6,1],[4,0],[5,0],[4,1],[5,1]]
    },
    alley: {
      name: 'NEON SERVICE ALLEY', kind: 'STREET CROSSFIRE',
      rows: ['..........','..........','..........','..........','..........','..........','..........','..........','..........','..........'],
      covers: [[1,2],[4,3],[7,2],[2,6],[5,7],[8,6]],
      objectivePoints: [[4,2],[5,2],[4,5]],
      playerPoints: [[3,9],[4,9],[5,9],[6,9],[2,8]],
      enemyPoints: [[2,0],[4,0],[6,0],[8,1],[1,2],[5,1],[7,2],[3,1],[9,2],[0,1],[5,0],[7,0]]
    },
    checkpoint: {
      name: 'CORPORATE CHECKPOINT', kind: 'PATROL CORDON',
      rows: ['..........','..........','..........','..........','..........','..........','..........','..........','..........','..........'],
      covers: [[1,2],[3,2],[6,2],[8,2],[2,5],[7,5],[4,7],[5,7]],
      objectivePoints: [[4,2],[5,2],[4,5]],
      playerPoints: [[3,9],[4,9],[5,9],[6,9],[2,8]],
      enemyPoints: [[2,0],[4,0],[5,0],[7,0],[1,1],[8,1],[3,2],[6,2],[0,2],[9,2],[4,1],[5,1]]
    },
    underpass: {
      name: 'SERVICE UNDERPASS', kind: 'CONSTRICTED STREET FIGHT',
      rows: [' ........ ','..........','..........','..........','..........','..........','..........','..........','..........',' ........ '],
      covers: [[1,2],[8,2],[3,4],[6,4],[2,7],[7,7]],
      objectivePoints: [[4,2],[5,2],[4,5]],
      playerPoints: [[3,9],[4,9],[5,9],[6,9],[2,8]],
      enemyPoints: [[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[1,1],[8,1],[3,2],[6,2],[4,1],[5,1]]
    },
    rooms: {
      name: 'SECURED INTERIOR', kind: 'LINKED ROOMS',
      rows: [
        '  ......  ',
        '  ......  ',
        '  ##D###  ',
        '  ...#..  ',
        '  ...D..  ',
        '  ...#..  ',
        '  ##D###  ',
        '  ......  ',
        '  ......  ',
        '   ....   '
      ],
      covers: [[2,1],[7,1],[2,4],[7,4],[2,8],[7,8]],
      objectivePoints: [[3,8],[4,4],[4,1]],
      playerPoints: [[3,9],[4,9],[5,9],[6,9]],
      enemyPoints: [[3,0],[6,0],[2,1],[7,1],[3,1],[6,1],[4,0],[5,0],[4,1],[5,1],[6,3],[7,5]]
    }
  });

  function choose(mission) {
    if (!mission || (['boss','rival'].includes(mission.type) || mission.oracleKey) && !mission.tacticalShape) return null;
    if (mission.tacticalShape === 'open') return null;
    if ((mission.enemies?.length||0)>8 && !mission.tacticalShape) return null;
    if (LAYOUTS[mission.tacticalShape]) return mission.tacticalShape;
    const type = mission.objective || mission.type;
    if (type === 'breach' || type === 'sabotage') return 'corridor';
    if (type === 'raid' || type === 'steal') return 'entrance';
    if (type === 'heist' || type === 'rescue') return 'rooms';
    if (type === 'extract') return (mission.sectorId==='undergrid'||mission.worldLocation==='reykjavik') ? 'corridor' : 'rooms';
    return null; // Large open terrain remains appropriate for battles/holding actions.
  }

  function reset(c) {
    if (!c) return;
    Object.assign(c, {obstacle:false,cover:false,hazard:false,coverDir:null,coverHp:0,coverMax:0,
      rubble:false,transparentObstacle:false,door:false,doorOpen:false,doorLocked:false,
      elevation:0,hazardTypeV12:null,hazardDamageV12:0,hazardStatusV12:null,
      coverTypeV12:null,wallTypeV12:null,objectiveIndex:undefined,hackable:false,hacked:false});
    c.el.className='cell';
    for (const key of ['material','cover','hazard','kind','exfil']) delete c.el.dataset[key];
  }
  function wall(c) {
    reset(c);c.obstacle=true;c.wallTypeV12='concrete';
    c.el.classList.add('obstacle','v12-wall');c.el.dataset.material='concrete';
  }
  function door(c,locked) {
    reset(c);c.door=true;c.doorLocked=locked;c.doorOpen=false;
    c.obstacle=true;c.wallTypeV12='security';
    c.el.classList.add('v12-door');if(locked)c.el.classList.add('locked');
  }
  function cover(c,type) {
    reset(c);c.cover=true;c.coverTypeV12=type;c.coverHp=18;c.coverMax=18;
    c.coverDir=['N','S','E','W'][(c.x+c.y)%4];
    c.el.classList.add('cover','v12-cover');c.el.dataset.cover=type;
  }
  function point(x, y) { return state().grid[y * 10 + x]; }
  function floorAt(x, y) {
    return x >= 0 && x < 10 && y >= 0 && y < 10 && !point(x,y).arenaVoid;
  }
  function objectivePositions(type, shape) {
    if (type === 'heist') return [[3,8],[4,4],[4,1]];
    if (type === 'rescue' || type === 'steal') return [[4,1],[4,8]];
    if (type === 'extract') return [[4,1]];
    if (type === 'sabotage' || type === 'breach' || type === 'raid' || type === 'secure') return [[3,1],[6,1]];
    if (type === 'hold') return [[4,4]];
    return shape.objectivePoints;
  }
  const DISTRICT_THEMES=Object.freeze({
    undergrid:{id:'undergrid',label:'UNDERGRID',cover:'utility',surface:'service'},
    floodline:{id:'floodline',label:'FLOODLINE',cover:'flood',surface:'wet'},
    dock_nine:{id:'dock_nine',label:'DOCK NINE',cover:'freight',surface:'dock'},
    crown_spire:{id:'crown_spire',label:'CROWN SPIRE',cover:'security',surface:'corporate'},
    old_market:{id:'old_market',label:'OLD MARKET',cover:'market',surface:'market'},
    neon_row:{id:'neon_row',label:'NEON ROW',cover:'street',surface:'neon'}
  });
  function districtTheme(mission){
    const id=mission?.sectorId||'unknown';
    return DISTRICT_THEMES[id]||{id,label:String(id).replaceAll('_',' ').toUpperCase(),cover:'street',surface:'street'};
  }
  const STREET_CONTROL_LABELS=Object.freeze({
    undergrid:'BREAKER BOX',
    floodline:'DRAINAGE PUMP',
    dock_nine:'POWER ISOLATOR',
    neon_row:'UTILITY JUNCTION'
  });
  // PWA12.102 — tell the player what spending the AP will actually do before
  // activation. Keep this presentation-only: the effect implementation below remains
  // the single source of gameplay truth.
  const STREET_CONTROL_EFFECT_PREVIEWS=Object.freeze({
    undergrid:'CUT HOSTILE OVERWATCH',
    floodline:'CLEAR POISON + RUNOFF',
    dock_nine:'STALL HOSTILES 1 TURN',
    neon_row:'CLOAK OPERATOR 1 TURN'
  });
  // PWA12.94 — Street Clashes inherit a small amount of tactical danger from
  // the physical district. These are intentionally sparse and never occupy
  // deployment, objective, cover or door cells. Ordinary contracts are unchanged.
  const STREET_DISTRICT_HAZARDS=Object.freeze({
    undergrid:[{x:5,y:5,type:'livewire',damage:7,status:'shock'}],
    floodline:[{x:4,y:6,type:'runoff',damage:5,status:'poison'},{x:6,y:6,type:'runoff',damage:5,status:'poison'}],
    dock_nine:[{x:5,y:4,type:'livewire',damage:6,status:'shock'}],
    neon_row:[{x:4,y:6,type:'livewire',damage:6,status:'shock'}]
  });
  function applyStreetDistrictHazards(mission,shape){
    if(!mission?.v134StreetEncounter)return;
    const specs=STREET_DISTRICT_HAZARDS[mission.sectorId]||[];
    if(!specs.length)return;
    const reserved=new Set([...shape.playerPoints,...shape.enemyPoints,...objectivePositions(state().objective?.type,shape)].map(([x,y])=>y*10+x));
    for(const spec of specs){
      const {x,y}=spec;if(reserved.has(y*10+x))continue;
      const c=point(x,y);
      if(!c||c.arenaVoid||c.obstacle||c.door||c.cover||c.objectiveIndex!=null||c.hackable)continue;
      c.hazard=true;c.hazardTypeV12=spec.type;c.hazardDamageV12=spec.damage;c.hazardStatusV12=spec.status||null;
      c.el.classList.add('hazard','v12-hazard','v14-district-hazard');c.el.dataset.hazard=spec.type;
    }
  }
  function stamp(mission, name) {
    const shape = LAYOUTS[name];
    const theme=districtTheme(mission);
    const grid = state().grid;
    if (!shape || !Array.isArray(grid) || grid.length !== 100) return false;
    const board = document.getElementById('board');
    if (!board) return false;

    // Rebuild only tactical terrain; previously authored district/mission metadata,
    // squad, campaign state and progression remain untouched.
    for (const c of grid) {
      reset(c);
      delete c.el.dataset.exfil;
      c.el.replaceChildren();
      const token = shape.rows[c.y][c.x];
      c.arenaVoid = token === ' ';
      c.arenaShapeV14 = name;
      c.arenaDistrictV14=theme.id;
      c.el.dataset.district=theme.id;
      c.el.dataset.surface=theme.surface;
      if (c.arenaVoid) {
        c.obstacle = true;
        c.transparentObstacle = false;
        c.el.classList.add('arena-void','obstacle');
        c.el.setAttribute('aria-hidden','true');
        continue;
      }
      c.el.removeAttribute('aria-hidden');
      c.el.classList.add('arena-floor');
      if (token === '#') wall(c);
      if (token === 'D') door(c, c.y===2 || name==='entrance');
    }
    for (const [x,y] of shape.covers) {
      const c=point(x,y);
      if (!c.obstacle) cover(c, name==='corridor'?'barrier':theme.cover);
    }
    const objective = state().objective;
    if (objective?.cells) {
      const spots=objectivePositions(objective.type, shape);
      for (let i=0;i<objective.cells.length;i++) {
        const p=spots[i] || shape.objectivePoints[i % shape.objectivePoints.length];
        const [x,y]=p;const c=point(x,y);
        if (c.obstacle || c.door) reset(c);
        Object.assign(objective.cells[i],{x,y});
        c.objectiveIndex=i;
        c.el.classList.add('objective-cell','v12-objective');
        c.el.dataset.kind=objective.cells[i].kind || 'security';
      }
      if (objective.exfil) {
        Object.assign(objective.exfil,{x:4,y:9});
        const c=point(4,9);
        c.obstacle=false;c.hazard=false;c.cover=false;c.objectiveIndex=null;
        c.el.classList.add('v14-exfil-cell');
        c.el.dataset.exfil='1';
      }
    }
    applyStreetDistrictHazards(mission,shape);
    // Restore optional terminals only to real, currently unoccupied floor tiles.
    // PWA12.96: hazardous physical Street Clashes promote the first terminal to
    // a deterministic district-infrastructure control instead of a random loot hack.
    let streetHazardControlPlaced=false;
    const hasStreetHazards=!!mission?.v134StreetEncounter && (STREET_DISTRICT_HAZARDS[mission.sectorId]||[]).length>0;
    for (const [x,y] of [[6,5],[3,5]]) {
      const c=point(x,y);
      if (!c.arenaVoid&&!c.obstacle&&!c.door&&!c.cover&&!c.hazard&&c.objectiveIndex==null&&!c.hackable) {
        c.hackable=true;c.hacked=false;c.el.classList.add('hackable-v10');
        if(hasStreetHazards&&!streetHazardControlPlaced){
          c.districtHazardControlV14=true;streetHazardControlPlaced=true;
          c.districtHazardControlLabelV14=STREET_CONTROL_LABELS[mission.sectorId]||'INFRASTRUCTURE CONTROL';
          c.el.classList.add('v14-district-control');c.el.dataset.kind='infrastructure-control';
          c.el.dataset.controlLabel=c.districtHazardControlLabelV14;
          c.districtHazardControlEffectV14=STREET_CONTROL_EFFECT_PREVIEWS[mission.sectorId]||'NEUTRALIZE LOCAL HAZARDS';
          c.el.dataset.controlEffect=c.districtHazardControlEffectV14;
          c.el.title=c.districtHazardControlLabelV14+' — 1 AP adjacent — '+c.districtHazardControlEffectV14;
          c.el.setAttribute('aria-label',c.districtHazardControlLabelV14+' — adjacent interaction, 1 AP — '+c.districtHazardControlEffectV14);
        }
        if (mission.type!=='heist')break;
      }
    }
    for (const c of grid) {
      if (!c.arenaVoid) c.el.classList.add('arena-floor');
      if (c.arenaVoid || c.door || c.cover || c.hazard || c.objectiveIndex != null) continue;
      for (const [dx,dy,cls] of [[0,-1,'edge-n'],[0,1,'edge-s'],[-1,0,'edge-w'],[1,0,'edge-e']]) {
        if (!floorAt(c.x+dx,c.y+dy)) c.el.classList.add(cls);
      }
    }
    board.dataset.arenaShape=name;
    board.dataset.arenaName=shape.name;
    board.dataset.arenaDistrict=theme.id;
    state().arenaShapeV14=name; // Transient: never appended to campaign serialization.
    state().losCache=new Map();
    state().v12TopologyRevision=(state().v12TopologyRevision||0)+1;
    const perf=root.ChromeRequiemV14Domains?.PerformanceV14?.perf;
    if (perf) {perf.movementCache=null;perf.visionCache=new WeakMap();}
    const label=document.querySelector('#objective-hud .v12-theater-inline');
    if(label)label.textContent=shape.name+' / '+shape.kind;
    const hint=document.getElementById('arena-shape-hint') || document.createElement('div');
    hint.id='arena-shape-hint';hint.setAttribute('aria-live','polite');
    hint.textContent=theme.label+' // '+shape.name+'  //  '+(name==='corridor'?'ADVANCE TO THE LOCKED BULKHEAD · CLICK ADJACENT DOOR TO BREACH':name==='entrance'?'CROSS THE ENTRY COURT · BREACH THE DOUBLE SECURITY DOOR':name==='alley'?'USE STREET COVER · BREAK THE HOSTILE LINE':name==='checkpoint'?'BREAK THE CORDON · USE BARRIERS AS COVER':name==='underpass'?'CONTROL THE NARROW APPROACH · DENY THE FLANKS':'CLEAR THE ROOMS · OPEN THE INTERIOR DOORS');
    if(streetHazardControlPlaced){
      const control=STREET_CONTROL_LABELS[mission.sectorId]||'INFRASTRUCTURE CONTROL';
      const payoff=STREET_CONTROL_EFFECT_PREVIEWS[mission.sectorId]||'NEUTRALIZE LOCAL HAZARDS';
      hint.textContent+='  //  '+control+': MOVE ADJACENT · 1 AP TO NEUTRALIZE HAZARDS · '+payoff;
    }
    board.appendChild(hint);
    return true;
  }

  function placeUnits(mission) {
    const shape=LAYOUTS[state().arenaShapeV14];
    if (!shape) return;
    const units=state().units||[];
    // Other legacy layers have already applied roster/equipment/doctrine/approach
    // mutations. Only their physical spawn cells are changed here.
    for (const c of state().grid) c.unit=null;
    const occupied=new Set();
    function deploy(unit, points, side) {
      const choices=[...points,...state().grid.filter(c=>!c.arenaVoid&&!c.obstacle&&!c.door&&c.objectiveIndex==null).sort((a,b)=>side==='player'?b.y-a.y:a.y-b.y).map(c=>[c.x,c.y])];
      const found=choices.find(([x,y])=>{const c=point(x,y);return !c.obstacle&&!c.arenaVoid&&!c.door&&c.objectiveIndex==null&&!occupied.has(y*10+x)});
      if (!found) throw new Error('Variable arena has insufficient legal squad deployment tiles');
      unit.x=found[0];unit.y=found[1];unit.facing=side==='player'?'N':'S';
      occupied.add(unit.y*10+unit.x);point(unit.x,unit.y).unit=unit;
    }
    units.filter(u=>u.team==='player'&&u.hp>0&&!u.dead).forEach(u=>deploy(u,shape.playerPoints,'player'));
    units.filter(u=>u.team==='enemy'&&u.hp>0&&!u.dead).forEach(u=>deploy(u,shape.enemyPoints,'enemy'));
    state().losCache=new Map();
    const perf=root.ChromeRequiemV14Domains?.PerformanceV14?.perf;
    if(perf){perf.movementCache=null;perf.visionCache=new WeakMap();}
  }

  const oldBuild=root.buildGrid;
  root.buildGrid=function(mission) {
    const result=oldBuild.apply(this,arguments);
    const name=choose(mission);
    state().arenaShapeV14=null;
    const board=document.getElementById('board');
    if(board) {delete board.dataset.arenaShape;delete board.dataset.arenaName;delete board.dataset.arenaDistrict;}
    document.getElementById('arena-shape-hint')?.remove();
    if(name)stamp(mission,name);
    return result;
  };
  const oldUnits=root.createCombatUnits;
  root.createCombatUnits=function(mission) {
    const result=oldUnits.apply(this,arguments);
    if(state().arenaShapeV14)placeUnits(mission);
    return result;
  };
  // Alarm waves previously arrived at fixed map-edge coordinates; choose a
  // reachable enemy-side floor tile when those coordinates fall in empty space.
  const oldReinforcement=root.spawnEnemyReinforcement;
  if(typeof oldReinforcement==='function')root.spawnEnemyReinforcement=function(type,x,y) {
    if(!state().arenaShapeV14)return oldReinforcement.apply(this,arguments);
    const c=x>=0&&x<10&&y>=0&&y<10?point(x,y):null;
    if(c&&!c.obstacle&&!c.unit&&!c.arenaVoid)return oldReinforcement.apply(this,arguments);
    const free=state().grid.filter(v=>!v.arenaVoid&&!v.obstacle&&!v.unit&&v.objectiveIndex==null&&!v.door);
    free.sort((a,b)=>a.y-b.y||Math.abs(a.x-x)-Math.abs(b.x-x)||a.x-b.x);
    const candidate=free[0];
    return candidate?oldReinforcement.call(this,type,candidate.x,candidate.y):undefined;
  };

  // PWA12.96 — Street hazards are tactical choices, not unavoidable decoration.
  // A nearby infrastructure terminal costs 1 AP to shut the district hazard grid
  // down. The wrapper is installed after ResponsiveV10, so these special controls
  // bypass its random terminal reward while ordinary terminals retain old behavior.
  // PWA12.100 — district infrastructure has a restrained secondary tactical payoff.
  // These effects deliberately reuse existing combat state/status mechanics rather than
  // introducing a parallel subsystem; hazard neutralization remains the primary reward.
  function applyDistrictControlEffectV14(mission,operator){
    const units=state().units||[];
    const district=mission?.sectorId;
    if(district==='undergrid'){
      let cut=0;for(const e of units){if(e.team==='enemy'&&e.hp>0&&e.overwatch){e.overwatch=false;cut++;}}
      return cut?`BREAKER BLACKOUT interrupts ${cut} hostile overwatch stance${cut===1?'':'s'}.`:'BREAKER BLACKOUT kills hostile surveillance power.';
    }
    if(district==='floodline'){
      let cleansed=0;for(const u of units){if(u.team==='player'&&u.hp>0&&u.statuses?.poison){delete u.statuses.poison;cleansed++;}}
      return cleansed?`DRAINAGE FLUSH clears toxic exposure from ${cleansed} operative${cleansed===1?'':'s'}.`:'DRAINAGE FLUSH pulls contaminated runoff off the fighting lane.';
    }
    if(district==='dock_nine'){
      let stalled=0;for(const e of units){if(e.team==='enemy'&&e.hp>0){e.disabledTurns=Math.max(e.disabledTurns||0,1);stalled++;}}
      return stalled?`POWER ISOLATION stalls ${stalled} hostile powered rig${stalled===1?'':'s'} for one turn.`:'POWER ISOLATION drops local cargo and security feeds.';
    }
    if(district==='neon_row'&&operator?.hp>0){
      operator.statuses=operator.statuses||{};operator.statuses.cloak=Math.max(operator.statuses.cloak||0,1);
      return `${operator.name||'Operator'} disappears into the NEON BLACKOUT for one turn.`;
    }
    return '';
  }

  // PWA12.103 — infrastructure controls are physical interactions, so the generic
  // ResponsiveV10 terminal highlight (weapon-range based) is misleading here. Correct it
  // after the normal highlight pass and surface a compact contextual prompt only when the
  // selected operative is actually adjacent and can make the 1-AP decision.
  function refreshDistrictControlFeedbackV14(){
    const board=document.getElementById('board');
    if(!board)return;
    let prompt=document.getElementById('district-control-context');
    const u=state().selectedUnit;
    const controls=(state().grid||[]).filter(c=>c?.districtHazardControlV14&&!c.hacked);
    let adjacent=null;
    for(const c of controls){
      const d=u?Math.abs(u.x-c.x)+Math.abs(u.y-c.y):Infinity;
      // Undo the inherited long-range terminal affordance. Physical controls are ready
      // only at Manhattan distance 1, matching onCombatCellClick below.
      c.el?.classList.toggle('ready-v10',!!u&&u.team==='player'&&state().turn==='player'&&d===1);
      c.el?.classList.toggle('v14-control-actionable',!!u&&u.team==='player'&&state().turn==='player'&&d===1&&u.ap>=1);
      if(d===1)adjacent=c;
    }
    if(!adjacent||!u||u.team!=='player'||state().turn!=='player'){
      prompt?.remove();return;
    }
    if(!prompt){prompt=document.createElement('div');prompt.id='district-control-context';prompt.setAttribute('role','status');prompt.setAttribute('aria-live','polite');board.appendChild(prompt);}
    const label=adjacent.districtHazardControlLabelV14||'INFRASTRUCTURE CONTROL';
    const effect=adjacent.districtHazardControlEffectV14||'NEUTRALIZE LOCAL HAZARDS';
    const ready=u.ap>=1;
    prompt.classList.toggle('disabled',!ready);
    prompt.innerHTML=`<strong>${label}</strong><span>${ready?'CLICK CONTROL · 1 AP':'NO AP · 1 AP REQUIRED'}</span><small>NEUTRALIZE HAZARDS · ${effect}</small>`;
  }
  const oldRefreshHighlightsV14=root.refreshCombatHighlights;
  if(typeof oldRefreshHighlightsV14==='function')root.refreshCombatHighlights=function(){
    const r=oldRefreshHighlightsV14.apply(this,arguments);refreshDistrictControlFeedbackV14();return r;
  };

  const oldCellClick=root.onCombatCellClick;
  if(typeof oldCellClick==='function')root.onCombatCellClick=function(x,y){
    const c=point(x,y),u=state().selectedUnit;
    if(c?.districtHazardControlV14&&!c.hacked&&u?.team==='player'&&state().turn==='player'&&!state().pendingAbility&&!state().pendingItem&&!state().inspectMode&&!state().moving){
      const d=Math.abs(u.x-x)+Math.abs(u.y-y);
      // PWA12.98: these are physical district controls, not wireless combat terminals.
      // Requiring adjacency makes route/cover/hazard positioning matter and prevents
      // long-range weapons from accidentally becoming long-range infrastructure hacks.
      if(d!==1){root.logMsg?.('Move adjacent to operate '+(c.districtHazardControlLabelV14||'the infrastructure control')+'.','sys');return}
      if(u.ap<1){root.logMsg?.('Need 1 AP to operate '+(c.districtHazardControlLabelV14||'the infrastructure control')+'.','sys');return}
      u.ap--;c.hacked=true;c.el.classList.add('hacked-v10','v14-district-control-off');c.el.classList.remove('ready-v10');
      let disabled=0;
      for(const h of state().grid||[]){
        if(!h?.el?.classList?.contains('v14-district-hazard'))continue;
        h.hazard=false;h.hazardTypeV12=null;h.hazardDamageV12=0;h.hazardStatusV12=null;
        h.el.classList.remove('hazard','v12-hazard','v14-district-hazard');delete h.el.dataset.hazard;disabled++;
      }
      root.spawnParticles?.(x,y,'#63ffae',18,3);root.floatText?.(x,y-.55,'GRID SAFE','#63ffae');
      root.logMsg?.(`${c.districtHazardControlLabelV14||'Infrastructure control'} neutralizes ${disabled} district hazard${disabled===1?'':'s'}.`,'good');
      const secondary=applyDistrictControlEffectV14(state().activeMission,u);
      if(secondary)root.logMsg?.(secondary,'good');
      state().losCache=new Map();state().v12TopologyRevision=(state().v12TopologyRevision||0)+1;
      document.getElementById('district-control-context')?.remove();
      root.updateCombat?.();root.checkWinLose?.();return;
    }
    return oldCellClick.apply(this,arguments);
  };

  root.CR14VariableArenas=Object.freeze({choose,layouts:LAYOUTS,stamp,placeUnits});
  root.ChromeRequiem=root.ChromeRequiem||{};
  root.ChromeRequiem.modules=root.ChromeRequiem.modules||{};
  root.ChromeRequiem.modules.VariableArenasV14=root.CR14VariableArenas;
})(globalThis);
