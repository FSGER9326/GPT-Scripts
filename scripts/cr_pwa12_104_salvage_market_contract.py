"""Static/source contract checks for the PWA12.104 salvage-market progression candidate."""
from pathlib import Path
import json,sys,re
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
mega=(root/'src/legacy/megacity-v11.js').read_text(encoding='utf-8')
city=(root/'src/legacy/city-life-v13.js').read_text(encoding='utf-8')
company=(root/'src/company/company-foundation-v13-5.js').read_text(encoding='utf-8')
css=(root/'src/styles/13-v13-5.css').read_text(encoding='utf-8')
meta=json.loads((root/'build-meta.json').read_text(encoding='utf-8'))
checks={
 'candidate version':meta['version']=='14.0.0-pwa.12.104-salvage-market-candidate.01',
 'schema retained':meta['schemaVersion']==14,
 'legacy loot delegated':"window.queueMissionSalvageV135==='function'" in mega,
 'durable salvage ledger':'s.salvageExchange.version=1' in company,
 'deterministic offer helper':'function salvageOfferForMissionV135(m)' in company,
 'three-way disposition':all(x in company for x in ["action==='keep'","action==='sell'","action==='strip'"]),
 'strip feeds canonical salvage':"Game.salvage=(Game.salvage||0)+d.stripValue" in company,
 'keep weapon does not auto-equip':"Game.stash.weapons.push(d.key)" in company,
 'market local supply pricing':'marketSupplyMultiplierV135' in company and 'window.marketSupplyMultiplierV135' in city,
 'rare stock consumed once':"delete Game.rareStock[shopId]" in city,
 'market supply badge':'marketSupplyBadgeV135' in company and 'LIMITED · ONE UNIT' in city,
 'safehouse intake rendered':'renderCompanyPanelV135();renderSalvageExchangeV135();' in company,
 'responsive salvage css':'PWA12.104 SALVAGE MARKET CANDIDATE 01' in css and '@media(max-width:720px)' in css,
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items(): print(('PASS' if v else 'FAIL'),k)
if failed: raise SystemExit('failed: '+', '.join(failed))
print('PASS salvage-market source contract',len(checks),'checks')
