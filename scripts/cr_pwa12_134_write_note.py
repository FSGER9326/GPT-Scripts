from pathlib import Path
import json,sys
root=Path(sys.argv[1]).resolve()
meta=json.loads((root/'build-meta.json').read_text(encoding='utf-8'))
note=f'''# Chrome Requiem PWA12.134 — Target Pressure Reservations Candidate 01

## Baseline and scope

Candidate only. Canonical was not modified. This candidate is rebased from `Chrome_Requiem_v14_PWA_pwa12_133_BOUNDED_CONTACT_RELAY_CANDIDATE_01_source.zip`, itself rebased from PWA12.132 and preserving the cumulative PWA12.107–123 route/door/hazard/session lineage plus PWA12.124 suppression tempo and PWA12.133 observation-bounded contact memory.

Candidate version: `{meta['version']}`  
Build hash: `{meta['buildHash']}`  
Save schema: `{meta['schemaVersion']}` (unchanged)

## Integrated combat improvement — short-lived target pressure / lethal reservations

PWA12.133 fixed enemy omniscience, but sequential enemy activations still independently selected the same highest-scoring visible target. That could waste multiple attacks or movement commitments on one already-doomed unit and made mixed squads feel less coordinated than their pathfinding.

PWA12.134 adds a transient squad-intent board on top of the bounded knowledge model:

- A hostile activation reserves the target it has legitimately selected through current LOS or PWA12.133 contact rules.
- Ordinary pressure claims apply a moderate score penalty to later squadmates considering the same target. They encourage distribution but never make a target illegal; if it remains clearly the best or only option, later enemies may still attack it.
- A **lethal reservation** is created only when the current enemy has a visible in-range hit whose conservative base damage is enough to finish the target. It is stronger and shorter-lived than ordinary pressure.
- Lethal prediction deliberately refuses to assume success against Parry or an unused Undying defensive build. Crits, random bonuses and stale last-known contacts never create a guaranteed-finish claim.
- Coordination strength is role-sensitive rather than hive-mind uniform: Boss/Drone/Enforcer respect reservations most; Guard moderately; Heavy and Brute less, preserving their aggressive archetypes.
- Last-known contact proxies can carry only ordinary pressure intent. They cannot become lethal claims and never recover hidden live coordinates.
- Reservations are transient, keyed to exact `Game.grid` + `Game.units` identity, and pruned when the acting enemy/real target dies, the short TTL expires, or a stage rebuild creates new combat identity.
- Readability extends the existing contact cue vocabulary with `PIN` for pressure and `FIN` for a predicted finishing commitment. `CONTACT` and `SCAN` remain intact.
- After a predicted finishing attack fails to kill, its reservation is downgraded to ordinary pressure so the squad can re-evaluate rather than irrationally avoiding a survivor.

No enemy/player HP, damage, armor, AP, initiative, move range, weapon values, mission rewards or world-time rules were changed.

## Verification performed

This development note is generated only after every preceding workflow command succeeds. The candidate pipeline therefore records only checks actually completed before packaging.

Focused checks:

- JavaScript syntax check of rebuilt `src/runtime/runtime-bundle.js`
- new PWA12.134 source/runtime integration contract
- new deterministic real-Chromium PWA12.134 target-pressure test at 390x844

The focused Chromium scenario verifies that Guard and Enforcer initially prefer the same wounded frontliner; after the Guard's **real `enemyAITakeTurn`** creates a pressure reservation, the Enforcer redistributes to the Hacker; the Guard displays `PIN`; an in-range conservative guaranteed finish creates `FIN`, uses the two-activation lethal TTL and redirects the Enforcer; a PWA12.133 last-known proxy can only create ordinary pressure and reports zero guaranteed damage; the pressure board is absent from serialized save data and resets on grid identity replacement. Browser page errors are treated as failures. The test emits `qa/pwa12-134-target-pressure-mobile.png`.

Inherited affected-flow regressions:

- PWA12.133 bounded contact relay
- PWA12.116 coordinated-door routing
- PWA12.117 hazard-aware routing
- PWA12.118 reachable-target routing
- PWA12.120 retreat-door routing
- PWA12.121 stale enemy-session isolation
- PWA12.122 delayed combat-effect session isolation
- PWA12.123 mission lifecycle/session isolation
- PWA12.124 suppression/AP tempo
- world-freeze browser behavior
- release preflight

## Files changed

- `src/legacy/mercenary-intelligence-v8.js`: pressure board, role-weighted reservation scoring, conservative lethal prediction, active-AI integration and `PIN`/`FIN` cues.
- `src/runtime/runtime-bundle.js`: rebuilt from checked-in legacy source markers.
- generated build/version/precache/service-worker/index metadata from the existing build tool.
- `tests/pwa12_134_target_pressure_contract.py` and `tests/pwa12_134_target_pressure_browser.py`.
- `qa/pwa12-134-target-pressure-mobile.png` from the focused real-browser run.

## Balance / design uncertainties

1. `24` ordinary and `56` lethal raw penalty values are intentionally strong enough to prevent obvious waste while remaining soft preferences. Longer mixed-squad play should measure whether high-threat Hacker/AgentEX targets still attract enough coordinated fire.
2. Heavy/Brute discipline multipliers intentionally let assault units ignore some squad intent. Encounter telemetry should confirm this reads as role character rather than inconsistency.
3. The board is currently hostile-team-wide because shipping missions effectively field one hostile team. Future mixed-hostile-faction fights should partition reservations by faction/doctrine/comms network.
4. `FIN` predicts only conservative immediate base-hit lethality, not delayed DOT, burst/chain collateral, crits or ally reactions. That restraint is deliberate; adding speculative lethality would make the AI feel clairvoyant.
5. Cue density remains compact at 390x844 in the focused capture, but 6–8 enemy battles should be checked before adding more intent labels.

## Next combat priority

**Objective-aware fire-and-maneuver coordination.** Reuse the bounded contact + reservation boards to let one suitable ranged unit deliberately hold/suppress a route while another role advances, flanks, breaches or contests the mission objective. The next scenario should combine multiple doors, cover, a hazard lane, extraction/hold pressure and a cloaked flank, proving that role coordination changes positioning without granting hidden information, bypassing AP/door costs, or creating deterministic scripted turns.
'''
path=root/'DEVELOPMENT_NOTE_PWA12_134_TARGET_PRESSURE_RESERVATIONS.md'
path.write_text(note,encoding='utf-8')
print(path)
