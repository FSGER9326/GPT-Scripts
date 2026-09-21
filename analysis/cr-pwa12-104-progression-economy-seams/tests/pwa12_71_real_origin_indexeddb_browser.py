"""Real-origin IndexedDB recovery acceptance test for Chrome Requiem.

Run in a browser environment where Chromium can navigate to a loopback origin:
  python tests/pwa12_71_real_origin_indexeddb_browser.py
This test deliberately requires IndexedDB, not the localStorage fallback. The
hosted test environment may block all browser navigations by administrator;
that environmental failure must not be reported as a product test failure/pass.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
    def log_message(self,*args):pass
    def do_GET(self):
        if self.path.split('?',1)[0] not in ('/','/index.html'):return super().do_GET()
        html=(ROOT/'index.html').read_text(encoding='utf-8').replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
        payload=html.encode('utf-8');self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload)
SERVER=ThreadingHTTPServer(('127.0.0.1',0),Handler)
thread=threading.Thread(target=SERVER.serve_forever,daemon=True);thread.start()
ORIGIN=f'http://127.0.0.1:{SERVER.server_port}/'
SNAP="""()=>({credits:Game.credits,day:Game.day,hour:Game.hour,rep:Game.rep,
 heat:structuredClone(Game.heat),history:Game.missionHistory.map(m=>m.id),
 story:!!Game.storyFlags?.indexedDbQa,crew:Game.roster[0]&&{name:Game.roster[0].name,level:Game.roster[0].level}})"""
IDB_INFO="""async()=>{
 const open=()=>new Promise((resolve,reject)=>{const r=indexedDB.open('chrome-requiem',2);r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error)});
 const db=await open();const tx=db.transaction(['saves','saveBackups'],'readonly');
 const fetch=name=>new Promise((resolve,reject)=>{const r=tx.objectStore(name).get('slot-2');r.onsuccess=()=>resolve(r.result||null);r.onerror=()=>reject(r.error)});
 const [p,b]=await Promise.all([fetch('saves'),fetch('saveBackups')]);db.close();
 return {primary:p?.envelope?.payload?.credits,backup:b?.envelope?.payload?.credits,primaryChecksum:p?.envelope?.checksum};
}"""
CORRUPT="""async()=>{
 const db=await new Promise((resolve,reject)=>{const r=indexedDB.open('chrome-requiem',2);r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error)});
 const tx=db.transaction('saves','readwrite');const store=tx.objectStore('saves');
 const rec=await new Promise((resolve,reject)=>{const r=store.get('slot-2');r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error)});
 if(!rec)throw Error('primary save missing');
 // No await between the put and transaction completion, avoiding IDB auto-close.
 rec.envelope.checksum='deliberately-corrupt-checksum';store.put(rec);
 await new Promise((resolve,reject)=>{tx.oncomplete=resolve;tx.onabort=()=>reject(tx.error);tx.onerror=()=>reject(tx.error)});
 db.close();return true;
}"""
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
  context=browser.new_context(viewport={'width':412,'height':915},is_mobile=True,has_touch=True)
  errors=[]
  def page():
   p=context.new_page();p.on('pageerror',lambda e:errors.append(str(e)))
   p.goto(ORIGIN,wait_until='domcontentloaded',timeout=25000)
   p.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
   assert p.evaluate('()=>ChromeRequiemV14Boot.backend')=='indexeddb','real IndexedDB backend not selected'
   return p
  a=page()
  snapA=a.evaluate("""async()=>{
    startNewGame('Native IndexedDB QA','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');
    Game.credits=43210;Game.day=9;Game.hour=18.75;Game.storyFlags.indexedDbQa=true;
    Game.missionHistory.push({id:'idb_campaign_m1',name:'Blacksite',success:true});
    ChromeRequiemV14Boot.bridge.save(2,true);await ChromeRequiemV14Boot.bridge.flush();
    return {credits:Game.credits,day:Game.day,hour:Game.hour};
  }""")
  snapB=a.evaluate("""async()=>{
    Game.credits=9731;Game.day=12;Game.hour=20;
    Game.missionHistory.push({id:'idb_campaign_m2',name:'Extraction',success:true});
    ChromeRequiemV14Boot.bridge.save(2,true);await ChromeRequiemV14Boot.bridge.flush();
    return {credits:Game.credits,day:Game.day,hour:Game.hour};
  }""")
  assert (snapA['credits'],snapB['credits'])==(43210,9731)
  info=a.evaluate(IDB_INFO);assert (info['primary'],info['backup'])==(9731,43210),info
  a.close()
  b=page();assert b.evaluate('()=>ChromeRequiemV14Boot.runtime.load(2)') is True
  loaded=b.evaluate(SNAP);assert loaded['credits']==9731 and loaded['day']==12 and loaded['history'][-1]=='idb_campaign_m2',loaded
  assert b.evaluate(CORRUPT)
  assert b.evaluate('()=>ChromeRequiemV14Boot.runtime.load(2)') is True
  recovered=b.evaluate(SNAP);assert recovered['credits']==43210 and recovered['day']==9 and recovered['history'][-1]=='idb_campaign_m1',recovered
  assert b.evaluate(IDB_INFO)['primary']==43210,'backup did not repair the native primary'
  b.close();c=page();assert c.evaluate('()=>ChromeRequiemV14Boot.runtime.load(2)') is True
  repaired=c.evaluate(SNAP);assert repaired['credits']==43210 and repaired['day']==9,repaired
  assert not errors,errors
  print('PASS native-origin IndexedDB: save A / save B / fresh-document load B / corrupt B checksum / restore A / fresh-document load repaired A; no page errors')
  context.close();browser.close()
finally:SERVER.shutdown();SERVER.server_close()
