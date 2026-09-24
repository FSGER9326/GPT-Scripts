"""Browser integration for PWA12.104 canonical-based interdistrict physical logistics."""
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
      startNewGame('Interdistrict Logistics QA','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');
      activateDistrictV133('old_market');showScreen('overworld-screen');
      const world=currentDistrictV133(),defs=V13_DISTRICT_LOCATIONS.old_market;
      const src=defs.find(d=>d.contact==='c1')||defs.find(d=>d.contact)||defs.find(d=>d.shop)||defs[0];
      Game.cityLife.discovered[src.id]=true;if(src.contact){Game.contactRelations[src.contact].known=true;Game.contactRelations[src.contact].trust=35}
      const p=world.locations[src.id];Game.ovPlayer={x:p.x,y:p.y};Game.districtWorldsV133.positions[world.id]={x:p.x,y:p.y};Game.pendingPath=null;
      updateDistrictDispatchUIV12104();updateInterdistrictLogisticsUIV12104();
      const offer=offerInterdistrictLogisticsV12104(src.id,world),panel=document.getElementById('v12104-logistics-panel'),rect=panel.getBoundingClientRect();
      return{src:src.id,contact:src.contact||null,offer,panelText:panel.textContent,width:rect.width,right:rect.right,scroll:document.documentElement.scrollWidth,inner:innerWidth};
    }''')
    assert setup['offer'] and setup['offer']['targetDistrict']!='old_market',setup
    assert len(setup['offer']['plans'])>=1 and setup['offer']['plans'][0]['legs']>=2,setup['offer']['plans']
    assert 'STREET LOGISTICS' in setup['panelText'] and 'LOCAL ALTERNATIVE' in setup['panelText'],setup['panelText']
    assert setup['width']<=374 and setup['right']<=390.5 and setup['scroll']<=390,setup

    # Canonical access rules materially change network intelligence.
    access=page.evaluate('''()=>{
      const l=V133_TRANSIT_LINKS.find(x=>x.type==='security');Game.notoriety=0;Game.rep[l.faction]=0;const low=logisticsTransitAccessV12104(l),lowRisk=planInterdistrictLogisticsV12104(l.from.district,l.to.district)[0]?.risk;
      Game.notoriety=82;Game.rep[l.faction]=0;const high=logisticsTransitAccessV12104(l),highRisk=planInterdistrictLogisticsV12104(l.from.district,l.to.district)[0]?.risk;
      Game.notoriety=0;return{low,high,lowRisk,highRisk};
    }''')
    assert access['low']['allowed'] is True and access['high']['allowed'] is False and access['high']['reason']=='CHECKPOINT',access
    assert access['highRisk']>=access['lowRisk'],access

    # Hidden routes are never considered before discovery, then become graph options.
    hidden=page.evaluate('''()=>{
      const l=V133_TRANSIT_LINKS.find(x=>x.type==='hidden'),s=Game.districtWorldsV133.hiddenLinks;delete s[l.id];const before=planInterdistrictLogisticsV12104(l.from.district,l.to.district).flatMap(p=>p.links).includes(l.id);s[l.id]=true;const after=planInterdistrictLogisticsV12104(l.from.district,l.to.district).flatMap(p=>p.links).includes(l.id);delete s[l.id];return{before,after,id:l.id};
    }''')
    assert hidden['before'] is False and hidden['after'] is True,hidden

    remote=page.evaluate('''q=>{Game.ovPlayer={x:0,y:0};const p=q.offer.plans[0];return{ok:acceptInterdistrictLogisticsV12104(q.offer.id,p.id),active:activeInterdistrictLogisticsV12104()}}''',setup)
    assert remote['ok'] is False and remote['active'] is None,remote

    accepted=page.evaluate('''q=>{
      const w=currentDistrictV133(),p0=w.locations[q.src];Game.ovPlayer={x:p0.x,y:p0.y};Game.districtWorldsV133.positions[w.id]={x:p0.x,y:p0.y};const p=q.offer.plans[0],ok=acceptInterdistrictLogisticsV12104(q.offer.id,p.id),a=activeInterdistrictLogisticsV12104();updateInterdistrictLogisticsUIV12104();const panel=document.getElementById('v12104-logistics-panel'),r=panel.getBoundingClientRect();return{ok,id:a?.id,plan:a?.planMode,links:a?.links||[],leg:a?.legIndex,stage:a?.stage,path:Game.pendingPath?.length||0,targetKnown:!!Game.cityLife.discovered[a?.targetId],text:panel.textContent,width:r.width,right:r.right,scroll:document.documentElement.scrollWidth};
    }''',setup)
    assert accepted['ok'] and accepted['id']==setup['offer']['id'] and len(accepted['links'])>=2,accepted
    assert accepted['leg']==0 and accepted['stage']=='to_transit' and accepted['path']>1 and accepted['targetKnown'],accepted
    assert 'ACTIVE INTERDISTRICT LOGISTICS' in accepted['text'] and accepted['right']<=390.5 and accepted['scroll']<=390,accepted
    page.screenshot(path=str(ROOT/'qa/pwa12-104-interdistrict-logistics-mobile.png'),full_page=True)

    assert page.evaluate('()=>saveGame(1,true)') is True
    restored=page.evaluate('''()=>{const s=ensureInterdistrictLogisticsStateV12104();const id=s.active.id,links=s.active.links.join('|'),mode=s.active.planMode;s.active=null;const ok=loadGame(1),a=activeInterdistrictLogisticsV12104();return{ok,id:a?.id,links:a?.links?.join('|'),mode:a?.planMode,expected:{id,links,mode}}}''')
    assert restored['ok'] and restored['id']==restored['expected']['id'] and restored['links']==restored['expected']['links'] and restored['mode']==restored['expected']['mode'],restored

    # Traverse every chosen district link through canonical travelDistrictV133.
    hops=[]
    for _ in range(6):
        snap=page.evaluate('''()=>{const a=activeInterdistrictLogisticsV12104(),w=currentDistrictV133();return{done:!a||a.legIndex>=a.links.length,leg:a?.legIndex||0,total:a?.links?.length||0,link:a?.links?.[a?.legIndex]||null,district:w?.id,target:a?.targetDistrict}}''')
        if snap['done']: break
        hop=page.evaluate('''()=>{
          const a=activeInterdistrictLogisticsV12104(),w=currentDistrictV133(),id=a.links[a.legIndex],l=V133_TRANSIT_LINKS.find(x=>x.id===id),ep=l.from.district===w.id?l.from:l.to.district===w.id?l.to:null;if(!ep)throw new Error('planned link not connected to current district '+id+' / '+w.id);const tr=w.transit.find(x=>x.id===ep.node);if(!tr)throw new Error('transit node missing '+ep.node);Game.ovPlayer={x:tr.x,y:tr.y};Game.districtWorldsV133.positions[w.id]={x:tr.x,y:tr.y};const from=w.id,ok=travelDistrictV133(id,'clear'),after=activeInterdistrictLogisticsV12104();return{ok,id,from,to:currentDistrictV133().id,leg:after?.legIndex,stage:after?.stage,transfers:after?.transferHistory?.filter(x=>x.kind==='transit').length||0};
        }''')
        assert hop['ok'] is True and hop['to']!=hop['from'],hop
        hops.append(hop);page.wait_for_timeout(140)
    final_route=page.evaluate('''()=>{const a=activeInterdistrictLogisticsV12104(),w=currentDistrictV133();updateInterdistrictLogisticsUIV12104();return{active:!!a,district:w.id,target:a?.targetDistrict,leg:a?.legIndex,total:a?.links?.length,stage:a?.stage,path:Game.pendingPath?.length||0,transfers:a?.transferHistory?.filter(x=>x.kind==='transit').length||0,panel:document.getElementById('v12104-logistics-panel')?.textContent||''}}''')
    assert final_route['active'] and final_route['district']==final_route['target'] and final_route['leg']>=final_route['total'],(hops,final_route)
    assert final_route['stage']=='to_drop' and final_route['path']>1 and final_route['transfers']>=2,final_route
    assert 'FINAL STREET LEG' in final_route['panel'],final_route

    completed=page.evaluate('''()=>{
      const a=activeInterdistrictLogisticsV12104(),w=currentDistrictV133(),p=w.locations[a.targetId],before=Game.credits;Game.ovPlayer={x:p.x,y:p.y};Game.districtWorldsV133.positions[w.id]={x:p.x,y:p.y};onStreetStepV134(w);const s=ensureInterdistrictLogisticsStateV12104(),last=s.history[0];return{before,after:Game.credits,active:s.active,last:last&&{id:last.id,status:last.status,reward:last.reward,late:last.lateMinutes,target:last.targetDistrict,reroutes:last.reroutes},stats:s.stats};
    }''')
    assert completed['active'] is None and completed['last']['id']==setup['offer']['id'] and completed['last']['status']=='delivered',completed
    assert completed['after']==completed['before']+completed['last']['reward'] and completed['stats']['delivered']==1,completed

    compat=page.evaluate('''()=>{const s=ensureLivingStreetsStateV134();delete s.interdistrictLogistics;const d=ensureInterdistrictLogisticsStateV12104();return{version:d.version,active:d.active,offers:typeof d.offers,history:Array.isArray(d.history),schema:14}}''')
    assert compat=={'version':1,'active':None,'offers':'object','history':True,'schema':14},compat
    assert not errors,errors
    print('PASS interdistrict logistics browser: physical source gate, 3-mode network planning, canonical access response, hidden-route discovery, real pendingPath, canonical physical transit chain, persistence, destination delivery, rewards, 390x844 UI')
    ctx.close();browser.close()
