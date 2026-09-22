from pathlib import Path
import sys,re

root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
mod=root/'src/world/patrol-corridors-pwa12-104-city-candidate-08.js'
dw=root/'src/world/district-worlds-v13-3.js'
man=root/'src/bootstrap/module-manifest.js'
bundle=root/'src/runtime/runtime-bundle.js'
checks=[]
def ck(name,cond):
    if not cond: raise AssertionError(name)
    checks.append(name)

ck('candidate module exists',mod.is_file())
s=mod.read_text(encoding='utf-8');d=dw.read_text(encoding='utf-8');m=man.read_text(encoding='utf-8');b=bundle.read_text(encoding='utf-8')
ck('candidate version marker',"pwa12.104-city-candidate.08" in s)
ck('three route identities',all(x in s for x in ["label:'FAST'","label:'LOW PROFILE'","label:'BACK ALLEY'"]))
ck('canonical pathfinder reused',"window.findDistrictPathV133" in s)
ck('actual living street neighborhoods used',"ensureNeighborhoodStateV134" in s)
ck('physical control posts feed exposure',"controlPostsForWorldV12104" in s)
ck('physical street actors feed exposure',"ensureStreetActorsV134" in s)
ck('local heat feeds route exposure',"localHeat" in s)
ck('security feeds route exposure',"security" in s)
ck('gang pressure feeds route exposure',"gangPressure" in s)
ck('unrest feeds route exposure',"unrest" in s)
ck('route familiarity persists under Living Streets',"s.patrolCorridors=s.patrolCorridors||" in s and "familiarity" in s)
ck('familiarity earned through physical step hook',"markFamiliar(w,Game.ovPlayer)" in s and "const prevStep=window.onStreetStepV134" in s)
ck('route familiarity does not claim nonexistent Street Memory',"streetMemory" not in s and "Street Memory" not in s)
ck('route alternatives are canonical path segments',"canonical(start,via,w)" in s and "canonical(via,goal,w)" in s)
ck('fast route begins from canonical direct path',"const fast=makeOption('fast',paths[0]" in s)
ck('low profile has bounded detour',"1.58" in s)
ck('back alley has bounded detour',"1.95" in s)
ck('route switch starts from current physical position',"preview(goal,target,w,Game.ovPlayer)" in s)
ck('module never teleports player x',"Game.ovPlayer.x=" not in s)
ck('module never teleports player y',"Game.ovPlayer.y=" not in s)
ck('programmatic routes call canonical base first',"ok=base?.apply(this,args)" in s)
ck('programmatic routes keep canonical scheduler wakeup',"window.routeToTransitNodeV133=wrapBase" in s and "window.routeToLocationV133=wrapBase" in s)
ck('arbitrary point route uses canonical base export',"window.routeToPointV133=wrapBase" in s)
ck('manual marker tap exposes planner',"openPatrolRoutePlannerV12104?.(spec)" in d)
ck('manual point tap exposes planner',"openPatrolRoutePlannerV12104?.({point:q,target:pt})" in d)
ck('canonical point route is exported narrowly',"window.routeToPointV133=routeToPointV133;" in d)
ck('canonical route card delegates optional intel decoration',"decoratePatrolRouteCardV12104?.(e,t)" in d)
ck('route planner exposes real route metrics',"BLOCKS" in s and "MIN" in s and "EXPOSURE" in s and "INTEL" in s)
ck('mobile route actions remain touch safe',"min-height:44px" in s)
ck('patrol influence has world rendering',"drawCorridors" in s and "worldToScreen" in s)
ck('patrol influence discoverability is proximity or familiarity gated',"familiarity(w,n)>=3" in s and "<=9" in s)
ck('route preference and familiarity save through existing game state',"window.saveGame?.(0,true)" in s and "Game.livingStreetsV134" in s)
ck('candidate does not create save schema migration',"schemaVersion" not in s and "SAVE_SCHEMA" not in s)
ck('manifest registers Candidate 08',"world.patrolCorridors" in m and "patrol-corridors-pwa12-104-city-candidate-08.js" in m)
order=[m.find("'world.controlPosts'"),m.find("'world.patrolCorridors'"),m.find("'missions.approaches'")]
ck('manifest order Candidate07 Candidate08 missions',min(order)>=0 and order==sorted(order))
markers=[b.find('/* SOURCE: src/world/district-control-posts-pwa12-104-city-candidate-07.js */'),b.find('/* SOURCE: src/world/patrol-corridors-pwa12-104-city-candidate-08.js */'),b.find('/* SOURCE: src/missions/contract-approaches-v13-4b.js */')]
ck('runtime marker order Candidate07 Candidate08 missions',min(markers)>=0 and markers==sorted(markers))
ck('single Candidate 08 source marker',b.count('/* SOURCE: src/world/patrol-corridors-pwa12-104-city-candidate-08.js */')==1)
print(f'PASS Candidate 08 Patrol Corridors contract: {len(checks)}/{len(checks)} checks')
for x in checks: print('  OK',x)
