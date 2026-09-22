"""Chromium integration for PWA12.104 narrative candidate: THE SECOND SIGNATURE."""
from pathlib import Path
import json, mimetypes, sys
from playwright.sync_api import sync_playwright

ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
QA=ROOT/'qa';QA.mkdir(parents=True,exist_ok=True)
HTML=(ROOT/'index.html').read_text(encoding='utf-8').replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
SHIM="""<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"""

def make_page(browser,viewport):
    ctx=browser.new_context(viewport=viewport)
    errors=[]
    def route(r):
        relative=r.request.url.split('http://cr.local/',1)[-1].split('?',1)[0] or 'index.html'
        path=ROOT/relative
        if path.is_file(): r.fulfill(status=200,body=path.read_bytes(),content_type=mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
        else: r.fulfill(status=404,body=b'not found')
    ctx.route('http://cr.local/**',route)
    page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content(HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1),wait_until='domcontentloaded')
    page.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
    return ctx,page,errors

def stage_mira(page,heat=10):
    return page.evaluate('''heat=>{
      startNewGame('Second Signature QA','AgentEX','street');
      document.getElementById('story-modal')?.classList.remove('open');
      const c=Game.contacts.find(x=>x.id==='c1');
      Game.activeMission=null;Game.heat.meridian=heat;
      Game.contactRelations.c1.known=true;Game.contactRelations.c1.trust=Math.max(32,Game.contactRelations.c1.trust||0);
      Game.cityLife.currentDistrict='old_market';Game.cityLife.currentLocation='loc_contact_c1';
      Game.ovPlayer={...Game.ovPlayer,x:c.x,y:c.y};
      renderContactDossierV13('c1');showScreen('v13-contact-screen');
      return {trust:Game.contactRelations.c1.trust,heat:Game.heat.meridian,credits:Game.credits,physical:CR14SecondSignatureV14.physicallyAtMira(),buttons:document.querySelectorAll('.v14-ss-choice').length,enabled:[...document.querySelectorAll('.v14-ss-choice')].filter(b=>!b.disabled).length};
    }''',heat)

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])

    # Desktop: full-settlement / ledger branch, plus durable save-load recovery.
    ctx,page,errors=make_page(browser,{'width':1440,'height':900})
    setup=stage_mira(page)
    assert setup['physical'] is True and setup['buttons']==2 and setup['enabled']==2,setup
    page.screenshot(path=str(QA/'pwa12-104-second-signature-desktop-choice.png'),full_page=True)
    page.locator('[data-ss-choice="enter_ledger"]').click()
    ledger=page.evaluate('''before=>({
      state:Game.storyFlags.secondSignatureV14,
      heat:Game.heat.meridian,trust:Game.contactRelations.c1.trust,credits:Game.credits,
      receipt:document.querySelector('.v14-second-signature.resolved h3')?.textContent||'',
      buttons:document.querySelectorAll('.v14-ss-choice').length,
      replay:resolveSecondSignatureV14('keep_nameless')
    })''',setup)
    s=ledger['state']
    assert s['outcome']=='ledger_witness' and s['choice']=='enter_ledger' and s['nextHook']=='second_signature_audit_echo',ledger
    assert s['payoutFraction']==1 and s['effects']['minutes']==10,ledger
    assert ledger['heat']==14 and ledger['trust']==setup['trust']+4 and ledger['credits']==setup['credits']+300,ledger
    assert ledger['replay'] is False and ledger['buttons']==0 and 'LEDGER' in ledger['receipt'],ledger
    page.screenshot(path=str(QA/'pwa12-104-second-signature-desktop-outcome.png'),full_page=True)

    saved=page.evaluate('''async()=>{
      const ok=saveGame(1,true);await ChromeRequiemV14Boot.bridge.flush();
      return {ok,state:JSON.parse(JSON.stringify(Game.storyFlags.secondSignatureV14)),heat:Game.heat.meridian,trust:Game.contactRelations.c1.trust,credits:Game.credits};
    }''')
    assert saved['ok'] is True,saved
    restored=page.evaluate('''async saved=>{
      Game.storyFlags.secondSignatureV14={version:1,stage:'corrupted'};Game.heat.meridian=99;Game.contactRelations.c1.trust=-50;Game.credits=1;
      const ok=await Promise.resolve(ChromeRequiemV14Boot.runtime.load(1));
      return {ok,state:Game.storyFlags.secondSignatureV14,heat:Game.heat.meridian,trust:Game.contactRelations.c1.trust,credits:Game.credits};
    }''',saved)
    assert restored['ok'] is True and restored['state']==saved['state'],(saved,restored)
    assert restored['heat']==saved['heat'] and restored['trust']==saved['trust'] and restored['credits']==saved['credits'],(saved,restored)
    assert not errors,errors
    ctx.close()

    # Mobile 390x844: off-book branch and layout/overflow assertions.
    ctx,page,errors=make_page(browser,{'width':390,'height':844})
    setup=stage_mira(page)
    page.screenshot(path=str(QA/'pwa12-104-second-signature-mobile-choice.png'),full_page=True)
    layout=page.evaluate('''()=>{const p=document.querySelector('.v14-second-signature'),bs=[...document.querySelectorAll('.v14-ss-choice')];return{viewport:innerWidth,panelRight:p.getBoundingClientRect().right,maxButtonRight:Math.max(...bs.map(b=>b.getBoundingClientRect().right)),minHeight:Math.min(...bs.map(b=>b.getBoundingClientRect().height)),cols:getComputedStyle(document.querySelector('.v14-ss-actions')).gridTemplateColumns}}''')
    assert layout['panelRight']<=layout['viewport']+1 and layout['maxButtonRight']<=layout['viewport']+1,layout
    assert layout['minHeight']>=48 and ' ' not in layout['cols'].strip(),layout
    page.locator('[data-ss-choice="keep_nameless"]').click()
    offbook=page.evaluate('''()=>({state:Game.storyFlags.secondSignatureV14,heat:Game.heat.meridian,trust:Game.contactRelations.c1.trust,credits:Game.credits,receipt:document.querySelector('.v14-second-signature.resolved h3')?.textContent||''})''')
    s=offbook['state']
    assert s['outcome']=='offbook_settlement' and s['choice']=='keep_nameless' and s['nextHook']=='second_signature_claim_market',offbook
    assert abs(s['payoutFraction']-.6)<1e-9 and s['effects']['minutes']==8,offbook
    assert offbook['heat']==8 and offbook['trust']==setup['trust']+2 and offbook['credits']==setup['credits']+300,offbook
    assert 'NAMELESS' in offbook['receipt'],offbook
    page.screenshot(path=str(QA/'pwa12-104-second-signature-mobile-outcome.png'),full_page=True)
    assert not errors,errors
    ctx.close()

    # Remote and active-mission resolution must remain locked.
    ctx,page,errors=make_page(browser,{'width':390,'height':844})
    setup=stage_mira(page)
    locked=page.evaluate('''()=>{
      Game.ovPlayer={...Game.ovPlayer,x:0,y:0};renderContactDossierV13('c1');
      const remote={physical:CR14SecondSignatureV14.physicallyAtMira(),disabled:[...document.querySelectorAll('.v14-ss-choice')].every(b=>b.disabled),resolve:resolveSecondSignatureV14('enter_ledger')};
      const c=Game.contacts.find(x=>x.id==='c1');Game.ovPlayer={...Game.ovPlayer,x:c.x,y:c.y};Game.activeMission={id:'qa_active'};renderContactDossierV13('c1');
      const mission={physical:CR14SecondSignatureV14.physicallyAtMira(),disabled:[...document.querySelectorAll('.v14-ss-choice')].every(b=>b.disabled),resolve:resolveSecondSignatureV14('keep_nameless')};
      return {remote,mission,state:Game.storyFlags.secondSignatureV14};
    }''')
    assert locked['remote']=={'physical':False,'disabled':True,'resolve':False},locked
    assert locked['mission']=={'physical':False,'disabled':True,'resolve':False},locked
    assert 'outcome' not in locked['state'],locked
    assert not errors,errors
    ctx.close();browser.close()

print('PASS Second Signature browser: desktop ledger branch, 390x844 off-book branch, physical/mission locks, exclusivity, real save-corrupt-reload restoration, responsive controls, screenshots, no page errors')
