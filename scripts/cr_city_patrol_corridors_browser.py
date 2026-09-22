"""Chromium integration QA for PWA12.104 Patrol Corridors + Risk-Aware Route Choice Candidate 08."""
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
      startNewGame('Patrol QA','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');Game.notoriety=0;Game.rep=Game.rep||{};Game.heat=Game.heat||{};
      activateDistrictV133('old_market');showScreen('overworld-screen');initOverworldV133();
      const w=currentDistrictV133(),ls=ensureLivingStreetsStateV134();ls.lastEventStep=ls.stepCount+999999;
      const ns=ensureNeighborhoodStateV134(w);for(const n of w.neighborhoods)Object.assign(ns[n.id],{localHeat:0,security:1,gangPressure:1,unrest:0,controller:'local'});
      const locs=Object.entries(w.locations).map(([id,p])=>({id,p}));
      const key=p=>(p||[]).map(q=>q.x+','+q.y).join('|');let best=null;
      const nearest=q=>{let z=null,d=1e9;for(const n of w.neighborhoods){const x=Math.hypot(q.x-n.x,q.y-n.y);if(x<d){d=x;z=n}}return z};
      outer:for(const a of locs)for(const g of locs){if(a.id===g.id||Math.hypot(a.p.x-g.p.x,a.p.y-g.p.y)<24)continue;const direct=findDistrictPathV133(a.p,g.p,w);if(!direct||direct.length<15)continue;for(const frac of [.35,.5,.65]){for(const n of w.neighborhoods)Object.assign(ns[n.id],{localHeat:0,security:1,gangPressure:1,unrest:0,controller:'local'});const q=direct[Math.min(direct.length-1,Math.max(1,Math.floor(direct.length*frac)))],hot=nearest(q);if(!hot)continue;Object.assign(ns[hot.id],{localHeat:100,security:5,gangPressure:2,unrest:2,controller:'local'});Game.ovPlayer={x:a.p.x,y:a.p.y};Game.districtWorldsV133.positions[w.id]={x:a.p.x,y:a.p.y};const target={kind:'location',id:g.id,label:g.id},plan=previewPatrolRoutesV12104(g.p,target,w,Game.ovPlayer);if(!plan)continue;for(const mode of ['low','back']){const o=plan.options[mode],f=plan.options.fast;if(o?.path?.length>4&&key(o.path)!==key(f.path)&&o.metrics.exposure<=f.metrics.exposure+.001){best={startId:a.id,goalId:g.id,start:{x:a.p.x,y:a.p.y},goal:{x:g.p.x,y:g.p.y},hot:hot.id,mode,fast:{steps:f.metrics.steps,exposure:f.metrics.exposure},chosen:{steps:o.metrics.steps,exposure:o.metrics.exposure},target};break outer}}}}
      if(!best)throw new Error('no materially distinct risk-aware route found');
      Game.ovPlayer={...best.start};Game.districtWorldsV133.positions[w.id]={...best.start};const st=Game.livingStreetsV134.patrolCorridors;st.preference='fast';st.familiarity={};st.history=[];st.stats={planned:0,switched:0,steps:0};
      const opened=openPatrolRoutePlannerV12104({point:best.goal,target:best.target});return{...best,opened,world:w.id,player:{...Game.ovPlayer},sources:CR_CITY_PATROL_CORRIDORS.patrolSources(w).length};
    }''')
    assert setup['opened'] and setup['world']=='old_market',setup
    assert setup['chosen']['exposure']<=setup['fast']['exposure']+0.001,setup
    assert setup['chosen']['steps']>0 and setup['fast']['steps']>0,setup

    ui=page.evaluate('''()=>{const p=document.getElementById('v12104-patrol-route-panel'),r=p.getBoundingClientRect(),buttons=[...p.querySelectorAll('.pr-choice')].map(b=>({text:b.textContent.trim(),h:b.getBoundingClientRect().height,mode:b.dataset.mode}));return{hidden:p.hidden,width:r.width,left:r.left,right:r.right,scroll:document.documentElement.scrollWidth,inner:innerWidth,buttons,text:p.textContent}}''')
    assert not ui['hidden'] and ui['width']<=380.5 and ui['left']>=-0.5 and ui['right']<=390.5 and ui['scroll']<=390,ui
    assert {x['mode'] for x in ui['buttons']}=={'fast','low','back'} and min(x['h'] for x in ui['buttons'])>=57.5,ui
    assert 'FAST' in ui['text'] and 'LOW PROFILE' in ui['text'] and 'BACK ALLEY' in ui['text'] and 'INTEL THIN' in ui['text'],ui
    page.screenshot(path=str(ROOT/'qa/pwa12-104-city-patrol-corridors-mobile.png'),full_page=True)

    commit=page.evaluate('''q=>{const before={x:Game.ovPlayer.x,y:Game.ovPlayer.y};const b=[...document.querySelectorAll('#v12104-patrol-route-panel .pr-choice')].find(x=>x.dataset.mode===q.mode);b.click();const plan=currentPatrolRoutePlanV12104();return{before,after:{x:Game.ovPlayer.x,y:Game.ovPlayer.y},goal:q.goal,path:Game.pendingPath?.length||0,target:Game._v133TravelTarget,plan,preference:Game.livingStreetsV134.patrolCorridors.preference,stats:{...Game.livingStreetsV134.patrolCorridors.stats}}}''',setup)
    assert commit['path']>1,commit
    # Canonical route commitment wakes the overworld scheduler immediately. It may legally consume
    # one physical street step before this evaluate() returns; what must never happen is a jump to goal.
    commit_tick=((commit['after']['x']-commit['before']['x'])**2+(commit['after']['y']-commit['before']['y'])**2)**0.5
    commit_goal=((commit['after']['x']-commit['goal']['x'])**2+(commit['after']['y']-commit['goal']['y'])**2)**0.5
    assert commit_tick<=1.5 and commit_goal>1.7,commit
    assert commit['plan']['mode']==setup['mode'] and commit['preference']==setup['mode'],commit
    assert commit['target']['kind']=='location' and commit['target']['id']==setup['goalId'],commit

    page.wait_for_function('q=>Game.ovPlayer&&(Game.ovPlayer.x!==q.x||Game.ovPlayer.y!==q.y)',arg=setup['start'],timeout=12000)
    moved=page.evaluate('''()=>({player:{x:Game.ovPlayer.x,y:Game.ovPlayer.y},path:Game.pendingPath?.length||0,pc:Game.livingStreetsV134.patrolCorridors,step:Game.livingStreetsV134.stepCount})''')
    assert moved['player']!=setup['start'] and moved['pc']['stats']['steps']>0,moved
    fam_total=sum(sum(v.values()) for v in moved['pc']['familiarity'].values())
    assert fam_total>0,moved

    assert page.evaluate('()=>saveGame(12,true)') is True
    restored=page.evaluate('''q=>{const pc=Game.livingStreetsV134.patrolCorridors;pc.preference='fast';pc.familiarity={};Game.pendingPath=null;Game._v133TravelTarget=null;const ok=loadGame(12);showScreen('overworld-screen');initOverworldV133();const r=Game.livingStreetsV134.patrolCorridors;return{ok,preference:r.preference,familiarity:r.familiarity,player:{x:Game.ovPlayer.x,y:Game.ovPlayer.y}}}''',setup)
    assert restored['ok'] and restored['preference']==setup['mode'],restored
    assert sum(sum(v.values()) for v in restored['familiarity'].values())>0,restored

    resumed=page.evaluate('''q=>{Game.livingStreetsV134.lastEventStep=Game.livingStreetsV134.stepCount+999999;const before={x:Game.ovPlayer.x,y:Game.ovPlayer.y},goal=currentDistrictV133().locations[q.startId],ok=routeToLocationV133(q.startId),plan=currentPatrolRoutePlanV12104();return{ok,before,after:{x:Game.ovPlayer.x,y:Game.ovPlayer.y},goal:{x:goal.x,y:goal.y},path:Game.pendingPath?.length||0,plan,preference:Game.livingStreetsV134.patrolCorridors.preference}}''',setup)
    assert resumed['ok'] and resumed['path']>1,resumed
    resumed_tick=((resumed['after']['x']-resumed['before']['x'])**2+(resumed['after']['y']-resumed['before']['y'])**2)**0.5
    resumed_goal=((resumed['after']['x']-resumed['goal']['x'])**2+(resumed['after']['y']-resumed['goal']['y'])**2)**0.5
    assert resumed_tick<=1.5 and resumed_goal>1.7,resumed
    assert resumed['plan'] and resumed['plan']['mode']==setup['mode'] and resumed['preference']==setup['mode'],resumed

    switched=page.evaluate('''()=>{const before={x:Game.ovPlayer.x,y:Game.ovPlayer.y},ok=switchPatrolRouteProfileV12104('fast'),plan=currentPatrolRoutePlanV12104();return{ok,before,after:{x:Game.ovPlayer.x,y:Game.ovPlayer.y},path:Game.pendingPath?.length||0,plan,stats:{...Game.livingStreetsV134.patrolCorridors.stats}}}''')
    switched_tick=((switched['after']['x']-switched['before']['x'])**2+(switched['after']['y']-switched['before']['y'])**2)**0.5
    assert switched['ok'] and switched_tick<=1.5 and switched['path']>1,switched
    assert switched['plan']['mode']=='fast' and switched['stats']['switched']>=1,switched
    assert not errors,errors
    print('PASS Candidate 08 browser: 390x844 route planner, distinct risk-aware physical routes, no teleport, canonical scheduler movement, learned route familiarity, save/load preference persistence, programmatic routing and in-motion profile switching')
    ctx.close();browser.close()
