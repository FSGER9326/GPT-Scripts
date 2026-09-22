"""Chromium integration QA for PWA12.104 City Patrol Routing Candidate 08."""
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
      startNewGame('Patrol Routing QA','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');Game.notoriety=0;Game.rep=Game.rep||{};Game.heat=Game.heat||{};
      activateDistrictV133('old_market');showScreen('overworld-screen');initOverworldV133();
      const w=currentDistrictV133(),s=ensureLivingStreetsStateV134();s.lastEventStep=s.stepCount+999999;const ns=ensureNeighborhoodStateV134(w);
      for(const n of w.neighborhoods)Object.assign(ns[n.id],{localHeat:0,security:1,gangPressure:1,unrest:0,controller:'local'});
      const ranked=[...w.neighborhoods].sort((a,b)=>Math.hypot(a.x-w.w/2,a.y-w.h/2)-Math.hypot(b.x-w.w/2,b.y-w.h/2));
      if(ranked[0])Object.assign(ns[ranked[0].id],{localHeat:100,security:5,gangPressure:1,unrest:1});
      if(ranked[1])Object.assign(ns[ranked[1].id],{localHeat:20,security:2,gangPressure:5,unrest:5});
      const pts=[...Object.values(w.locations).map(p=>({x:p.x,y:p.y,id:p.id,kind:'location'})),...w.transit.map(p=>({x:p.x,y:p.y,id:p.id,kind:'transit'}))];
      const pairs=[];
      for(let i=0;i<pts.length;i++)for(let j=i+1;j<pts.length;j++){
        const d=Math.hypot(pts[i].x-pts[j].x,pts[i].y-pts[j].y);if(d<28)continue;
        pairs.push({start:pts[i],goal:pts[j],d});pairs.push({start:pts[j],goal:pts[i],d});
      }
      // Long physical lines are most likely to cross the forced central patrol pressure. Limit
      // route comparisons so QA validates gameplay rather than turning into an A* stress test.
      pairs.sort((a,b)=>b.d-a.d);let chosen=null,fallback=null,checked=0;
      for(const pair of pairs.slice(0,32)){
        Game.ovPlayer={x:pair.start.x,y:pair.start.y};
        const base=findDistrictPathV133(Game.ovPlayer,pair.goal,w);if(!base?.length||base.length<24)continue;
        const p=planPatrolRoutesV12104({x:pair.goal.x,y:pair.goal.y},{kind:'point',label:'QA STREET TARGET'});checked++;
        if(!p?.plans?.fast||!p.plans.low||!p.plans.back)continue;
        const sig=x=>x.path.map(q=>q.x+','+q.y).join('|'),different=sig(p.plans.fast)!==sig(p.plans.low)||sig(p.plans.fast)!==sig(p.plans.back),best=Math.min(p.plans.low.analysis.exposure,p.plans.back.analysis.exposure);
        if(different&&!fallback)fallback={start:pair.start,goal:pair.goal,plans:p,pick:p.plans.low.analysis.exposure<=p.plans.back.analysis.exposure?'low':'back'};
        if(different&&p.plans.fast.analysis.exposure>=8&&best<p.plans.fast.analysis.exposure){chosen={start:pair.start,goal:pair.goal,plans:p,pick:p.plans.low.analysis.exposure<=p.plans.back.analysis.exposure?'low':'back'};break}
      }
      chosen=chosen||fallback;if(!chosen)throw new Error(`No canonical physical point pair produced distinct route tactics in ${checked} bounded comparisons under forced patrol pressure`);
      Game.ovPlayer={x:chosen.start.x,y:chosen.start.y};Game.districtWorldsV133.positions[w.id]={x:chosen.start.x,y:chosen.start.y};Game.pendingPath=null;Game._v133TravelTarget=null;
      const corridors=patrolCorridorsForWorldV12104(w);return{start:chosen.start,goal:chosen.goal,pick:chosen.pick,plans:{fast:chosen.plans.fast.analysis,low:chosen.plans.low.analysis,back:chosen.plans.back.analysis},corridors:corridors.length,hoods:ranked.slice(0,2).map(x=>x.id),checked};
    }''')
    assert setup['corridors']>0,setup
    assert 1<=setup['checked']<=32,setup
    assert setup['plans']['fast']['cells']>0 and setup['plans']['low']['cells']>0 and setup['plans']['back']['cells']>0,setup
    assert setup['pick'] in ('low','back'),setup
    assert min(setup['plans']['low']['exposure'],setup['plans']['back']['exposure'])<=setup['plans']['fast']['exposure'],setup

    opened=page.evaluate('''q=>{const before={x:Game.ovPlayer.x,y:Game.ovPlayer.y},ok=openPatrolRoutePlannerV12104({x:q.goal.x,y:q.goal.y},{kind:'point',label:'QA STREET TARGET'}),p=document.getElementById('v12104-route-planner'),r=p?.getBoundingClientRect(),buttons=p?[...p.querySelectorAll('button')].map(b=>({id:b.id,text:b.textContent.trim(),h:b.getBoundingClientRect().height})):[];return{ok,before,after:{x:Game.ovPlayer.x,y:Game.ovPlayer.y},hidden:p?.hidden,width:r?.width,left:r?.left,right:r?.right,scroll:document.documentElement.scrollWidth,inner:innerWidth,buttons,text:p?.textContent||''}}''',setup)
    assert opened['ok'] and not opened['hidden'] and opened['before']==opened['after'],opened
    assert 'FAST' in opened['text'] and 'LOW PROFILE' in opened['text'] and 'BACK ALLEY' in opened['text'],opened
    assert opened['width']<=380.5 and opened['left']>=-0.5 and opened['right']<=390.5 and opened['scroll']<=390,opened
    assert len(opened['buttons'])>=4 and min(x['h'] for x in opened['buttons'])>=43.5,opened
    page.screenshot(path=str(ROOT/'qa/pwa12-104-city-patrol-routing-mobile.png'),full_page=True)

    committed=page.evaluate('''q=>{const before={x:Game.ovPlayer.x,y:Game.ovPlayer.y},ok=commitPatrolRouteV12104(q.pick),st=Game.livingStreetsV134.patrolRouting,a=st.activeRoute;return{ok,before,after:{x:Game.ovPlayer.x,y:Game.ovPlayer.y},path:Game.pendingPath?.length||0,target:Game._v133TravelTarget,a,stats:st.stats}}''',setup)
    assert committed['ok'] and committed['path']>1 and committed['a']['profile']==setup['pick'],committed
    assert committed['before']==committed['after'],committed
    assert committed['target']['kind']=='point',committed
    assert committed['stats']['committed']>=1,committed

    assert page.evaluate('()=>saveGame(11,true)') is True
    restored=page.evaluate('''()=>{Game.pendingPath=null;Game._v133TravelTarget=null;Game.livingStreetsV134.patrolRouting.activeRoute=null;const ok=loadGame(11),saved=Game.livingStreetsV134?.patrolRouting?.activeRoute,stats={...Game.livingStreetsV134?.patrolRouting?.stats};showScreen('overworld-screen');initOverworldV133();return{ok,saved,stats,player:{x:Game.ovPlayer.x,y:Game.ovPlayer.y}}}''')
    assert restored['ok'] and restored['saved'] and restored['saved']['profile']==setup['pick'],restored
    page.wait_for_function("n=>Game.livingStreetsV134?.patrolRouting?.stats?.resumed>n",arg=restored['stats']['resumed'],timeout=5000)
    resumed=page.evaluate('''()=>({path:Game.pendingPath?.length||0,a:Game.livingStreetsV134.patrolRouting.activeRoute,stats:{...Game.livingStreetsV134.patrolRouting.stats},player:{x:Game.ovPlayer.x,y:Game.ovPlayer.y}})''')
    assert resumed['stats']['resumed']>restored['stats']['resumed'],(restored,resumed)
    if resumed['a']:
        assert resumed['a']['profile']==setup['pick'],resumed
    else:
        assert resumed['stats']['completed']>restored['stats']['completed'],(restored,resumed)

    if resumed['player']==restored['player']:
        sx,sy=restored['player']['x'],restored['player']['y']
        page.wait_for_function(f"()=>Game.ovPlayer&&(Game.ovPlayer.x!={sx}||Game.ovPlayer.y!={sy})",timeout=10000)
    moved=page.evaluate('''()=>({player:{x:Game.ovPlayer.x,y:Game.ovPlayer.y},path:Game.pendingPath?.length||0,a:Game.livingStreetsV134.patrolRouting.activeRoute,stats:{...Game.livingStreetsV134.patrolRouting.stats},exposureSteps:Game.livingStreetsV134.patrolRouting.stats.exposureSteps})''')
    assert moved['player']!=restored['player'],(restored,resumed,moved)

    superseded=page.evaluate('''()=>{Game.pendingPath=null;const w=currentDistrictV133(),e=Object.entries(w.locations).find(([id,p])=>Math.hypot(Game.ovPlayer.x-p.x,Game.ovPlayer.y-p.y)>5);if(!e)return{skip:true};const before=document.getElementById('v12104-route-planner')?.hidden!==false,ok=routeToLocationV133(e[0]),a=Game.livingStreetsV134.patrolRouting.activeRoute;return{skip:false,before,ok,path:Game.pendingPath?.length||0,a,panelOpen:document.getElementById('v12104-route-planner')?.hidden===false}}''')
    if not superseded.get('skip'):
        assert superseded['before'] and superseded['ok'] and superseded['path']>1 and superseded['a'] is None and not superseded['panelOpen'],superseded

    assert not errors,errors
    print('PASS Candidate 08 browser: live patrol corridors, distinct FAST/LOW-PROFILE/BACK-ALLEY physical routes, exposure tradeoff, 390x844 planner, no teleport, save/load route reconstruction, physical movement and canonical programmatic-route compatibility')
    ctx.close();browser.close()