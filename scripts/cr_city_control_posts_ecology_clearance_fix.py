from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve()
p=root/'src/world/district-control-posts-pwa12-104-city-candidate-07.js'
s=p.read_text(encoding='utf-8')
needle="const prevDraw=window.drawLivingStreetsV134;"
insert="""/* A physically resolved post owns the live Access Ecology friction for exactly one
   crossing. This prevents the same lockdown/toll being charged a second time after
   the player already handled it in-world; canonical faction/security access still runs. */
const prevEcoPrepare=window.prepareTransitAccessEcologyV12104;
if(prevEcoPrepare)window.prepareTransitAccessEcologyV12104=function(l,current,mode){const e=prevEcoPrepare.apply(this,arguments),c=validClearance(l?.id);if(!c)return e;return{...(e||{}),allowed:true,blocked:false,label:'CONTROL POST CLEARED',reason:'',costDelta:0,minutesDelta:0,heatDelta:0,riskDelta:0,controlPostClearance:copy(c),mode}};

"""
if 'controlPostClearance:copy(c)' not in s:
    if needle not in s:raise SystemExit('Candidate 07 ecology-clearance wrapper seam missing')
    s=s.replace(needle,insert+needle,1)
p.write_text(s,encoding='utf-8')
print('hardened Candidate 07 one-crossing Access Ecology clearance')
