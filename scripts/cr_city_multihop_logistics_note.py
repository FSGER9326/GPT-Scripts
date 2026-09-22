from pathlib import Path
import json,sys
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True)
meta=json.loads((root/'build-meta.json').read_text(encoding='utf-8'))
note=f'''# Chrome Requiem PWA12.104 — City Multi-Hop Logistics Candidate 04

## Candidate identity

- Version: `{meta.get('version')}`
- Build hash: `{meta.get('buildHash')}`
- Save schema: `{meta.get('schemaVersion')}`
- Canonical base reconstructed and verified before modification: `14.0.0-pwa.12.104-street-contact-support`, build `4313da4acd4c324a7672c36e`, schema 14.
- Canonical was not overwritten or promoted by this workflow.

## Player-facing increment

Candidate 04 adds **long-haul multi-hop logistics** to the physical city simulation. Eligible street contacts/services can now offer a run whose route has three real places and two real district crossings:

`physical pickup → first transit crossing → physical intermediate handoff → second transit crossing → physical final delivery`

The chain is generated from the existing district transit graph and existing physical contact/shop/clinic locations. Each leg is quoted through the Candidate 02 interdistrict route model, so A* street distance, available transit links, local route pressure, fares and access restrictions remain meaningful.

The long-haul option is added alongside the existing direct city run rather than replacing it. Accepting requires the crew to be physically at the pickup. Each transit leg is selected by the player and commits the existing `Game.pendingPath` to a real transit node. The existing `travelDistrictV133()` crossing remains authoritative.

The intermediate handoff is a true world-state gate: reaching the first destination does not pay or finish the job. The crew must physically reach the handoff location, the active dispatch enters a persisted `handoff` phase, and only while still at that location can the player prepare the second leg. Save/load during this handoff is supported.

The original delivery deadline is shared by both legs, so a safer/slower first route consumes time available for the second. Selected leg values combine into the final long-haul payout with a modest chain premium. Completion at the final physical location applies credits, destination neighborhood heat/prosperity/unrest effects, and contact-trust consequences.

Candidate 03 disruptions remain active on each transit leg. A resolved first-leg disruption is archived into the multi-hop plan at handoff, and disruption arm/trigger state is deliberately reset before leg 2 so the second physical crossing can develop its own incident instead of inheriting stale state.

## Architecture and persistence

- New module: `src/world/multihop-logistics-pwa12-104-city-candidate-04.js`.
- Surgical integration seam in Candidate 02 completion: multi-hop arrivals delegate to Candidate 04 instead of being mistaken for ordinary final delivery.
- Module order: Living Streets → District Dispatches → Interdistrict Logistics → Dynamic Disruptions → Multi-Hop Logistics → Mission Approaches.
- State remains under the existing `Game.livingStreetsV134.districtDispatches` owner (`multiHopOffers` plus fields on the active/history dispatch record).
- Save schema remains **14**; no key rename or destructive migration was introduced.
- No code in Candidate 04 assigns a new player coordinate to simulate travel. Existing physical path/transit authorities remain in control.

## Verification performed by the successful workflow

The packaging step that emitted this note runs only after all preceding build/test steps succeed.

- Exact PWA12.104 canonical reconstruction verified against build hash `4313da4acd4c324a7672c36e` and schema 14 before patches.
- Candidate 01 cumulative District Dispatches contract.
- Candidate 02 Interdistrict Logistics contract.
- Candidate 03 Dynamic Disruptions contract.
- Candidate 04 Multi-Hop Logistics contract.
- Production rebundle/build and Node syntax checks for city modules, district-worlds and runtime bundle.
- PWA12.104 Street Contact Support regression.
- PWA12.103 district-control context regression.
- PWA12.100 district-control effects regression.
- Save snapshot atomicity and corrupted-save recovery regressions.
- Active-city and route-marker performance contracts.
- Manifest and service-worker tests.
- Chromium Candidate 04 integration at **390×844** covering: coexistence with direct runs, physical pickup, first transit path, canonical crossing, physical intermediate handoff, save/load at handoff, second-leg activation, second transit path, canonical second crossing, physical final delivery, reward/state persistence, and mobile overflow geometry.
- Candidate 03 dynamic-disruption Chromium regression.
- Candidate 02 interdistrict Chromium regression.
- Existing PWA12.49 operation-routing and PWA12.45 multi-stage consequence Chromium regressions to protect city→mission→combat/extraction flows.

## Known boundaries

- One multi-hop dispatch may be active at a time because the existing dispatch system and `Game.pendingPath` are single-authority by design.
- Candidate 04 deliberately models exactly **two crossings / one handoff** per long-haul run. It does not auto-chain an arbitrary number of districts.
- The fixed overall deadline is established at acceptance from the two baseline leg windows plus a transfer buffer; choosing slower routes consumes that same deadline rather than renegotiating it.
- Long-haul offers are cached per source/day like the existing dispatch boards; city conditions can affect the generated quote, but an accepted job is not repriced mid-run.
- This increment does not introduce a second hidden transit simulator. Offscreen crossing behavior remains whatever the canonical transit system already models.

## Next city-system target

**District access ecology / changing route availability**: let faction territorial pressure, live incidents, infrastructure control and contact favors dynamically open, close, discount or compromise specific physical transit links and handoff services. The player should be able to learn those changes through street intelligence before committing a long-haul chain, then adapt the same multi-hop system when a district becomes hostile, a checkpoint hardens, or a covert passage becomes available.
'''
path=out/'DEVELOPMENT_NOTE_PWA12_104_CITY_MULTIHOP_LOGISTICS_CANDIDATE_04.md';path.write_text(note,encoding='utf-8');print(path)
