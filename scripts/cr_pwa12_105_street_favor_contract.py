from pathlib import Path
import json,sys
R=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
src=(R/'src/world/living-streets-v13-4a.js').read_text(encoding='utf-8')
city=(R/'src/legacy/city-life-v13.js').read_text(encoding='utf-8')
bundle=(R/'src/runtime/runtime-bundle.js').read_text(encoding='utf-8')
for s in (src,bundle):
    assert 's.contactFavors=s.contactFavors||{}' in s
    assert 's.contactFavorHistory=s.contactFavorHistory||{}' in s
    assert 'function awardStreetFavorV134' in s
    assert 'function resolveStreetFavorV134' in s
    assert 'window.CR14MultiStageOperations?.nearContact' in s
    assert "choice==='countermove'" in s
    assert 'v134StreetFavorFollowUp:true' in s
    assert 'factionRepGain:4+diff' in s
    assert "h.localHeat=clampV134(beforeLocal-12,0,100)" in s
    assert "clampV134(beforeFaction-8,0,100)" in s
    assert 'TURN FAVOR INTO COUNTERMOVE' in s
assert 'window.decorateStreetFavorDossierV134?.(id);' in city
assert 'window.decorateStreetFavorDossierV134?.(id);' in bundle
meta=json.loads((R/'build-meta.json').read_text())
assert meta['version']=='14.0.0-pwa.12.105-faction-street-favors'
assert meta['schemaVersion']==14
print('PWA12.105 faction street favor contract PASS')
