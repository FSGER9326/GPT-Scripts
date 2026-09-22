from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
mod=(root/'src/world/access-ecology-pwa12-104-city-candidate-05.js').read_text(encoding='utf-8')
world=(root/'src/world/district-worlds-v13-3.js').read_text(encoding='utf-8')
manifest=(root/'src/bootstrap/module-manifest.js').read_text(encoding='utf-8')
bundle=(root/'src/runtime/runtime-bundle.js').read_text(encoding='utf-8')
checks={
 'candidate version':"pwa12.104-city-candidate.05" in mod,
 'live neighborhood state':'ensureNeighborhoodStateV134' in mod and 'localHeat' in mod and 'gangPressure' in mod and 'unrest' in mod and 'security' in mod,
 'faction reputation':'Game.rep' in mod and 'Game.heat' in mod and 'FACTIONS' in mod,
 'notoriety':'Game.notoriety' in mod,
 'five transit families':all(x in mod for x in ["l.type==='metro'","l.type==='border'","l.type==='freight'","l.type==='security'","l.type==='hidden'"]),
 'dynamic lock states':all(x in mod for x in ['FACTION LOCKDOWN','METRO ID SWEEP','STREET LOCKDOWN']),
 'dynamic soft states':all(x in mod for x in ['CARGO TOLL','STREET LEVY','PLATFORM SCREENING','FRIENDLY CORRIDOR','COVERT BYPASS']),
 'physical contact sponsorship':'sourceContact' in mod and "phase==='choose_transit'" in mod and 'Math.hypot' in mod,
 'trust is real cost':"changeContactTrustV13?.(c.id,-3,'Sponsored city transit access')" in mod,
 'sponsor persisted in active dispatch':'accessEcologySponsors' in mod and 'saveGame?.(0,true)' in mod,
 'persistent ecology history':'livingStreetsV134' in mod and 'accessEcology' in mod and 'history' in mod,
 'live route refresh':'refreshTransitAccessEcologyV12104' in mod and 'baseEcology' in mod,
 'choice authority wrapped':'chooseInterdistrictTransitV12104' in mod and 'baseChoose.apply' in mod,
 'physical route remains':'routeToTransitNodeV133' not in mod,
 'no teleport':'Game.ovPlayer=' not in mod,
 'canonical travel hook':'prepareTransitAccessEcologyV12104' in world and 'commitTransitAccessEcologyV12104' in world,
 'canonical fare retained':"let cost=Math.max(0,(link.cost||0)+(ecology?.costDelta||0))" in world,
 'canonical time retained':"advanceTime(Math.max(1,(link.minutes||12)+(ecology?.minutesDelta||0)))" in world,
 'canonical access still present':'accessForLinkV133(link)' in world and "mode==='bribe'" in world and "mode==='hack'" in world,
 'canonical crossing callback retained':'onDistrictTransitCompleteV12104' in world,
 'manifest registration':"'world.accessEcology'" in manifest and 'access-ecology-pwa12-104-city-candidate-05.js' in manifest,
 'runtime registration':'/* SOURCE: src/world/access-ecology-pwa12-104-city-candidate-05.js */' in bundle,
 'runtime order':bundle.index('multihop-logistics-pwa12-104-city-candidate-04.js')<bundle.index('access-ecology-pwa12-104-city-candidate-05.js')<bundle.index('contract-approaches-v13-4b.js'),
 'mobile css':'@media(max-width:520px)' in mod and 'min-height:44px' in mod,
 'save schema untouched':'schemaVersion' not in mod,
 'ecology stats':'sponsors' in mod and 'lockouts' in mod and 'tolls' in mod and 'crossings' in mod,
 'sponsor does not claim canonical bypass':'ordinary checkpoint rules still apply' in mod,
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items(): print(('PASS ' if v else 'FAIL ')+k)
if failed: raise SystemExit('Candidate 05 contract failed: '+', '.join(failed))
print(f'PASS access ecology contract: {len(checks)} checks')
