from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
mod=(root/'src/world/transit-incidents-pwa12-104-city-candidate-06.js').read_text()
streets=(root/'src/world/living-streets-v13-4a.js').read_text()
manifest=(root/'src/bootstrap/module-manifest.js').read_text()
bundle=(root/'src/runtime/runtime-bundle.js').read_text()
meta=json.loads((root/'build-meta.json').read_text()) if (root/'build-meta.json').exists() else {}
checks={
 'candidate 06 module exists': bool(mod),
 'persistent living-streets owner': 's.transitIncidents=s.transitIncidents||' in mod,
 'one active physical incident': 'active:null,history:[]' in mod,
 'incident uses real transit node': "w.transit?.find(t=>t.id===op?.sourceNodeId)" in mod,
 'incident stores physical x/y': 'x:n.x,y:n.y' in mod,
 'incident stores neighborhood': 'neighborhood:hoodIdAt(w,n)' in mod,
 'live access ecology drives incident': 'evaluateTransitAccessEcologyV12104' in mod and 'needsIncident(e)' in mod,
 'open friendly routes stay quiet': "QUIET=new Set(['OPEN ACCESS'" in mod,
 'physical routing uses existing transit route': 'routeToTransitNodeV133?.(inc.nodeId)' in mod,
 'custom physical target prevents menu teleport': "kind:'v12104incident'" in mod,
 'arrival requires physical proximity': 'Math.hypot(Game.ovPlayer.x-inc.x,Game.ovPlayer.y-inc.y)<=1.65' in mod,
 'street-step arrival hook': 'window.onStreetStepV134=function' in mod and 'detect();update()' in mod,
 'physical marker rendered in living streets': 'window.drawLivingStreetsV134=function' in mod and 'function draw(ctx,w,W,H,t)' in mod,
 'marker can be tapped': 'window.handleLivingStreetTapV134=function' in mod and 'function tap(q)' in mod,
 'no player teleport assignment': 'Game.ovPlayer=' not in mod,
 'compliance has cost/time consequences': 'function comply()' in mod and 'Game.credits' in mod and 'window.advanceTime?.(inc.profile.wait||3)' in mod,
 'agentex and hacker bypasses': "kind==='agentex'?'AgentEX':'Hacker'" in mod,
 'contact cover spends trust': "changeContactTrustV13?.(c.id,-3,'Cleared a physical transit incident')" in mod,
 'fight uses established street combat bridge': 'window.launchStreetCombatV134?.(inc.profile.actor,w)' in mod,
 'living streets settlement notifies candidate': 'window.onTransitIncidentStreetCombatSettledV12104?.(m,success)' in streets,
 'combat success grants crossing clearance': "if(success){grant('fight',{missionId:m.id});return true}" in mod,
 'combat failure returns to route planning': "a.phase='choose_transit'" in mod and "resolution='fight_failed'" in mod,
 'retreat preserves original deadline': 'a.transitIncidentCarryDeadline=deadline' in mod,
 'later route consumes carry deadline': 'if(ok&&carry){a.deadline=carry' in mod,
 'clearance is one crossing only': 'c.consumed=true;c.crossedAt=nowMin()' in mod,
 'cleared incident zeroes ecology surcharge once': "label:'INCIDENT CLEARED',reason:'',costDelta:0,minutesDelta:0,heatDelta:0" in mod,
 'canonical transit authority still present': 'travelDistrictV133' in bundle,
 'multi-hop selection preserved': 'p.selectedLeg1=chosen' in mod and 'p.selectedLeg2=chosen' in mod,
 'state saved during incident transitions': mod.count('window.saveGame?.(0,true)')>=7,
 'route planning buttons expose physical approach': 'APPROACH ${e.label} PHYSICALLY' in mod,
 'mobile actions minimum 44px': 'min-height:44px' in mod,
 'module registered after access ecology': "'world.transitIncidents':{path:'./src/world/transit-incidents-pwa12-104-city-candidate-06.js'" in manifest and manifest.index("'world.accessEcology'")<manifest.index("'world.transitIncidents'")<manifest.index("'missions.approaches'"),
 'runtime ordered after access ecology': '/* SOURCE: src/world/transit-incidents-pwa12-104-city-candidate-06.js */' in bundle and bundle.index('/* SOURCE: src/world/access-ecology-pwa12-104-city-candidate-05.js */')<bundle.index('/* SOURCE: src/world/transit-incidents-pwa12-104-city-candidate-06.js */')<bundle.index('/* SOURCE: src/missions/contract-approaches-v13-4b.js */'),
 'save schema unchanged': meta.get('schemaVersion')==14,
 'candidate version stamped': meta.get('version')=='14.0.0-pwa.12.104-city-transit-incidents-candidate.06',
}
for k,v in checks.items(): print(('PASS' if v else 'FAIL'),k)
failed=[k for k,v in checks.items() if not v]
assert not failed,failed
print(f'PASS Candidate 06 physical transit incidents contract: {len(checks)} checks')
