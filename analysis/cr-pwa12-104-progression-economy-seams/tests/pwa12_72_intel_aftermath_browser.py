"""Actual Chromium core-success integration and desktop/mobile casefile QA.

Programmatically resolves the tactical success condition to isolate debrief effects;
not a full naturally played contract.
"""
from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa'/'pwa12_72';OUT.mkdir(parents=True,exist_ok=True)
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
 start=p.evaluate('''()=>{
   startNewGame('Cipher','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');
   const c=Game.contacts[0];Game.ovPlayer={...Game.ovPlayer,x:c.x,y:c.y};
   Game.heat.wraiths=38;
   Game.missionHistory.push({id:'casefile_browser_71',name:'Blacksite Requiem',contact:c.id,diff:2,targetFaction:'wraiths',operationIntelRecoveredV14:{bonus:170},reward:540});
   renderContactDossierV13(c.id);showScreen('v13-contact-screen');
   return{id:c.id,name:c.name};
 }''')
 assert p.locator('.v14-intel-lead button').count()==2,start
 p.locator('.v14-intel-lead button').first.click()
 before=p.evaluate('''id=>({
   job:Game.contacts.find(c=>c.id===id).missions.find(m=>m.intelFollowUpV14)?.id,
   heat:Game.heat.wraiths,trust:Game.contactRelations[id].trust,
   ledger:document.querySelector('.v14-intel-ledger summary')?.textContent
 })''',start['id'])
 assert before['job'] and before['heat']==38 and '0 CLOSED' in before['ledger'],before
 # Invoke the canonical mission-success function after setting up a valid completed
 # objective, rather than merely inserting a fake completed history item or calling
 # the aftermarket helper directly. Combat path traversal remains a separate test.
 after=p.evaluate('''id=>{
  const c=Game.contacts.find(c=>c.id===id),job=c.missions.find(m=>m.intelFollowUpV14);
  if(!job)throw Error('Missing follow-up');
  Game.activeMission=job;Game.objective={type:'sabotage',completed:true,quiet:false,exfil:null};Game.gameOver=false;
  finalizeMissionSuccess();
  renderContactDossierV13(id);showScreen('v13-contact-screen');
  return{
   finished:Game.missionHistory.find(m=>m.id===job.id)?.intelAftermathV14,
   outcomes:Game.journal.filter(j=>j.id?.startsWith('intel_outcome_')).map(j=>j.desc),
   heat:Game.heat.wraiths,trust:Game.contactRelations[id].trust,
   ledger:document.querySelector('.v14-intel-ledger summary')?.textContent,
   ledgerText:document.querySelector('.v14-intel-ledger-list')?.textContent,
   offered:c.missions.filter(m=>m.id===job.id).length
  };
 }''',start['id'])
 assert after['finished'] and after['finished']['heatReduced']==20,after
 assert after['heat']==before['heat']-8 and after['trust']==before['trust']+7,(before,after)
 assert len(after['outcomes'])==1 and '1 CLOSED' in after['ledger'] and not after['offered'],after
 assert 'audit relay' in after['ledgerText'].lower(),after
 p.locator('.v14-intel-ledger summary').click()
 p.screenshot(path=str(OUT/'pwa12_72_closed_casefile_desktop.png'),animations='disabled')
 p.set_viewport_size({'width':412,'height':839});p.wait_for_timeout(100)
 mobile=p.evaluate('''()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,
  closed:document.querySelector('.v14-intel-ledger summary')?.textContent,
  notes:document.querySelector('.v14-intel-ledger-list')?.textContent})''')
 p.screenshot(path=str(OUT/'pwa12_72_closed_casefile_mobile.png'),animations='disabled')
 assert mobile['scroll']<=mobile['width']+1 and '1 CLOSED' in mobile['closed'],mobile
 assert not errors and not missing,(errors,missing)
 print('PASS PWA12.72 real Chromium core-success integration: completed follow-up -> idempotent world consequence and closed casefile; desktop/mobile screenshots; zero page errors, missing assets, mobile overflow',flush=True)
 print('AFTERMATH_STATE',before,after,mobile,flush=True)
 b.close()
