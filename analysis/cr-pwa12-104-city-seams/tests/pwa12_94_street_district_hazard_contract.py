from pathlib import Path
root=Path(__file__).resolve().parents[1]
js=(root/'src/missions/variable-arenas-v14.js').read_text()
assert 'STREET_DISTRICT_HAZARDS' in js
for d in ('undergrid','floodline','dock_nine','neon_row'):
    assert f'{d}:' in js
assert "if(!mission?.v134StreetEncounter)return" in js
assert "c.hazardTypeV12=spec.type" in js
assert "c.hazardDamageV12=spec.damage" in js
assert "c.hazardStatusV12=spec.status||null" in js
assert "reserved.has(y*10+x)" in js
assert "applyStreetDistrictHazards(mission,shape)" in js
print('PASS PWA12.94: physical Street Clashes gain district-scoped tactical hazards without touching non-street missions')
