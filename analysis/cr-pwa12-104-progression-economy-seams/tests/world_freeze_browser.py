from pathlib import Path
import mimetypes, hashlib
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'index.html').read_text(encoding='utf-8')
shim="""<script>const __crls=(()=>{const s=new Map();return{getItem:k=>s.has(String(k))?s.get(String(k)):null,setItem:(k,v)=>s.set(String(k),String(v)),removeItem:k=>s.delete(String(k)),clear:()=>s.clear(),key:i=>[...s.keys()][i]??null,get length(){return s.size}}})();try{Object.defineProperty(window,'localStorage',{value:__crls,configurable:true})}catch(e){};try{Object.defineProperty(window,'sessionStorage',{value:__crls,configurable:true})}catch(e){}</script>"""
html=html.replace('<head>','<head><base href="http://cr.local/">'+shim,1).replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 p=b.new_page(viewport={'width':1280,'height':800});missing=[];errors=[]
 def handler(route):
  u=route.request.url
  if not u.startswith('http://cr.local/'):return route.abort()
  rel=u[len('http://cr.local/'):].split('?',1)[0] or 'index.html';fp=ROOT/rel
  if fp.exists() and fp.is_file():route.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream')
  else:missing.append(rel);route.fulfill(status=404,body=b'not found',content_type='text/plain')
 p.route('http://cr.local/**',handler);p.on('pageerror',lambda e:errors.append(str(e)))
 p.set_content(html,wait_until='domcontentloaded');p.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=15000)
 p.evaluate("""()=>{startNewGame('Vex','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');showScreen('overworld-screen');activateDistrictV133('old_market',null);initOverworld();Game.ovStaticDirty=true;Game.ovCamera.follow=false;Game.ovCamera.x=Game.ovCamera.tx;Game.ovCamera.y=Game.ovCamera.ty;}""")
 p.wait_for_timeout(350)
 def snap():
  st=p.evaluate("""()=>{const s=Game.livingStreetsV134;return{day:Game.day,hour:Game.hour,steps:s.stepCount,actors:(s.actors?.old_market||[]).map(a=>[a.id,a.x,a.y,a.steps]),player:[Game.ovPlayer.x,Game.ovPlayer.y],pending:Game.pendingPath?.length||0}}""")
  st['canvas']=hashlib.sha256(p.locator('#overworld').screenshot()).hexdigest();return st
 a=snap();p.wait_for_timeout(900);bstate=snap()
 assert a==bstate,(a,bstate)
 p.evaluate('CR14ActionTime.wait(15)');p.wait_for_timeout(220);c=snap()
 delta=(c['day']-a['day'])*24+(c['hour']-a['hour'])
 assert abs(delta-.25)<1e-9,(a,c)
 assert c['steps']>a['steps'],(a,c)
 p.wait_for_timeout(900);d=snap();assert c==d,(c,d)
 # route once; time must advance, then freeze again after path is forcibly concluded
 moved=p.evaluate("""()=>{const w=currentDistrictV133();const id=Object.keys(w.locations||{}).find(x=>x!=='v133_safehouse');return id?routeToLocationV133(id):false}""")
 assert moved is not False,moved
 p.wait_for_timeout(220);e=snap();assert (e['day'],e['hour'])!=(d['day'],d['hour']),(d,e)
 p.evaluate("""()=>{Game.pendingPath=null;Game._v133TravelTarget=null;Game.ovCamera.follow=false;Game.ovCamera.x=Game.ovCamera.tx;Game.ovCamera.y=Game.ovCamera.ty}""");p.wait_for_timeout(250);f=snap();p.wait_for_timeout(800);g=snap();assert f==g,(f,g)
 assert not errors,errors
 assert not missing,missing
 print('WORLD FREEZE BROWSER PASS',{'idle':a,'wait':c,'movement':e})
 b.close()
