"""Static/integration contract for PWA12.104 city multi-hop logistics candidate 04."""
from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
mod=(root/'src/world/multihop-logistics-pwa12-104-city-candidate-04.js').read_text(encoding='utf-8')
c2=(root/'src/world/interdistrict-logistics-pwa12-104-city-candidate-02.js').read_text(encoding='utf-8')
dyn=(root/'src/world/dynamic-logistics-disruptions-pwa12-104-city-candidate-03.js').read_text(encoding='utf-8')
manifest=(root/'src/bootstrap/module-manifest.js').read_text(encoding='utf-8')
bundle=(root/'src/runtime/runtime-bundle.js').read_text(encoding='utf-8')
meta=json.loads((root/'build-meta.json').read_text(encoding='utf-8'))
checks={
 'module exists': bool(mod),
 'version tag': "pwa12.104-city-candidate.04" in mod,
 'offer is physical-source gated': 'nearSource(w)' in mod and 's.active||!n||n.id!==o.sourceId' in mod,
 'two-hop topology search': 'directLinks(w.id,mid)' in mod and 'directLinks(mid,fin)' in mod and "fin===w.id||fin===mid" in mod,
 'quotes both physical legs': 'quoteInterdistrictDispatchV12104?.(sourceId,mid,hand.id' in mod and 'quoteInterdistrictDispatchV12104?.(hand.id,fin,dest.id' in mod,
 'intermediate physical handoff persisted': "p.stage='handoff'" in mod and 'p.handoffAt=nowMin()' in mod,
 'second leg requires handoff proximity': "p.stage!=='handoff'" in mod and 'Math.hypot(Game.ovPlayer.x-hp.x,Game.ovPlayer.y-hp.y)>2.15' in mod,
 'second leg reuses normal city transit choice': 'applyLeg(a,p.leg2)' in mod and 'chooseInterdistrictTransitV12104' in mod,
 'overall deadline survives route choices': 'a.deadline=deadline' in mod and 'deadline=p.deadline' in mod,
 'chain payout depends on selected legs': 'selectedLeg1' in mod and 'selectedLeg2' in mod and '*1.12' in mod,
 'dynamic disruptions archived per leg': 'plan.disruptions' in mod and 'archiveDisruption' in mod,
 'second leg can arm a fresh disruption': 'delete a.dynamicDisruptionTriggered' in mod and 'delete a.dynamicDisruptionArm' in mod,
 'final delivery physically gated': 'nearTarget(a,w)' in mod and "p.stage!==2||a.phase!=='last_mile'" in mod,
 'final state affects destination neighborhood': "mutate(h,'localHeat'" in mod and "mutate(h,'prosperity'" in mod,
 'contact trust consequences': 'changeContactTrustV13' in mod and 'Completed long-haul delivery' in mod,
 'persistence stays in dispatch state': 'ensureDistrictDispatchStateV12104' in mod and 'multiHopOffers' in mod,
 'save called at acceptance': "streetToastV134?.('LONG-HAUL RUN · LEG 1 READY')" in mod and 'saveGame?.(0,true)' in mod,
 'candidate02 completion delegates multi-hop': "a?.multiHop&&typeof window.tryCompleteMultiHopDispatchV12104==='function'" in c2,
 'no player teleport assignment': 'Game.ovPlayer={' not in mod and 'Game.ovPlayer =' not in mod,
 'physical transit routing retained': 'routeToLocationV133' in mod and 'Game.pendingPath=null' in mod,
 'mobile responsive panel': '@media(max-width:520px)' in mod and 'calc(100% - 28px)' in mod,
 'base direct-run UI preserved': 'enhanceOffer' in mod and 'v12104-interdistrict-panel' in mod and 'LONG-HAUL OPTION' in mod,
 'manifest registration': "'world.multiHopLogistics'" in manifest and 'multihop-logistics-pwa12-104-city-candidate-04.js' in manifest,
 'manifest order': manifest.index("'world.dynamicLogisticsDisruptions'") < manifest.index("'world.multiHopLogistics'") < manifest.index("'missions.approaches'"),
 'runtime source registered': 'SOURCE: src/world/multihop-logistics-pwa12-104-city-candidate-04.js' in bundle,
 'runtime order': bundle.index('SOURCE: src/world/dynamic-logistics-disruptions-pwa12-104-city-candidate-03.js') < bundle.index('SOURCE: src/world/multihop-logistics-pwa12-104-city-candidate-04.js') < bundle.index('SOURCE: src/missions/contract-approaches-v13-4b.js'),
 'candidate03 15-minute time fix preserved': 'advanceTime(15)' in dyn,
 'build version': meta.get('version')=='14.0.0-pwa.12.104-city-multihop-logistics-candidate.04',
 'save schema unchanged': meta.get('schemaVersion')==14,
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items(): print(('PASS' if v else 'FAIL'),k)
if failed: raise SystemExit('contract failures: '+', '.join(failed))
print(f'PASS multi-hop logistics contract: {len(checks)} checks')
