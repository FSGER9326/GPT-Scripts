from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text(); SHIM="<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"
HTML=HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1).replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox']); p=b.new_page(viewport={'width':1280,'height':900}); errs=[]
 def route(r):
  rel=r.request.url.split('http://cr.local/',1)[-1].split('?',1)[0] or 'index.html'; fp=ROOT/rel
  r.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream') if fp.is_file() else r.fulfill(status=404,body=b'x')
 p.route('http://cr.local/**',route);p.on('pageerror',lambda e:errs.append(str(e)));p.set_content(HTML,wait_until='domcontentloaded');p.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
 p.evaluate("()=>{startNewGame('Vex','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');showScreen('combat');const m={id:'alarm_chain',type:'heist',objective:'heist',_v12ObjectiveAssigned:true,name:'Alarm chain',desc:'QA',contact:null,diff:3,enemies:['Guard','Enforcer','Drone'],reward:600,xp:70,targetFaction:'meridian',factionRepGain:0,factionRepLoss:{}};Game.activeMission=m;initCombat(m);Game.alerted=true;Game.objective.completed=true;checkWinLose()}")
 p.wait_for_function('()=>CR14MultiStageOperations.active?.index===1')
 mid=p.evaluate("()=>({enemies:Game.units.filter(u=>u.team==='enemy').map(u=>u.className),strip:document.getElementById('operation-stage-strip').textContent,alerted:Game.alerted})")
 assert len(mid['enemies'])==4 and 'Drone' in mid['enemies'] and 'ESCALATED' in mid['strip'] and mid['alerted'],mid
 p.evaluate("()=>{Game.objective.completed=true;checkWinLose()}");p.wait_for_function('()=>CR14MultiStageOperations.active?.index===2')
 end=p.evaluate("()=>({enemies:Game.units.filter(u=>u.team==='enemy').map(u=>u.className),hazards:Game.grid.filter(c=>c.hazardTypeV12==='livewire').map(c=>[c.x,c.y]),strip:document.getElementById('operation-stage-strip').textContent,alerted:Game.alerted})")
 assert len(end['enemies'])==3 and 'Guard' in end['enemies'] and len(end['hazards'])==2 and 'ESCALATED' in end['strip'] and end['alerted'],end
 assert not errs,errs
 print('PASS PWA12.45 loud perimeter breach escalates later enemy response and energizes two extraction hazards',mid,end)
 b.close()
