"""Fast browser integration for post-exfil intel contacts (does not simulate a whole campaign)."""
from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text().replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
# Isolated set_content documents have an opaque origin; provide the same stable
# fallback storage shim as the existing tested operation-checkpoint browser suite.
SHIM="""<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"""
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    ctx=browser.new_context(viewport={'width':420,'height':830})
    errors=[]
    def route(r):
        relative=r.request.url.split('http://cr.local/',1)[-1].split('?',1)[0] or 'index.html'
        path=ROOT/relative
        if path.is_file():r.fulfill(status=200,body=path.read_bytes(),content_type=mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
        else:r.fulfill(status=404,body=b'not found')
    ctx.route('http://cr.local/**',route)
    page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content(HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1),wait_until='domcontentloaded')
    page.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
    setup=page.evaluate('''()=>{
      startNewGame('Intel Contact QA','Hacker','street');
      const c=Game.contacts[0]; Game.ovPlayer={x:c.x,y:c.y}; Game.activeMission=null;
      Game.heat[c.faction]=10; const initial=Game.contactRelations[c.id].trust;
      Game.missionHistory.push({id:'intel_qa_alpha',name:'The Broken Ledger',contact:c.id,operationIntelRecoveredV14:{bonus:180,route:'security'}});
      Game.missionHistory.push({id:'intel_qa_beta',name:'The Ghost Archive',contact:c.id,operationIntelRecoveredV14:{bonus:125,route:'security'}});
      renderContactDossierV13(c.id);
      document.getElementById('story-modal')?.classList.remove('open');
      showScreen('v13-contact-screen');
      return{id:c.id,faction:c.faction,initial,leads:document.querySelectorAll('.v14-intel-lead').length,buttons:document.querySelectorAll('.v14-intel-lead-actions button').length};
    }''')
    assert setup['leads']==2 and setup['buttons']==4,setup
    page.screenshot(path=str(ROOT/'qa/pwa12-68-intel-handoff-mobile.png'),full_page=True)
    page.locator('.v14-intel-lead-actions button').first.click()
    first=page.evaluate('''id=>({trust:Game.contactRelations[id].trust,heat:Game.heat[Game.contacts.find(c=>c.id===id).faction],leads:CR14MultiStageOperations.pendingLeads(id).length,done:Game.journal.filter(j=>j.id?.startsWith('intel_debrief_')).length})''',setup['id'])
    assert first=={'trust':setup['initial']+8,'heat':16,'leads':1,'done':1},first
    page.locator('.v14-intel-lead-actions button').last.click()
    second=page.evaluate('''id=>({trust:Game.contactRelations[id].trust,heat:Game.heat[Game.contacts.find(c=>c.id===id).faction],leads:CR14MultiStageOperations.pendingLeads(id).length,done:Game.journal.filter(j=>j.id?.startsWith('intel_debrief_')).length})''',setup['id'])
    assert second=={'trust':setup['initial']+8,'heat':8,'leads':0,'done':2},second
    assert not page.locator('.v14-intel-leads').count()
    # Physically distant players can see an intel lead but cannot resolve it.
    far=page.evaluate('''id=>{Game.missionHistory.push({id:'intel_qa_gamma',name:'Distant Ledger',contact:id,operationIntelRecoveredV14:{bonus:140}});Game.ovPlayer={x:0,y:0};renderContactDossierV13(id);return{near:CR14MultiStageOperations.nearContact(id),buttons:document.querySelectorAll('.v14-intel-lead-actions button').length}}''',setup['id'])
    # c1 is in the lower city (x7,y11); remote interaction must remain locked.
    assert far=={'near':False,'buttons':0},far
    assert not errors,errors
    print('PASS PWA12.67 browser: physically located handoff, two distinct exclusive outcomes, one-time markers, remote lock, mobile controls, no page errors')
    ctx.close();browser.close()
