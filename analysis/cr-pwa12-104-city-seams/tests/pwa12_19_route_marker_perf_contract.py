from pathlib import Path
p=Path(__file__).resolve().parents[1]/'src/world/district-worlds-v13-3.js'
s=p.read_text(encoding='utf-8')
checks={
 'marker style computed once in collection': "style:markerStyle133(kind,l)" in s and "style:markerStyle133('transit',tr)" in s,
 'main map reuses marker style': "m.style||markerStyle133(m.kind,m.def)" in s,
 'minimap reuses marker style': "m.style||semanticMarkerV136(m.kind,m.def)" in s,
 'offscreen route dots culled': "p.x<-4||p.y<-4||p.x>W+4||p.y>H+4" in s,
}
for k,v in checks.items(): print(('PASS' if v else 'FAIL'),k)
assert all(checks.values())
