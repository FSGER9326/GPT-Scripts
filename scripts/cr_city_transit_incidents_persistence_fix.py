from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve()
mod=root/'src/world/transit-incidents-pwa12-104-city-candidate-06.js'
s=mod.read_text(encoding='utf-8')
old="""const prevInit=window.initOverworldV133;if(prevInit){const wrapped=function(){const r=prevInit.apply(this,arguments);setTimeout(()=>{detect();update()},0);return r};window.initOverworldV133=wrapped;if(window.initOverworld===prevInit)window.initOverworld=wrapped}"""
new="""function restoreIncidentRoute(){
 const a=active(),inc=currentIncident(),w=world();if(!a||!inc||inc.status!=='approach'||a.phase!=='to_incident'||w?.id!==inc.district||!Game.ovPlayer)return false;
 if(Math.hypot(Game.ovPlayer.x-inc.x,Game.ovPlayer.y-inc.y)<=1.65)return engageIncident(inc);
 if(Game.pendingPath?.length){Game._v133TravelTarget={kind:'v12104incident',id:inc.id,label:`TRANSIT INCIDENT // ${inc.ecology.label}`};return true}
 return routeIncident(inc)
}
window.restoreTransitIncidentRouteV12104=restoreIncidentRoute;
const prevInit=window.initOverworldV133;if(prevInit){const wrapped=function(){const r=prevInit.apply(this,arguments);setTimeout(()=>{restoreIncidentRoute();detect();update()},0);return r};window.initOverworldV133=wrapped;if(window.initOverworld===prevInit)window.initOverworld=wrapped}"""
if new not in s:
    if old not in s: raise SystemExit('Candidate 06 init-overworld restore seam missing')
    s=s.replace(old,new,1)
mod.write_text(s,encoding='utf-8')

# Strengthen the focused browser QA around the actual save/load lifecycle: pendingPath is
# transient in canonical saves, so entering the overworld must reconstruct the physical route
# from the persisted incident/node/dispatch state.
test=root/'tests/pwa12_104_city_transit_incidents_browser.py'
t=test.read_text(encoding='utf-8')
old_test="""    restored=page.evaluate('''()=>{Game.livingStreetsV134.transitIncidents.active=null;Game.pendingPath=null;const ok=loadGame(6),a=activeInterdistrictDispatchV12104(),i=Game.livingStreetsV134?.transitIncidents?.active;return{ok,id:a?.id,phase:a?.phase,incident:i?.id,status:i?.status,path:Game.pendingPath?.length||0}}''')
    assert restored['ok'] and restored['id']==setup['offerId'] and restored['status']=='approach' and restored['path']>0,restored
    page.wait_for_function(\"()=>Game.livingStreetsV134?.transitIncidents?.active?.status==='engaged'\",timeout=30000)
"""
new_test="""    restored=page.evaluate('''()=>{Game.livingStreetsV134.transitIncidents.active=null;Game.pendingPath=null;Game._v133TravelTarget=null;const ok=loadGame(6);showScreen('overworld-screen');initOverworldV133();const a=activeInterdistrictDispatchV12104(),i=Game.livingStreetsV134?.transitIncidents?.active;return{ok,id:a?.id,phase:a?.phase,incident:i?.id,status:i?.status}}''')
    assert restored['ok'] and restored['id']==setup['offerId'] and restored['status']=='approach',restored
    page.wait_for_function(\"()=>((Game.pendingPath?.length||0)>0&&Game._v133TravelTarget?.kind==='v12104incident')||Game.livingStreetsV134?.transitIncidents?.active?.status==='engaged'\",timeout=5000)
    resumed=page.evaluate('''()=>({path:Game.pendingPath?.length||0,target:Game._v133TravelTarget?.kind||null,status:Game.livingStreetsV134?.transitIncidents?.active?.status||null})''')
    assert (resumed['path']>0 and resumed['target']=='v12104incident') or resumed['status']=='engaged',resumed
    page.wait_for_function(\"()=>Game.livingStreetsV134?.transitIncidents?.active?.status==='engaged'\",timeout=30000)
"""
if new_test not in t:
    if old_test not in t: raise SystemExit('Candidate 06 browser save/load seam missing')
    t=t.replace(old_test,new_test,1)
test.write_text(t,encoding='utf-8')
print('hardened Candidate 06 save/load physical route resumption')
