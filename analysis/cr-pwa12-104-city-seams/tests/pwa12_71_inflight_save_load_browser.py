"""Browser regression: a new save slot must load correctly in the same event turn.

Uses the localStorage backend because this environment blocks browser navigation to a
non-opaque origin. The companion Node regression also exercises delayed IndexedDB-
style writes and backup restoration, without misrepresenting them as native-IDB QA.
"""
from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text(encoding='utf-8').replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
SHIM="""<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"""
HTML=HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1)
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 context=browser.new_context(viewport={'width':412,'height':915},device_scale_factor=1,is_mobile=True,has_touch=True)
 errors=[]
 def route(r):
  rel=r.request.url.split('http://cr.local/',1)[-1].split('?',1)[0] or 'index.html'
  file=ROOT/rel
  r.fulfill(status=200,body=file.read_bytes(),content_type=mimetypes.guess_type(file.name)[0] or 'application/octet-stream') if file.is_file() else r.fulfill(status=404,body=b'not found')
 context.route('http://cr.local/**',route)
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(HTML,wait_until='domcontentloaded');page.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
 result=page.evaluate("""async()=>{
   startNewGame('Rapid Checkpoint QA','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');
   const b=ChromeRequiemV14Boot.bridge;
   const backend=b.backendName;
   Game.credits=43210;Game.day=9;Game.hour=18.75;
   Game.missionHistory.push({id:'rapid_qa',name:'Blacksite Recovery',success:true});
   const first=b.save(2,true);
   Game.credits=7;Game.day=1;
   const loaded=await b.load(2);
   const after={credits:Game.credits,day:Game.day,mission:Game.missionHistory.at(-1)?.id};
   const envelope=await b.resolveEnvelope(2);
   return {backend,first,loaded,after,payload:envelope?.payload&&{credits:envelope.payload.credits,day:envelope.payload.day},saveVersion:envelope?.schemaVersion};
 }""")
 assert result['first'] is True,result
 assert result['loaded'] is True,result
 assert result['after']=={'credits':43210,'day':9,'mission':'rapid_qa'},result
 assert result['payload']=={'credits':43210,'day':9} and result['saveVersion']==14,result
 assert not errors,errors
 page.screenshot(path=str(ROOT/'qa/pwa12-71-rapid-save-load-mobile.png'))
 print('PASS PWA12.71 real Chromium rapid save->load same turn: expected persisted campaign snapshot restored, schema 14, no page errors; backend='+result['backend'])
 browser.close()
