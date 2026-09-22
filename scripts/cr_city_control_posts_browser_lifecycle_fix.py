from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve()
p=root/'tests/pwa12_104_city_control_posts_browser.py'
s=p.read_text(encoding='utf-8')
old="""    fight_setup=page.evaluate('''q=>{activateDistrictV133('old_market');showScreen('overworld-screen');initOverworldV133();const w=currentDistrictV133(),st=ensureLivingStreetsStateV134();st.lastEventStep=st.stepCount+999999;const c=st.controlPosts.clearances[q.linkId];if(c)c.consumed=true;delete st.controlPosts.suppressed['old_market:'+q.linkId];const p=controlPostForLinkV12104(q.linkId,'old_market');if(!p)throw new Error('control post did not reform after consumed clearance');Game.ovPlayer={x:p.x,y:p.y};Game.districtWorldsV133.positions.old_market={x:p.x,y:p.y};const opened=openControlPostV12104(q.linkId),ok=fightControlPostV12104(q.linkId);return{opened,ok,active:Game.activeMission?{street:!!Game.activeMission.v134StreetEncounter,actor:Game.activeMission.v134StreetActorType}:null,combat:st.controlPosts.activeCombat}}''',setup)
    assert fight_setup['opened'] and fight_setup['ok'] and fight_setup['active']['street'] and fight_setup['combat'],fight_setup
    page.wait_for_function('()=>!!Game.activeMission?.v134StreetEncounter',timeout=5000)
    fight_done=page.evaluate('''q=>{const m=Game.activeMission,ok=settleStreetCombatV134(m,true),st=Game.livingStreetsV134.controlPosts,sup=st.suppressed['old_market:'+q.linkId],c=st.clearances[q.linkId];showScreen('overworld-screen');initOverworldV133();const post=controlPostForLinkV12104(q.linkId,'old_market');return{ok,actor:m.v134StreetActorType,sup,c,post,last:st.history[0]}}''',setup)
"""
new="""    fight_setup=page.evaluate('''q=>{activateDistrictV133('old_market');showScreen('overworld-screen');initOverworldV133();const w=currentDistrictV133(),st=ensureLivingStreetsStateV134();st.lastEventStep=st.stepCount+999999;const c=st.controlPosts.clearances[q.linkId];if(c)c.consumed=true;delete st.controlPosts.suppressed['old_market:'+q.linkId];const p=controlPostForLinkV12104(q.linkId,'old_market');if(!p)throw new Error('control post did not reform after consumed clearance');Game.ovPlayer={x:p.x,y:p.y};Game.districtWorldsV133.positions.old_market={x:p.x,y:p.y};const opened=openControlPostV12104(q.linkId),ok=fightControlPostV12104(q.linkId);return{opened,ok,active:Game.activeMission?.id||null,combat:st.controlPosts.activeCombat}}''',setup)
    assert fight_setup['opened'] and fight_setup['ok'] and fight_setup['combat'],fight_setup
    # Living Streets uses the established V10 tactical briefing. Candidate 07 must
    # enter that player-facing lifecycle, not assume combat is active before DEPLOY.
    page.wait_for_function(\"()=>{const s=document.getElementById('v10-briefing');return s&&getComputedStyle(s).display!=='none'&&[...s.querySelectorAll('button')].some(b=>b.textContent.includes('DEPLOY'))}\",timeout=5000)
    briefing=page.evaluate('''()=>{const s=document.getElementById('v10-briefing'),b=[...s.querySelectorAll('button')].find(x=>x.textContent.includes('DEPLOY'));return{screen:[...document.querySelectorAll('.screen')].find(x=>getComputedStyle(x).display!=='none')?.id||null,deploy:!!b,active:Game.activeMission?.id||null}}''')
    assert briefing['screen']=='v10-briefing' and briefing['deploy'] and briefing['active'] is None,briefing
    deployed=page.evaluate('''()=>{const s=document.getElementById('v10-briefing'),b=[...s.querySelectorAll('button')].find(x=>x.textContent.includes('DEPLOY'));if(!b)return false;b.click();return true}''')
    assert deployed,briefing
    page.wait_for_function('()=>!!Game.activeMission?.v134StreetEncounter',timeout=5000)
    fight_done=page.evaluate('''q=>{const m=Game.activeMission,ok=settleStreetCombatV134(m,true),st=Game.livingStreetsV134.controlPosts,sup=st.suppressed['old_market:'+q.linkId],c=st.clearances[q.linkId];showScreen('overworld-screen');initOverworldV133();const post=controlPostForLinkV12104(q.linkId,'old_market');return{ok,actor:m.v134StreetActorType,sup,c,post,last:st.history[0]}}''',setup)
"""
if new not in s:
    if old not in s:raise SystemExit('Candidate 07 browser combat lifecycle seam missing')
    s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Candidate 07 browser now exercises canonical V10 briefing -> DEPLOY -> street combat lifecycle')
