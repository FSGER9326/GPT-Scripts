from pathlib import Path
import json,sys,re,hashlib
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True)
meta=json.loads((root/'build-meta.json').read_text(encoding='utf-8'))
bundle=(root/'src/runtime/runtime-bundle.js').read_text(encoding='utf-8');css=(root/'src/styles/runtime-bundle.css').read_text(encoding='utf-8');sw=(root/'service-worker.js').read_text(encoding='utf-8')
js_count=bundle.count('/* SOURCE: ');css_count=css.count('/* SOURCE: ')
precache=len(re.findall(r'"\./[^\"]+"', (root/'precache-manifest.js').read_text(encoding='utf-8')))
text=f'''# Chrome Requiem PWA12.104 — Patrol Corridors + Risk-Aware Physical Route Choice — Candidate 08

## Provenance and safety

This candidate was produced only after reconstructing the exact PWA12.104 canonical and asserting the canonical runtime identity `14.0.0-pwa.12.104-street-contact-support`, build hash `4313da4acd4c324a7672c36e`, schema 14. The cumulative City Candidates 01–07 were then reapplied through their established patch/test lineage before Candidate 08. Canonical itself was not edited or promoted.

Candidate version: `{meta['version']}`  
Candidate build hash: `{meta['buildHash']}`  
Save schema: `{meta['schemaVersion']}`  
Ordered JS sources: {js_count}  
Ordered CSS sources: {css_count}  
Precache entries: {precache}

## Substantial player-facing change

Candidate 08 adds **Patrol Corridors + Risk-Aware Physical Route Choice** to ordinary district navigation. Clicking a physical location, transit node, or arbitrary walkable map point now opens a street-route planner instead of immediately committing the only available line.

The player can choose:

- **FAST** — canonical shortest physical route; accepts exposure.
- **LOW PROFILE** — bounded detour chosen to reduce security, Local Heat, known patrol and control-post exposure.
- **BACK ALLEY** — more aggressive surveillance avoidance with a larger but still bounded detour budget.

All three choices are assembled from the existing `findDistrictPathV133()` street graph. Candidate 08 does not introduce teleportation or a second movement scheduler. Programmatic calls still invoke the canonical route function first so its existing movement wake-up/target ownership remains authoritative, then replace only `Game.pendingPath` with the selected canonical-path composition.

Route exposure reads the real Living Streets neighborhood state (`localHeat`, `security`, `gangPressure`, `unrest`), current physical street actors, and Candidate 07 control posts. Changing those systems therefore changes route advice rather than merely changing UI flavor.

The city map also renders subdued influence rings for relevant patrol/control sources once the crew is close enough or has learned that neighborhood. Physical street steps increase persisted route familiarity under `Game.livingStreetsV134.patrolCorridors`. With thin familiarity the planner gives qualitative exposure bands; sufficient familiarity reveals numeric exposure. The chosen route preference, familiarity, bounded history, and statistics persist through the existing Game save state without a schema migration.

While moving, the active-route card exposes FAST / LOW PROFILE / BACK ALLEY switching. A switch recomputes from the crew's **current physical position** to the existing destination; it never rewinds or teleports the crew.

## Architecture inspected before editing

The run audits the exact canonical and cumulative Candidate 07 seams before applying Candidate 08, including `district-worlds-v13-3.js`, Living Streets neighborhood/encounter state, physical street actors, Candidate 07 control posts, `Game.pendingPath`, `routeToPointV133`, `routeToLocationV133`, `routeToTransitNodeV133`, route-card rendering, overworld tap handling, street-step authority, save ownership, module order, runtime-bundle order, and existing city→combat routing.

Candidate 08 adds only one narrow canonical export (`window.routeToPointV133`) plus optional planner/decorator calls in the existing map-tap/route-card seams. The feature module loads after Candidate 07 control posts and before mission approaches.

## Verification evidence

The packaging step is reached only after all preceding workflow gates succeed. Those gates include:

- Candidate 08 structural/architecture contract, including canonical pathfinder reuse, physical patrol/control-post inputs, bounded detours, no player-coordinate assignment, canonical scheduler wake-up, mobile touch sizing, save ownership, and runtime/module order.
- Production rebundle/build and `node --check` for Candidate 08, district-world routing, Living Streets, Candidate 07, and the shipping runtime bundle.
- Candidate 01–07 cumulative contracts plus PWA12.104 Street Contact Support, district-control behavior, street combat/aftermath, save atomicity/recovery, active-city performance, route-marker performance, manifest and service-worker regressions.
- Chromium integration at **390×844**: a genuinely different risk-aware route is discovered from live district pressure, the planner fits without horizontal overflow, committing a route does not teleport the player, the canonical movement scheduler physically advances the crew, physical steps earn familiarity, preference/familiarity survive save/load, programmatic routing continues to honor the saved profile, and an in-motion profile switch replans from the current physical position.
- Candidate 07 control-post and Candidate 06 transit-incident browser regressions plus the established city→operation and multi-stage combat/extraction browser flows.

The mobile QA capture generated by that Chromium run is packaged with this note.

## Known boundaries

1. LOW PROFILE and BACK ALLEY are **bounded recompositions of canonical A\*** segments through plausible physical waypoints. They intentionally do not replace the canonical district pathfinder with a parallel weighted-A* authority. In a district whose walkable graph has no useful alternative, two profiles can legitimately collapse onto the same street line.
2. Patrol influence is a route-planning risk field inferred from current neighborhood pressure, physical street actors, and control posts. Patrol actors themselves are not yet continuously moving simulation agents with predictive future positions.
3. Exposure is recalculated when a route is planned or switched. A major condition change after commitment does not automatically seize control of the route; the player can manually switch, while Candidate 03 remains the authority for logistics-route disruptions.
4. Familiarity is neighborhood-level knowledge earned by physical movement. It is intentionally not a second global Street Memory system and does not reveal exact exposure immediately.
5. The preferred route profile persists; the ordinary `Game.pendingPath` remains transient according to canonical save architecture. Candidate 08 does not invent serialized path ownership.
6. Influence rendering is procedural UI/canvas work; no bespoke patrol-corridor environment art is introduced in this increment.

## Next city-system target

**Moving Patrols + Live Route Interception.** Patrol corridors should become temporally active: security/gang patrol actors move along short physical circuits, route exposure updates as they move, and crossing a patrol envelope can trigger a visible tail/search/challenge state. Street Memory/familiarity should forecast patrol windows rather than guarantee safety. The player should be able to wait, shadow a patrol, change route profile, duck into a known service/contact location, or accept a physical street encounter. Violent escalation must continue through the existing Living Streets combat bridge and feed Local Heat, faction pressure, and Candidate 07 control infrastructure.
'''
(root/'DEVELOPMENT_NOTE_PWA12_104_CITY_PATROL_CORRIDORS_CANDIDATE_08.md').write_text(text,encoding='utf-8')
(out/'DEVELOPMENT_NOTE_PWA12_104_CITY_PATROL_CORRIDORS_CANDIDATE_08.md').write_text(text,encoding='utf-8')
print(text)
