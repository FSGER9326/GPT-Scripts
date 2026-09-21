"""Real Chromium validation for mission-shaped arenas, door gating, objective reachability and responsive visual capture."""
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
    page=browser.new_page(viewport={'width':1440,'height':950},device_scale_factor=1)
    errors=[];missing=[]
    def route(r):
        url=r.request.url
        if not url.startswith('http://cr.local/'):return r.abort()
        rel=url.split('http://cr.local/',1)[1].split('?',1)[0] or 'index.html'; fp=ROOT/rel
        if fp.is_file():r.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream')
        else:missing.append(rel);r.fulfill(status=404,body=b'not found',content_type='text/plain')
    page.route('http://cr.local/**',route)
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content(HTML,wait_until='domcontentloaded')
    page.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=35000)
    page.evaluate("()=>{startNewGame('Vex','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');showScreen('combat')}")
    for kind,name,shape in [('breach','Corridor breach','corridor'),('raid','Building entrance','entrance'),('heist','Secure inner rooms','rooms'),('extract','Data recovery','rooms')]:
        page.evaluate("""({kind,name})=>{const m={id:'arena_'+kind,type:kind,objective:kind,_v12ObjectiveAssigned:true,name,desc:name,contact:null,diff:1,enemies:['Guard','Enforcer'],reward:400,xp:70,targetFaction:'meridian',factionRepGain:0,factionRepLoss:{}};Game.activeMission=m;initCombat(m)}""",{'kind':kind,'name':name})
        page.wait_for_timeout(600)
        data=page.evaluate("""()=>({shape:Game.arenaShapeV14,voids:Game.grid.filter(c=>c.arenaVoid).length,units:Game.units.map(u=>({team:u.team,x:u.x,y:u.y,blocked:cellAt(u.x,u.y)?.obstacle})),doors:Game.grid.filter(c=>c.door).map(c=>({x:c.x,y:c.y,locked:c.doorLocked,obstacle:c.obstacle})),objectives:Game.objective.cells.map(o=>({x:o.x,y:o.y,kind:o.kind,void:cellAt(o.x,o.y)?.arenaVoid})),exfil:Game.objective.exfil,board:document.getElementById('board')?.dataset.arenaShape,errors:window.CR14VariableArenas?.choose?.(Game.activeMission)})""")
        assert data['shape']==shape and data['board']==shape and data['voids']>=18, data
        assert not any(u['blocked'] for u in data['units']),data
        assert all(not o['void'] for o in data['objectives']),data
        assert len(data['doors'])>=1 and all(d['obstacle'] for d in data['doors']),data
        print('ARENA',kind,data,flush=True)
        if kind in ('breach','raid','heist'):
            page.wait_for_timeout(900)
            path=OUT/f'pwa12-41-{shape}-desktop.png';page.screenshot(path=str(path));print('SCREENSHOT',path,flush=True)
        # Every objective must be reachable from the crew once authored doors are opened.
        paths=page.evaluate('''()=>{
          const crew=Game.units.find(u=>u.team==='player');const doors=Game.grid.filter(c=>c.door);
          const originals=doors.map(c=>c.obstacle);doors.forEach(c=>c.obstacle=false);
          const blockers=Game.grid.map(c=>c.unit);Game.grid.forEach(c=>c.unit=null);
          ChromeRequiemV14Domains.PerformanceV14.perf.movementCache=null;
          const result=Game.objective.cells.map(o=>({x:o.x,y:o.y,steps:combatPathDistance({x:crew.x,y:crew.y},o.x,o.y)}));
          doors.forEach((c,i)=>c.obstacle=originals[i]);Game.grid.forEach((c,i)=>c.unit=blockers[i]);
          ChromeRequiemV14Domains.PerformanceV14.perf.movementCache=null;return result;
        }''')
        print('REACH_DEBUG',kind,paths,page.evaluate("()=>Game.grid.map(c=>c.obstacle?'#':c.door?'D':'.').join('').match(/.{10}/g)"),flush=True)
        assert all(o['steps']!=float('inf') for o in paths), (kind,paths)
        print('ACCESSIBLE_OBJECTIVES',kind,paths,flush=True)
        if kind=='breach':
            # A reinforcement requested at an obsolete square-map edge must land
            # on a real, unoccupied tile in the shaped enemy-side section.
            wave=page.evaluate('''()=>{
              const previous=Game.units.length;
              spawnEnemyReinforcement('Drone',9,0);
              const drone=Game.units[Game.units.length-1];
              return {before:previous,after:Game.units.length,x:drone.x,y:drone.y,
                      valid:!cellAt(drone.x,drone.y).arenaVoid&&!cellAt(drone.x,drone.y).obstacle};
            }''')
            assert wave['after']==wave['before']+1 and wave['valid'],wave
            print('SHAPED_REINFORCEMENT',wave,flush=True)
            # The locked doorway, rather than the frame, is the tactical choke point.
            blocker=page.evaluate("""()=>({blocked:!hasLOS({x:4,y:3},{x:4,y:1}),path:combatPathDistance({x:4,y:3},4,1)})""")
            assert blocker['blocked'] and blocker['path']==float('inf'),blocker
            page.evaluate("""()=>{const u=Game.units.find(u=>u.team==='player');cellAt(u.x,u.y).unit=null;u.x=4;u.y=3;cellAt(4,3).unit=u;Game.selectedUnit=u;Game.turn='player';u.ap=2;onCombatCellClick(4,2)}""")
            opened=page.evaluate("""()=>({door:cellAt(4,2).door,open:cellAt(4,2).doorOpen,obstacle:cellAt(4,2).obstacle,ap:Game.selectedUnit.ap,los:hasLOS({x:4,y:3},{x:4,y:1}),path:combatPathDistance({x:4,y:3},4,1)})""")
            assert opened['door'] and opened['open'] and not opened['obstacle'] and opened['ap']==1 and opened['los'],opened
            print('BREACH',{'before':blocker,'after':opened},flush=True)
        if kind=='extract':
            # Use the real action deck to finish the upload at the reshaped terminal.
            page.evaluate('''()=>{
              const u=Game.units.find(x=>x.team==='player');cellAt(u.x,u.y).unit=null;
              const terminal=Game.objective.cells[0];u.x=terminal.x;u.y=terminal.y;
              cellAt(u.x,u.y).unit=u;Game.selectedUnit=u;Game.turn='player';u.ap=3;updateCombat();
            }''')
            page.wait_for_function("()=>!!Array.from(document.querySelectorAll('#actions button')).find(b=>b.textContent.includes('UPLOAD'))",timeout=6000)
            for i in range(3):
                page.locator('#actions button').filter(has_text='UPLOAD').first.click(timeout=6000)
                page.wait_for_function('(n)=>Game.objective.progress===n',arg=i+1,timeout=6000)
            protected=page.evaluate("()=>({complete:Game.objective.completed,gameOver:Game.gameOver,hud:document.getElementById('objective-hud').textContent,exfil:Game.objective.exfil})")
            assert protected['complete'] and not protected['gameOver'] and '[04,09]' in protected['hud'],protected
            page.evaluate('''()=>{
              const u=Game.units.find(x=>x.team==='player');cellAt(u.x,u.y).unit=null;
              u.x=4;u.y=9;cellAt(4,9).unit=u;Game.selectedUnit=u;Game.turn='player';u.ap=1;updateCombat();
            }''')
            page.wait_for_function("()=>!!document.querySelector('#actions .v14-exfil-action:not([disabled])')",timeout=6000)
            page.screenshot(path=str(OUT/'pwa12-41-rooms-exfil-desktop.png'))
            page.locator('#actions .v14-exfil-action').click(timeout=6000)
            page.wait_for_function('()=>Game.gameOver===true',timeout=6000)
            assert page.evaluate("Game.objective.exfilReady && !serializeGame().includes('arenaShapeV14')")
            print('SHAPED_EXFIL',protected,flush=True)
    # Unshaped elimination contracts still receive the historical open arena.
    page.evaluate('''()=>{const m={id:'open_elim',type:'eliminate',objective:'eliminate',_v12ObjectiveAssigned:true,name:'Open terrain',desc:'An outdoor fight',enemies:['Guard'],diff:1,reward:100,xp:20,targetFaction:'iron',factionRepGain:0,factionRepLoss:{}};Game.activeMission=m;initCombat(m)}''')
    assert page.evaluate("Game.arenaShapeV14===null && !document.getElementById('board').dataset.arenaShape && Game.grid.every(c=>!c.arenaVoid)")
    print('OPEN_ARENA_PRESERVED',flush=True)
    page.set_viewport_size({'width':390,'height':844})
    page.evaluate("""()=>{const m={id:'mobile_breach',type:'breach',objective:'breach',_v12ObjectiveAssigned:true,name:'SERVICE CORRIDOR',desc:'Reach the access door',contact:null,diff:1,enemies:['Guard'],reward:300,xp:50,targetFaction:'iron',factionRepGain:0,factionRepLoss:{}};Game.activeMission=m;initCombat(m)}""")
    page.wait_for_timeout(500)
    mobile=page.evaluate("""()=>({shape:Game.arenaShapeV14,width:document.documentElement.scrollWidth,viewport:innerWidth,door:Game.grid.filter(c=>c.door).length,button:document.querySelector('#actions .end-turn')?.getBoundingClientRect().height})""")
    page.screenshot(path=str(OUT/'pwa12-41-corridor-mobile.png'))
    assert mobile['shape']=='corridor' and mobile['width']<=mobile['viewport']+1 and mobile['door']>=1,mobile
    print('MOBILE',mobile,'ERRORS',errors[:8],'MISSING',missing[:8],flush=True)
    assert not errors and not missing,(errors,missing)
    browser.close()
