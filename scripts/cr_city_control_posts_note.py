from pathlib import Path
import json,sys
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True)
meta=json.loads((root/'build-meta.json').read_text(encoding='utf-8'))
qa=root/'qa/pwa12-104-city-control-posts-mobile.png'
note=f'''# Chrome Requiem — PWA12.104 City District Control Posts Candidate 07

## Candidate identity
- Candidate: `{meta.get('version')}`
- Build hash: `{meta.get('buildHash')}`
- Save schema: `{meta.get('schemaVersion')}`
- Canonical base reconstructed and asserted before editing: `14.0.0-pwa.12.104-street-contact-support` / build `4313da4acd4c324a7672c36e` / schema 14.
- Canonical was not overwritten or promoted.

## Pre-edit inspection and architectural decision
The workflow reconstructs the exact PWA12.104 canonical first, builds it, and asserts the known build identity before applying any city candidate. It audits canonical world generation, transit links, A* route state, location/transit interaction, Living Streets encounter state and the save owner. Candidates 01–06 are then reapplied and their contracts are validated before Candidate 07 is introduced. A cumulative pre-07 audit is packaged beside this note.

The implementation follows these verified authorities rather than creating a parallel city engine:
- `district-worlds-v13-3.js` remains authoritative for generated district geometry, physical transit-node coordinates, A* routing, `Game.pendingPath` and the actual `travelDistrictV133()` crossing.
- Living Streets remains authoritative for neighborhood `localHeat`, `security`, `gangPressure`, `unrest`, free-roam movement/encounters and the existing tactical street-combat bridge.
- Candidate 05 Access Ecology remains the single live evaluator for endpoint pressure and faction/reputation context.
- Candidate 06 remains authoritative when an active logistics dispatch has already materialized a physical transit incident on the same crossing. Candidate 07 suppresses its own duplicate post in that case.
- Save state continues to be serialized from `Game`; Candidate 07 therefore persists under `Game.livingStreetsV134.controlPosts` without a save-schema migration.

## Substantial player-facing improvement: persistent free-roam district control posts
Control infrastructure now exists outside jobs. When live Access Ecology indicates meaningful physical friction at an ordinary transit approach — lockdown, ID sweep, screening, street levy, cargo toll, inspection or equivalent elevated pressure — a control post appears at the real transit node in the explorable district.

The post is derived from the actual crossing and its live endpoint neighborhoods, not from an abstract travel menu. It is drawn on the overworld, can be tapped, and routes the crew through the existing A* path into `Game.pendingPath`. The player is never teleported. Reaching the post through ordinary street movement opens the interaction.

The post also intercepts ordinary transit. Candidate 07 patches the narrow lexical seam inside canonical `openTransitNodeV133()` / `travelDistrictV133()` because the canonical transit modal calls its closure-local travel function. This prevents a UI path from bypassing the world object while preserving canonical travel as the crossing authority.

At a physical post the player can, when applicable:
- submit to the inspection / pay the local toll, consuming credits and time and changing neighborhood pressure;
- use AgentEX credentials to lower local/faction pressure;
- use a Hacker to spoof the control system, trading speed for additional local/faction heat;
- force the checkpoint and enter the established Living Streets tactical-combat bridge;
- back away and choose another physical route.

A successful resolution grants one persisted crossing clearance for that exact link. The clearance expires after 120 game minutes and is consumed only after a successful canonical district crossing. The already-resolved Access Ecology lock/surcharge is zeroed for that one crossing so the player is not charged twice for the same checkpoint, but canonical faction/security requirements are still evaluated normally.

A successful violent resolution additionally suppresses that control post for 180 game minutes. Neighborhood/faction combat consequences are still owned by `settleStreetCombatV134()`; Candidate 07 only records the post suppression and one-crossing clearance after the established aftermath runs.

Because `Game.pendingPath` is intentionally transient, Candidate 07 persists the approach objective itself. Loading a save made while walking to a post reconstructs the A* route from the saved district/link objective and the crew's restored physical position.

## Candidate 07 implementation files
- `src/world/district-control-posts-pwa12-104-city-candidate-07.js` — live post derivation, physical marker/tap/arrival flow, UI, resolutions, clearance/suppression/persistence and Candidate 06 coexistence.
- `src/world/district-worlds-v13-3.js` — three narrow optional seams: pre-crossing control-post authority, successful-crossing commit callback and transit-node interception. Canonical pathfinding/transit implementation remains otherwise authoritative.
- `src/bootstrap/module-manifest.js` — Candidate 07 registration after Candidate 06 and before mission approaches.
- `src/runtime/runtime-bundle.js` — matching ordered source marker for the production rebundler.
- `tests/pwa12_104_city_control_posts_contract.py` — structural/architecture contract.
- `tests/pwa12_104_city_control_posts_browser.py` — Chromium free-roam/navigation/persistence/combat/mobile integration QA.

## Verified evidence
This note is generated only after the packaging workflow has passed the preceding gates. The final workflow covers:
- exact PWA12.104 canonical reconstruction and identity assertion before editing;
- canonical pre-edit city audit and cumulative pre-07 city audit;
- cumulative Candidate 01–06 contracts before Candidate 07;
- Candidate 07 focused contract and JavaScript syntax checks;
- canonical Street Contact Support, district-control, street-combat/aftermath, save atomicity/recovery, active-city performance, route-marker performance, manifest and service-worker regressions;
- Chromium at 390×844 proving a control post exists with **no active dispatch**, blocks ordinary transit bypass, creates a real A* `Game.pendingPath` without moving the player instantly, survives save/load by reconstructing that route, is physically reached through the production overworld movement loop, exposes touch-safe mobile UI, persists a Hacker clearance, crosses through canonical `travelDistrictV133()`, consumes the clearance exactly once, and uses the established tactical street-combat bridge for violent resolution/suppression;
- cumulative Candidate 06, 05, 04, 03 and 02 browser regressions;
- existing PWA12.49 operation-routing and PWA12.45 multi-stage combat/extraction browser regressions.

Mobile QA capture: `{qa.name}` ({'present' if qa.exists() else 'missing at note-generation time'}).

## Known boundaries
- Posts are systemic live world objects derived from transit-link and neighborhood state, not permanently authored barricade scenery. If the underlying pressure clears, an unresolved derived post can disappear; this is intentional reactivity rather than static level decoration.
- Candidate 07 currently places control infrastructure only on physical district transit approaches. It does not yet project search zones deep into ordinary streets or gate shops/clinics directly.
- Hidden/covert links do not receive ordinary visible control posts; their discoverability remains governed by the existing hidden-route system.
- Only violent resolution enters tactical combat. Compliance, credentials and hacking remain compact street interactions with explicit resource/time/state consequences rather than bespoke minigames.
- One crossing clearance lasts 120 game minutes and is consumed on successful travel. A violent victory suppresses the post for 180 game minutes. These values have integration coverage but have not received a long-campaign balance study.
- Candidate 06 physical logistics incidents deliberately supersede Candidate 07 on the same link while active so the player never receives two checkpoint systems at one coordinate.
- The post marker is procedural canvas/UI presentation; Candidate 07 does not add bespoke barricade environment art.

## Next city-system target
**Patrol corridors and risk-aware route choice.** Extend control posts into visible street influence: security sweeps, gang patrol corridors and temporary search zones should project onto nearby road segments. The route planner should offer physically distinct FAST / LOW-PROFILE / BACK-ALLEY routes using the existing A* graph with different heat/security/exposure weights, while Street Memory controls how much risk information is revealed. This would make the route to a contact or transit node a meaningful tactical city decision instead of only making the destination interactive.
'''
path=out/'DEVELOPMENT_NOTE_PWA12_104_CITY_CONTROL_POSTS_CANDIDATE_07.md'
path.write_text(note,encoding='utf-8');print(path)
