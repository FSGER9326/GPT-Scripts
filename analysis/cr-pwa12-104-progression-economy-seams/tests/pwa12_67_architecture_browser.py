"""PWA12.67: verify asset-backed tactical wall/cover art stays presentation only on desktop and mobile."""
from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text(encoding='utf-8')
SHIM="""<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"""
HTML=HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1).replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 p=b.new_page(viewport={'width':1280,'height':850},device_scale_factor=1)
 errors=[];missing=[]
 p.on('pageerror',lambda e:errors.append(str(e)))
 def route(r):
  u=r.request.url
  if not u.startswith('http://cr.local/'):return r.abort()
  rel=u[len('http://cr.local/'):].split('?',1)[0] or 'index.html';fp=ROOT/rel
  if fp.is_file():r.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream')
  else:missing.append(rel);r.fulfill(status=404,body=b'NOT FOUND')
 p.route('http://cr.local/**',route)
 p.set_content(HTML,wait_until='domcontentloaded');p.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=30000)
 p.evaluate("()=>{startNewGame('Vex','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');showScreen('combat')}")
 all_themes={'old_market':'market_street','dock_nine':'dock','forge_belt':'warehouse','undergrid':'server_room','neon_row':'club','glass_heights':'office_entry','civic_circuit':'parking_garage','ash_blocks':'tenement_hall'}
 for sector,theme in all_themes.items():
  p.evaluate("""({sector})=>{const m={id:'art_'+sector,type:'raid',objective:'raid',sectorId:sector,name:'Art test',desc:'Art test',contact:null,diff:1,enemies:['Guard','Enforcer'],reward:100,xp:20,targetFaction:'meridian',factionRepGain:0,factionRepLoss:{}};Game.activeMission=m;initCombat(m)}""",{'sector':sector})
  p.wait_for_timeout(1450)
  info=p.evaluate("""()=>{const board=document.getElementById('board'),grid=Game.grid;
   const walls=grid.filter(c=>c.obstacle&&!c.door&&!c.arenaVoid),covers=grid.filter(c=>c.cover),walkable=grid.filter(c=>!c.obstacle&&!c.cover&&!c.arenaVoid),
   wallLayers=walls.map(c=>c._v14EnvObject).filter(e=>e&&e.classList.contains('v14-env-architecture')&&e.style.backgroundImage.includes('architecture/')),
   coverLayers=covers.map(c=>c._v14EnvObject).filter(e=>e&&e.classList.contains('v14-env-architecture')&&e.style.backgroundImage.includes('architecture/'));
   return {theme:board?.dataset?.v14Environment,walls:walls.length,covers:covers.length,wallLayers:wallLayers.length,coverLayers:coverLayers.length,
    staticGrid:grid.map(c=>`${c.x},${c.y},${!!c.obstacle},${!!c.cover},${!!c.door}`).join('|'),
    wallImage:wallLayers[0]?.style.backgroundImage,coverImage:coverLayers[0]?.style.backgroundImage,
    pointerEvents:wallLayers[0]?getComputedStyle(wallLayers[0]).pointerEvents:null,
    hasArtOnWalkable:walkable.some(c=>c._v14EnvObject?.classList.contains('v14-env-architecture'))}}""")
  assert info['theme']==theme,(sector,info)
  assert info['walls']>0 and info['covers']>0 and info['wallLayers']>=1 and info['wallLayers']<=info['walls'] and info['coverLayers']==info['covers'],(sector,info)
  assert theme in info['wallImage'] and theme in info['coverImage'] and info['pointerEvents']=='none' and not info['hasArtOnWalkable'],(sector,info)
  if sector in ('old_market','dock_nine','undergrid'):
   p.locator('#board').screenshot(path=str(ROOT/'qa'/f'pwa12-67-{sector}-desktop.png'))
  print('DISTRICT_ART_PASS',sector,theme,'walls',info['walls'],'covers',info['covers'],flush=True)
 p.set_viewport_size({'width':390,'height':844})
 p.evaluate("""()=>{const m={id:'art_mobile',type:'raid',objective:'raid',sectorId:'old_market',name:'Mobile art',desc:'Mobile art',diff:1,enemies:['Guard'],reward:100,xp:20,targetFaction:'meridian',factionRepGain:0,factionRepLoss:{}};Game.activeMission=m;initCombat(m)}""")
 p.wait_for_timeout(1450)
 mobile=p.evaluate("""()=>({board:document.getElementById('board').getBoundingClientRect().width,viewport:innerWidth,scroll:document.documentElement.scrollWidth,walls:Game.grid.filter(c=>c.obstacle&&!c.door&&!c.arenaVoid&&c._v14EnvObject?.classList.contains('v14-env-architecture')).length})""")
 p.locator('#board').screenshot(path=str(ROOT/'qa'/'pwa12-67-old-market-mobile.png'))
 assert mobile['board']>200 and mobile['board']<=390 and mobile['scroll']<=mobile['viewport']+1 and mobile['walls']>0,mobile
 assert not errors and not missing,(errors,missing)
 print('MOBILE_ART_PASS',mobile,'PAGE_ERRORS',len(errors),'MISSING_ASSETS',len(missing),flush=True)
 b.close()
