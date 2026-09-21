from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text()
SHIM="<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"
HTML=HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1).replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
SNAP="""()=>{const u=Game.roster[0];return {credits:Game.credits,day:Game.day,hour:Game.hour,rep:Game.rep,heat:structuredClone(Game.heat),factionPower:structuredClone(Game.factionPower),districtControl:structuredClone(Game.districtControl),rival:structuredClone(Game.rival),stash:structuredClone(Game.stash),safehouse:structuredClone(Game.safehouse),missionHistory:structuredClone(Game.missionHistory),storyFlags:structuredClone(Game.storyFlags),crew:{name:u.name,level:u.level,xp:u.xp,injuries:structuredClone(u.injuries),loyalty:u.loyalty,cyber:structuredClone(u.cyber),inventory:structuredClone(u.inventory)}}}"""
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox']);p=b.new_page();errs=[]
 def route(r):
  rel=r.request.url.split('http://cr.local/',1)[-1].split('?',1)[0] or 'index.html';fp=ROOT/rel
  r.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream') if fp.is_file() else r.fulfill(status=404,body=b'x')
 p.route('http://cr.local/**',route);p.on('pageerror',lambda e:errs.append(str(e)));p.set_content(HTML,wait_until='domcontentloaded');p.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
 p.evaluate("""()=>{startNewGame('Persistence QA','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');Game.credits=43210;Game.day=9;Game.hour=18.75;Game.rep=37;Game.heat={meridian:17,wraiths:4,iron:29,chrome:8,spine:13};Game.factionPower={meridian:61,wraiths:39,iron:52,chrome:47,spine:33};Game.districtControl={nero:'iron',undercity:'wraiths',steelworks:'iron',neon:'chrome',spine:'spine',mirage:'meridian'};Game.rival={name:'Black Halo',score:73,lastDay:8};Game.stash={weapons:['smg_mk1'],armor:['vest_mk1']};Game.safehouse={workshop:3,infirmary:2,bar:2,server:4};Game.missionHistory=[{id:'qa_done',name:'Ghost Wire',success:true,day:7}];Game.storyFlags={...Game.storyFlags,persistence_qa:true};const u=Game.roster[0];u.xp=(u.xp||0)+777;u.level=Math.max(3,u.level||1);u.injuries=['burn'];u.loyalty=8;u.cyber=['reflex'];u.inventory={medkit:2,grenade:1};applySkillsToUnit(u);saveGame(1,false)}""")
 p.evaluate('()=>ChromeRequiemV14Boot.bridge.flush()');before=p.evaluate(SNAP)
 p.evaluate("()=>{Game.credits=1;Game.day=1;Game.hour=0;Game.rep=0;Game.roster=[];Game.missionHistory=[];Game.storyFlags={}}")
 ok=p.evaluate('()=>ChromeRequiemV14Boot.runtime.load(1)');assert ok is True
 after=p.evaluate(SNAP);assert before==after,f'durable semantic mismatch: before={before} after={after}'
 # Derived combat stats must be recomputed from class/gear/skills on load, not compared to arbitrary pre-save mutations.
 derived=p.evaluate("()=>{const u=Game.roster[0];return [u.maxHp,u.damage,u.armor,u.range,u.move,u.maxAp].every(Number.isFinite)&&u.hp<=u.maxHp}")
 assert derived
 assert not errs,errs
 print('PASS PWA12.56 progressed campaign semantic save/load equivalence; derived combat stats normalized safely')
 b.close()
