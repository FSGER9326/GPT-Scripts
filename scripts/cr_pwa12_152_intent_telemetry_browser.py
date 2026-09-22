#!/usr/bin/env python3
from pathlib import Path
import contextlib, http.server, json, socket, threading, sys
from playwright.sync_api import sync_playwright

ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
QA=ROOT/'qa'; QA.mkdir(exist_ok=True)

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

def serve():
    handler=lambda *a,**k: Quiet(*a,directory=str(ROOT),**k)
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    return server

server=serve(); url=f'http://127.0.0.1:{server.server_port}/index.html'
errors=[]
try:
  with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=3,is_mobile=True,has_touch=True)
    page.on('pageerror',lambda e: errors.append('pageerror:'+str(e)))
    page.goto(url,wait_until='domcontentloaded',timeout=45000)
    page.wait_for_timeout(900)
    version=page.evaluate('window.CR14_BUILD_VERSION || null')
    if not version or '12.152' not in version: raise AssertionError(f'wrong version: {version}')
    result=page.evaluate('''() => {
      const combat=document.querySelector('#combat'), board=document.querySelector('#combat #board');
      if(!combat||!board) return {error:'missing combat/board'};
      combat.style.display='block';combat.style.visibility='visible';combat.style.opacity='1';
      board.style.display='grid';board.style.gridTemplateColumns='repeat(3,72px)';board.style.gap='8px';board.style.alignContent='center';board.style.justifyContent='center';board.style.minHeight='300px';
      board.querySelectorAll('.pwa152-fixture').forEach(n=>n.remove());
      const intents=['CONTACT','SCAN','PIN','FIN','SWEEP','BASE','WATCH','SUP','GO'];
      const expected={CONTACT:'CTC',SCAN:'SCN',PIN:'PIN',FIN:'FIN',SWEEP:'SWP',BASE:'BAS',WATCH:'WCH',SUP:'SUP',GO:'GO'};
      const rows=[];
      for(const intent of intents){
        const u=document.createElement('div');u.className='unit pwa152-fixture';u.style.position='relative';u.style.width='56px';u.style.height='56px';u.style.border='1px solid rgba(130,200,220,.45)';u.style.background='rgba(8,16,22,.92)';u.style.display='flex';u.style.alignItems='center';u.style.justifyContent='center';u.style.color='#d8eef3';u.style.font='600 8px system-ui';u.textContent=intent;
        const cue=document.createElement('div');cue.className='v133-contact-cue '+(intent==='SCAN'?'scan':intent==='PIN'?'pin':intent==='FIN'?'fin':(intent==='SWEEP'||intent==='BASE')?'sweep':intent==='WATCH'?'watch':intent==='SUP'?'sup':intent==='GO'?'go':'');cue.dataset.intent=intent;cue.textContent=intent;u.appendChild(cue);board.appendChild(u);
        const cs=getComputedStyle(cue), ps=getComputedStyle(cue,'::after');const r=cue.getBoundingClientRect();
        rows.push({intent,w:r.width,h:r.height,pointer:cs.pointerEvents,pseudo:(ps.content||'').replaceAll('\\"','').replaceAll('"',''),expected:expected[intent]});
      }
      return {rows,overflow:document.documentElement.scrollWidth-window.innerWidth,innerWidth:window.innerWidth};
    }''')
    if result.get('error'): raise AssertionError(result['error'])
    for row in result['rows']:
      if row['w']>26 or row['h']>12: raise AssertionError('cue bounds '+json.dumps(row))
      if row['pointer']!='none': raise AssertionError('pointer interception '+json.dumps(row))
      if row['pseudo']!=row['expected']: raise AssertionError('wrong compact code '+json.dumps(row))
    if result['overflow']>0: raise AssertionError('horizontal overflow '+str(result['overflow']))
    shot=QA/'pwa12-152-intent-telemetry-mobile.png';page.screenshot(path=str(shot),full_page=True)
    page.set_viewport_size({'width':1280,'height':800});page.wait_for_timeout(200)
    desktop=page.evaluate('''() => {const cue=document.querySelector('.pwa152-fixture .v133-contact-cue');const ps=getComputedStyle(cue,'::after');return {text:cue.textContent,pseudo:ps.content,width:cue.getBoundingClientRect().width}}''')
    if desktop['text']!='CONTACT': raise AssertionError('desktop semantic text lost: '+json.dumps(desktop))
    print(json.dumps({'version':version,'mobile':result,'desktop':desktop,'consoleErrors':errors,'screenshot':str(shot)},indent=2))
    browser.close()
finally:
  server.shutdown();server.server_close()
print('PWA12.152 Chromium combat-intent telemetry acceptance PASS')
