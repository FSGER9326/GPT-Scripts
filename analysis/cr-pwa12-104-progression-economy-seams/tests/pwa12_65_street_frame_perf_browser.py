"""Integration test: one street collection resolution each per rendered frame."""
from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text().replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
SHIM="""<script>const __crls=(()=>{const s=new Map();return{getItem:k=>s.has(String(k))?s.get(String(k)):null,setItem:(k,v)=>s.set(String(k),String(v)),removeItem:k=>s.delete(String(k)),clear:()=>s.clear(),key:i=>[...s.keys()][i]??null,get length(){return s.size}}})();try{Object.defineProperty(window,'localStorage',{value:__crls,configurable:true})}catch(e){};try{Object.defineProperty(window,'sessionStorage',{value:__crls,configurable:true})}catch(e){}</script>"""
HTML=HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1)
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 page=b.new_page(viewport={'width':1280,'height':800})
 errors=[];missing=[]
 def route(r):
  rel=r.request.url.split('http://cr.local/',1)[-1].split('?',1)[0] or 'index.html';p=ROOT/rel
  if p.is_file():r.fulfill(status=200,body=p.read_bytes(),content_type=mimetypes.guess_type(p.name)[0] or 'application/octet-stream')
  else:missing.append(rel);r.fulfill(status=404,body=b'not found')
 page.route('http://cr.local/**',route)
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(HTML,wait_until='domcontentloaded')
 try:
  page.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
 except Exception:
  print('BOOT DEBUG:',{'errors':errors[:8],'missing':missing[:12],'boot':page.evaluate('()=>({boot:!!window.ChromeRequiemV14Boot,ready:window.ChromeRequiemV14Boot?.ready,overlay:document.getElementById("cr14-boot-overlay")?.textContent})')})
  raise
 result=page.evaluate("""()=>{
   startNewGame('Street Perf QA','Hacker','street');
   document.getElementById('story-modal')?.classList.remove('open');
   showScreen('overworld-screen');activateDistrictV133('old_market',null);initOverworld();
   const world=currentDistrictV133(), ctx=document.getElementById('overworld').getContext('2d');
   if(!world||!ctx||!window.CR14StreetPresentation)throw Error('Overworld unavailable');
   const originalActors=window.ensureStreetActorsV134, originalObjects=window.ensureInteractablesV134;
   let actorCalls=0,objectCalls=0;
   window.ensureStreetActorsV134=(...args)=>{actorCalls++;return originalActors(...args)};
   window.ensureInteractablesV134=(...args)=>{objectCalls++;return originalObjects(...args)};
   try {
     const before=[actorCalls,objectCalls];
     const first=CR14StreetPresentation.drawLivingStreetsV14(ctx,world,1280,800,Game.ovTile||28,null);
     const mid=[actorCalls,objectCalls];
     const second=CR14StreetPresentation.drawLivingStreetsV14(ctx,world,1280,800,Game.ovTile||28,null);
     const after=[actorCalls,objectCalls];
     const hud=document.getElementById('v14-street-proximity');
     return{first,second,before,mid,after,hudPresent:!!hud};
   } finally {
     window.ensureStreetActorsV134=originalActors;
     window.ensureInteractablesV134=originalObjects;
   }
 }""")
 assert result['mid']==[1,1] and result['after']==[2,2],result
 assert result['hudPresent'],result
 assert not errors,errors
 assert not missing,missing
 print('PASS street-frame browser',result)
 b.close()
