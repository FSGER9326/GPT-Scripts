from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text(); SHIM="<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"
HTML=HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1).replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox']);p=b.new_page(viewport={'width':1280,'height':900});errs=[]
 def route(r):
  rel=r.request.url.split('http://cr.local/',1)[-1].split('?',1)[0] or 'index.html';fp=ROOT/rel
  r.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream') if fp.is_file() else r.fulfill(status=404,body=b'x')
 p.route('http://cr.local/**',route);p.on('pageerror',lambda e:errs.append(str(e)));p.set_content(HTML,wait_until='domcontentloaded');p.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
 p.evaluate("()=>{startNewGame('Vex','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');showScreen('combat');const m={id:'override_chain',type:'heist',objective:'heist',_v12ObjectiveAssigned:true,name:'Override chain',desc:'QA',contact:null,diff:3,enemies:['Guard','Enforcer','Drone'],reward:600,xp:70,targetFaction:'meridian',factionRepGain:0,factionRepLoss:{}};Game.activeMission=m;initCombat(m);Game.alerted=true;const c=CR14MultiStageOperations.active.console,u=Game.units.find(x=>x.team==='player'&&x.className==='Hacker')||Game.units.find(x=>x.team==='player');const spot=Game.grid.find(v=>!v.obstacle&&!v.arenaVoid&&!v.unit&&Math.abs(v.x-c.x)+Math.abs(v.y-c.y)<=1);const old=Game.grid.find(v=>v.unit===u);if(old)old.unit=null;u.x=spot.x;u.y=spot.y;spot.unit=u;Game.selectedUnit=u;u.ap=Math.max(u.ap,2);const a=objectiveActionAvailable(u);if(!a||!a.label.includes('OVERRIDE'))throw Error('override action unavailable');a.run();Game.objective.completed=true;checkWinLose()}")
 p.wait_for_function('()=>CR14MultiStageOperations.active?.index===1')
 mid=p.evaluate("()=>({active:CR14MultiStageOperations.active,enemies:Game.units.filter(u=>u.team==='enemy').map(u=>u.className),strip:document.getElementById('operation-stage-strip').textContent,alerted:Game.alerted})")
 assert mid['active']['securitySuppressed'] and len(mid['enemies'])==3 and 'SUPPRESSED' in mid['strip'] and mid['alerted'],mid
 p.evaluate("()=>{Game.objective.completed=true;checkWinLose()}");p.wait_for_function('()=>CR14MultiStageOperations.active?.index===2')
 end=p.evaluate("()=>({enemies:Game.units.filter(u=>u.team==='enemy').map(u=>u.className),hazards:Game.grid.filter(c=>c.hazardTypeV12==='livewire').length,strip:document.getElementById('operation-stage-strip').textContent})")
 assert len(end['enemies'])==2 and end['hazards']==0 and 'SUPPRESSED' in end['strip'],end
 assert not errs,errs
 print('PASS PWA12.47 optional security override suppresses loud-operation reinforcements and containment hazards',mid,end)
 b.close()
