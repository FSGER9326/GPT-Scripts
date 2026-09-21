"""PWA12.70 contact-level browser QA: new and archived casefiles, desktop/mobile screenshot."""
from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa'/'pwa12_70';OUT.mkdir(parents=True,exist_ok=True)
html=(ROOT/'index.html').read_text().replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
shim="""<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"""
html=html.replace('<head>','<head><base href="http://cr.local/">'+shim,1)
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 c=b.new_context(viewport={'width':1280,'height':850},device_scale_factor=1)
 errors=[];missing=[]
 def route(r):
  url=r.request.url
  if not url.startswith('http://cr.local/'):return r.abort()
  rel=url[len('http://cr.local/'):].split('?',1)[0] or 'index.html';fp=ROOT/rel
  if fp.is_file():r.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream')
  else:missing.append(rel);r.fulfill(status=404,body=b'NOT FOUND')
 c.route('http://cr.local/**',route)
 p=c.new_page();p.on('pageerror',lambda e:errors.append(str(e)))
 p.set_content(html,wait_until='domcontentloaded')
 p.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
 boot=p.evaluate("""()=>{
  startNewGame('Cipher','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');
  const c=Game.contacts[0];if(!c)throw Error('No city contacts');
  Game.ovPlayer={...Game.ovPlayer,x:c.x,y:c.y};
  Game.missionHistory.push({id:'casefile_browser_70',name:'Blacksite Requiem',contact:c.id,diff:2,targetFaction:'meridian',operationIntelRecoveredV14:{bonus:170},reward:540});
  renderContactDossierV13(c.id);showScreen('v13-contact-screen');
  return{contact:c.id,name:c.name,leads:CR14MultiStageOperations.pendingLeads(c.id).length};
 }""")
 assert boot['leads']==1,boot
 assert p.locator('.v14-intel-lead button').count()==2
 p.locator('.v14-intel-lead button').first.click()
 state=p.evaluate("""()=>({
  active:Game.activeMission?.id||null,
  ledger:document.querySelector('.v14-intel-ledger summary')?.textContent,
  followups:[...document.querySelectorAll('#v13-contracts .v14-intel-followup-card h4')].map(e=>e.textContent),
  journal:Game.journal.find(j=>j.id?.startsWith('intel_debrief_'))?.decision,
  count:Game.contacts.find(c=>c.id===Game.missionHistory[Game.missionHistory.length-1].contact)?.missions.filter(m=>m.intelFollowUpV14).length
 })""")
 assert state['ledger'] and '1 RESOLVED' in state['ledger'] and state['journal']=='disclose' and state['followups'],state
 p.locator('.v14-intel-ledger summary').click()
 assert 'CUT THE AUDIT' in p.locator('.v14-intel-ledger-list').inner_text()
 p.screenshot(path=str(OUT/'pwa12_70_intel_desktop.png'),animations='disabled')
 p.set_viewport_size({'width':412,'height':839})
 p.wait_for_timeout(200)
 mobile=p.evaluate("""()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,summary:document.querySelector('.v14-intel-ledger summary')?.textContent,buttons:[...document.querySelectorAll('.v14-intel-lead-actions button')].length})""")
 p.screenshot(path=str(OUT/'pwa12_70_intel_mobile.png'),animations='disabled')
 assert mobile['scroll']<=mobile['width']+1 and '1 RESOLVED' in mobile['summary'],mobile
 assert not errors and not missing,(errors,missing)
 print('PASS PWA12.70 actual contact UI: in-person disclosure -> follow-up card and expandable resolved ledger; desktop/mobile screenshots; no page errors/missing assets; no mobile overflow',flush=True)
 print('BROWSER_STATE',boot,state,mobile,flush=True)
 b.close()
