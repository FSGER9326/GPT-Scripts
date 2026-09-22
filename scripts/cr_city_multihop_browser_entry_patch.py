from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve();p=root/'tests/pwa12_104_city_multihop_logistics_browser.py'
s=p.read_text(encoding='utf-8')
old_life="updateInterdistrictDispatchUIV12104();updateMultiHopDispatchUIV12104();"
new_life="updateDistrictDispatchUIV12104();updateInterdistrictDispatchUIV12104();updateMultiHopDispatchUIV12104();"
if old_life not in s: raise SystemExit('browser local-board lifecycle seam missing')
s=s.replace(old_life,new_life,1)
old="const base=document.getElementById('v12104-interdistrict-panel'),offer=offerMultiHopDispatchV12104(src.id,w);return{src:src.id,sourceDistrict:w.id,offer,baseText:base?.textContent||'',hasDirect:!!base?.querySelector('#v12104-cross-accept'),hasMulti:!!base?.querySelector('#v12104-multi-accept')};"
new="const base=document.getElementById('v12104-interdistrict-panel'),local=document.getElementById('v12104-dispatch-panel'),offer=offerMultiHopDispatchV12104(src.id,w);return{src:src.id,sourceDistrict:w.id,offer,baseText:base?.textContent||'',localText:local?.textContent||'',hasDirect:!!(local?.querySelector('#v12104-open-city-run')||base?.querySelector('#v12104-cross-accept')),hasMulti:!!(local?.querySelector('#v12104-open-multihop')||base?.querySelector('#v12104-multi-accept'))};"
if old not in s: raise SystemExit('browser entry assertion seam missing')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('browser QA now initializes and validates normal preserved local-board entry points')
