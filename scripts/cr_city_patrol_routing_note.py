from pathlib import Path
import json,sys
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True)
meta=json.loads((root/'build-meta.json').read_text(encoding='utf-8'))
text=f'''# Chrome Requiem PWA12.104 — City Patrol Routing Candidate 08

## Candidate identity

- Version: `{meta.get('version')}`
- Build hash: `{meta.get('buildHash')}`
- Save schema: `{meta.get('schemaVersion')}`
- Base: exact reconstructed PWA12.104 canonical (`14.0.0-pwa.12.104-street-contact-support`, build `4313da4acd4c324a7672c36e`)
- Canonical was reconstructed, asserted and audited before cumulative city candidates were reapplied. Canonical itself was not modified or promoted.

## Player-facing improvement — Patrol Corridors + Risk-Aware Physical Route Choice

Candidate 08 makes intra-district navigation a tactical city decision rather than always accepting the single cheapest A* line.

Live Local Heat, neighborhood Security, Gang Pressure and Unrest now project physical patrol influence onto the existing district street grid. Candidate 07 control posts also project strong influence into their approach streets. The result is a set of visible security-sweep and gang-patrol corridors anchored to the same neighborhoods, transit nodes and locations the player already walks through.

A direct player map-tap to a distant location, transit node or ordinary walkable street point now opens a compact route-tactics sheet with three genuinely different physical paths when the graph permits them:

- **FAST** — canonical PWA12.104 A* path; prioritizes normal terrain cost and distance.
- **LOW PROFILE** — performs a risk-aware A* search that strongly penalizes security/gang exposure and elevated local heat, accepting detours to cross quieter streets.
- **BACK ALLEY** — uses the same walkable graph but heavily favors alleys, tunnels, pedestrian cuts, yards and industrial/service terrain while penalizing arterials, security roads, plazas and obvious transit approaches.

Every choice is a real `Game.pendingPath`. The player is not teleported and the candidate does not create a parallel movement scheduler. A narrow one-shot override is fed into canonical `routeToPointV133()`, which still owns pending-path installation, camera follow, the overworld scheduler, long-route events and route-card lifecycle.

The planner reports path cells, total exposure, security exposure, gang exposure and detour percentage. Patrol corridors and all three candidate routes are drawn over the physical district while the planner is open.

Programmatic routes used by existing dispatches, services, control posts and mission code do **not** automatically open the planner. They continue to call canonical `routeToLocationV133()` / `routeToTransitNodeV133()` exactly as before. The route-choice UI is confined to direct player map exploration, preventing Candidate 08 from destabilizing the cumulative city automation.

## Persistence

Selected manual tactical routes store only their durable objective/profile/analysis under `Game.livingStreetsV134.patrolRouting`; the long `Game.pendingPath` array remains transient, matching established architecture. On save/load and overworld re-entry Candidate 08 recomputes the selected risk-aware path from the restored physical crew position and hands it back to canonical route authority.

A later canonical/programmatic route supersedes the saved manual route cleanly. Candidate 08 also yields resumption authority when a Candidate 07 control-post approach or Candidate 06 transit incident is active.

No save migration was required; schema remains 14.

## Exact implementation surfaces

- Added `src/world/patrol-routing-pwa12-104-city-candidate-08.js`.
- Registered `world.patrolRouting` after Candidate 07 and before mission approaches in `src/bootstrap/module-manifest.js`.
- Added the corresponding ordered `runtime-bundle.js` source marker; the rebundler remains authoritative.
- Added a narrow optional route-override/commit callback seam to `src/world/district-worlds-v13-3.js` while preserving canonical route scheduling.
- Patched only the direct-map-tap branches of `handleMapTapV133()` to expose route tactics; programmatic location/transit routes are unchanged.
- Added focused Candidate 08 structural and Chromium/mobile QA tests.

## Verified evidence from the successful packaging workflow

The artifact is emitted only after all preceding workflow gates succeed. That final run verifies:

- exact PWA12.104 canonical reconstruction and build identity before modification;
- stage validation for City Candidates 01–07;
- Candidate 08 focused structural contract and JavaScript syntax;
- production build;
- canonical Street Contact Support, district-control, street-combat/aftermath, save atomicity/recovery, active-city/route-marker performance, manifest and service-worker regressions;
- Candidate 08 Chromium integration at 390×844, including live corridor generation, distinct physical route geometries under forced patrol pressure, route-exposure tradeoff, touch-safe/no-overflow route planner, no-teleport commit, save/load path reconstruction and actual physical movement;
- cumulative Candidate 07/06/05/04/03/02 browser regressions;
- existing PWA12.49 city→operation routing and PWA12.45 multi-stage combat/extraction regressions.

The final mobile screenshot is packaged as `pwa12-104-city-patrol-routing-mobile.png`.

## Known boundaries

1. Patrol corridors are systemic influence fields derived from current neighborhood state and control-post geography; they are not yet independently roaming patrol squads with pursuit AI.
2. The player currently receives exact route-exposure metrics when opening Route Tactics. Route knowledge/fog-of-war is intentionally deferred rather than pretending an exact PWA12.104 Street Memory system exists; the exact canonical Living Streets source has no such route-memory authority.
3. Candidate 08 changes the path geometry but deliberately does not replace the existing Living Streets encounter director. Walking a different neighborhood therefore changes which systemic geography the crew traverses without creating a second encounter scheduler.
4. Direct player map taps expose Route Tactics. Programmatic job/control-post/service routes stay deterministic unless the player later manually replans on the map.
5. Risk fields are recomputed from current neighborhood state when planning/resuming; an already committed pending path is not continuously mutated under the player's feet.
6. The new weighted searches reuse the same walkable grid and no-corner-cut rule but necessarily cost more CPU than canonical FAST A*. They run on explicit planning/resume, not every animation frame.

## Next city-system target

**Mobile Patrol Presence + Route Intelligence.** Turn the new influence corridors into moving security/gang patrol actors with search direction, temporary sweep windows and physical interception, while adding earned route intelligence from visited streets, contacts and terminals so exact exposure is not omniscient. Known corridors should be precise; poorly known neighborhoods should show uncertainty until the crew scouts them or buys intelligence. Route encounters should continue through the existing Living Streets/street-combat authorities, and patrol outcomes should feed Local Heat, district control and future corridor strength.
'''
path=root/'DEVELOPMENT_NOTE_PWA12_104_CITY_PATROL_ROUTING_CANDIDATE_08.md';path.write_text(text,encoding='utf-8')
(out/path.name).write_text(text,encoding='utf-8')
print(path)