from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve()
p=root/'tests/pwa12_104_city_dispatches_browser.py'
s=p.read_text(encoding='utf-8')
old="activateDistrictV133('old_market');showScreen('overworld-screen');"
new="activateDistrictV133('old_market');showScreen('overworld-screen');initOverworldV133();"
if old not in s:
    raise SystemExit('local dispatch browser lifecycle seam missing')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('fixed local dispatch browser to use canonical overworld initialization lifecycle')
