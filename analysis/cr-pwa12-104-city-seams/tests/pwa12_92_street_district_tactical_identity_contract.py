from pathlib import Path
root=Path(__file__).resolve().parents[1]
js=(root/'src/missions/variable-arenas-v14.js').read_text()
css=(root/'src/styles/26-v14-variable-arenas.css').read_text()
bundle=(root/'src/runtime/runtime-bundle.js').read_text()
assert 'DISTRICT_THEMES' in js and "undergrid:{id:'undergrid'" in js and "crown_spire:{id:'crown_spire'" in js
assert 'board.dataset.arenaDistrict=theme.id' in js
assert 'c.el.dataset.surface=theme.surface' in js
assert "cover(c, name==='corridor'?'barrier':theme.cover)" in js
assert "theme.label+' // '+shape.name" in js
for d in ('undergrid','floodline','dock_nine','crown_spire'):
    assert f'data-arena-district="{d}"' in css
assert 'DISTRICT_THEMES' in bundle and 'arenaDistrict=theme.id' in bundle
print('PASS PWA12.92: tactical Street Clash arenas preserve visible physical district identity')
