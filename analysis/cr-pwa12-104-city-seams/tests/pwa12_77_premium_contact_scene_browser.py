"""Browser screenshot and behavior regression for premium contact location scene."""
from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text(encoding='utf-8')
SHIM="""<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"""
HTML=HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1).replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
ROOT.joinpath('qa').mkdir(exist_ok=True)
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for label,viewport,id in [('desktop',{'width':1440,'height':900},'c1'),('mobile',{'width':390,'height':844},'c1'),('undergrid',{'width':1280,'height':800},'c22')]:
  ctx=browser.new_context(viewport=viewport,device_scale_factor=1);p=ctx.new_page();errors=[];missing=[]
  p.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   url=r.request.url
   if not url.startswith('http://cr.local/'):return r.abort()
   rel=url[len('http://cr.local/'):].split('?',1)[0] or 'index.html';fp=ROOT/rel
   if fp.is_file():r.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream')
   else:missing.append(rel);r.fulfill(status=404,body=b'NOT FOUND')
  p.route('http://cr.local/**',route)
  p.set_content(HTML,wait_until='domcontentloaded');p.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=35000)
  data=p.evaluate('''id=>{startNewGame('Premium QA','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');
    Game.contactRelations[id].known=true;
    // Ensure there is an accessible mission card and that its handler remains intact.
    renderContactDossierV13(id);showScreen('v13-contact-screen');
    const s=Game.day+'|'+Game.hour+'|'+Game.credits+'|'+Game.missionHistory.length;
    return {before:s,contact:id,available:Game.contacts.find(c=>c.id===id)?.missions.length||0};}''',id)
  # Verify the remote dossier does not misrepresent physical presence, then
  # visit the real contact location and redraw the unchanged gameplay panel.
  badge=p.evaluate("()=>document.querySelector('.v14-contact-scene-status')?.textContent")
  assert 'REMOTE DOSSIER' in badge,(label,badge)
  local=p.evaluate('''id=>{const c=Game.contacts.find(x=>x.id===id);if(Game.districtWorldsV133?.activeId!==c.sectorId)activateDistrictV133(c.sectorId,null);Game.ovPlayer={x:c.x,y:c.y};renderContactDossierV13(id);return {near:window.CR14MultiStageOperations.nearContact(id),badge:document.querySelector('.v14-contact-scene-status')?.textContent}}''',id)
  assert local['near'] and 'IN PERSON' in local['badge'],(label,local)
  p.wait_for_timeout(700)
  view=p.evaluate('''()=>{const screen=document.querySelector('#v13-contact-screen'),hero=screen.querySelector('.v14-contact-scene'),h=hero?.getBoundingClientRect(),portrait=hero?.querySelector('.v14-contact-scene-portrait'),shell=screen.querySelector('.v13-contact-shell');
    return {heroCount:screen.querySelectorAll(':scope > .v14-contact-scene').length,heroName:hero?.querySelector('h2')?.textContent,heroId:hero?.dataset.contactId,heroWidth:h?.width,heroHeight:h?.height,portraitLoaded:!!portrait?.naturalWidth,art:hero?.style.getPropertyValue('--v14-contact-backdrop'),status:hero?.querySelector('.v14-contact-scene-status')?.textContent,screenWidth:screen.scrollWidth,windowWidth:innerWidth,contractCount:screen.querySelectorAll('#v13-contracts [data-m]').length,screenScroll:shell.scrollHeight>0,gameState:Game.day+'|'+Game.hour+'|'+Game.credits+'|'+Game.missionHistory.length};}''')
  assert view['heroCount']==1 and view['heroId']==id and view['heroWidth']>300 and view['heroHeight']>=140,(label,view)
  assert view['portraitLoaded'] and view['art'].startswith('url('),(label,view)
  assert view['screenWidth']<=view['windowWidth']+1,(label,view)
  assert view['contractCount']==data['available'] and view['gameState']==data['before'],(label,view,data)
  assert not errors and not missing,(label,errors,missing)
  p.screenshot(path=str(ROOT/'qa'/f'pwa12-73-premium-contact-{label}.png'),full_page=True)
  if label=='desktop':
   transition=p.evaluate('''()=>{Game.contactRelations.c22.known=true;renderContactDossierV13('c22');const other=document.querySelector('.v14-contact-scene');renderContactDossierV13('c1');const back=document.querySelector('.v14-contact-scene');return {sameElement:other===back,count:document.querySelectorAll('#v13-contact-screen > .v14-contact-scene').length,id:back.dataset.contactId,art:back.style.getPropertyValue('--v14-contact-backdrop'),gameplay:Game.day+'|'+Game.hour+'|'+Game.credits+'|'+Game.missionHistory.length}}''')
   assert transition['sameElement'] and transition['count']==1 and transition['id']=='c1' and transition['gameplay']==data['before'],transition
   p.locator('#v13-contracts [data-m]').first.click()
   mission=p.evaluate('''()=>({screen:Game.screen,mission:Game.activeMission?.id||Game.pendingMission?.id||null})''')
   assert mission['mission'] or mission['screen']!='v13-contact-screen',mission
  print('PASS',label,view['heroName'],view['heroId'],'contracts',view['contractCount'],'portrait',view['portraitLoaded'],'horizontal-overflow',view['screenWidth']-view['windowWidth'],flush=True)
  ctx.close()
 browser.close()
print('PASS PWA12.73 premium contact scene desktop/mobile/undergrid',flush=True)
