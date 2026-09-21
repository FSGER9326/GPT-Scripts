"""Browser regression for static physical lighting on the canonical tactical renderer.

Exercises every environment on mobile/desktop; validates visual-only layering,
existing movement/target semantics, asset decoding, and input affordance.
"""
from pathlib import Path
import mimetypes
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa'/'pwa12_79'; OUT.mkdir(parents=True,exist_ok=True)
THEMES={'old_market':'market_street','dock_nine':'dock','forge_belt':'warehouse',
'undergrid':'server_room','neon_row':'club','glass_heights':'office_entry',
'civic_circuit':'parking_garage','ash_blocks':'tenement_hall'}
for theme in THEMES.values():
    path=ROOT/'assets/art/cinematic-fields'/f'{theme}.webp'
    assert path.is_file(),path
    with Image.open(path) as image:
        assert image.size==(768,768) and image.mode in ('RGBA','RGB'),(path,image.size,image.mode)
HTML=(ROOT/'index.html').read_text()
SHIM="""<script>const m=new Map(),s={getItem:k=>m.get(String(k))??null,setItem:(k,v)=>m.set(String(k),String(v)),removeItem:k=>m.delete(String(k)),clear:()=>m.clear(),key:i=>[...m.keys()][i]??null,get length(){return m.size}};Object.defineProperty(window,'localStorage',{value:s,configurable:true});Object.defineProperty(window,'sessionStorage',{value:s,configurable:true});</script>"""
HTML=HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1).replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    for label,viewport in [('desktop',{'width':1440,'height':900}),('mobile',{'width':390,'height':844})]:
        context=browser.new_context(viewport=viewport,device_scale_factor=1)
        page=context.new_page();errors=[];missing=[]
        page.on('pageerror',lambda e: errors.append(str(e)))
        def route(r):
            u=r.request.url
            if not u.startswith('http://cr.local/'):return r.abort()
            rel=u[len('http://cr.local/'):].split('?',1)[0] or 'index.html'
            target=ROOT/rel
            if not target.is_file():
                missing.append(rel);return r.fulfill(status=404,body=b'not found')
            return r.fulfill(status=200,body=target.read_bytes(),content_type=mimetypes.guess_type(target.name)[0] or 'application/octet-stream')
        page.route('http://cr.local/**',route)
        page.set_content(HTML,wait_until='domcontentloaded')
        page.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=35000)
        page.evaluate("()=>{startNewGame('Lighting QA','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');showScreen('combat');document.getElementById('banner')?.classList.remove('show')}")
        previous_element=None
        for sector,theme in THEMES.items():
            page.evaluate("""sec=>{const m={id:'qa79_'+sec,name:sec,type:'raid',objective:'raid',sectorId:sec,targetFaction:'spine',enemies:['Guard','Enforcer'],diff:2,reward:1,xp:1,factionRepGain:0,factionRepLoss:{}};Game.activeMission=m;initCombat(m)}""",sector)
            page.wait_for_function("theme=>document.getElementById('board')?.dataset.v14Environment===theme",arg=theme,timeout=7000)
            page.wait_for_timeout(180)
            check=page.evaluate("""async()=>{const b=document.getElementById('board'),l=b.querySelectorAll(':scope>.cr79-lightfield'),a=l[0],s=a?getComputedStyle(a):null;
              const img=a?.style.backgroundImage||'';const matched=img.match(/url\\(\"?([^\"\\)]+)\"?\\)/);let decoded=false;
              if(matched){const image=new Image();image.src=matched[1];try{await image.decode();decoded=image.naturalWidth===768&&image.naturalHeight===768}catch{}}
              return {theme:b.dataset.v14Environment,n:l.length,src:img,decoded,light:s&&{pointer:s.pointerEvents,z:s.zIndex,opacity:parseFloat(s.opacity)},gridZ:getComputedStyle(document.getElementById('grid')).zIndex,unitZ:getComputedStyle(document.getElementById('units')).zIndex,board:b.getBoundingClientRect().width,scroll:document.documentElement.scrollWidth,width:innerWidth,buttons:[...document.querySelectorAll('#actions>button')].map(e=>e.getBoundingClientRect().height),gridSignature:Game.grid.map(c=>[c.x,c.y,!!c.obstacle,!!c.cover,!!c.door]).join('|'),unitCount:Game.combatUnits?.length||document.querySelectorAll('#units>.unit').length,elementSame:window.__qaLight===a}}""")
            assert check['theme']==theme and check['n']==1 and theme in check['src'] and check['decoded'],(label,sector,check)
            assert check['light']['pointer']=='none' and int(check['gridZ'])<int(check['light']['z'])<int(check['unitZ']),(label,sector,check)
            assert check['board']>=250 and check['scroll']<=check['width']+1 and len(check['buttons'])>=7 and all(h>=40 for h in check['buttons']),(label,sector,check)
            assert check['unitCount']>=2,(label,sector,check)
            if previous_element is not None:assert check['elementSame'],(label,sector,'duplicate node/replacement')
            page.evaluate("window.__qaLight=document.getElementById('board').querySelector(':scope>.cr79-lightfield')")
            previous_element=theme
            # Applying the environment repeatedly must not affect combat semantics or create more nodes.
            repeated=page.evaluate("""()=>{const sig=Game.grid.map(c=>[c.x,c.y,!!c.obstacle,!!c.cover,!!c.door]).join('|');applyEnvironmentSkinV14();applyEnvironmentSkinV14();return{n:document.querySelectorAll('#board>.cr79-lightfield').length,signature:Game.grid.map(c=>[c.x,c.y,!!c.obstacle,!!c.cover,!!c.door]).join('|'),same:window.__qaLight===document.querySelector('#board>.cr79-lightfield')}}""")
            assert repeated=={'n':1,'signature':check['gridSignature'],'same':True},(label,sector,repeated)
            if sector in ('old_market','neon_row'):
                # The mission-start banner is transient presentation, not the light field;
                # remove it for a readable still of the actual settled battlefield.
                page.evaluate("()=>document.querySelectorAll('#board>.banner').forEach(el=>el.remove())")
                page.screenshot(path=str(OUT/f'{label}_{sector}.png'),full_page=True)
            print('LIGHTFIELD_PASS',label,sector,theme,'board',round(check['board']),'opacity',check['light']['opacity'],flush=True)
        assert not errors and not missing,(label,errors,missing)
        context.close()
    browser.close()
print('PWA12.79 STATIC LIGHTFIELDS PASS: eight environments x two viewports; decoded assets, stable geometry, unchanged input layers',flush=True)
