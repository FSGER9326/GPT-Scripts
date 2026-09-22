from pathlib import Path
import json,sys,shutil
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True)
m=json.loads((root/'build-meta.json').read_text(encoding='utf-8'))
note=f"""# Chrome Requiem PWA12.104 City Interdistrict Logistics Candidate 02

## Provenance
- Reconstructed exact canonical `14.0.0-pwa.12.104-street-contact-support` and reproduced canonical build hash `4313da4acd4c324a7672c36e` before editing.
- Reapplied verified District Dispatches Candidate 01 as the cumulative local-job foundation, then added Candidate 02's interdistrict layer.
- Candidate version: `{m['version']}`.
- Candidate build hash: `{m['buildHash']}`.
- Save schema remains `{m['schemaVersion']}`.
- Canonical and prior candidates were not overwritten.

## Implemented
**Interdistrict Logistics** extends physical street dispatches across district boundaries without introducing menu teleportation. At a physically reached contact/shop/clinic, the existing local dispatch board remains available and gains an explicit INTERDISTRICT RUN entry. A city run chooses a real destination location in an adjacent district and quotes the direct physical transit options between the two districts. Border, metro, freight, security and discovered hidden links have distinct risk/cost profiles. Security gates react to reputation/notoriety; watchlisted metro routes are flagged unavailable; undiscovered hidden routes do not appear.

Accepting a city run does not move the player. The player chooses a transit leg, which commits the existing `routeToTransitNodeV133()` / `Game.pendingPath` street route to that real transit node. The normal canonical transit modal and `travelDistrictV133()` remain authoritative for fare, access, time, bribe/hack rules, notoriety and district activation. Candidate 02 adds one optional successful-transit hook; after the chosen crossing succeeds, the destination coordinate is revealed and a physical last-mile route is committed through `routeToLocationV133()`. Completion occurs only at the destination's actual world coordinate through the existing Living Streets step flow.

Route quotes combine real A* street paths on both sides of the crossing with neighborhood Local Heat, Security, Gang Pressure and Unrest plus transit-specific risk. Payout/deadline therefore differ by route. Delivery affects credits, destination heat/prosperity/unrest and source-contact trust; contraband through a security gate creates additional destination heat. State remains nested inside `Game.livingStreetsV134.districtDispatches`, so no schema bump is required.

## Verification executed
- Exact canonical deterministic reconstruction before patching.
- JS syntax checks for both city candidate modules, the patched district core and rebuilt runtime bundle.
- Existing District Dispatches focused contract.
- Candidate 02 focused interdistrict contract.
- PWA12.104 street-contact support; PWA12.103/PWA12.100 district-control regressions.
- Save snapshot atomicity and corrupted-save recovery regressions.
- Active-city and route-marker performance contracts.
- Manifest and service-worker tests.
- Chromium end-to-end QA at 390x844: local board preservation, explicit city-board toggle, multiple transit choices, remote acceptance rejection, physical pendingPath to transit, save/load while en route, canonical transit crossing, destination reveal, physical last-mile pendingPath, delivery/reward, and no horizontal overflow.
- Existing operation-routing and stage-consequence Chromium regressions.

## Known limits
- Candidate 02 intentionally supports one direct interdistrict transit leg per run. Multi-hop deliveries are not yet generated.
- Quote risk is locked when a route option is selected. Neighborhood conditions can still change while travelling, but an accepted payout is not repriced mid-run.
- Existing canonical transit access rules remain authoritative. Candidate 02 describes their pressure but does not replace checkpoint UI or invent new bypass mechanics.
- One active dispatch remains the authority to keep route ownership and mobile HUD state unambiguous.

## Next city target
Add **live route disruption and multi-hop logistics**: allow two-stage interdistrict chains where district incidents can invalidate or degrade a planned leg and force a physical reroute through another metro/freight/border/hidden node, while preserving player-selected transit and checkpoint consequences.
"""
path=root/'DEVELOPMENT_NOTE_PWA12_104_CITY_INTERDISTRICT_LOGISTICS_CANDIDATE_02.md'
path.write_text(note,encoding='utf-8');shutil.copy2(path,out/path.name)
print(note)
