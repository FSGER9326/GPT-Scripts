from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve()
p=root/'src/world/interdistrict-logistics-pwa12-104-city-candidate-02.js'
s=p.read_text(encoding='utf-8')
old="a.transitMode=ctx.mode||'clear';a.transitAt=nowMin();a.phase='last_mile';revealTarget(a);setTimeout(()=>{window.routeToLocationV133?.(a.targetId);update()},0);window.addJournal?.('side','CITY TRANSIT LEG'"
new="a.transitMode=ctx.mode||'clear';a.transitAt=nowMin();a.phase='last_mile';revealTarget(a);const routed=window.routeToLocationV133?.(a.targetId);a.lastMileRouted=!!routed;update();window.addJournal?.('side','CITY TRANSIT LEG'"
if old not in s:
    raise SystemExit('interdistrict deferred last-mile seam missing')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('made interdistrict last-mile routing synchronous before transit save')
