from pathlib import Path
s=Path('src/missions/variable-arenas-v14.js').read_text()
for district, preview in {
    'undergrid':'CUT HOSTILE OVERWATCH',
    'floodline':'CLEAR POISON + RUNOFF',
    'dock_nine':'STALL HOSTILES 1 TURN',
    'neon_row':'CLOAK OPERATOR 1 TURN',
}.items():
    assert f"{district}:'{preview}'" in s
assert 'districtHazardControlEffectV14=STREET_CONTROL_EFFECT_PREVIEWS[mission.sectorId]' in s
assert 'c.el.dataset.controlEffect=c.districtHazardControlEffectV14' in s
assert "c.el.title=c.districtHazardControlLabelV14+' — 1 AP adjacent — '+c.districtHazardControlEffectV14" in s
assert "' — adjacent interaction, 1 AP — '+c.districtHazardControlEffectV14" in s
assert "NEUTRALIZE HAZARDS · '+payoff" in s
# Presentation preview must not change the established physical interaction cost/range.
assert 'if(d!==1)' in s and 'if(u.ap<1)' in s and 'u.ap--;c.hacked=true' in s
print('PASS PWA12.102 district control payoff preview')
