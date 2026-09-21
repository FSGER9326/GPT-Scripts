from pathlib import Path
s=Path('src/missions/variable-arenas-v14.js').read_text()
assert 'function applyDistrictControlEffectV14' in s
assert "district==='undergrid'" in s and 'e.overwatch=false' in s
assert "district==='floodline'" in s and 'delete u.statuses.poison' in s
assert "district==='dock_nine'" in s and 'disabledTurns=Math.max' in s
assert "district==='neon_row'" in s and 'statuses.cloak=Math.max' in s
assert 'applyDistrictControlEffectV14(state().activeMission,u)' in s
assert "if(d!==1)" in s and "if(u.ap<1)" in s
assert 'setInterval' not in s[s.index('function applyDistrictControlEffectV14'):s.index('const oldCellClick')]
print('PASS PWA12.100 district control effects')
