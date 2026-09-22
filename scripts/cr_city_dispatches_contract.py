from pathlib import Path
import sys,re
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
mod=(root/'src/world/district-dispatches-pwa12-104-city-candidate-01.js').read_text(encoding='utf-8')
man=(root/'src/bootstrap/module-manifest.js').read_text(encoding='utf-8')
bundle=(root/'src/runtime/runtime-bundle.js').read_text(encoding='utf-8')
living_marker='/* SOURCE: src/world/living-streets-v13-4a.js */'
dispatch_marker='/* SOURCE: src/world/district-dispatches-pwa12-104-city-candidate-01.js */'
approach_marker='/* SOURCE: src/missions/contract-approaches-v13-4b.js */'
checks={
 'module registered':"'world.districtDispatches'" in man,
 'module ordered after living streets':"'world.livingStreets','world.districtDispatches','missions.approaches'" in man,
 'runtime source marker present':bundle.count(dispatch_marker)==1,
 'runtime marker order':all(x in bundle for x in [living_marker,dispatch_marker,approach_marker]) and bundle.index(living_marker)<bundle.index(dispatch_marker)<bundle.index(approach_marker),
 'state nested in living streets':'street.districtDispatches=street.districtDispatches||{}' in mod,
 'physical source gate':'sourceIsPhysicalD' in mod and 'nearLocationD' in mod,
 'official route authority':'routeToLocationV133' in mod,
 'no product teleport':'Game.ovPlayer=' not in mod,
 'real path risk':'findDistrictPathV133' in mod and 'routeMetricsD' in mod,
 'neighborhood consequences':'localHeat' in mod and 'prosperity' in mod and 'gangPressure' in mod,
 'trust consequence':'changeContactTrustV13' in mod,
 'save persistence':'saveGame?.(0,true)' in mod,
 'street-step completion hook':'window.onStreetStepV134=function' in mod,
 'mobile layout':'@media(max-width:520px)' in mod,
 'frozen world preserved':'setInterval' not in mod and 'requestAnimationFrame' not in mod,
 'schema untouched':'schemaVersion' not in mod and 'V13_SAVE_KEY' not in mod,
 'single active dispatch':'state.active' in mod,
 'deadline':'deadline' in mod and 'lateMinutes' in mod,
 'dispatch families':all(x in mod for x in ['courier','medical','data','contraband']),
 'history bounded':'slice(0,24)' in mod,
 'target discovery on acceptance':'revealTargetD' in mod,
}
failed=[k for k,v in checks.items() if not v]
if failed: raise SystemExit('FAIL district dispatch contract: '+', '.join(failed))
print(f"PASS district dispatch contract: {len(checks)} checks")
