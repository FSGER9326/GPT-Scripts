from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text().replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
HTML=HTML.replace('<head>','<head><base href="http://cr.local/">',1)
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 page=b.new_page(viewport={'width':1280,'height':800})
 def route(r):
  rel=r.request.url.split('http://cr.local/',1)[-1].split('?',1)[0] or 'index.html';p=ROOT/rel
  r.fulfill(status=200,body=p.read_bytes(),content_type=mimetypes.guess_type(p.name)[0] or 'application/octet-stream') if p.is_file() else r.fulfill(status=404,body=b'')
 page.route('http://cr.local/**',route);page.set_content(HTML,wait_until='domcontentloaded');page.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
 result=page.evaluate("""()=>{
  startNewGame('Backdrop QA','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');
  showScreen('overworld-screen');activateDistrictV133('old_market',null);initOverworld();
  const world=currentDistrictV133(),W=640,H=360,dpr=Math.max(1,devicePixelRatio||1),cached=staticBackdropV193(world,W,H),again=staticBackdropV193(world,W,H);
  const legacy=document.createElement('canvas');legacy.width=Math.round(W*dpr);legacy.height=Math.round(H*dpr);const x=legacy.getContext('2d');x.setTransform(dpr,0,0,dpr,0,0);
  const bg=x.createRadialGradient(W*.5,H*.18,0,W*.5,H*.18,Math.max(W,H)*.9);bg.addColorStop(0,world.cfg.ground);bg.addColorStop(.64,world.cfg.bg);bg.addColorStop(1,'#010305');x.fillStyle=bg;x.fillRect(0,0,W,H);x.fillStyle=world.cfg.accent+'07';x.fillRect(0,0,W,H);
  x.save();for(let i=0;i<55;i++){const hx=randV133(world.id,i,'texturex')*W,hy=randV133(world.id,i,'texturey')*H,rr=8+randV133(world.id,i,'texturer')*34;x.fillStyle=i%3===0?'rgba(255,255,255,.010)':'rgba(0,0,0,.025)';x.beginPath();x.arc(hx,hy,rr,0,Math.PI*2);x.fill()}x.restore();
  const a=cached.getContext('2d').getImageData(0,0,cached.width,cached.height).data,b=x.getImageData(0,0,legacy.width,legacy.height).data;let diff=0;for(let i=0;i<a.length;i++)if(a[i]!==b[i]){diff++;if(diff>10)break}
  return{sameObject:cached===again,diff,width:cached.width,height:cached.height};
 }""")
 assert result['sameObject'],result
 assert result['diff']==0,result
 print('PASS PWA12.93 browser: cache hit reuses canvas; cached backdrop is pixel-identical to legacy draw',result)
 b.close()
