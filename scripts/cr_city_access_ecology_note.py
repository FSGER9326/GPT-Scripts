from pathlib import Path
import json,sys
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True)
meta=json.loads((root/'build-meta.json').read_text(encoding='utf-8'))
text=f'''# Chrome Requiem PWA12.104 — City Access Ecology Candidate 05

## Provenance

This candidate is rebuilt cumulatively from the exact PWA12.104 canonical reconstruction before Candidates 01–05 are applied. Canonical identity is checked before editing as `14.0.0-pwa.12.104-street-contact-support`, build `4313da4acd4c324a7672c36e`, schema 14. Canonical is not overwritten or promoted.

Candidate version: `{meta['version']}`  
Build hash: `{meta['buildHash']}`  
Save schema: `{meta['schemaVersion']}`

## Player-facing improvement — District Access Ecology

Physical transit links now react to the city state at their real endpoint neighborhoods instead of remaining static once a logistics quote is generated. Metro, border, freight, security and discovered hidden links read live Local Heat, Security, Gang Pressure and Unrest at both physical transit endpoints. Faction-linked routes additionally read faction reputation/heat and player notoriety.

The resulting states include Metro ID Sweeps, Faction/Street Lockdowns, Platform Screening, Cargo Tolls, Street Levies, Friendly Corridors/Priority Clearance and Covert Bypasses. These modify live availability, local fare, delay and risk. The existing PWA12.104 `travelDistrictV133()` remains the crossing authority: Candidate 05 only contributes a pre-crossing live verdict plus cost/time deltas, while canonical fare validation, security bribe/hack rules, district activation, arrival nodes, transit completion and save behavior remain in place.

When a live ecology lock closes a logistics route, an eligible physical pickup/handoff contact with at least 30 trust can spend local influence to sponsor that specific crossing. The player must still be physically at that contact and loses 3 trust. Sponsorship clears only Candidate 05's live district lock; ordinary canonical checkpoint rules still apply. The sponsorship record is stored in the active dispatch and therefore persists with the existing district-dispatch state.

Candidate 05 applies to the cumulative direct, multi-hop and disrupted logistics loops. It does not add a parallel travel menu and does not teleport the crew.

## Persistence

No schema migration. `Game.livingStreetsV134.accessEcology` stores bounded crossing/sponsorship history and counters. Per-job sponsorship and committed ecology snapshots live inside the already persisted active dispatch. Schema remains 14.

## Verification performed by CI

- Exact canonical PWA12.104 reconstruction/build-hash gate before modification.
- Candidate 01 District Dispatches cumulative contract.
- Candidate 02 Interdistrict Logistics contract.
- Candidate 03 Dynamic Disruptions contract.
- Candidate 04 Multi-Hop Logistics contract.
- Candidate 05 Access Ecology contract.
- Production rebundle/build and Node syntax checks.
- Existing Street Contact Support, district-control context/effects, save atomicity/recovery, active-city performance, route-marker performance, manifest and service-worker contracts.
- Chromium at 390×844 exercising live endpoint pressure, route lockout, physical-contact sponsorship, save/load of sponsorship, real pendingPath routing to the physical transit node, canonical crossing, last-mile routing, persistent ecology history, friendly security access, freight toll pressure and discovered hidden-route bypass.
- Candidate 04 multi-hop browser regression.
- Candidate 03 dynamic-disruption browser regression.
- Candidate 02 interdistrict browser regression.
- PWA12.49 operation-routing and PWA12.45 stage-consequence browser regressions protecting city→mission→combat/extraction flows.

Only successful CI assertions are evidence. Any failed intermediate run is documented separately in the task handoff and is not counted as verification.

## Known boundaries

- Ecology is evaluated from the neighborhoods nearest each physical transit endpoint; it is not a separate citywide hidden simulation.
- A contact sponsorship clears the new ecology lock only. It intentionally does not bypass canonical checkpoint reputation/notoriety/bribe/hack authority.
- Dynamic route repricing changes local access cost/delay/risk, not the underlying district graph topology. Hidden routes still require discovery.
- One active dispatch remains authoritative because the existing city layer has one `Game.pendingPath`.

## Next city-system target

**Transit incidents as physical world objects.** Convert the most important lockdowns/tolls from state-only access conditions into visible, temporary checkpoint/patrol/gang-control objects placed at the actual transit approach. Reaching the node should let the player inspect, negotiate, sneak around, fight through, or retreat/reroute, with outcomes feeding Local Heat, faction standing and the Access Ecology state. This should reuse existing street encounters/combat rather than becoming another modal-only minigame.
'''
(root/'DEVELOPMENT_NOTE_PWA12_104_CITY_ACCESS_ECOLOGY_CANDIDATE_05.md').write_text(text,encoding='utf-8')
(out/'DEVELOPMENT_NOTE_PWA12_104_CITY_ACCESS_ECOLOGY_CANDIDATE_05.md').write_text(text,encoding='utf-8')
print(out/'DEVELOPMENT_NOTE_PWA12_104_CITY_ACCESS_ECOLOGY_CANDIDATE_05.md')
