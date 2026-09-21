"""Browser regression for status/awareness DOM invalidation and icon parity."""
from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'index.html').read_text(encoding='utf-8')
shim="""<script>const _ls=new Map();const store={getItem:k=>_ls.get(String(k))??null,setItem:(k,v)=>_ls.set(String(k),String(v)),removeItem:k=>_ls.delete(String(k)),clear:()=>_ls.clear(),key:i=>[..._ls.keys()][i]??null,get length(){return _ls.size}};Object.defineProperty(window,'localStorage',{value:store,configurable:true});Object.defineProperty(window,'sessionStorage',{value:store,configurable:true});</script>"""
html=html.replace('<head>','<head><base href="http://cr.local/">'+shim,1).replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
with sync_playwright() as pw:
    b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    p=b.new_page(viewport={'width':1280,'height':800});errors=[];missing=[]
    def handler(route):
        u=route.request.url
        if not u.startswith('http://cr.local/'):return route.abort()
        rel=u[len('http://cr.local/'):].split('?',1)[0] or 'index.html';fp=ROOT/rel
        if fp.is_file():route.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream')
        else:missing.append(rel);route.fulfill(status=404,body=b'not found')
    p.route('http://cr.local/**',handler)
    p.on('pageerror',lambda e:errors.append(str(e)))
    p.set_content(html,wait_until='domcontentloaded')
    p.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=30000)
    result=p.evaluate("""()=>{
        startNewGame('Vex','Hacker','street');
        document.getElementById('story-modal')?.classList.remove('open');
        showScreen('combat');
        const m={id:'status_perf',type:'heist',name:'Status performance',desc:'QA',diff:2,
          enemies:['Guard','Enforcer','Drone'],reward:600,xp:70,targetFaction:'meridian'};
        Game.activeMission=m;initCombat(m);
        const enemy=Game.units.find(u=>u.team==='enemy'&&u.hp>0);
        if(!enemy)throw Error('No enemy unit');
        enemy.statuses={shock:2,burn:2,marked:1,armor_up:2,cloak:1,poison:2,bleed:2};
        enemy.disabledTurns=1;enemy.overwatch=true;enemy.awareness=40;
        syncCombatUnits();
        const statusNode=enemy.el.querySelector('.statuses'),awareness=enemy.el.querySelector('.awareness');
        const icons=()=>[...statusNode.children].map(el=>el.className);
        const expected=['st-shock','st-burn','st-stun','st-marked','st-armor','st-cloak','st-overwatch','st-poison','st-burn'];
        const actual=icons();if(JSON.stringify(actual)!==JSON.stringify(expected))throw Error('Original icon ordering/bleed style changed '+actual);
        const before=[...statusNode.children],fill=awareness.querySelector('i');
        if(fill.style.width!=='40%'||enemy.el.classList.contains('alerted'))throw Error('Initial awareness presentation incorrect');
        const observer=new MutationObserver(()=>{});
        observer.observe(statusNode,{childList:true,subtree:true,attributes:true});
        observer.observe(awareness,{childList:true,subtree:true,attributes:true});
        observer.observe(enemy.el,{attributes:true,attributeFilter:['class']});
        for(let i=0;i<100;i++)syncCombatUnits();
        const stableMutations=observer.takeRecords();
        if(stableMutations.length)throw Error('Stable unit caused '+stableMutations.length+' status/awareness mutations');
        if(before.some((x,i)=>statusNode.children[i]!==x))throw Error('Stable unit icons recreated');
        enemy.awareness=100;enemy.statuses.poison=0;enemy.statuses.bleed=0;
        syncCombatUnits();
        if(statusNode.children.length!==7||fill.style.width!=='100%'||!enemy.el.classList.contains('alerted'))throw Error('Status/awareness transition not reflected');
        observer.takeRecords();
        for(let i=0;i<20;i++)syncCombatUnits();
        if(observer.takeRecords().length)throw Error('Stable post-transition unit still mutating DOM');
        const oldNode=enemy.el;oldNode.remove();enemy.el=null;syncCombatUnits();
        if(enemy.el===oldNode||!enemy.el.querySelector('.statuses')||!enemy.el.querySelector('.awareness'))throw Error('Unit recreation failed');
        if(enemy.el.querySelector('.statuses').children.length!==7||enemy.el.querySelector('.awareness i').style.width!=='100%')throw Error('Unit recreation lost status/awareness');
        return {units:Game.units.length,originalIcons:actual,stableRefreshes:100,stableMutations:stableMutations.length,recreation:true};
    }""")
    (ROOT/'qa').mkdir(exist_ok=True)
    p.screenshot(path=str(ROOT/'qa/pwa12-66-combat-status-browser.png'))
    assert not errors,errors
    assert not missing,missing
    print('PASS PWA12.61 browser status/awareness invalidation',result)
    b.close()
