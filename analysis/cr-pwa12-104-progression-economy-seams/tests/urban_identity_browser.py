from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'index.html').read_text(encoding='utf-8')
shim="""<script>const __crls=(()=>{const s=new Map();return{getItem:k=>s.has(String(k))?s.get(String(k)):null,setItem:(k,v)=>s.set(String(k),String(v)),removeItem:k=>s.delete(String(k)),clear:()=>s.clear(),key:i=>[...s.keys()][i]??null,get length(){return s.size}}})();try{Object.defineProperty(window,'localStorage',{value:__crls,configurable:true})}catch(e){};window.__urbanDraws=[];const __origDI=CanvasRenderingContext2D.prototype.drawImage;CanvasRenderingContext2D.prototype.drawImage=function(img,...args){const s=img?.currentSrc||img?.src||'';if(s&&/urban-identity|street\/vehicles/.test(s))window.__urbanDraws.push(s);return __origDI.call(this,img,...args)};</script>"""
html=html.replace('<head>','<head><base href="http://cr.local/">'+shim,1)
html=html.replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    page=browser.new_page(viewport={'width':1280,'height':800})
    missing=[];errors=[]
    def handler(route):
        url=route.request.url
        if not url.startswith('http://cr.local/'): return route.abort()
        rel=url[len('http://cr.local/'):].split('?',1)[0]
        fp=ROOT/rel
        if fp.exists() and fp.is_file(): route.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream')
        else: missing.append(rel);route.fulfill(status=404,body=b'not found',content_type='text/plain')
    page.route('http://cr.local/**',handler)
    page.on('pageerror',lambda e: errors.append(str(e)))
    page.set_content(html,wait_until='domcontentloaded',timeout=30000)
    page.wait_for_timeout(1300)
    page.evaluate("""()=>{startNewGame('Vex','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');showScreen('overworld-screen');activateDistrictV133('old_market',null);initOverworld();Game.ovStaticDirty=true;renderDistrictStaticV133()}""")
    page.wait_for_timeout(850)
    page.evaluate("Game.ovStaticDirty=true;renderDistrictStaticV133()")
    market=page.evaluate("""()=>({state:{...CR14UrbanIdentity.state},draws:[...new Set(window.__urbanDraws.filter(x=>x.includes('old_market')||x.includes('/street/vehicles/')))]})""")
    assert market['state']['storefronts']>0,market
    assert market['state']['entrances']>0,market
    assert market['state']['furniture']>0,market
    assert market['state']['parkedVehicles']>0,market
    assert any(('storefronts/old_market.webp' in x) or ('storefront-variants/old_market/' in x) for x in market['draws']),market
    assert any(('entrances/old_market.webp' in x) or ('entrance-variants/old_market/' in x) for x in market['draws']),market
    assert any('furniture/old_market.webp' in x for x in market['draws']),market
    page.evaluate("""()=>{activateDistrictV133('civic_circuit',null);initOverworld();const w=currentDistrictV133();const links=V133_TRANSIT_LINKS;const tr=w.transit.find(t=>(t.linkIds||[]).some(id=>links.find(l=>l.id===id)?.type==='security'));if(!tr)throw new Error('no security transit');Game.ovCamera.follow=false;const r=document.querySelector('#overworld-screen .wrap').getBoundingClientRect();Game.ovCamera.x=Math.max(0,tr.x-r.width/Game.ovTile/2);Game.ovCamera.y=Math.max(0,tr.y-r.height/Game.ovTile/2);Game.ovCamera.tx=Game.ovCamera.x;Game.ovCamera.ty=Game.ovCamera.y;window.__urbanDraws=[];Game.ovStaticDirty=true;renderDistrictStaticV133()}""")
    page.wait_for_timeout(500)
    page.evaluate("Game.ovStaticDirty=true;renderDistrictStaticV133()")
    civic=page.evaluate("""()=>({state:{...CR14UrbanIdentity.state},draws:[...new Set(window.__urbanDraws)]})""")
    assert civic['state']['checkpoints']>0,civic
    assert any('checkpoints/meridian.webp' in x for x in civic['draws']),civic
    assert not errors,errors
    assert not missing,missing
    print('URBAN IDENTITY BROWSER PASS',{'market':market,'civic':civic})
    browser.close()
