"""Chromium integration QA for cumulative PWA12.104 city dynamic disruptions candidate 03."""
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
      startNewGame('Dynamic Disruption QA','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');Game.notoriety=0;
      activateDistrictV133('old_market');showScreen('overworld-screen');initOverworldV133();
      const w=currentDistrictV133(),defs=V13_DISTRICT_LOCATIONS.old_market,src=defs.find(d=>d.contact==='c1')||defs.find(d=>d.contact)||defs.find(d=>d.shop)||defs[0];
      Game.cityLife.discovered[src.id]=true;if(src.contact){Game.contactRelations[src.contact].known=true;Game.contactRelations[src.contact].trust=35}
      const p=w.locations[src.id];Game.ovPlayer={x:p.x,y:p.y};Game.districtWorldsV133.positions[w.id]={x:p.x,y:p.y};Game.pendingPath=null;
      const offer=offerInterdistrictDispatchV12104(src.id,w);const accepted=acceptInterdistrictDispatchV12104(offer.id),a=activeInterdistrictDispatchV12104();
      const viable=a.options.filter(o=>!o.blocked).map(o=>{const n=w.transit.find(t=>t.id===o.sourceNodeId),path=n&&findDistrictPathV133(Game.ovPlayer,{x:n.x,y:n.y},w);return{o,len:path?.length||0}}).filter(x=>x.len>=4).sort((x,y)=>(x.o.linkType==='security')-(y.o.linkType==='security')||y.len-x.len);
      const pick=viable[0]||a.options.filter(o=>!o.blocked).map(o=>({o,len:999}))[0];const ok=chooseInterdistrictTransitV12104(pick.o.linkId);
      const hs=ensureNeighborhoodStateV134(w);Object.values(hs).forEach(h=>{h.localHeat=100;h.security=5;h.gangPressure=5;h.unrest=5});
      return{src:src.id,offerId:offer.id,accepted,chosen:ok,linkId:pick.o.linkId,linkType:pick.o.linkType,path:Game.pendingPath?.length||0,deadline:a.deadline,targetDistrict:a.targetDistrict,targetId:a.targetId,viable:a.options.filter(o=>!o.blocked).length};
    }''')
    assert setup['accepted'] and setup['chosen'] and setup['path']>=4 and setup['viable']>=2,setup
    first=page.evaluate('''()=>{const w=currentDistrictV133();function step(){const n=Game.pendingPath?.[1];if(!n)return false;Game.ovPlayer={x:n.x,y:n.y};Game.districtWorldsV133.positions[w.id]={x:n.x,y:n.y};Game.pendingPath.shift();advanceTime(.25);onStreetStepV134(w);return true}const ok=step(),a=activeInterdistrictDispatchV12104();return{ok,path:Game.pendingPath?.length||0,armed:a?.dynamicDisruptionArm||null,alert:a?.dynamicDisruption||null}}''')
    assert first['ok'] and first['armed'] and first['alert'] is None,first
    alert=page.evaluate('''()=>{const w=currentDistrictV133();const n=Game.pendingPath?.[1];if(!n)return{ok:false};Game.ovPlayer={x:n.x,y:n.y};Game.districtWorldsV133.positions[w.id]={x:n.x,y:n.y};Game.pendingPath.shift();advanceTime(.25);onStreetStepV134(w);updateInterdistrictDisruptionUIV12104();const a=activeInterdistrictDispatchV12104(),d=a?.dynamicDisruption,p=document.getElementById('v12104-disruption-panel'),r=p.getBoundingClientRect();return{ok:true,status:d?.status,title:d?.title,pressure:d?.pressure,link:d?.linkId,alt:d?.alternativeLinkId,path:Game.pendingPath?.length||0,deadline:a?.deadline,text:p?.textContent||'',width:r.width,right:r.right,left:r.left,scroll:document.documentElement.scrollWidth,inner:innerWidth}}''')
    assert alert['ok'] and alert['status']=='alert' and alert['pressure']>=.92 and alert['path']==0,alert
    assert alert['alt'] and 'LIVE ROUTE DISRUPTION' in alert['text'] and 'REROUTE' in alert['text'] and 'PUSH THROUGH' in alert['text'],alert
    assert alert['width']<=374 and alert['left']>=-0.5 and alert['right']<=390.5 and alert['scroll']<=390,alert
    page.screenshot(path=str(ROOT/'qa/pwa12-104-city-dynamic-disruption-mobile.png'),full_page=True)
    assert page.evaluate('()=>saveGame(3,true)') is True
    reroute=page.evaluate('''()=>{const a=activeInterdistrictDispatchV12104(),before={link:a.chosenLinkId,deadline:a.deadline};const ok=rerouteInterdistrictDisruptionV12104(),d=a.dynamicDisruption;return{ok,before,link:a.chosenLinkId,deadline:a.deadline,path:Game.pendingPath?.length||0,status:d.status,to:d.toLinkId}}''')
    assert reroute['ok'] and reroute['link']!=reroute['before']['link'] and reroute['to']==reroute['link'],reroute
    assert reroute['deadline']==reroute['before']['deadline'] and reroute['path']>0 and reroute['status']=='rerouted',reroute
    restored=page.evaluate('''()=>{ensureDistrictDispatchStateV12104().active=null;Game.pendingPath=null;const ok=loadGame(3);updateInterdistrictDisruptionUIV12104();const a=activeInterdistrictDispatchV12104(),d=a?.dynamicDisruption,p=document.getElementById('v12104-disruption-panel');return{ok,id:a?.id,status:d?.status,link:a?.chosenLinkId,deadline:a?.deadline,path:Game.pendingPath?.length||0,visible:p?.style.display,text:p?.textContent||''}}''')
    assert restored['ok'] and restored['id']==setup['offerId'] and restored['status']=='alert' and restored['link']==setup['linkId'],restored
    assert restored['path']==0 and restored['visible']=='block' and 'LIVE ROUTE DISRUPTION' in restored['text'],restored
    pushed=page.evaluate('''()=>{
      const a=activeInterdistrictDispatchV12104(),w=currentDistrictV133(),before={link:a.chosenLinkId,deadline:a.deadline,risk:a.risk,time:((Game.day-1)*24+Game.hour)*60};
      let best=null,bd=1e9;for(const n of w.neighborhoods){const d=Math.hypot(Game.ovPlayer.x-n.x,Game.ovPlayer.y-n.y);if(d<bd){bd=d;best=n.id}}const h=ensureNeighborhoodStateV134(w)[best];h.localHeat=40;const heatBefore=h.localHeat;
      const ok=pushThroughInterdistrictDisruptionV12104(),d=a.dynamicDisruption;return{ok,before,link:a.chosenLinkId,deadline:a.deadline,risk:a.risk,time:((Game.day-1)*24+Game.hour)*60,heatBefore,heatAfter:h.localHeat,path:Game.pendingPath?.length||0,status:d.status,reason:d.reason};
    }''')
    assert pushed['ok'] and pushed['link']==pushed['before']['link'] and pushed['deadline']==pushed['before']['deadline'],pushed
    assert pushed['path']>0 and pushed['status']=='pushed' and pushed['time']>=pushed['before']['time']+14.9,pushed
    assert pushed['risk']>=pushed['before']['risk'] and pushed['heatAfter']>pushed['heatBefore'],pushed
    crossed=page.evaluate('''()=>{
      const a=activeInterdistrictDispatchV12104(),op=a.options.find(o=>o.linkId===a.chosenLinkId),w=currentDistrictV133(),node=w.transit.find(t=>t.id===op.sourceNodeId);Game.ovPlayer={x:node.x,y:node.y};Game.districtWorldsV133.positions[w.id]={x:node.x,y:node.y};Game.pendingPath=null;
      const before={day:Game.day,hour:Game.hour,credits:Game.credits},ok=travelDistrictV133(op.linkId,'clear'),after=activeInterdistrictDispatchV12104(),nw=currentDistrictV133();return{ok,before,afterTime:{day:Game.day,hour:Game.hour,credits:Game.credits},district:nw.id,phase:after?.phase,targetKnown:!!Game.cityLife.discovered[after?.targetId],path:Game.pendingPath?.length||0,target:after?.targetId};
    }''')
    assert crossed['ok'] and crossed['district']==setup['targetDistrict'] and crossed['phase']=='last_mile' and crossed['targetKnown'] and crossed['path']>0,crossed
    completed=page.evaluate('''()=>{const w=currentDistrictV133(),a=activeInterdistrictDispatchV12104(),p=w.locations[a.targetId],before=Game.credits;Game.ovPlayer={x:p.x,y:p.y};Game.districtWorldsV133.positions[w.id]={x:p.x,y:p.y};Game.pendingPath=null;onStreetStepV134(w);const s=ensureDistrictDispatchStateV12104(),last=s.history[0];return{before,after:Game.credits,active:s.active,last:last&&{id:last.id,status:last.status,reward:last.reward,cross:!!last.crossDistrict,disruption:last.dynamicDisruption},stats:s.stats}}''')
    assert completed['active'] is None and completed['last']['id']==setup['offerId'] and completed['last']['status']=='delivered' and completed['last']['cross'],completed
    assert completed['last']['disruption']['status']=='pushed' and completed['after']==completed['before']+completed['last']['reward'],completed
    assert not errors,errors
    print('PASS dynamic disruption browser: physical halt, persistent alert, alternate physical reroute, push-through cost, preserved deadline, canonical transit, last-mile delivery, 390x844 UI')
    ctx.close();browser.close()
