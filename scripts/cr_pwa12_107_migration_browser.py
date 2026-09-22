#!/usr/bin/env python3
from pathlib import Path
import contextlib, http.server, json, socketserver, sys, threading, time
from playwright.sync_api import sync_playwright

ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
class ReuseTCP(socketserver.TCPServer): allow_reuse_address=True
handler=lambda *a,**kw: Quiet(*a,directory=str(ROOT),**kw)
server=ReuseTCP(('127.0.0.1',0),handler);port=server.server_address[1]
th=threading.Thread(target=server.serve_forever,daemon=True);th.start()
url=f'http://127.0.0.1:{port}/index.html'
try:
  with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    page=browser.new_page()
    page.goto(url,wait_until='domcontentloaded')
    page.wait_for_function("()=>window.ChromeRequiemV14Boot && typeof window.serializeGame==='function'",timeout=30000)
    legacy=page.evaluate("""()=>{const p=JSON.parse(window.serializeGame());p.version=4;p.playerName='Legacy PWA12.107';p.day=17;p.credits=8765;delete p.operationCheckpointV14;delete p.livingStreetsV14;return p}""")
    page.evaluate("""async p=>{localStorage.clear();localStorage.setItem('chrome_requiem_save_2',JSON.stringify(p));await new Promise(resolve=>{const r=indexedDB.deleteDatabase('chrome-requiem');r.onsuccess=r.onerror=r.onblocked=()=>resolve()})}""",legacy)
    page.reload(wait_until='domcontentloaded')
    page.wait_for_function("()=>window.ChromeRequiemV14Boot && typeof window.ChromeRequiemV14Boot.load==='function'",timeout=30000)
    ok=page.evaluate("()=>window.ChromeRequiemV14Boot.load(2)")
    assert ok is True, f'legacy slot failed to migrate/load: {ok!r}'
    state=page.evaluate("()=>({name:Game.playerName,day:Game.day,credits:Game.credits})")
    assert state['name']=='Legacy PWA12.107',state
    assert state['day']==17,state
    assert state['credits']==8765,state
    # Resolve the migrated envelope through whichever public bridge exposure this build provides.
    info=page.evaluate("""async()=>{const b=window.ChromeRequiemV14Boot;const bridge=b.bridge||b.saveBridge||b.legacyBridge;let e=null;if(bridge?.resolveEnvelope)e=await bridge.resolveEnvelope(2);return {schema:e?.schemaVersion??null,migratedFrom:e?.migratedFrom??null,backend:b.backendName||b.backend||null}}""")
    if info['schema'] is not None: assert info['schema']==14,info
    print('PWA12.107 legacy v4 migration browser PASS',json.dumps({'state':state,'envelope':info},sort_keys=True))
    browser.close()
finally:
  server.shutdown();server.server_close()
