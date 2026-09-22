from pathlib import Path
import json,sys
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True)
m=json.loads((root/'build-meta.json').read_text())
note=f'''# Chrome Requiem PWA12.104 City Dynamic Disruptions Candidate 03

## Provenance
- Reconstructed exact canonical `14.0.0-pwa.12.104-street-contact-support` before applying any city candidate.
- Canonical deterministic build hash verified as `4313da4acd4c324a7672c36e`.
- Candidate 01 District Dispatches and Candidate 02 Interdistrict Logistics are reapplied cumulatively from their isolated patch scripts.
- Candidate version: `{m['version']}`.
- Candidate build hash: `{m['buildHash']}`.
- Save schema remains `{m['schemaVersion']}`.

## Player-facing improvement
**Live physical transit disruptions** now connect neighborhood pressure to interdistrict logistics while preserving the existing city simulation as authority.

While the crew is physically walking the first leg of an accepted interdistrict run, current Local Heat, Security, Gang Pressure, Unrest, the selected transit type, and quoted route risk can deterministically produce a one-time disruption such as a gang cordon, security sweep, metro service cut, freight inspection, compromised covert route, or border lockdown.

A disruption stops the current `Game.pendingPath` at the crew's actual street position. It does not teleport, auto-cross, or resolve in a menu. The player can:

- **Reroute** to another already-valid transit option. The system calls the existing Candidate 02 physical transit routing, creates a new real path to that alternate transit node, and preserves the original absolute delivery deadline.
- **Push through** the original crossing. The system recomputes the physical route from the crew's current position, preserves the original deadline, applies an explicit 15-minute delay through canonical `advanceTime(minutes)`, raises local heat, and increases the dispatch's route risk.

Only one disruption can occur per dispatch. Alert/resolution data is stored inside the already-persisted active dispatch object under `Game.livingStreetsV134.districtDispatches`, so the save schema does not change. An unresolved disruption survives save/load and restores its mobile route-decision panel.

## Architecture preserved
- `district-worlds-v13-3.js` remains authoritative for A* street paths, `Game.pendingPath`, transit nodes, district crossing, fares and crossing time.
- `living-streets-v13-4a.js` remains authoritative for neighborhood state and street-step progression.
- Candidate 01 remains the local physical dispatch authority.
- Candidate 02 remains the interdistrict offer/transit/last-mile/delivery authority.
- Candidate 03 wraps the existing `onStreetStepV134` seam after Candidate 02, evaluates disruption pressure only after real street movement, and delegates reroute/push routing back to Candidate 02 APIs.
- Existing mission staging, combat/extraction, saves and schema are not replaced.

## Verification executed
This note is generated only after all preceding workflow gates succeed:
- exact PWA12.104 canonical reconstruction and canonical build-hash assertion;
- production candidate build and JS syntax checks;
- cumulative Candidate 01 dispatch contract;
- Candidate 02 interdistrict logistics contract;
- Candidate 03 dynamic-disruption contract;
- PWA12.104 street-contact-support, PWA12.103/PWA12.100 district-control, save snapshot atomicity, corrupted-save recovery, active-city/route-marker performance, manifest and service-worker regressions;
- Chromium 390×844 Candidate 03 flow covering real physical route progress, forced high-pressure disruption, route halt, mobile alert geometry, save/load of unresolved disruption, alternate-node reroute with unchanged deadline, push-through with +15 minutes / local-heat / risk consequences and unchanged deadline, canonical district crossing and physical last-mile delivery;
- Candidate 02 browser regression plus existing operation-routing and stage-consequence browser regressions.

## Known limits
- Candidate 03 intentionally allows at most one disruption per dispatch to keep logistics tense without becoming interruption spam.
- Disruption pressure is sampled from the neighborhood the crew is physically moving through when the check fires; it is not a second independent city-event simulator.
- The feature works with direct Candidate 02 district crossings. It does not yet build multi-hop journeys across several intermediate districts.
- Rerouting preserves the original contract deadline rather than renegotiating payout or timing; the cost of changing plans is therefore the extra physical travel itself.
- Pushing through adds a fixed 15-minute delay plus local heat and route-risk pressure. This is deliberately legible and deterministic once the disruption has occurred.

## Next city target
Build **multi-hop city logistics with intermediate handoffs**: jobs that can require two district crossings and a physical mid-route handoff/safehouse, with the route planner exposing distinct sequences rather than only direct links. Dynamic disruptions should be able to invalidate a later leg and force a new physical sequence, while faction access, local heat/security and discovered hidden routes determine which chains remain viable.
'''
path=root/'DEVELOPMENT_NOTE_PWA12_104_CITY_DYNAMIC_DISRUPTIONS_CANDIDATE_03.md';path.write_text(note,encoding='utf-8');(out/path.name).write_text(note,encoding='utf-8');print(note)
