from pathlib import Path
import mimetypes,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];district=sys.argv[1] if len(sys.argv)>1 else 'old_market';out=Path(sys.argv[2]) if len(sys.argv)>2 else ROOT/'qa'/'overworld-current.png'
width=int(sys.argv[3]) if len(sys.argv)>3 else 1280;height=int(sys.argv[4]) if len(sys.argv)>4 else 800
html=(ROOT/'index.html').read_text();html=html.replace('<head>','<head><base href="http://cr.local/"><script>const __crls=(()=>{const s=new Map();return{getItem:k=>s.has(String(k))?s.get(String(k)):null,setItem:(k,v)=>s.set(String(k),String(v)),removeItem:k=>s.delete(String(k)),clear:()=>s.clear(),key:i=>[...s.keys()][i]??null,get length(){return s.size}}})();try{Object.defineProperty(window,\'localStorage\',{value:__crls,configurable:true})}catch(e){}</script>',1).replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage']);page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 def route(r):
  path=ROOT/r.request.url[len('http://cr.local/'):].split('?',1)[0]
  if path.is_file():r.fulfill(status=200,body=path.read_bytes(),content_type=mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
  else:r.fulfill(status=404,body=b'no',content_type='text/plain')
 page.route('http://cr.local/**',route);page.set_content(html,wait_until='domcontentloaded',timeout=30000);page.wait_for_timeout(1000)
 page.evaluate('''district=>{startNewGame('Vex','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');showScreen('overworld-screen');activateDistrictV133(district,null);initOverworld();Game.ovCamera.follow=false;let w=currentDistrictV133(),n=w.neighborhoods[0],r=document.querySelector('#overworld-screen .wrap').getBoundingClientRect();Game.ovCamera.x=Math.max(0,n.x-r.width/Game.ovTile/2);Game.ovCamera.y=Math.max(0,n.y-r.height/Game.ovTile/2);Game.ovCamera.tx=Game.ovCamera.x;Game.ovCamera.ty=Game.ovCamera.y;Game.ovStaticDirty=true;renderDistrictStaticV133()}''',district)
 page.wait_for_timeout(1600);page.evaluate('Game.ovStaticDirty=true;renderDistrictStaticV133()');page.wait_for_timeout(300)
 out.parent.mkdir(parents=True,exist_ok=True);page.screenshot(path=str(out));print({'screenshot':str(out),'district':district,'errors':errors,'state':page.evaluate('({tile:Game.ovTile,world:currentDistrictV133()?.id,buildings:currentDistrictV133()?.buildings?.length,identity:CR14UrbanIdentity.state})')});browser.close()
