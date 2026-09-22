"""Chromium integration QA for PWA12.104 City Transit Incidents Candidate 06."""
from pathlib import Path
import mimetypes,sys
from playwright.sync_api import sync_playwright
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();(ROOT/'qa').mkdir(exist_ok=True)
HTML=(ROOT/'index.html').read_text().replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
SHIM="""<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"""
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    ctx=browser.new_context(viewport={'width':390,'height':844});errors=[]
    def route(r):
        rel=r.request.url.split('http://cr.local/',1)[-1].split('?',1)[0] or 'index.html';p=ROOT/rel
        r.fulfill(status=200,body=p.read_bytes(),content_type=mimetypes.guess_type(p.name)[0] or 'application/octet-stream') if p.is_file() else r.fulfill(status=404,body=b'not found')
    ctx.route('http://cr.local/**',route);page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content(HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1),wait_until='domcontentloaded');page.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
    setup=page.evaluate('''()=>{
      startNewGame('Transit Incident QA','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');Game.notoriety=0;Game.rep=Game.rep||{};Game.heat=Game.heat||{};
      activateDistrictV133('old_market');showScreen('overworld-screen');initOverworldV133();
      const w=currentDistrictV133(),defs=V13_DISTRICT_LOCATIONS.old_market,src=defs.find(d=>d.contact==='c1')||defs.find(d=>d.contact)||defs.find(d=>d.shop)||defs[0];Game.cityLife.discovered[src.id]=true;
      if(src.contact){Game.contactRelations[src.contact].known=true;Game.contactRelations[src.contact].trust=45}
      const p=w.locations[src.id];Game.ovPlayer={x:p.x,y:p.y};Game.districtWorldsV133.positions[w.id]={x:p.x,y:p.y};Game.pendingPath=null;Game._v133TravelTarget=null;
      Object.values(ensureNeighborhoodStateV134(w)).forEach(h=>Object.assign(h,{localHeat:5,security:1,gangPressure:1,unrest:1,controller:'local'}));
      const offer=offerInterdistrictDispatchV12104(src.id,w),ok=acceptInterdistrictDispatchV12104(offer.id),a=activeInterdistrictDispatchV12104();
      const op=a.options.find(o=>o.linkType==='metro')||a.options.find(o=>o.linkType==='border')||a.options.find(o=>o.linkType==='freight')||a.options.find(o=>o.linkType==='security')||a.options.find(o=>o.linkType!=='hidden');
      if(!op)throw new Error('No non-hidden interdistrict option');
      return{src:src.id,contact:src.contact,offerId:offer.id,accepted:ok,linkId:op.linkId,linkType:op.linkType,sourceNode:op.sourceNodeId,target:a.targetDistrict,deadline:a.deadline,player:{x:Game.ovPlayer.x,y:Game.ovPlayer.y}};
    }''')
    assert setup['accepted'],setup
    pressured=page.evaluate('''q=>{
      const l=V133_TRANSIT_LINKS.find(x=>x.id===q.linkId),a=l.from.district==='old_market'?l.from:l.to,b=l.from.district==='old_market'?l.to:l.from;
      function press(d,node){const w=generateDistrictV133(d),tr=w.transit.find(x=>x.id===node),states=ensureNeighborhoodStateV134(w);let id=null,bd=1e9;for(const n of w.neighborhoods){const dd=Math.hypot(tr.x-n.x,tr.y-n.y);if(dd<bd){bd=dd;id=n.id}}const h=states[id];Object.assign(h,{localHeat:92,security:5,gangPressure:q.linkType==='freight'?5:2,unrest:q.linkType==='freight'?4:2,controller:'local'});return{id,x:tr.x,y:tr.y}}
      const h1=press(a.district,a.node),h2=press(b.district,b.node);refreshTransitAccessEcologyV12104();const eco=evaluateTransitAccessEcologyV12104(q.linkId,'old_market','courier');return{eco,h1,h2,needs:CR_CITY_TRANSIT_INCIDENTS.needsIncident(eco)};
    }''',setup)
    assert pressured['needs'],pressured
    started=page.evaluate('''q=>{const before={x:Game.ovPlayer.x,y:Game.ovPlayer.y},ok=chooseInterdistrictTransitV12104(q.linkId),a=activeInterdistrictDispatchV12104(),inc=Game.livingStreetsV134.transitIncidents.active,n=currentDistrictV133().transit.find(t=>t.id===q.sourceNode);return{ok,before,after:{x:Game.ovPlayer.x,y:Game.ovPlayer.y},phase:a?.phase,path:Game.pendingPath?.length||0,target:Game._v133TravelTarget,inc,node:n,deadline:a?.deadline}}''',setup)
    assert started['ok'] and started['phase']=='to_incident' and started['path']>0 and started['target']['kind']=='v12104incident',started
    assert started['inc']['x']==started['node']['x'] and started['inc']['y']==started['node']['y'],started
    assert started['before']==started['after'],started
    assert page.evaluate('()=>saveGame(6,true)') is True
    restored=page.evaluate('''()=>{Game.livingStreetsV134.transitIncidents.active=null;Game.pendingPath=null;const ok=loadGame(6),a=activeInterdistrictDispatchV12104(),i=Game.livingStreetsV134?.transitIncidents?.active;return{ok,id:a?.id,phase:a?.phase,incident:i?.id,status:i?.status,path:Game.pendingPath?.length||0}}''')
    assert restored['ok'] and restored['id']==setup['offerId'] and restored['status']=='approach' and restored['path']>0,restored
    page.wait_for_function("()=>Game.livingStreetsV134?.transitIncidents?.active?.status==='engaged'",timeout=30000)
    engaged=page.evaluate('''()=>{const i=Game.livingStreetsV134.transitIncidents.active,a=activeInterdistrictDispatchV12104(),p=document.getElementById('v12104-transit-incident-panel'),r=p.getBoundingClientRect(),buttons=[...p.querySelectorAll('button')].map(b=>({text:b.textContent,h:b.getBoundingClientRect().height}));return{status:i.status,phase:a.phase,dist:Math.hypot(Game.ovPlayer.x-i.x,Game.ovPlayer.y-i.y),deadline:a.deadline,width:r.width,left:r.left,right:r.right,scroll:document.documentElement.scrollWidth,inner:innerWidth,display:getComputedStyle(p).display,buttons,text:p.textContent}}''')
    assert engaged['status']=='engaged' and engaged['phase']=='incident' and engaged['dist']<=1.65,engaged
    assert engaged['display']!='none' and engaged['width']<=374.5 and engaged['left']>=-0.5 and engaged['right']<=390.5 and engaged['scroll']<=390,engaged
    assert engaged['buttons'] and min(x['h'] for x in engaged['buttons'])>=43.5,engaged
    page.screenshot(path=str(ROOT/'qa/pwa12-104-city-transit-incidents-mobile.png'),full_page=True)
    assert page.evaluate('()=>saveGame(7,true)') is True

    # Verify the violent option really enters the established tactical street-combat bridge,
    # then use the canonical aftermath function to verify Candidate 06 receives the result.
    combat=page.evaluate('''()=>{const ok=fightTransitIncidentV12104();return{ok,phase:activeInterdistrictDispatchV12104()?.phase,status:Game.livingStreetsV134.transitIncidents.active?.status}}''')
    assert combat['ok'] and combat['phase']=='incident_combat' and combat['status']=='combat',combat
    page.wait_for_function('()=>!!Game.activeMission?.v134StreetEncounter',timeout=5000)
    combat_done=page.evaluate('''()=>{const m=Game.activeMission,actor=m?.v134StreetActorType,ok=settleStreetCombatV134(m,true),a=activeInterdistrictDispatchV12104(),i=Game.livingStreetsV134.transitIncidents.active;return{ok,actor,phase:a?.phase,status:i?.status,clear:a?.transitIncidentClearances?.[i?.linkId]||null}}''')
    assert combat_done['ok'] and combat_done['actor'] in ('security','gang','contractor') and combat_done['phase']=='incident_cleared' and combat_done['status']=='cleared' and combat_done['clear'],combat_done

    # Restore the untouched engaged save and verify retreat is a genuine route-choice consequence.
    ret=page.evaluate('''q=>{const ok=loadGame(7);showScreen('overworld-screen');initOverworldV133();const a=activeInterdistrictDispatchV12104(),before=a.deadline,inc=Game.livingStreetsV134.transitIncidents.active,r=retreatTransitIncidentV12104(),b=activeInterdistrictDispatchV12104(),alt=b.options.find(o=>o.linkId!==q.linkId&&!o.blocked);let chosen=null;if(alt){chosen=chooseInterdistrictTransitV12104(alt.linkId)}return{ok,r,before,after:b?.deadline,carry:b?.transitIncidentCarryDeadline||null,phase:b?.phase,alt:alt?.linkId||null,chosen,path:Game.pendingPath?.length||0,player:{x:Game.ovPlayer.x,y:Game.ovPlayer.y},inc:{x:inc.x,y:inc.y}}}''',setup)
    assert ret['ok'] and ret['r'],ret
    if ret['alt']:
        assert ret['chosen'] and ret['after']==ret['before'] and ret['path']>0,ret

    # Restore again and clear nonviolently with the Hacker; clearance must persist across save/load.
    cleared=page.evaluate('''q=>{loadGame(7);showScreen('overworld-screen');initOverworldV133();updateTransitIncidentUIV12104();const i=Game.livingStreetsV134.transitIncidents.active,h=ensureNeighborhoodStateV134(currentDistrictV133())[i.neighborhood],before={min:Math.round((((Game.day||1)-1)*24+(Game.hour||0))*60),heat:h.localHeat},ok=spoofTransitIncidentV12104('hacker'),a=activeInterdistrictDispatchV12104(),c=a.transitIncidentClearances?.[q.linkId],after={min:Math.round((((Game.day||1)-1)*24+(Game.hour||0))*60),heat:h.localHeat};return{ok,before,after,phase:a.phase,status:Game.livingStreetsV134.transitIncidents.active.status,clear:c}}''',setup)
    assert cleared['ok'] and cleared['phase']=='incident_cleared' and cleared['status']=='cleared' and cleared['clear'] and not cleared['clear']['consumed'],cleared
    assert cleared['after']['min']-cleared['before']['min']==3,cleared
    assert page.evaluate('()=>saveGame(8,true)') is True
    persisted=page.evaluate('''q=>{Game.livingStreetsV134.transitIncidents.active=null;const ok=loadGame(8),a=activeInterdistrictDispatchV12104(),i=Game.livingStreetsV134.transitIncidents.active,c=a.transitIncidentClearances?.[q.linkId];return{ok,status:i?.status,phase:a?.phase,clear:c}}''',setup)
    assert persisted['ok'] and persisted['status']=='cleared' and persisted['phase']=='incident_cleared' and persisted['clear'],persisted

    # Enter the same physical transit node only after clearance; canonical crossing remains authority.
    proceed=page.evaluate('''q=>{const i=Game.livingStreetsV134.transitIncidents.active;Game.ovPlayer={x:i.x,y:i.y};Game.districtWorldsV133.positions[i.district]={x:i.x,y:i.y};const ok=continueTransitIncidentV12104(),a=activeInterdistrictDispatchV12104();return{ok,phase:a?.phase,chosen:a?.chosenLinkId,deadline:a?.deadline}}''',setup)
    assert proceed['ok'] and proceed['phase']=='to_transit' and proceed['chosen']==setup['linkId'],proceed
    crossed=page.evaluate('''q=>{const a=activeInterdistrictDispatchV12104(),before=currentDistrictV133().id,ok=travelDistrictV133(q.linkId,'clear'),b=activeInterdistrictDispatchV12104(),c=b?.transitIncidentClearances?.[q.linkId],st=Game.livingStreetsV134.transitIncidents;return{ok,before,after:currentDistrictV133()?.id,phase:b?.phase,path:Game.pendingPath?.length||0,clear:c,active:st.active,history:st.history[0],stats:st.stats}}''',setup)
    assert crossed['ok'] and crossed['after']==setup['target'] and crossed['after']!=crossed['before'],crossed
    assert crossed['phase']=='last_mile' and crossed['path']>0 and crossed['clear']['consumed'] and crossed['active'] is None,crossed
    assert crossed['history']['status']=='crossed' and crossed['stats']['crossed']>=1,crossed
    assert not errors,errors
    print('PASS Candidate 06 browser: physical transit incident placement/navigation, save-load, 390x844 UI, tactical-combat bridge, retreat/replan deadline, nonviolent clearance, canonical crossing and last mile')
    ctx.close();browser.close()
