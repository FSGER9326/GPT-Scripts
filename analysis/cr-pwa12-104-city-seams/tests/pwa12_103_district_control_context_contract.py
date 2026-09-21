from pathlib import Path
s=Path('src/missions/variable-arenas-v14.js').read_text(encoding='utf-8')
css=Path('src/styles/26-v14-variable-arenas.css').read_text(encoding='utf-8')
assert 'refreshDistrictControlFeedbackV14' in s
assert "d===1" in s and "v14-control-actionable" in s
assert "CLICK CONTROL · 1 AP" in s and "NO AP · 1 AP REQUIRED" in s
assert "district-control-context" in s and "district-control-context" in css
assert "classList.toggle('ready-v10'" in s
assert 'NEUTRALIZE HAZARDS' in s
print('PASS PWA12.103: district controls correct inherited range highlights and expose adjacent 1-AP contextual feedback')
