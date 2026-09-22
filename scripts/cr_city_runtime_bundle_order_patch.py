from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve()
p=root/'src/runtime/runtime-bundle.js'
s=p.read_text(encoding='utf-8')
local='/* SOURCE: src/world/district-dispatches-pwa12-104-city-candidate-01.js */'
cross='/* SOURCE: src/world/interdistrict-logistics-pwa12-104-city-candidate-02.js */'
mission='/* SOURCE: src/missions/contract-approaches-v13-4b.js */'
living='/* SOURCE: src/world/living-streets-v13-4a.js */'
if mission not in s or living not in s:
    raise SystemExit('authoritative runtime marker seam missing')
if local not in s:
    s=s.replace(mission,local+'\n'+cross+'\n'+mission,1)
elif cross not in s:
    s=s.replace(mission,cross+'\n'+mission,1)
# Validate exact relative order before rebundler consumes these markers.
pos=[s.index(x) for x in (living,local,cross,mission)]
if pos!=sorted(pos):
    raise SystemExit(f'city runtime marker order invalid: {pos}')
p.write_text(s,encoding='utf-8')
print('integrated cumulative city modules into runtime marker order:',living,'->',local,'->',cross,'->',mission)
