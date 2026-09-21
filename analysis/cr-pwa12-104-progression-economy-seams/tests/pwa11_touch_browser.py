from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'index.html').read_text(encoding='utf-8')
shim="""<script>const __crls=(()=>{const s=new Map();return{getItem:k=>s.has(String(k))?s.get(String(k)):null,setItem:(k,v)=>s.set(String(k),String(v)),removeItem:k=>s.delete(String(k)),clear:()=>s.clear(),key:i=>[...s.keys()][i]??null,get length(){return s.size}}})();try{Object.defineProperty(window,'localStorage',{value:__crls,configurable:true})}catch(e){};try{Object.defineProperty(window,'sessionStorage',{value:__crls,configurable:true})}catch(e){}</script>"""
html=html.replace('<head>','<head><base href="http://cr.local/">'+shim,1).replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    device=dict(pw.devices['Pixel 7']); device.pop('default_browser_type',None)
    context=browser.new_context(**device)
    page=context.new_page();missing=[];errors=[]
    def handler(route):
        u=route.request.url
        if not u.startswith('http://cr.local/'):return route.abort()
        rel=u[len('http://cr.local/'):].split('?',1)[0] or 'index.html';fp=ROOT/rel
        if fp.exists() and fp.is_file():route.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream')
        else:missing.append(rel);route.fulfill(status=404,body=b'not found',content_type='text/plain')
    page.route('http://cr.local/**',handler);page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content(html,wait_until='domcontentloaded');page.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=15000)
    page.evaluate("""()=>{startNewGame('Vex','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');showScreen('overworld-screen');activateDistrictV133('old_market',null);initOverworld();Game.ovStaticDirty=true;}""")
    page.wait_for_timeout(220)
    state=page.evaluate("""()=>{const b=document.getElementById('ov-wait-btn'),r=b?.getBoundingClientRect();return{touch:navigator.maxTouchPoints,overflow:Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)-innerWidth,wait:!!b&&getComputedStyle(b).display!=='none',rect:r?{x:r.x,y:r.y,w:r.width,h:r.height}:null,day:Game.day,hour:Game.hour,screenH:document.getElementById('overworld-screen').getBoundingClientRect().height,canvasH:document.getElementById('overworld').getBoundingClientRect().height}}""")
    assert state['touch']>0,state
    assert state['overflow']<=1,state
    assert state['wait'] and state['rect']['h']>=44,state
    assert state['screenH']>=device['viewport']['height']-2 and state['canvasH']>220,state
    before=page.evaluate('()=>({day:Game.day,hour:Game.hour})')
    r=state['rect'];page.touchscreen.tap(r['x']+r['w']/2,r['y']+r['h']/2);page.wait_for_timeout(120)
    after=page.evaluate('()=>({day:Game.day,hour:Game.hour})')
    delta=(after['day']-before['day'])*24+(after['hour']-before['hour'])
    assert abs(delta-.25)<1e-7,(before,after,delta)
    assert not errors,errors
    assert not missing,missing
    print('PWA11 TOUCH BROWSER PASS',{'device':device['viewport'],'state':state,'after':after})
    browser.close()
