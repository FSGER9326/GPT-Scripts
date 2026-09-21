from pathlib import Path
s=Path('src/missions/variable-arenas-v14.js').read_text()
assert 'districtHazardControlV14=true' in s
assert "c.el.classList.add('v14-district-control')" in s
assert "u.ap--;c.hacked=true" in s
assert "h.hazard=false;h.hazardTypeV12=null;h.hazardDamageV12=0;h.hazardStatusV12=null" in s
assert "h.el.classList.remove('hazard','v12-hazard','v14-district-hazard')" in s
assert "if(c?.districtHazardControlV14&&!c.hacked" in s
assert "return oldCellClick.apply(this,arguments)" in s
assert "mission?.v134StreetEncounter" in s
print('PASS PWA12.96: hazardous physical Street Clashes expose a 1-AP infrastructure override while ordinary terminal behavior is preserved')
