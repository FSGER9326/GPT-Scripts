from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
mod=(root/'src/world/interdistrict-logistics-pwa12-104-city-candidate-02.js').read_text(encoding='utf-8')
world=(root/'src/world/district-worlds-v13-3.js').read_text(encoding='utf-8')
man=(root/'src/bootstrap/module-manifest.js').read_text(encoding='utf-8')
bundle=(root/'src/runtime/runtime-bundle.js').read_text(encoding='utf-8')
checks={
 'cumulative local dispatch dependency':(root/'src/world/district-dispatches-pwa12-104-city-candidate-01.js').exists(),
 'module registered':"'world.interdistrictLogistics'" in man,
 'ordered after local dispatches':"'world.districtDispatches','world.interdistrictLogistics','missions.approaches'" in man,
 'runtime bundle includes module':'/* SOURCE: src/world/interdistrict-logistics-pwa12-104-city-candidate-02.js */' in bundle,
 'state reuses living streets dispatch owner':'ensureDistrictDispatchStateV12104' in mod and 'crossOffers' in mod,
 'direct physical transit graph':'V133_TRANSIT_LINKS' in mod and 'directLinks' in mod,
 'destination world uses canonical generator':'generateDistrictV133' in mod,
 'street route metrics on both sides':'findDistrictPathV133' in mod and 'p1=' in mod and 'p2=' in mod,
 'neighborhood risk inputs':all(x in mod for x in ('localHeat','gangPressure','unrest','security')),
 'distinct transit risk':all(x in mod for x in ('metro:.08','border:.18','freight:.24','security:.42','hidden:.06')),
 'checkpoint pressure represented':'CHECKPOINT PRESSURE' in mod,
 'watchlisted metro blocked':'WATCHLIST — BLOCKED' in mod,
 'hidden route respects discovery':"hiddenLinks?.[link.id]" in mod,
 'source must be physically near':'physicalSource' in mod and 'nearSource' in mod,
 'choice routes to physical transit node':'routeToTransitNodeV133' in mod,
 'no cross district teleport':'activateDistrictV133' not in mod,
 'canonical travel hook optional':'onDistrictTransitCompleteV12104?.' in world,
 'hook preserves canonical transit authority':'advanceTime(link.minutes||12)' in world and 'Game.credits-=cost' in world,
 'transit completion opens last mile':'phase=\'last_mile\'' in mod and 'routeToLocationV133' in mod,
 'last mile routing atomic before save':'lastMileRouted=!!routed' in mod and 'setTimeout(()=>{window.routeToLocationV133' not in mod,
 'delivery requires physical destination proximity':"Math.hypot(Game.ovPlayer.x-p.x,Game.ovPlayer.y-p.y)>2.15" in mod,
 'delivery changes neighborhood state':'localHeat' in mod and 'prosperity' in mod and 'unrest' in mod,
 'contact trust consequence':'changeContactTrustV13' in mod,
 'one active dispatch authority':'s.active' in mod and 'crossDistrict:true' in mod,
 'save schema unchanged by module':'schemaVersion' not in mod,
 'mobile width constrained':'width:min(360px,calc(100% - 28px))' in mod and '@media(max-width:520px)' in mod,
 'frozen world no recurring timers':'setInterval' not in mod and 'requestAnimationFrame' not in mod,
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items(): print(('PASS ' if v else 'FAIL ')+k)
if failed: raise SystemExit('interdistrict logistics contract failures: '+', '.join(failed))
print(f'PASS interdistrict logistics contract: {len(checks)} checks')
