"""Chromium integration QA for PWA12.104 City Access Ecology Candidate 05."""
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
      startNewGame('Access Ecology QA','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');Game.notoriety=0;Game.rep=Game.rep||{};Game.heat=Game.heat||{};
      activateDistrictV133('old_market');showScreen('overworld-screen');initOverworldV133();
      const w=currentDistrictV133(),defs=V13_DISTRICT_LOCATIONS.old_market,src=defs.find(d=>d.contact==='c1')||defs.find(d=>d.contact)||defs.find(d=>d.shop)||defs[0];
      Game.cityLife.discovered[src.id]=true;if(src.contact){Game.contactRelations[src.contact].known=true;Game.contactRelations[src.contact].trust=40}
      const p=w.locations[src.id];Game.ovPlayer={x:p.x,y:p.y};Game.districtWorldsV133.positions[w.id]={x:p.x,y:p.y};Game.pendingPath=null;
      Object.values(ensureNeighborhoodStateV134(w)).forEach(h=>{h.localHeat=5;h.security=1;h.gangPressure=1;h.unrest=1;h.controller='local'});
      updateInterdistrictDispatchUIV12104();updateMultiHopDispatchUIV12104();
      const offer=offerMultiHopDispatchV12104(src.id,w),ok=acceptMultiHopDispatchV12104(offer.id),a=activeMultiHopDispatchV12104(),metro=a.options.find(o=>o.linkType==='metro')||a.options[0];
      return{src:src.id,contact:src.contact,offerId:offer.id,accepted:ok,linkId:metro.linkId,linkType:metro.linkType,sourceNode:metro.sourceNodeId,target:a.targetDistrict,phase:a.phase,trust:src.contact?Game.contactRelations[src.contact].trust:null};
    }''')
    assert setup['accepted'] and setup['phase']=='choose_transit',setup
    pressured=page.evaluate('''q=>{
      const l=V133_TRANSIT_LINKS.find(x=>x.id===q.linkId),a=l.from.district==='old_market'?l.from:l.to,b=l.from.district==='old_market'?l.to:l.from;
      function press(d,node){const w=generateDistrictV133(d),tr=w.transit.find(x=>x.id===node),states=ensureNeighborhoodStateV134(w);let id=null,bd=1e9;for(const n of w.neighborhoods){const dd=Math.hypot(tr.x-n.x,tr.y-n.y);if(dd<bd){bd=dd;id=n.id}}Object.assign(states[id],{localHeat:88,security:5,gangPressure:2,unrest:2,controller:'local'});return id}
      const h1=press(a.district,a.node),h2=press(b.district,b.node);refreshTransitAccessEcologyV12104();updateInterdistrictDispatchUIV12104();decorateTransitAccessEcologyV12104();const eco=evaluateTransitAccessEcologyV12104(q.linkId,'old_market','courier'),p=document.getElementById('v12104-multihop-panel'),btn=p?.querySelector(`[data-multi-link="${q.linkId}"]`),box=btn?.closest('.choice'),r=p?.getBoundingClientRect();return{eco,h1,h2,text:box?.textContent||'',disabled:!!btn?.disabled,sponsor:!!box?.querySelector('.v12104-eco-sponsor'),width:r?.width||0,left:r?.left||0,right:r?.right||0,scroll:document.documentElement.scrollWidth,inner:innerWidth};
    }''',setup)
    if setup['linkType']=='metro':
        assert pressured['eco']['blocked'] and pressured['eco']['label']=='METRO ID SWEEP',pressured
    else:
        assert pressured['eco']['label']!='OPEN ACCESS' or setup['linkType']=='hidden',pressured
    if pressured['eco']['blocked']:
        assert pressured['disabled'] and pressured['sponsor'],pressured
        assert pressured['width']<=374.5 and pressured['left']>=-0.5 and pressured['right']<=390.5 and pressured['scroll']<=390,pressured
        page.screenshot(path=str(ROOT/'qa/pwa12-104-city-access-ecology-mobile.png'),full_page=True)
        rejected=page.evaluate('(id)=>({ok:chooseInterdistrictTransitV12104(id),path:Game.pendingPath?.length||0})',setup['linkId'])
        assert not rejected['ok'] and rejected['path']==0,rejected
        sponsored=page.evaluate('''q=>{const before=Game.contactRelations[q.contact]?.trust,ok=sponsorTransitAccessV12104(q.linkId),after=Game.contactRelations[q.contact]?.trust,eco=evaluateTransitAccessEcologyV12104(q.linkId,'old_market','courier'),a=activeMultiHopDispatchV12104();return{ok,before,after,eco,stored:a?.accessEcologySponsors?.[q.linkId]||null,stats:Game.livingStreetsV134.accessEcology.stats}}''',setup)
        assert sponsored['ok'] and sponsored['after']==sponsored['before']-3 and sponsored['eco']['label']=='CONTACT COVER' and not sponsored['eco']['blocked'] and sponsored['stored'],sponsored
        assert sponsored['stats']['sponsors']>=1,sponsored
        assert page.evaluate('()=>saveGame(4,true)') is True
        restored=page.evaluate('''q=>{ensureDistrictDispatchStateV12104().active=null;const ok=loadGame(4),a=activeMultiHopDispatchV12104(),eco=evaluateTransitAccessEcologyV12104(q.linkId,a?.sourceDistrict,a?.kind);return{ok,id:a?.id,sponsor:a?.accessEcologySponsors?.[q.linkId]||null,blocked:eco?.blocked,label:eco?.label}}''',setup)
        assert restored['ok'] and restored['id']==setup['offerId'] and restored['sponsor'] and not restored['blocked'] and restored['label']=='CONTACT COVER',restored
    else:
        page.screenshot(path=str(ROOT/'qa/pwa12-104-city-access-ecology-mobile.png'),full_page=True)
    chosen=page.evaluate('''id=>{const a=activeMultiHopDispatchV12104(),ok=chooseInterdistrictTransitV12104(id),b=activeMultiHopDispatchV12104();return{ok,path:Game.pendingPath?.length||0,phase:b?.phase,chosen:b?.chosenOption,eco:b?.accessEcologyCommitted}}''',setup['linkId'])
    assert chosen['ok'] and chosen['path']>0 and chosen['phase']=='to_transit' and chosen['chosen']['linkId']==setup['linkId'] and chosen['eco'],chosen
    crossed=page.evaluate('''()=>{const a=activeMultiHopDispatchV12104(),op=a.chosenOption,w=currentDistrictV133(),n=w.transit.find(t=>t.id===op.sourceNodeId),beforeCredits=Game.credits,beforeMin=Math.round((((Game.day||1)-1)*24+(Game.hour||0))*60),eco=evaluateTransitAccessEcologyV12104(op.linkId,w.id,a.kind);Game.ovPlayer={x:n.x,y:n.y};Game.districtWorldsV133.positions[w.id]={x:n.x,y:n.y};Game.pendingPath=null;const ok=travelDistrictV133(op.linkId,'clear'),afterMin=Math.round((((Game.day||1)-1)*24+(Game.hour||0))*60),b=activeMultiHopDispatchV12104();return{ok,from:w.id,to:currentDistrictV133()?.id,phase:b?.phase,path:Game.pendingPath?.length||0,beforeCredits,afterCredits:Game.credits,timeDelta:afterMin-beforeMin,eco,history:Game.livingStreetsV134.accessEcology.history[0],stats:Game.livingStreetsV134.accessEcology.stats}}''')
    assert crossed['ok'] and crossed['to']==setup['target'] and crossed['phase']=='last_mile' and crossed['path']>0,crossed
    assert crossed['timeDelta']>=1 and crossed['stats']['crossings']>=1 and crossed['history']['type']=='crossing',crossed
    systemic=page.evaluate('''()=>{
      const sec=V133_TRANSIT_LINKS.find(l=>l.type==='security'),hid=V133_TRANSIT_LINKS.find(l=>l.type==='hidden'),freight=V133_TRANSIT_LINKS.find(l=>l.type==='freight');
      let friendly=null,covert=null,toll=null;
      if(sec){Game.rep[sec.faction]=45;Game.heat[sec.faction]=0;Game.notoriety=0;friendly=evaluateTransitAccessEcologyV12104(sec.id,sec.from.district,'courier')}
      if(hid){Game.districtWorldsV133.hiddenLinks[hid.id]=true;covert=evaluateTransitAccessEcologyV12104(hid.id,hid.from.district,'data')}
      if(freight){const ep=freight.from,w=generateDistrictV133(ep.district),tr=w.transit.find(x=>x.id===ep.node),st=ensureNeighborhoodStateV134(w);let id=null,bd=1e9;for(const n of w.neighborhoods){const d=Math.hypot(tr.x-n.x,tr.y-n.y);if(d<bd){bd=d;id=n.id}}Object.assign(st[id],{localHeat:60,security:2,gangPressure:5,unrest:4,controller:'local'});toll=evaluateTransitAccessEcologyV12104(freight.id,freight.from.district,'contraband')}
      return{friendly,covert,toll};
    }''')
    assert systemic['friendly'] and systemic['friendly']['friendly'] and systemic['friendly']['riskDelta']<0,systemic
    assert systemic['covert'] and not systemic['covert']['blocked'] and systemic['covert']['label']=='COVERT BYPASS',systemic
    assert systemic['toll'] and systemic['toll']['costDelta']>0 and systemic['toll']['label'] in ('CARGO TOLL','FREIGHT INSPECTION'),systemic
    assert not errors,errors
    print('PASS access ecology browser: live physical corridor pressure, lockout/sponsor persistence, physical routing/crossing, toll/friendly/covert states, 390x844 UI')
    ctx.close();browser.close()
