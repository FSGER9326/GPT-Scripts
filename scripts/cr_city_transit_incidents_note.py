from pathlib import Path
import json,sys,hashlib
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True)
meta=json.loads((root/'build-meta.json').read_text())
qa=root/'qa/pwa12-104-city-transit-incidents-mobile.png'
note=f'''# Chrome Requiem — PWA12.104 City Transit Incidents Candidate 06

## Candidate identity
- Candidate: `{meta.get('version')}`
- Build hash: `{meta.get('buildHash')}`
- Save schema: `{meta.get('schemaVersion')}`
- Canonical base reconstructed before editing: `14.0.0-pwa.12.104-street-contact-support` / `4313da4acd4c324a7672c36e` / schema 14.
- Canonical was not overwritten or promoted.

## Pre-edit inspection
The workflow first reconstructs and builds the exact PWA12.104 canonical and asserts its known build identity. Before Candidate 06 is applied it audits the actual canonical `district-worlds-v13-3.js`, `living-streets-v13-4a.js`, bootstrap manifest, path/travel authority, Living Streets neighborhood state, encounter flow, street-combat bridge and save owner. It then reapplies Candidates 01–05 and audits the cumulative pre-06 travel/logistics/access-ecology seams. The audit reports are packaged with this candidate.

The decisive architectural findings were:
- `district-worlds-v13-3.js` remains the authority for A* district paths, `Game.pendingPath`, transit nodes and `travelDistrictV133()`.
- Living Streets owns neighborhood `security`, `gangPressure`, `unrest`, `localHeat`, actor contact, street events and the established `launchStreetCombatV134()` / `settleStreetCombatV134()` tactical bridge.
- Candidate 05 already evaluates live conditions at both real transit endpoints; Candidate 06 therefore converts that existing friction into a physical world encounter instead of creating a second transit-risk model.
- The runtime draw/tap extension points (`drawLivingStreetsV134`, `handleLivingStreetTapV134`, `onStreetStepV134`) allow one physical marker/arrival interaction without rewriting the overworld renderer.

## Substantial player-facing improvement: physical transit incidents
Access Ecology conditions that represent actual friction — ID sweeps, lockdowns, screenings, cargo tolls, freight inspections, street levies and crowd delays — now become a physically placed transit incident when selected for an active interdistrict or multi-hop logistics run.

The incident is placed at the real source transit node and stores that world coordinate and neighborhood. The crew is routed there through the existing A* path and `Game.pendingPath`. The crew is not teleported. A procedural barricade/checkpoint marker is rendered on the explorable district map and can be tapped to route back to it. The incident only engages after the player physically reaches its radius through Living Streets movement.

At the checkpoint the player can, depending on context and crew:
- submit/pay the local surcharge and wait through the inspection;
- use AgentEX credentials;
- use a Hacker to spoof checkpoint systems;
- call the pickup/handoff contact and spend 3 trust;
- fight through using the existing tactical street-combat system;
- back off and physically replan another route while preserving the original delivery deadline.

A resolved incident grants exactly one local corridor clearance. The normal base transit fare/time, canonical security requirements, bribe/hack logic, district activation and arrival remain owned by `travelDistrictV133()`. Candidate 06 only zeroes the already-resolved Access Ecology surcharge/lock for that one crossing and consumes the clearance after crossing.

Violent resolution does not use a fake modal combat result. It launches `launchStreetCombatV134()` and lets the existing street-combat aftermath change neighborhood heat/unrest/gang/security and faction pressure. Candidate 06 adds one narrow aftermath callback so a victory clears the physical checkpoint; a loss returns the dispatch to route planning with the original deadline.

State persists under `Game.livingStreetsV134.transitIncidents` plus the already persisted active dispatch, so schema 14 remains unchanged.

## Files changed by Candidate 06
- `src/world/transit-incidents-pwa12-104-city-candidate-06.js` — new physical incident simulation, marker, choices, persistence and one-crossing clearance integration.
- `src/world/living-streets-v13-4a.js` — one optional post-aftermath callback after existing street-combat consequences.
- `src/bootstrap/module-manifest.js` — Candidate 06 module registration after Access Ecology and before mission approaches.
- `src/runtime/runtime-bundle.js` — matching ordered source marker for the production rebundler.
- `tests/pwa12_104_city_transit_incidents_contract.py` and `tests/pwa12_104_city_transit_incidents_browser.py` — focused static/integration coverage.

## Verified evidence
The final workflow is required to pass before packaging. It covers:
- exact canonical reconstruction and identity assertion;
- pre-edit canonical and cumulative architecture audits;
- Candidate 01–05 contracts;
- Candidate 06 focused contract and JS syntax validation;
- canonical Street Contact Support, district-control, save atomicity/recovery, active-city performance, route-marker performance, manifest and service-worker regressions;
- Chromium 390×844 physical incident flow: route selection → real street path → physical arrival → save/load → mobile incident UI → existing tactical street-combat bridge → retreat/replan deadline preservation → nonviolent clearance persistence → canonical crossing → physical last mile;
- existing Candidate 05, Candidate 04, Candidate 03 and Candidate 02 browser regressions;
- existing PWA12.49 operation-routing and PWA12.45 multi-stage combat/extraction regressions.

Mobile QA capture expected: `{qa.name}` ({'present' if qa.exists() else 'missing at note-generation time'}).

## Known boundaries
- Candidate 06 materializes Access Ecology friction for active logistics routes; it does not yet seed permanent free-roam checkpoints on every district transit node.
- One physical transit incident is active at a time, matching the single authoritative `Game.pendingPath` / single active dispatch architecture.
- The incident marker is procedural UI/canvas presentation, not a bespoke environment-art barricade asset.
- The tactical fight deliberately reuses the established Living Streets checkpoint/alley combat arena and enemy composition. Candidate 06 does not create a second combat ruleset or handcrafted checkpoint battle map.
- Incident pressure is snapshotted when the route is committed. Conditions changing during the approach do not mutate the already materialized checkpoint; Candidate 03 remains responsible for mid-route disruption after an ordinary transit leg is committed.
- A Candidate 06 clearance bypasses only the Access Ecology friction that the player physically resolved. Canonical faction/security access requirements still apply at the actual crossing.

## Next city-system target
**Persistent district control posts and free-roam access infrastructure.** Promote the successful incident representation beyond active delivery jobs: security posts, gang tolls, faction patrol checkpoints and inspection crews should persist as discoverable world objects/actors around important transit approaches, appear or disappear as neighborhood control/heat changes, and affect ordinary free-roam transit and services. Outcomes should feed district control, patrol density, Access Ecology and service availability, while violent outcomes continue to use the existing street-combat bridge. This would make faction control visibly inhabit the city rather than only emerging when a logistics route is selected.
'''
(out/'DEVELOPMENT_NOTE_PWA12_104_CITY_TRANSIT_INCIDENTS_CANDIDATE_06.md').write_text(note)
print(out/'DEVELOPMENT_NOTE_PWA12_104_CITY_TRANSIT_INCIDENTS_CANDIDATE_06.md')
