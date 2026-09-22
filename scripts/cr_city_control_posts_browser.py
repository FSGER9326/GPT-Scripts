"""Chromium integration QA for PWA12.104 City District Control Posts Candidate 07."""
from pathlib import Path
import mimetypes,sys
from playwright.sync_api import sync_playwright
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();(ROOT/'qa').mkdir(exist_ok=True)
HTML=(ROOT/'index.html').read_text(encoding='utf-8').replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
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
      startNewGame('Control Post QA','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');Game.notoriety=0;Game.rep=Game.rep||{};Game.heat=Game.heat||{};
      activateDistrictV133('old_market');showScreen('overworld-screen');initOverworldV133();
      const w=currentDistrictV133(),s=ensureLivingStreetsStateV134();s.lastEventStep=s.stepCount+999999;
      const src=Object.entries(w.locations)[0];if(src){Game.ovPlayer={x:src[1].x,y:src[1].y};Game.districtWorldsV133.positions[w.id]={x:src[1].x,y:src[1].y}}
      const linkId='old_civic_gate',l=V133_TRANSIT_LINKS.find(x=>x.id===linkId);if(!l)throw new Error('old_civic_gate missing');
      function press(ep){const ww=generateDistrictV133(ep.district),tr=ww.transit.find(x=>x.id===ep.node),states=ensureNeighborhoodStateV134(ww);let id=null,bd=1e9;for(const n of ww.neighborhoods){const d=Math.hypot(tr.x-n.x,tr.y-n.y);if(d<bd){bd=d;id=n.id}}Object.assign(states[id],{localHeat:92,security:5,gangPressure:2,unrest:2,controller:'local'});return{id,x:tr.x,y:tr.y}}
      const a=press(l.from),b=press(l.to),post=controlPostForLinkV12104(linkId,'old_market'),node=w.transit.find(t=>t.id===l.from.node);
      return{linkId,from:l.from.district,to:l.to.district,sourceNode:l.from.node,a,b,post,node,dispatch:activeInterdistrictDispatchV12104?.()||null,player:{x:Game.ovPlayer.x,y:Game.ovPlayer.y}};
    }''')
    assert setup['dispatch'] is None,setup
    assert setup['post'] and setup['post']['x']==setup['node']['x'] and setup['post']['y']==setup['node']['y'],setup
    assert setup['post']['ecology']['blocked'],setup

    bypass=page.evaluate('''q=>{const before=currentDistrictV133().id,player={x:Game.ovPlayer.x,y:Game.ovPlayer.y},ok=travelDistrictV133(q.linkId,'clear');return{ok,before,after:currentDistrictV133().id,player,now:{x:Game.ovPlayer.x,y:Game.ovPlayer.y}}}''',setup)
    assert not bypass['ok'] and bypass['before']==bypass['after'] and bypass['player']==bypass['now'],bypass

    routed=page.evaluate('''q=>{const before={x:Game.ovPlayer.x,y:Game.ovPlayer.y},ok=routeControlPostV12104(q.linkId),st=Game.livingStreetsV134.controlPosts;return{ok,before,after:{x:Game.ovPlayer.x,y:Game.ovPlayer.y},path:Game.pendingPath?.length||0,target:Game._v133TravelTarget,approach:st.approach}}''',setup)
    assert routed['ok'] and routed['path']>1 and routed['target']['kind']=='v12104controlpost' and routed['approach']['linkId']==setup['linkId'],routed
    assert routed['before']==routed['after'],routed

    assert page.evaluate('()=>saveGame(9,true)') is True
    restored=page.evaluate('''()=>{Game.pendingPath=null;Game._v133TravelTarget=null;Game.livingStreetsV134.controlPosts.approach=null;const ok=loadGame(9);showScreen('overworld-screen');initOverworldV133();return{ok,approach:Game.livingStreetsV134?.controlPosts?.approach}}''')
    assert restored['ok'] and restored['approach']['linkId']==setup['linkId'],restored
    page.wait_for_function("()=>Game.pendingPath?.length>1&&Game._v133TravelTarget?.kind==='v12104controlpost'",timeout=5000)
    resumed=page.evaluate('''()=>({path:Game.pendingPath.length,target:Game._v133TravelTarget,player:{x:Game.ovPlayer.x,y:Game.ovPlayer.y}})''')
    assert resumed['path']>1 and resumed['target']['linkId']==setup['linkId'],resumed

    page.wait_for_function("()=>{const p=document.getElementById('v12104-control-post-panel');return p&&!p.hidden&&Game.livingStreetsV134?.controlPosts?.engaged?.linkId==='old_civic_gate'}",timeout=30000)
    engaged=page.evaluate('''q=>{const p=document.getElementById('v12104-control-post-panel'),r=p.getBoundingClientRect(),post=controlPostForLinkV12104(q.linkId,'old_market'),buttons=[...p.querySelectorAll('button')].map(b=>({text:b.textContent.trim(),h:b.getBoundingClientRect().height}));return{dist:post?Math.hypot(Game.ovPlayer.x-post.x,Game.ovPlayer.y-post.y):null,width:r.width,left:r.left,right:r.right,scroll:document.documentElement.scrollWidth,inner:innerWidth,buttons,text:p.textContent,engaged:Game.livingStreetsV134.controlPosts.engaged,path:Game.pendingPath?.length||0}}''',setup)
    assert engaged['engaged']['linkId']==setup['linkId'] and engaged['dist'] is not None and engaged['dist']<=1.7,engaged
    assert engaged['width']<=380.5 and engaged['left']>=-0.5 and engaged['right']<=390.5 and engaged['scroll']<=390,engaged
    assert engaged['buttons'] and min(x['h'] for x in engaged['buttons'])>=43.5,engaged
    assert any('HACKER' in x['text'] for x in engaged['buttons']),engaged
    page.screenshot(path=str(ROOT/'qa/pwa12-104-city-control-posts-mobile.png'),full_page=True)

    hacked=page.evaluate('''q=>{const p=controlPostForLinkV12104(q.linkId,'old_market'),h=ensureNeighborhoodStateV134(currentDistrictV133())[p.neighborhood],before={min:Math.round((((Game.day||1)-1)*24+(Game.hour||0))*60),heat:h.localHeat,fheat:Number(Game.heat?.[p.faction]||0)},ok=spoofControlPostV12104(q.linkId,'hacker'),c=Game.livingStreetsV134.controlPosts.clearances[q.linkId],after={min:Math.round((((Game.day||1)-1)*24+(Game.hour||0))*60),heat:h.localHeat,fheat:Number(Game.heat?.[p.faction]||0)},post=controlPostForLinkV12104(q.linkId,'old_market');return{ok,before,after,c,post}}''',setup)
    assert hacked['ok'] and hacked['c'] and not hacked['c']['consumed'] and hacked['c']['method']=='hacker' and hacked['post'] is None,hacked
    assert hacked['after']['min']-hacked['before']['min']==3 and hacked['after']['heat']>=hacked['before']['heat'],hacked
    assert page.evaluate('()=>saveGame(10,true)') is True
    persisted=page.evaluate('''q=>{Game.livingStreetsV134.controlPosts.clearances={};const ok=loadGame(10),c=Game.livingStreetsV134?.controlPosts?.clearances?.[q.linkId];return{ok,c}}''',setup)
    assert persisted['ok'] and persisted['c'] and not persisted['c']['consumed'],persisted

    crossed=page.evaluate('''q=>{const before=currentDistrictV133().id,credits=Game.credits,ok=travelDistrictV133(q.linkId,'clear'),st=Game.livingStreetsV134.controlPosts,c=st.clearances[q.linkId];return{ok,before,after:currentDistrictV133().id,creditsBefore:credits,creditsAfter:Game.credits,c,history:st.history[0],stats:st.stats}}''',setup)
    assert crossed['ok'] and crossed['before']=='old_market' and crossed['after']=='civic_circuit',crossed
    assert crossed['c']['consumed'] and crossed['stats']['crossings']>=1 and crossed['history']['type']=='crossing',crossed

    fight_setup=page.evaluate('''q=>{activateDistrictV133('old_market');showScreen('overworld-screen');initOverworldV133();const w=currentDistrictV133(),st=ensureLivingStreetsStateV134();st.lastEventStep=st.stepCount+999999;const c=st.controlPosts.clearances[q.linkId];if(c)c.consumed=true;delete st.controlPosts.suppressed['old_market:'+q.linkId];const p=controlPostForLinkV12104(q.linkId,'old_market');if(!p)throw new Error('control post did not reform after consumed clearance');Game.ovPlayer={x:p.x,y:p.y};Game.districtWorldsV133.positions.old_market={x:p.x,y:p.y};const opened=openControlPostV12104(q.linkId),ok=fightControlPostV12104(q.linkId);return{opened,ok,active:Game.activeMission?{street:!!Game.activeMission.v134StreetEncounter,actor:Game.activeMission.v134StreetActorType}:null,combat:st.controlPosts.activeCombat}}''',setup)
    assert fight_setup['opened'] and fight_setup['ok'] and fight_setup['active']['street'] and fight_setup['combat'],fight_setup
    page.wait_for_function('()=>!!Game.activeMission?.v134StreetEncounter',timeout=5000)
    fight_done=page.evaluate('''q=>{const m=Game.activeMission,ok=settleStreetCombatV134(m,true),st=Game.livingStreetsV134.controlPosts,sup=st.suppressed['old_market:'+q.linkId],c=st.clearances[q.linkId];showScreen('overworld-screen');initOverworldV133();const post=controlPostForLinkV12104(q.linkId,'old_market');return{ok,actor:m.v134StreetActorType,sup,c,post,last:st.history[0]}}''',setup)
    assert fight_done['ok'] and fight_done['actor'] in ('security','gang','contractor'),fight_done
    assert fight_done['sup'] and fight_done['sup']['until']>fight_done['sup']['at'] and fight_done['c']['method']=='fight' and fight_done['post'] is None,fight_done
    assert not errors,errors
    print('PASS Candidate 07 browser: job-independent physical control post, canonical path approach, save/load route reconstruction, 390x844 UI, Hacker clearance, canonical crossing, one-crossing consumption and street-combat suppression')
    ctx.close();browser.close()