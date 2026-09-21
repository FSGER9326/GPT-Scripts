"""Browser integration for PWA12.104 canonical-based physical district dispatches."""
from pathlib import Path
import mimetypes,sys
from playwright.sync_api import sync_playwright
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();(ROOT/'qa').mkdir(exist_ok=True)
HTML=(ROOT/'index.html').read_text().replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
SHIM="""<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"""
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    ctx=browser.new_context(viewport={'width':390,'height':844});errors=[]
    def route(r):
        rel=r.request.url.split('http://cr.local/',1)[-1].split('?',1)[0] or 'index.html';p=ROOT/rel
        r.fulfill(status=200,body=p.read_bytes(),content_type=mimetypes.guess_type(p.name)[0] or 'application/octet-stream') if p.is_file() else r.fulfill(status=404,body=b'not found')
    ctx.route('http://cr.local/**',route);page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content(HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1),wait_until='domcontentloaded');page.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
    setup=page.evaluate('''()=>{
      startNewGame('District Dispatch QA','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');
      activateDistrictV133('old_market');showScreen('overworld-screen');
      const world=currentDistrictV133(),defs=V13_DISTRICT_LOCATIONS.old_market;
      const src=defs.find(d=>d.contact==='c1')||defs.find(d=>d.contact)||defs.find(d=>d.shop)||defs[0];
      Game.cityLife.discovered[src.id]=true;if(src.contact){Game.contactRelations[src.contact].known=true;Game.contactRelations[src.contact].trust=35}
      const p=world.locations[src.id];Game.ovPlayer={x:p.x,y:p.y};Game.districtWorldsV133.positions[world.id]={x:p.x,y:p.y};Game.pendingPath=null;
      updateDistrictDispatchUIV12104();const offer=offerDistrictDispatchV12104(src.id,world),panel=document.getElementById('v12104-dispatch-panel'),rect=panel.getBoundingClientRect();
      return{src:src.id,contact:src.contact||null,offer,panelText:panel.textContent,width:rect.width,right:rect.right,scroll:document.documentElement.scrollWidth,inner:innerWidth};
    }''')
    assert setup['offer'] and setup['offer']['blocks']>=10,setup
    assert 'STREET DISPATCH' in setup['panelText'] and setup['width']<=374 and setup['right']<=390.5 and setup['scroll']<=390,setup
    risk=page.evaluate('''q=>{
      const w=currentDistrictV133(),sp=w.locations[q.src],tp=w.locations[q.offer.targetId],states=ensureNeighborhoodStateV134(w),ids=[sp.neighborhood,tp.neighborhood];
      for(const id of ids){Object.assign(states[id],{localHeat:0,security:0,gangPressure:0,unrest:0})}const low=quoteDistrictDispatchV12104(q.src,q.offer.targetId,w,'contraband');
      for(const id of ids){Object.assign(states[id],{localHeat:90,security:5,gangPressure:5,unrest:5})}const high=quoteDistrictDispatchV12104(q.src,q.offer.targetId,w,'contraband');
      return{low:{risk:low.risk,payout:low.payout},high:{risk:high.risk,payout:high.payout}};
    }''',setup)
    assert risk['high']['risk']>risk['low']['risk'] and risk['high']['payout']>risk['low']['payout'],risk
    remote=page.evaluate('''q=>{const w=currentDistrictV133();Game.ovPlayer={x:0,y:0};return{near:nearDistrictDispatchLocationV12104(w),accepted:acceptDistrictDispatchV12104(q.offer.id),active:activeDistrictDispatchV12104()}}''',setup)
    assert remote['accepted'] is False and remote['active'] is None,remote
    accepted=page.evaluate('''q=>{const w=currentDistrictV133(),p=w.locations[q.src];Game.ovPlayer={x:p.x,y:p.y};Game.districtWorldsV133.positions[w.id]={x:p.x,y:p.y};const ok=acceptDistrictDispatchV12104(q.offer.id),a=activeDistrictDispatchV12104();updateDistrictDispatchUIV12104();const panel=document.getElementById('v12104-dispatch-panel'),r=panel.getBoundingClientRect();return{ok,active:a&&a.id,target:a&&a.targetId,path:Game.pendingPath?.length||0,targetKnown:!!Game.cityLife.discovered[a?.targetId],panel:panel.textContent,width:r.width,right:r.right,scroll:document.documentElement.scrollWidth,credits:Game.credits}}''',setup)
    assert accepted['ok'] and accepted['active']==setup['offer']['id'] and accepted['path']>1 and accepted['targetKnown'],accepted
    assert 'ACTIVE LOCAL DISPATCH' in accepted['panel'] and accepted['right']<=390.5 and accepted['scroll']<=390,accepted
    page.screenshot(path=str(ROOT/'qa/pwa12-104-city-dispatches-mobile.png'),full_page=True)
    assert page.evaluate('()=>saveGame(1,true)') is True
    restored=page.evaluate('''()=>{Game.livingStreetsV134.districtDispatches.active=null;const ok=loadGame(1),a=activeDistrictDispatchV12104();return{ok,id:a?.id||null,target:a?.targetId||null}}''')
    assert restored=={'ok':True,'id':setup['offer']['id'],'target':setup['offer']['targetId']},restored
    completed=page.evaluate('''q=>{const w=currentDistrictV133(),a=activeDistrictDispatchV12104(),p=w.locations[a.targetId],before=Game.credits;Game.ovPlayer={x:p.x,y:p.y};Game.districtWorldsV133.positions[w.id]={x:p.x,y:p.y};onStreetStepV134(w);const s=ensureDistrictDispatchStateV12104(),last=s.history[0];return{before,after:Game.credits,active:s.active,last:last&&{id:last.id,status:last.status,reward:last.reward,late:last.lateMinutes},stats:s.stats}}''',setup)
    assert completed['active'] is None and completed['last']['id']==setup['offer']['id'] and completed['last']['status']=='delivered',completed
    assert completed['after']==completed['before']+completed['last']['reward'] and completed['stats']['delivered']==1,completed
    compat=page.evaluate('''()=>{const s=ensureLivingStreetsStateV134();delete s.districtDispatches;const d=ensureDistrictDispatchStateV12104();return{version:d.version,active:d.active,offers:typeof d.offers,history:Array.isArray(d.history),schema:14}}''')
    assert compat=={'version':1,'active':None,'offers':'object','history':True,'schema':14},compat
    assert not errors,errors
    print('PASS city dispatch browser: physical source gate, dynamic route risk, real pendingPath, persistence, street-step delivery, rewards, 390x844 UI')
    ctx.close();browser.close()
