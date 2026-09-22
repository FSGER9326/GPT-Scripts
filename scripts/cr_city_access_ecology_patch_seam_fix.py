from pathlib import Path
import sys

p=Path(sys.argv[1] if len(sys.argv)>1 else 'scripts/cr_city_access_ecology_patch.py')
s=p.read_text(encoding='utf-8')
old='needle4="window.onDistrictTransitCompleteV12104?.({linkId:link.id,fromDistrict:current,toDistrict:to.district,mode});saveGame(0,true);return true"\nrepl4="window.onDistrictTransitCompleteV12104?.({linkId:link.id,fromDistrict:current,toDistrict:to.district,mode});window.commitTransitAccessEcologyV12104?.(ecology,{linkId:link.id,fromDistrict:current,toDistrict:to.district,mode});saveGame(0,true);return true"'
new='needle4="window.onDistrictTransitCompleteV12104?.({linkId:link.id,link,fromDistrict:current,toDistrict:to.district,fromNode:ep.node,toNode:to.node,mode,cost});saveGame(0,true);return true"\nrepl4="window.onDistrictTransitCompleteV12104?.({linkId:link.id,link,fromDistrict:current,toDistrict:to.district,fromNode:ep.node,toNode:to.node,mode,cost});window.commitTransitAccessEcologyV12104?.(ecology,{linkId:link.id,fromDistrict:current,toDistrict:to.district,mode});saveGame(0,true);return true"'
if new in s:
    print('Candidate 05 transit completion seam already hardened')
elif old in s:
    p.write_text(s.replace(old,new,1),encoding='utf-8')
    print('Hardened Candidate 05 transit completion seam for Candidate 02 callback payload')
else:
    raise SystemExit('Candidate 05 transit callback patch-script seam not found')
