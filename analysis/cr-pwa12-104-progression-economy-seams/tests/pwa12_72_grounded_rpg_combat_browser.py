"""Grounded RPG visual QA on the current PWA12.71 canonical (save/load-race base)."""
from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text(encoding='utf-8')
SHIM="""<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"""
HTML=HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1).replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for label,viewport in [('desktop',{'width':1440,'height':900}),('mobile',{'width':390,'height':844})]:
  ctx=browser.new_context(viewport=viewport,device_scale_factor=1)
  p=ctx.new_page();errors=[];missing=[];p.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   url=r.request.url
   if not url.startswith('http://cr.local/'):return r.abort()
   rel=url[len('http://cr.local/'):].split('?',1)[0] or 'index.html';fp=ROOT/rel
   if fp.is_file():r.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream')
   else:missing.append(rel);r.fulfill(status=404,body=b'NOT FOUND')
  p.route('http://cr.local/**',route)
  p.set_content(HTML,wait_until='domcontentloaded');p.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=30000)
  p.evaluate("""()=>{startNewGame('Vex','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');const m={id:'qa71',name:'ACTION LEGIBILITY QA',desc:'Action Legibility',type:'raid',objective:'raid',sectorId:'old_market',targetFaction:'spine',enemies:['Guard','Enforcer'],diff:2,reward:1,xp:1,factionRepGain:0,factionRepLoss:{}};Game.activeMission=m;showScreen('combat');initCombat(m);document.getElementById('banner')?.classList.remove('show');} """)
  p.wait_for_timeout(1600)
  info=p.evaluate("""()=>{const buttons=[...document.querySelectorAll('#actions>button')],board=document.querySelector('#board').getBoundingClientRect();return {boardWidth:board.width,scrollWidth:document.documentElement.scrollWidth,width:innerWidth,buttons:buttons.map(b=>({name:b.querySelector('span')?.textContent,cost:b.querySelector('small.v14-action-ap')?.textContent,aria:b.getAttribute('aria-label'),height:b.getBoundingClientRect().height,spanRect:b.querySelector('span')?.getBoundingClientRect().toJSON(),buttonRect:b.getBoundingClientRect().toJSON()})),longAbility:[...document.querySelectorAll('#actions>button span')].some(s=>s.textContent==='Ghost in the Machine'),totalButtons:document.querySelectorAll('#actions>button').length}}""")
  print(label,info,flush=True)
  assert info['totalButtons']>=7 and info['boardWidth']>220,(label,info)
  assert all(b['height']>=40 for b in info['buttons']),(label,info)
  assert info['scrollWidth']<=info['width']+1 and info['boardWidth']>220,info
  assert not errors and not missing,(errors,missing)
  (ROOT/'qa').mkdir(exist_ok=True)
  p.screenshot(path=str(ROOT/'qa'/f'pwa12-72-grounded-rpg-{label}.png'),full_page=True)
  ctx.close()
 browser.close()
print('PWA12.72 GROUNDED RPG VISUAL BROWSER PASS',flush=True)
