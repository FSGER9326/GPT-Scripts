"""Chromium integration QA for cumulative PWA12.104 city interdistrict logistics candidate 02."""
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
      startNewGame('Interdistrict Logistics QA','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');
      activateDistrictV133('old_market');showScreen('overworld-screen');initOverworldV133();
      const w=currentDistrictV133(),defs=V13_DISTRICT_LOCATIONS.old_market,src=defs.find(d=>d.contact==='c1')||defs.find(d=>d.contact)||defs.find(d=>d.shop)||defs[0];
      Game.cityLife.discovered[src.id]=true;if(src.contact){Game.contactRelations[src.contact].known=true;Game.contactRelations[src.contact].trust=35}
      const p=w.locations[src.id];Game.ovPlayer={x:p.x,y:p.y};Game.districtWorldsV133.positions[w.id]={x:p.x,y:p.y};Game.pendingPath=null;
      updateDistrictDispatchUIV12104();updateInterdistrictDispatchUIV12104();
      const local=document.getElementById('v12104-dispatch-panel'),toggle=document.getElementById('v12104-open-city-run'),offer=offerInterdistrictDispatchV12104(src.id,w);
      return{src:src.id,contact:src.contact||null,offer,localText:local?.textContent||'',toggle:!!toggle,localDisplay:local?.style.display};
    }''')
    assert setup['offer'] and setup['offer']['targetDistrict']!='old_market',setup
    assert len(setup['offer']['options'])>=2,setup
    assert setup['toggle'] and 'STREET DISPATCH' in setup['localText'] and setup['localDisplay']!='none',setup
    route_choice=page.evaluate('''q=>{
      const risks=q.offer.options.map(o=>o.risk),types=q.offer.options.map(o=>o.linkType),payouts=q.offer.options.map(o=>o.payout);
      openInterdistrictDispatchBoardV12104();const p=document.getElementById('v12104-interdistrict-panel'),r=p.getBoundingClientRect();
      return{types,risks,payouts,text:p.textContent,width:r.width,right:r.right,scroll:document.documentElement.scrollWidth,inner:innerWidth};
    }''',setup)
    assert len(set(route_choice['types']))>=2 or max(route_choice['risks'])>min(route_choice['risks']),route_choice
    assert 'CITY LOGISTICS' in route_choice['text'] and 'BACK TO LOCAL BOARD' in route_choice['text'],route_choice
    assert route_choice['width']<=374 and route_choice['right']<=390.5 and route_choice['scroll']<=390,route_choice
    remote=page.evaluate('''q=>{const w=currentDistrictV133();Game.ovPlayer={x:0,y:0};return acceptInterdistrictDispatchV12104(q.offer.id)}''',setup)
    assert remote is False,remote
    accepted=page.evaluate('''q=>{
      const w=currentDistrictV133(),p=w.locations[q.src];Game.ovPlayer={x:p.x,y:p.y};Game.districtWorldsV133.positions[w.id]={x:p.x,y:p.y};
      const ok=acceptInterdistrictDispatchV12104(q.offer.id),a=activeInterdistrictDispatchV12104();updateInterdistrictDispatchUIV12104();const panel=document.getElementById('v12104-interdistrict-panel');
      return{ok,phase:a?.phase,active:a?.id,path:Game.pendingPath?.length||0,text:panel?.textContent||''};
    }''',setup)
    assert accepted['ok'] and accepted['phase']=='choose_transit' and accepted['path']==0 and 'Choose the city leg' in accepted['text'],accepted
    chosen=page.evaluate('''()=>{
      const a=activeInterdistrictDispatchV12104(),op=a.options.find(o=>!o.blocked);const before={day:Game.day,hour:Game.hour,credits:Game.credits};
      const ok=chooseInterdistrictTransitV12104(op.linkId),w=currentDistrictV133(),node=w.transit.find(t=>t.id===op.sourceNodeId);
      return{ok,linkId:op.linkId,linkType:op.linkType,sourceNodeId:op.sourceNodeId,phase:a.phase,path:Game.pendingPath?.length||0,before,node:{x:node.x,y:node.y},targetDistrict:a.targetDistrict,targetId:a.targetId,deadline:a.deadline};
    }''')
    assert chosen['ok'] and chosen['phase']=='to_transit' and chosen['path']>0,chosen
    assert page.evaluate('()=>saveGame(2,true)') is True
    restored=page.evaluate('''()=>{ensureDistrictDispatchStateV12104().active=null;const ok=loadGame(2),a=activeInterdistrictDispatchV12104();return{ok,id:a?.id||null,phase:a?.phase||null,link:a?.chosenLinkId||null}}''')
    assert restored['ok'] and restored['id']==setup['offer']['id'] and restored['phase']=='to_transit' and restored['link']==chosen['linkId'],restored
    crossed=page.evaluate('''q=>{
      const a=activeInterdistrictDispatchV12104(),w=currentDistrictV133(),node=w.transit.find(t=>t.id===q.sourceNodeId);Game.ovPlayer={x:node.x,y:node.y};Game.districtWorldsV133.positions[w.id]={x:node.x,y:node.y};Game.pendingPath=null;
      const before={day:Game.day,hour:Game.hour,credits:Game.credits},ok=travelDistrictV133(q.linkId,'clear'),after=activeInterdistrictDispatchV12104(),nw=currentDistrictV133();
      return{ok,before,afterTime:{day:Game.day,hour:Game.hour,credits:Game.credits},district:nw.id,phase:after?.phase,transitMode:after?.transitMode,targetKnown:!!Game.cityLife.discovered[after?.targetId],path:Game.pendingPath?.length||0,target:after?.targetId};
    }''',chosen)
    assert crossed['ok'] and crossed['district']==chosen['targetDistrict'] and crossed['phase']=='last_mile',crossed
    assert crossed['targetKnown'] and crossed['path']>0,crossed
    assert (crossed['afterTime']['day'],crossed['afterTime']['hour'])!=(crossed['before']['day'],crossed['before']['hour']) or crossed['afterTime']['credits']!=crossed['before']['credits'],crossed
    post=page.evaluate('''()=>{updateInterdistrictDispatchUIV12104();const p=document.getElementById('v12104-interdistrict-panel'),r=p.getBoundingClientRect();return{text:p.textContent,width:r.width,right:r.right,scroll:document.documentElement.scrollWidth}}''')
    assert 'LAST MILE' in post['text'] and post['right']<=390.5 and post['scroll']<=390,post
    page.screenshot(path=str(ROOT/'qa/pwa12-104-city-interdistrict-logistics-mobile.png'),full_page=True)
    completed=page.evaluate('''()=>{
      const w=currentDistrictV133(),a=activeInterdistrictDispatchV12104(),p=w.locations[a.targetId],before=Game.credits;Game.ovPlayer={x:p.x,y:p.y};Game.districtWorldsV133.positions[w.id]={x:p.x,y:p.y};Game.pendingPath=null;onStreetStepV134(w);const s=ensureDistrictDispatchStateV12104(),last=s.history[0];
      return{before,after:Game.credits,active:s.active,last:last&&{id:last.id,status:last.status,reward:last.reward,cross:!!last.crossDistrict},stats:s.stats};
    }''')
    assert completed['active'] is None and completed['last']['id']==setup['offer']['id'] and completed['last']['status']=='delivered' and completed['last']['cross'],completed
    assert completed['after']==completed['before']+completed['last']['reward'] and completed['stats']['crossDelivered']==1,completed
    compat=page.evaluate('''()=>{const s=ensureDistrictDispatchStateV12104();return{schema:14,crossOffers:typeof s.crossOffers,crossAccepted:s.stats.crossAccepted,crossDelivered:s.stats.crossDelivered}}''')
    assert compat['schema']==14 and compat['crossOffers']=='object' and compat['crossAccepted']==1 and compat['crossDelivered']==1,compat
    assert not errors,errors
    print('PASS interdistrict logistics browser: local-board preservation, route choice, physical transit node routing, canonical transit crossing, save/load, physical last-mile delivery, rewards, 390x844 UI')
    ctx.close();browser.close()
