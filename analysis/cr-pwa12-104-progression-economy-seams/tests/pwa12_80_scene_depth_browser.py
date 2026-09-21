"""Browser regression: deterministic lightfields/physical architecture and unchanged tactical semantics."""
from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text(encoding='utf-8')
SHIM="""<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"""
HTML=HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1).replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
THEMES={'old_market':'market_street','dock_nine':'dock','forge_belt':'warehouse','undergrid':'server_room','neon_row':'club','glass_heights':'office_entry','civic_circuit':'parking_garage','ash_blocks':'tenement_hall'}
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page(viewport={'width':1280,'height':850},device_scale_factor=1)
 errors=[];missing=[];page.on('pageerror',lambda e:errors.append(str(e)))
 def route(r):
  url=r.request.url
  if not url.startswith('http://cr.local/'):return r.abort()
  rel=url[len('http://cr.local/'):].split('?',1)[0] or 'index.html';fp=ROOT/rel
  if fp.is_file():r.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream')
  else:missing.append(rel);r.fulfill(status=404,body=b'NOT FOUND')
 page.route('http://cr.local/**',route)
 page.set_content(HTML,wait_until='domcontentloaded');page.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=30000)
 page.evaluate("()=>{startNewGame('Vex','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');showScreen('combat')}")
 initial=None
 for sector,theme in THEMES.items():
  page.evaluate("""sector=>{const m={id:'scene_'+sector,type:'raid',objective:'raid',sectorId:sector,name:'Scene QA',desc:'Scene QA',diff:1,enemies:['Guard','Enforcer'],reward:100,xp:20,targetFaction:'meridian',factionRepGain:0,factionRepLoss:{}};Game.activeMission=m;initCombat(m)}""",sector)
  page.wait_for_timeout(240)
  data=page.evaluate("""()=>{const board=document.querySelector('#board'),light=board.querySelector(':scope > .cr79-lightfield');const art=[...board.querySelectorAll('.v14-env-object.v14-env-architecture')];const obj=art.find(a=>a.style.backgroundImage.includes('architecture/physical/'));const unit=document.querySelector('#board .unit');const c=Game.grid.filter(x=>x.obstacle||x.cover||x.door||x.hazard).map(x=>[x.x,x.y,!!x.obstacle,!!x.cover,!!x.door,!!x.hazard]);return {theme:board.dataset.v14Environment,lights:board.querySelectorAll(':scope > .cr79-lightfield').length,lightImage:light?.style.backgroundImage,lightPointer:getComputedStyle(light).pointerEvents,lightZ:parseInt(getComputedStyle(light).zIndex),unitZ:parseInt(getComputedStyle(document.querySelector('#units')).zIndex),physical:art.filter(a=>a.style.backgroundImage.includes('architecture/physical/')).length,objectPointer:getComputedStyle(obj).pointerEvents,canClickGrid:getComputedStyle(document.querySelector('#grid')).pointerEvents,geometry:JSON.stringify(c),unitCount:document.querySelectorAll('#units .unit').length}}""")
  assert data['theme']==theme and data['lights']==1 and f'/{theme}.webp' in data['lightImage'],(sector,data)
  assert data['lightPointer']=='none' and data['lightZ']<data['unitZ'] and data['objectPointer']=='none' and data['physical']>0,(sector,data)
  assert data['unitCount']>=3 and not errors and not missing,(sector,data,errors,missing)
  if sector=='old_market':
   initial=data['geometry'];page.evaluate("()=>document.querySelector('#banner')?.classList.remove('show')");page.wait_for_timeout(1650);page.screenshot(path=str(ROOT/'qa/pwa12-80-combat-desktop.png'),full_page=True)
  print('PASS',sector,'lightfield',data['lights'],'physical-assets',data['physical'],flush=True)
 page.set_viewport_size({'width':390,'height':844});page.evaluate("()=>{const m={id:'scene_mobile',type:'raid',objective:'raid',sectorId:'old_market',name:'Scene QA',desc:'Scene QA',diff:1,enemies:['Guard','Enforcer'],reward:100,xp:20,targetFaction:'meridian',factionRepGain:0,factionRepLoss:{}};Game.activeMission=m;initCombat(m);document.querySelector('#banner')?.classList.remove('show')}");page.wait_for_timeout(1150)
 size=page.evaluate("""()=>({board:document.querySelector('#board').getBoundingClientRect().width,scroll:document.documentElement.scrollWidth,viewport:innerWidth,light:document.querySelectorAll('#board>.cr79-lightfield').length})""")
 assert 200<size['board']<=390 and size['scroll']<=size['viewport']+1 and size['light']==1,size
 page.screenshot(path=str(ROOT/'qa/pwa12-80-combat-mobile.png'),full_page=True)
 assert not errors and not missing,(errors,missing)
 print('PWA12.80 SCENE DEPTH PASS mobile',size,'errors',len(errors),'missing',len(missing),flush=True)
 browser.close()
