from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve()
p=root/'src/world/dynamic-logistics-disruptions-pwa12-104-city-candidate-03.js'
s=p.read_text(encoding='utf-8')
old="if(typeof window.advanceTime==='function')window.advanceTime(.25);else if(typeof advanceTime==='function')advanceTime(.25);"
new="if(typeof window.advanceTime==='function')window.advanceTime(15);else if(typeof advanceTime==='function')advanceTime(15);"
if old not in s:raise SystemExit('dynamic disruption push-through time seam missing')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('fixed push-through to canonical advanceTime(minutes): 15 minute penalty')
