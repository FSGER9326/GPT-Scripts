from pathlib import Path
import sys
p=Path(sys.argv[1] if len(sys.argv)>1 else 'scripts/cr_city_control_posts_patch.py')
t=p.read_text(encoding='utf-8')
a=t.find('needle2="window.onDistrictTransitCompleteV12104')
b=t.find('needle3="function openTransitNodeV133',a)
if a<0 or b<0:raise SystemExit('Candidate 07 brittle completion patch block not found')
replacement=r'''# Candidate 06 may have extended the transit completion callback text. Patch only
# inside the lexical travelDistrictV133 body and anchor on its unique final save/return.
if 'commitControlPostTransitV12104' not in s:
    start=s.find("function travelDistrictV133(linkId,mode='clear')")
    end=s.find("window.travelDistrictV133=travelDistrictV133;",start)
    if start<0 or end<0: raise SystemExit('travelDistrictV133 block missing for Candidate 07 completion hook')
    block=s[start:end]
    marker="saveGame(0,true);return true"
    if marker not in block: raise SystemExit('travelDistrictV133 final save/return seam missing')
    block=block.replace(marker,"window.commitControlPostTransitV12104?.({linkId:link.id,fromDistrict:current,toDistrict:to.district,mode});"+marker,1)
    s=s[:start]+block+s[end:]
'''
t=t[:a]+replacement+t[b:]
p.write_text(t,encoding='utf-8')
print('hardened Candidate 07 lexical transit completion seam')
