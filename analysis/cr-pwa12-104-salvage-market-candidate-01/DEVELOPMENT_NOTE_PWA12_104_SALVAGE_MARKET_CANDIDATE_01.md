# Chrome Requiem PWA12.104 Salvage Market Candidate 01

## Baseline
Reconstructed and hash-verified against canonical `14.0.0-pwa.12.104-street-contact-support` / `4313da4acd4c324a7672c36e` before any edits. Canonical was not modified.

## Implemented
- Replaced broad automatic manufacturer loot with a deterministic field-salvage intake that is idempotent by mission id.
- Successful eligible operations can produce a manufacturer/district-provenance weapon or attachment recovery.
- Recovery condition affects only economy, never combat stats. Pending salvage offers KEEP, SELL, or STRIP.
- KEEP adds the existing canonical weapon to shared stash without auto-equipping, or adds an attachment copy to the armory.
- SELL converts the recovery into a bounded fraction of its base value.
- STRIP converts it into the existing salvage resource used by equipment maintenance, closing the mission-loot → repair loop.
- Added visible local-industry supply discounts and imported-goods premiums to city markets using existing district industry data.
- Rare-stock purchases now consume that one limited entry instead of remaining infinitely purchasable for the day.
- Added safehouse Salvage Intake UI and mobile-responsive controls.

## Persistence
Salvage-exchange state lives additively inside existing `companyV135`, which is already serialized wholesale. Missing state defaults on load, so save schema remains 14 and older saves do not require destructive migration.

## Verification
The workflow first reconstructed canonical and asserted its exact recorded build hash. It then rebuilt this candidate and ran JavaScript syntax validation, the focused source contract, canonical save-recovery/load-menu/PWA contracts, a Pixel 7 browser integration covering KEEP/SELL/STRIP, pending-save restoration, synthetic old-save default migration, weapon swap, attachment install/remove, combat-unit stat bridging, strip-to-maintenance repair spending, local/import market supply, one-shot rare stock, and inherited stage/routing/architecture browser regressions.

The legacy PWA12.54 progressed-campaign equivalence test was executed as an A/B control against untouched canonical and the candidate. Both produced the identical pre-existing mismatch set: `['city', 'cityLife', 'districtWorldsV133', 'megaMapV132', 'ovPlayer', 'roster']`. Because untouched canonical fails identically, this was recorded as a controlled baseline defect rather than a candidate regression. See `progressed-campaign-control.log`.

See `static-regression.log`, `browser-regression.log`, and `progressed-campaign-control.log` for exact executed output.

## Concrete QA observations
- Pixel 7 viewport: Salvage Intake width 366 px inside a 400 px modal, 0 px internal overflow and 0 px right overflow.
- Deterministic Kestrel recovery: `kestrel_needle`, FIELD-WORN 68%, base ¢2350, sell ¢971, strip ⚙4.
- KEEP preserved credits/salvage, added the weapon to stash, and did not auto-equip it.
- Equipment swap verified `kestrel_needle` at DMG 16 / RNG 9 / CRIT 27 versus the prior pistol at DMG 7 / RNG 4 / CRIT 15 for the QA operative.
- `stock_stabilizer` recovery added one owned copy, installed successfully, removed successfully through the weapon-bench UI, and reinstalled successfully; equipped sniper range rose to 10.
- Combat-unit derivation matched roster stats exactly: weapon `kestrel_needle`, DMG 16, RNG 10, CRIT 27.
- STRIP yielded ⚙2 in the exercised case; an 18-wear repair then cost ¢40 + ⚙1 and reset wear to 0.
- SELL yielded exactly ¢190 in the exercised case.
- Market helper returned local-manufacturer ×0.92 and imported-manufacturer ×1.12; rendered cards showed both labels.
- A manually injected rare `rifle_mk2` was visible before purchase, consumed successfully, removed from `Game.rareStock`, and disappeared from the shop afterward.
- Company diagnostics passed 12/12. Inherited stage-consequence, operation-routing, and eight-district architecture/mobile-art regressions passed with 0 page errors / 0 missing assets.

## Balance risks
The recovery frequency and resale/strip coefficients are first-pass economy tuning. Local/import price modifiers are deliberately modest because reputation, district wealth, and heat already modify prices. The implementation avoids random stat quality tiers; all kept gear retains its canonical item stats. Campaign-scale telemetry is still needed to determine whether salvage inflow sustains maintenance without making cash or parts trivial.

## Next progression priority
Add equipment specialization through workshop services (calibration/refit choices with reversible trade-offs) or consumable field-loadout limits, after campaign-scale telemetry establishes the new salvage economy’s steady-state pressure.

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
