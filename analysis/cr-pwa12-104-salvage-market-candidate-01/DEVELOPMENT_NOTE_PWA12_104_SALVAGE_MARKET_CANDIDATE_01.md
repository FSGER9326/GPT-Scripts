# Chrome Requiem PWA12.104 Salvage Market Candidate 01

## Baseline
Reconstructed and hash-verified against canonical  /  before any edits. Canonical was not modified.

## Implemented
- Replaced broad automatic manufacturer loot with a deterministic field-salvage intake that is idempotent by mission id.
- Successful eligible operations can produce a manufacturer/district-provenance weapon or attachment recovery.
- Recovery condition affects only economy, never combat stats. Pending salvage offers KEEP, SELL, or STRIP.
- KEEP adds the existing canonical weapon to shared stash without auto-equipping, or adds an attachment copy to the armory.
- SELL converts the recovery into a bounded fraction of its base value.
- STRIP converts it into the existing salvage resource used by equipment maintenance, closing the mission-loot -> repair loop.
- Added visible local-industry supply discounts and imported-goods premiums to city markets using existing district industry data.
- Rare-stock purchases now consume that one limited entry instead of remaining infinitely purchasable for the day.
- Added safehouse Salvage Intake UI and mobile-responsive controls.

## Persistence
Salvage-exchange state lives additively inside existing , which is already serialized wholesale. Missing state defaults on load, so save schema remains 14 and older saves do not require destructive migration.

## Verification
The workflow first reconstructed canonical and asserted its exact recorded build hash. It then rebuilt this candidate and ran JavaScript syntax validation, the focused source contract, canonical save-recovery/load-menu/PWA contracts, a Pixel 7 browser integration covering KEEP/SELL/STRIP, pending-save restoration, synthetic old-save default migration, weapon swap, attachment install/remove, combat-unit stat bridging, strip-to-maintenance repair spending, local/import market supply, one-shot rare stock, and inherited stage/routing/architecture browser regressions.

The legacy PWA12.54 progressed-campaign equivalence test was also executed as an A/B control against untouched canonical and the candidate. Result: CONTROLLED PRE-EXISTING FAILURE: AssertionError: durable save/load mismatches: ['city', 'cityLife', 'districtWorldsV133', 'megaMapV132', 'ovPlayer', 'roster']. This is treated as pre-existing only when canonical and candidate produce the identical mismatch set; see .

See , , and  for exact executed output.

## Balance risks
The recovery frequency and resale/strip coefficients are first-pass economy tuning. Local/import price modifiers are deliberately modest because reputation, district wealth, and heat already modify prices. The implementation avoids random stat quality tiers; all kept gear retains its canonical item stats.

## Next progression priority
Add equipment specialization through workshop services (calibration/refit choices with reversible trade-offs) or consumable field loadout limits, after campaign-scale telemetry establishes whether salvage inflow is sustaining maintenance without trivializing cash flow.

## Build meta
```json
{
  "version": "14.0.0-pwa.12.104-salvage-market-candidate.01",
  "buildHash": "edcf4b3076eae4c95d397b3d",
  "builtAt": "2026-09-21T23:54:20.269207Z",
  "schemaVersion": 14,
  "releaseTarget": "pwa"
}
```
