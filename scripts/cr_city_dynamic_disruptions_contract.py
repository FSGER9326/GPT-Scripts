from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
mod=(root/'src/world/dynamic-logistics-disruptions-pwa12-104-city-candidate-03.js').read_text(encoding='utf-8')
man=(root/'src/bootstrap/module-manifest.js').read_text(encoding='utf-8')
bundle=(root/'src/runtime/runtime-bundle.js').read_text(encoding='utf-8')
checks={
 'candidate 02 dependency':(root/'src/world/interdistrict-logistics-pwa12-104-city-candidate-02.js').exists(),
 'module registered':"'world.dynamicLogisticsDisruptions'" in man,
 'ordered after interdistrict logistics':"'world.interdistrictLogistics','world.dynamicLogisticsDisruptions','missions.approaches'" in man,
 'runtime marker present':'/* SOURCE: src/world/dynamic-logistics-disruptions-pwa12-104-city-candidate-03.js */' in bundle,
 'runtime marker follows candidate02':bundle.find('/* SOURCE: src/world/interdistrict-logistics-pwa12-104-city-candidate-02.js */')<bundle.find('/* SOURCE: src/world/dynamic-logistics-disruptions-pwa12-104-city-candidate-03.js */')<bundle.find('/* SOURCE: src/missions/contract-approaches-v13-4b.js */'),
 'uses active dispatch persistence':'activeInterdistrictDispatchV12104' in mod and 'dynamicDisruption' in mod,
 'no save schema bump':'schemaVersion' not in mod,
 'uses neighborhood heat security gang unrest':all(x in mod for x in ('localHeat','security','gangPressure','unrest')),
 'transit types affect pressure':all(x in mod for x in ('metro:.08','border:.12','freight:.15','security:.22','hidden:-.06')),
 'deterministic pressure roll':'hash(a.id,op.linkId,hid,Game.day||1)' in mod,
 'extreme pressure guaranteed':'x.pressure>=.92' in mod,
 'only one disruption per dispatch':'dynamicDisruptionTriggered' in mod,
 'disruption halts physical route':'Game.pendingPath=null' in mod and 'Game._v133TravelTarget=null' in mod,
 'reroute uses existing physical transit routing':'chooseInterdistrictTransitV12104?.(alt.linkId)' in mod,
 'push uses existing physical transit routing':'chooseInterdistrictTransitV12104?.(link)' in mod,
 'reroute preserves deadline':'const deadline=a.deadline' in mod and 'a.deadline=deadline' in mod,
 'push preserves deadline':'const oldDeadline=a.deadline' in mod and 'a.deadline=oldDeadline' in mod,
 'push costs canonical street time':"advanceTime(.25)" in mod,
 'push changes local heat':'h.localHeat=clamp' in mod,
 'push changes route risk':'a.risk=Number(clamp' in mod,
 'no teleport district activation':'activateDistrictV133' not in mod,
 'street-step integration':'const prevStep=window.onStreetStepV134' in mod,
 'load return integration':'const prevInit=window.initOverworldV133' in mod,
 'journal and save evidence hooks':'CITY ROUTE DISRUPTED' in mod and 'saveGame?.(0,true)' in mod,
 'mobile panel constrained':'width:min(380px,calc(100% - 28px))' in mod and '@media(max-width:520px)' in mod and 'min-height:44px' in mod,
 'no recurring world timer':'setInterval' not in mod and 'requestAnimationFrame' not in mod,
 'diagnostic api exposed':all(x in mod for x in ('evaluateInterdistrictDisruptionV12104','rerouteInterdistrictDisruptionV12104','pushThroughInterdistrictDisruptionV12104','updateInterdistrictDisruptionUIV12104')),
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items():print(('PASS ' if v else 'FAIL ')+k)
if failed:raise SystemExit('dynamic disruption contract failures: '+', '.join(failed))
print(f'PASS dynamic disruption contract: {len(checks)} checks')
