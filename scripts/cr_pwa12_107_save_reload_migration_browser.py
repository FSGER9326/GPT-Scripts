from pathlib import Path
import json, mimetypes, sys
from playwright.sync_api import sync_playwright

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
BASE_HTML=(ROOT/'index.html').read_text(encoding='utf-8')

def storage_shim(seed=None):
    pairs=[]
    for k,v in (seed or {}).items():
        pairs.append([str(k),str(v)])
    literal=json.dumps(pairs,separators=(',',':'))
    return f"<script>const __s=new Map({literal});const __ls={{getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){{return __s.size}}}};Object.defineProperty(window,'localStorage',{{value:__ls,configurable:true}});Object.defineProperty(window,'sessionStorage',{{value:__ls,configurable:true}});</script>"

def html(seed=None):
    return BASE_HTML.replace('<head>','<head><base href="http://cr.local/">'+storage_shim(seed),1).replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')

def attach(page, errors, missing):
    def route(r):
        rel=r.request.url.split('http://cr.local/',1)[-1].split('?',1)[0] or 'index.html'
        fp=ROOT/rel
        if fp.is_file():
            r.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream')
        else:
            missing.append(rel);r.fulfill(status=404,body=b'x')
    page.route('http://cr.local/**',route)
    page.on('pageerror',lambda e: errors.append(str(e)))

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page();errors=[];missing=[];attach(page,errors,missing)
    page.set_content(html(),wait_until='domcontentloaded')
    page.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
    backend=page.evaluate('()=>ChromeRequiemV14Boot.backend')

    page.evaluate("""()=>{
      startNewGame('Txn QA','Hacker','street');
      document.getElementById('story-modal')?.classList.remove('open');
      Game.credits=43210;Game.day=9;Game.hour=18.75;
      Game.rep={...(Game.rep||{}),meridian:37,wraiths:-8};
      Game.heat={...(Game.heat||{}),meridian:17,wraiths:4};
      Game.missionHistory=[{id:'qa_done',name:'Ghost Wire',success:true,day:7}];
      Game.storyFlags={...(Game.storyFlags||{}),pwa12107:true};
      Game.ovPlayer={x:11,y:7};
      const u=Game.roster[0];u.hp=Math.max(1,u.maxHp-7);u.xp=(u.xp||0)+345;u.inventory={...(u.inventory||{}),medkit:2};
      if(Game.cityLife)Game.cityLife.currentDistrict='steelworks';
      saveGame(1,true);
    }""")
    page.evaluate('()=>ChromeRequiemV14Boot.bridge.flush()')
    before=page.evaluate("()=>{const d=JSON.parse(serializeGame());delete d.savedAt;return d}")

    # Normal new-game save -> destroy live fields -> reload -> continue.
    page.evaluate("()=>{Game.credits=1;Game.day=1;Game.hour=0;Game.rep={};Game.roster=[];Game.missionHistory=[];Game.storyFlags={};Game.ovPlayer={x:0,y:0}}")
    assert page.evaluate('()=>ChromeRequiemV14Boot.runtime.load(1)') is True
    restored=page.evaluate("()=>({name:Game.playerName||Game.name,credits:Game.credits,day:Game.day,hour:Game.hour,rep:Game.rep,history:Game.missionHistory,flag:Game.storyFlags?.pwa12107,roster:Game.roster.length,loadBusy:ChromeRequiemV14Boot.bridge.loadInProgress})")
    assert restored['credits']==43210 and restored['day']==9 and restored['flag'] is True and restored['roster']>0,restored
    assert restored['rep'].get('meridian')==37,restored
    assert restored['loadBusy'] is False

    # Save then immediately Load without an explicit flush: the inherited pending-write
    # barrier must still make the just-requested snapshot win.
    assert page.evaluate("()=>{Game.credits=55555;return saveGame(1,true)}") is True
    page.evaluate('()=>{Game.credits=2}')
    assert page.evaluate('()=>ChromeRequiemV14Boot.runtime.load(1)') is True
    assert page.evaluate('()=>Game.credits')==55555
    page.evaluate('()=>advanceTime(15)')
    assert page.evaluate('()=>Game.credits')==55555
    assert page.evaluate('()=>ChromeRequiemV14Boot.bridge.loadInProgress') is False

    migrated_seed=before.copy();migrated_seed['version']='4';migrated_seed['credits']=24680;migrated_seed['day']=6
    legacy_raw=json.dumps(migrated_seed,separators=(',',':'))

    # Separate boot with only a legacy v4-style key present. This exercises the real boot
    # migration path into schema 14 before loading slot 2 through the transaction bridge.
    page2=browser.new_page();errors2=[];missing2=[];attach(page2,errors2,missing2)
    page2.set_content(html({'chrome_requiem_save_2':legacy_raw}),wait_until='domcontentloaded')
    page2.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
    migration=page2.evaluate("""async()=>{
      const m=ChromeRequiemV14Boot.migrations[2];
      const e=await ChromeRequiemV14Boot.bridge.resolveEnvelope(2);
      const ok=await ChromeRequiemV14Boot.runtime.load(2);
      return{status:m?.status,sourceKey:m?.sourceKey||null,schema:e?.schemaVersion,migratedFrom:e?.migratedFrom,slot:e?.slot,ok,credits:Game.credits,day:Game.day,busy:ChromeRequiemV14Boot.bridge.loadInProgress};
    }""")
    assert migration['status']=='migrated',migration
    assert migration['schema']==14 and migration['slot']==2 and migration['ok'] is True,migration
    assert migration['credits']==24680 and migration['day']==6 and migration['busy'] is False,migration

    assert not errors,(errors,missing[:10])
    assert not errors2,(errors2,missing2[:10])
    print('PASS PWA12.107 Chromium save/reload/continue + immediate save/load + legacy migration',{'backend':backend,'restored':restored,'migration':migration},flush=True)
    browser.close()
