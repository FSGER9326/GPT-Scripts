from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
mod=(root/'src/world/interdistrict-logistics-pwa12-104-city-candidate-02.js').read_text(encoding='utf-8')
core=(root/'src/world/district-worlds-v13-3.js').read_text(encoding='utf-8')
manifest=(root/'src/bootstrap/module-manifest.js').read_text(encoding='utf-8')
meta=json.loads((root/'build-meta.json').read_text(encoding='utf-8'))
checks={
 'versioned module':"pwa12.104-city-logistics-candidate.02" in mod,
 'physical source gate':'nearDistrictDispatchLocationV12104' in mod and 'near.id!==sourceId' in mod,
 'city graph planner':'V133_TRANSIT_LINKS' in mod and 'enumeratePathsL' in mod and 'planInterdistrictLogisticsV12104' in mod,
 'route choice modes':all(x in mod for x in ['FASTEST','CHEAPEST','LOW PROFILE']),
 'hidden route discovery':'hiddenLinks' in mod and "link.type!=='hidden'" in mod,
 'security/notoriety response':'Game.notoriety' in mod and 'Game.rep' in mod and 'CHECKPOINT' in mod and 'WATCHLIST' in mod,
 'manual transit authority':'routeToTransitNodeV133' in mod and 'travelDistrictV133?.(' not in mod and 'travelDistrictV133(' not in mod,
 'canonical transit completion hook':'onDistrictTransitCompleteV12104' in core and "activateDistrictV133(to.district,to.node);showScreen('overworld-screen');initOverworldV133();window.onDistrictTransitCompleteV12104?." in core,
 'no product teleport':'Game.ovPlayer=' not in mod,
 'destination street route':'routeToLocationV133' in mod and "stage='to_drop'" in mod,
 'deviation replanning':'replanActiveInterdistrictLogisticsV12104' in mod and 'LOGISTICS ROUTE DEVIATION' in mod,
 'persistent living street state':'interdistrictLogistics' in mod and 'livingStreetsV134' in mod and 'transferHistory' in mod,
 'save checkpoints':'saveGame?.(0,true)' in mod,
 'contact consequence':'changeContactTrustV13' in mod,
 'neighborhood consequence':all(x in mod for x in ['localHeat','prosperity','unrest']),
 'deadline and late payout':'deadline' in mod and 'lateMinutes' in mod and 'reward' in mod,
 'local dispatch coexistence':'activeDistrictDispatchV12104' in mod and 'offerDistrictDispatchV12104' in mod,
 'mobile layout':'@media(max-width:520px)' in mod and 'min-height:44px' in mod,
 'module manifest':"world.interdistrictLogistics" in manifest and "interdistrict-logistics-pwa12-104-city-candidate-02.js" in manifest,
 'schema preserved':meta.get('schemaVersion')==14,
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items(): print(('PASS' if v else 'FAIL'),k)
if failed: raise SystemExit('contract failures: '+', '.join(failed))
print(f'PASS interdistrict logistics contract: {len(checks)} checks')
