"""Chromium integration: complete a three-area operation through real objective actions."""
from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa'
HTML=(ROOT/'index.html').read_text(encoding='utf-8')
SHIM="""<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"""
HTML=HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1).replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    page=browser.new_page(viewport={'width':1280,'height':900},device_scale_factor=1)
    errors=[];missing=[]
    def route(r):
        url=r.request.url
        if not url.startswith('http://cr.local/'):return r.abort()
        rel=url.split('http://cr.local/',1)[1].split('?',1)[0] or 'index.html'; fp=ROOT/rel
        if fp.is_file():r.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream')
        else:missing.append(rel);r.fulfill(status=404,body=b'not found',content_type='text/plain')
    page.route('http://cr.local/**',route)
    page.on('pageerror',lambda e:errors.append(e.stack or str(e)))
    page.set_content(HTML,wait_until='domcontentloaded')
    page.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
    page.evaluate("()=>{startNewGame('Vex','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');showScreen('combat');const m={id:'multi_heist',type:'heist',objective:'heist',_v12ObjectiveAssigned:true,name:'Three-floor extraction',desc:'Recover the encrypted vault archive.',contact:null,diff:2,enemies:['Guard','Enforcer','Drone'],reward:600,xp:70,targetFaction:'meridian',factionRepGain:0,factionRepLoss:{}};Game.activeMission=m;initCombat(m)}")
    first=page.evaluate("()=>({stage:CR14MultiStageOperations.active,shape:Game.arenaShapeV14,objective:Game.objective.type,credits:Game.credits,history:Game.missionHistory.length,clock:[Game.day,Game.hour],save:JSON.stringify(serializeGame()),door:cellAt(4,2).door})")
    assert first['stage']['index']==0 and first['shape']=='corridor' and first['objective']=='breach' and first['door'],first
    page.evaluate("()=>{const u=Game.units.find(x=>x.team==='player');u.hp-=7;u.statuses.marked=2;u.inventory.testPayload=3;Game.selectedUnit=u;Game.turn='player';u.ap=3;cellAt(u.x,u.y).unit=null;u.x=4;u.y=3;cellAt(4,3).unit=u;onCombatCellClick(4,2)}")
    assert page.evaluate("()=>cellAt(4,2).doorOpen && Game.selectedUnit.ap===2"),'Breaching must use the real tactical door action'
    page.screenshot(path=str(OUT/'pwa12-44-01-perimeter-desktop.png'))
    # Use real action-deck callbacks, moving an operator to each node without simulating time.
    for idx in (0,1):
        page.evaluate("""i=>{const u=Game.units.find(x=>x.team==='player');const t=Game.objective.cells[i];const c=cellAt(u.x,u.y);if(c)c.unit=null;u.x=t.x;u.y=t.y;cellAt(u.x,u.y).unit=u;Game.selectedUnit=u;Game.turn='player';u.ap=3;updateCombat()}""",idx)
        page.locator('#actions button').filter(has_text='BREACH SECURITY').first.click(timeout=10000)
    page.wait_for_function('()=>CR14MultiStageOperations.active?.index===1',timeout=12000)
    second=page.evaluate("()=>({stage:CR14MultiStageOperations.active,shape:Game.arenaShapeV14,type:Game.objective.type,exfil:Game.objective.exfil,credits:Game.credits,history:Game.missionHistory.length,clock:[Game.day,Game.hour],hp:Game.units.find(x=>x.team==='player').hp,marked:Game.units.find(x=>x.team==='player').statuses.marked,inventory:Game.units.find(x=>x.team==='player').inventory.testPayload,opId:Game.activeMission.id})")
    assert second['shape']=='rooms' and second['type']=='heist' and second['exfil'] is None and second['hp']==first['credits']*0+page.evaluate("()=>Game.roster[0].hp")-7, second
    assert second['marked']==2 and second['inventory']==3 and second['credits']==first['credits'] and second['history']==first['history'] and second['clock']==first['clock'] and second['opId']=='multi_heist',second
    page.screenshot(path=str(OUT/'pwa12-44-02-interior-desktop.png'))
    for idx in (0,1,2):
        page.evaluate("""i=>{const u=Game.units.find(x=>x.team==='player');const t=Game.objective.cells[i];const c=cellAt(u.x,u.y);if(c)c.unit=null;u.x=t.x;u.y=t.y;cellAt(u.x,u.y).unit=u;Game.selectedUnit=u;Game.turn='player';u.ap=3;updateCombat()}""",idx)
        page.locator('#actions button').filter(has_text='BREACH NODE').first.click(timeout=10000)
    page.wait_for_function('()=>CR14MultiStageOperations.active?.index===2',timeout=12000)
    last=page.evaluate("()=>({stage:CR14MultiStageOperations.active,shape:Game.arenaShapeV14,type:Game.objective.type,exfil:Game.objective.exfil,ready:Game.objective.exfilReady,credits:Game.credits,history:Game.missionHistory.length,hp:Game.units.find(x=>x.team==='player').hp,clock:[Game.day,Game.hour],marker:!!cellAt(4,0).el.dataset.exfil})")
    assert last['shape']=='entrance' and last['type']=='extract' and last['exfil']=={'x':4,'y':0} and last['marker'] and not last['ready'],last
    assert last['hp']==second['hp'] and last['credits']==first['credits'] and last['history']==first['history'] and last['clock']==first['clock'],last
    page.screenshot(path=str(OUT/'pwa12-44-03-extraction-desktop.png'))
    # Eliminate the enemies: doing so must not bypass the exit requirement.
    page.evaluate("()=>{for(const u of Game.units.filter(u=>u.team==='enemy')){u.hp=0;u.dead=true;const c=cellAt(u.x,u.y);if(c&&c.unit===u)c.unit=null}checkWinLose()}")
    assert page.evaluate('()=>!Game.gameOver && CR14MultiStageOperations.active?.index===2 && !Game.objective.exfilReady')
    page.evaluate("()=>{const u=Game.units.find(x=>x.team==='player');const c=cellAt(u.x,u.y);if(c)c.unit=null;u.x=4;u.y=1;cellAt(u.x,u.y).unit=u;Game.selectedUnit=u;Game.turn='player';u.ap=2;updateCombat()}")
    page.locator('#actions .v14-exfil-action:not([disabled])').click(timeout=10000)
    page.wait_for_function('()=>Game.gameOver===true',timeout=8000)
    done=page.evaluate("()=>({active:CR14MultiStageOperations.active,credits:Game.credits,history:Game.missionHistory.filter(m=>m.id==='multi_heist').length,completed:Game.objective?.exfilReady,save:JSON.stringify(serializeGame())})")
    assert done['active'] is None and done['credits']==first['credits']+600 and done['history']==1 and done['completed'],done
    assert 'operationStageV14' not in done['save'] and 'arenaShapeV14' not in done['save']
    # A regular elimination must remain a single open battle.
    page.evaluate("()=>{const m={id:'single_elim',type:'eliminate',objective:'eliminate',name:'One fight',desc:'Open ground',tacticalShape:'open',_v12ObjectiveAssigned:true,contact:null,diff:1,enemies:['Guard'],reward:100,xp:20,targetFaction:'iron',factionRepGain:0,factionRepLoss:{}};Game.activeMission=m;initCombat(m)}")
    single=page.evaluate('()=>({active:CR14MultiStageOperations.active,shape:Game.arenaShapeV14,board:document.getElementById("board").dataset.arenaShape,gameOver:Game.gameOver,mission:Game.activeMission?.id,chosen:CR14VariableArenas.choose(Game.activeMission),type:Game.activeMission?.type,objective:Game.activeMission?.objective,tacticalShape:Game.activeMission?.tacticalShape,stageStrip:document.getElementById("operation-stage-strip")?.textContent})')
    assert single['active'] is None and single['shape'] is None,single
    page.set_viewport_size({'width':390,'height':844})
    page.evaluate("()=>{const m={id:'mobile_multi',type:'extract',objective:'extract',name:'Mobile operation',desc:'Mobile',contact:null,diff:2,enemies:['Guard','Drone'],reward:100,xp:20,targetFaction:'iron',factionRepGain:0,factionRepLoss:{}};Game.activeMission=m;initCombat(m)}")
    mobile=page.evaluate("()=>({stage:CR14MultiStageOperations.active?.index,shape:Game.arenaShapeV14,overflow:document.documentElement.scrollWidth-innerWidth,strip:document.getElementById('operation-stage-strip')?.textContent,boardHeight:document.getElementById('board').getBoundingClientRect().height})")
    page.screenshot(path=str(OUT/'pwa12-44-mobile-operation.png'))
    assert mobile['stage']==0 and mobile['shape']=='corridor' and mobile['overflow']<=1 and mobile['boardHeight']>=220,mobile
    # The v12 emergency extraction wrapper must not recurse; starting a new
    # operation after abort must clear all transient stages.
    assert page.evaluate('()=>abortMissionV8()===true && Game.activeMission===null')
    page.evaluate("()=>{const m={id:'after_abort',type:'eliminate',objective:'eliminate',tacticalShape:'open',_v12ObjectiveAssigned:true,name:'After abort',desc:'Fresh operation',contact:null,diff:1,enemies:['Guard'],reward:100,xp:20,targetFaction:'iron',factionRepGain:0,factionRepLoss:{}};Game.activeMission=m;initCombat(m)}")
    assert page.evaluate('()=>CR14MultiStageOperations.active===null && Game.arenaShapeV14===null && !document.getElementById("operation-stage-strip")')
    assert not errors and not missing,(errors,missing)
    print('PASS PWA12.44 actual three-stage operation, real breach/objectives/exfil, HP/status/inventory carry, one reward, no world time on transition, single-stage fallback, mobile; screenshots captured')
    print('STAGES',first['stage'],second['stage'],last['stage'],'DONE',done,'MOBILE',mobile)
    browser.close()
