"""Regression: large open and shaped arena deployments must map every enemy to a unique legal cell."""
from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text(encoding='utf-8').replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
SHIM="""<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"""
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    ctx=browser.new_context(viewport={'width':412,'height':839},device_scale_factor=1,is_mobile=True,has_touch=True)
    errors=[]
    def route(r):
        relative=r.request.url.split('http://cr.local/',1)[-1].split('?',1)[0] or 'index.html'
        file=ROOT/relative
        r.fulfill(status=200,body=file.read_bytes(),content_type=mimetypes.guess_type(file.name)[0] or 'application/octet-stream') if file.is_file() else r.fulfill(status=404,body=b'not found')
    ctx.route('http://cr.local/**',route)
    page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content(HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1),wait_until='domcontentloaded')
    page.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
    for amount,shape in [(9,'open'),(12,'open'),(9,'rooms')]:
        result=page.evaluate('''({amount,shape})=>{
            startNewGame('Hunter Spawn QA','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');
            const mission={id:'aaA_hunter_qa',name:'Hunter Deployment',desc:'QA',type:'bounty',objective:'bounty',diff:3,tacticalShape:shape,enemies:Array(amount-1).fill('Guard').concat('Boss')};
            buildGrid(mission);createCombatUnits(mission);
            const enemies=Game.units.filter(u=>u.team==='enemy');
            const occupied=enemies.map(u=>Game.grid.find(c=>c.x===u.x&&c.y===u.y));
            const unique=new Set(enemies.map(u=>`${u.x}:${u.y}`));
            const valid=occupied.every((c,i)=>c && !c.obstacle && !c.arenaVoid && !c.door && c.unit===enemies[i]);
            const targets=enemies.filter(u=>u.isObjectiveTarget);
            return {amount,shape,enemyCount:enemies.length,uniqueCount:unique.size,occupiedCells:Game.grid.filter(c=>c.unit?.team==='enemy').length,valid,targetCount:targets.length,targetCell:targets.map(u=>({name:u.name,x:u.x,y:u.y}))};
        }''',{'amount':amount,'shape':shape})
        assert result['enemyCount']==amount,result
        assert result['uniqueCount']==amount and result['occupiedCells']==amount and result['valid'],result
        assert result['targetCount']==1 and result['targetCell'],result
        print(f'PASS {shape} {amount} enemy deployment: unique legal targetable cells and exactly one bounty target')
    # Also capture the actual player-facing tactical screen, not just state checks.
    screenshot_state=page.evaluate('''()=>{
        startNewGame('Hunter Spawn QA','Hacker','street');
        document.getElementById('story-modal')?.classList.remove('open');
        const mission={id:'aaA_hunter_screen',name:'HUNTER RESPONSE',desc:'Nine hostile actors',
            type:'bounty',objective:'bounty',diff:3,tacticalShape:'open',
            enemies:Array(8).fill('Guard').concat('Boss'),reward:900,xp:70};
        Game.activeMission=mission;showScreen('combat');initCombat(mission);
        document.getElementById('banner')?.classList.remove('show');
        return {enemies:Game.units.filter(u=>u.team==='enemy').length,
            unique:new Set(Game.units.filter(u=>u.team==='enemy').map(u=>`${u.x}:${u.y}`)).size,
            board:document.getElementById('board').getBoundingClientRect().width,
            scroll:document.documentElement.scrollWidth,width:innerWidth};
    }''')
    assert screenshot_state['enemies']==9 and screenshot_state['unique']==9,screenshot_state
    assert screenshot_state['board']>=220 and screenshot_state['scroll']<=screenshot_state['width']+1,screenshot_state
    page.wait_for_timeout(1750)
    (ROOT/'qa').mkdir(exist_ok=True)
    page.screenshot(path=str(ROOT/'qa/pwa12-74-hunter-deployment-mobile.png'),full_page=True)
    print('PASS mobile tactical screenshot: nine separately deployed enemies, no horizontal overflow')
    assert not errors,errors
    browser.close()
