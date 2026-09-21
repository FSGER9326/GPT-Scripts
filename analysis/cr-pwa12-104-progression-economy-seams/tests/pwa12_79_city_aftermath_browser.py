"""Browser QA of new city consequence from a completed Intel Dossier operation.
The core success condition is arranged programmatically; not a naturally played battle.
"""
from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa'/'pwa12_79';OUT.mkdir(exist_ok=True)
html=(ROOT/'index.html').read_text().replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
shim="""<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"""
html=html.replace('<head>','<head><base href="http://cr.local/">'+shim,1)
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 ctx=browser.new_context(viewport={'width':1280,'height':850},device_scale_factor=1)
 errors=[];missing=[]
 def route(r):
  url=r.request.url
  if not url.startswith('http://cr.local/'):return r.abort()
  rel=url[len('http://cr.local/'):].split('?',1)[0] or 'index.html';fp=ROOT/rel
  if fp.is_file():r.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream')
  else:missing.append(rel);r.fulfill(status=404,body=b'NOT FOUND')
 ctx.route('http://cr.local/**',route)
 p=ctx.new_page();p.on('pageerror',lambda e:errors.append(str(e)))
 p.set_content(html,wait_until='domcontentloaded');p.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
 state=p.evaluate('''()=>{
 startNewGame('Neon','Hacker','street');Game.storyFlags.story_mission_1_complete=true;document.getElementById('story-modal')?.classList.remove('open');
 const c=Game.contacts.find(c=>c.sectorId==='old_market')||Game.contacts[0];
 Game.districtWorldsV133.activeId=c.sectorId;Game.ovPlayer={...Game.ovPlayer,x:c.x,y:c.y};
 Game.missionHistory.push({id:'pwa77_browser_source',name:'Blacksite Signal',contact:c.id,sectorId:'old_market',diff:2,targetFaction:'meridian',operationIntelRecoveredV14:{bonus:180},reward:500});
 const api=CR14MultiStageOperations,lead=api.pendingLeads(c.id)[0];if(!lead||!api.resolveLead(c.id,lead.key,'disclose'))throw Error('Intelligence disclosure could not be completed');
 const job=c.missions.find(m=>m.intelFollowUpV14);if(!job)throw Error('No followup');
 Game.activeMission=job;Game.objective={type:'sabotage',completed:true,quiet:false,exfil:null};Game.gameOver=false;
 finalizeMissionSuccess();
 // Complete the normal debrief flow before capturing the playable city, rather
 // than screenshotting the mission-complete overlay over a hidden world.
 returnToOverworld(true);document.getElementById('v10-debrief-continue')?.click();
 document.getElementById('story-modal')?.classList.remove('open');showScreen('overworld-screen');updateNeighborhoodHUDV134();
 return {job:job.id,area:Game.districtWorldsV133.activeId,heat:Game.heat.meridian,time:Game.hour,day:Game.day,imp:intelDistrictAftermathV134(currentDistrictV133()),label:document.getElementById('v134-neighborhood-status')?.innerText};
 }''')
 assert state['imp']=={'securityRelief':1,'traceRelief':0,'closed':1},state
 assert 'AUDIT RELAY OFFLINE' in state['label'],state
 assert not missing and not errors,(missing[:5],errors[:5])
 p.wait_for_timeout(150)
 p.evaluate('''()=>{Game.ovStaticDirty=true;Game._v133FrameRect=null;initOverworld();}''')
 p.wait_for_timeout(300)
 p.screenshot(path=str(OUT/'pwa12_79_old_market_audit_offline_desktop.png'),animations='disabled')
 p.set_viewport_size({'width':412,'height':839});p.wait_for_timeout(80)
 mobile=p.evaluate('''()=>({label:document.getElementById('v134-neighborhood-status')?.innerText,width:innerWidth,scroll:document.documentElement.scrollWidth,time:Game.hour,day:Game.day,imp:intelDistrictAftermathV134(currentDistrictV133())})''')
 assert 'AUDIT RELAY OFFLINE' in mobile['label'] and mobile['imp']['closed']==1,mobile
 assert mobile['scroll']<=mobile['width']+1,mobile
 assert mobile['time']==state['time'] and mobile['day']==state['day'],(state,mobile)
 p.screenshot(path=str(OUT/'pwa12_79_old_market_audit_offline_mobile.png'),animations='disabled')
 assert not errors and not missing,(errors,missing[:5])
 print('PASS PWA12.79 Chromium district aftermath: completed intel casefile -> target-district HUD and patrol relief; desktop/mobile render, no passive time advancement, no errors/404 or mobile overflow',flush=True)
 print('STATE',state,mobile,flush=True)
 browser.close()
