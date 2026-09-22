"""Chromium integration QA for cumulative PWA12.104 city multi-hop logistics candidate 04."""
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
      startNewGame('Multi-Hop QA','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');Game.notoriety=0;
      activateDistrictV133('old_market');showScreen('overworld-screen');initOverworldV133();
      const w=currentDistrictV133(),defs=V13_DISTRICT_LOCATIONS.old_market,src=defs.find(d=>d.contact==='c1')||defs.find(d=>d.contact)||defs.find(d=>d.shop)||defs[0];
      Game.cityLife.discovered[src.id]=true;if(src.contact){Game.contactRelations[src.contact].known=true;Game.contactRelations[src.contact].trust=35}
      const p=w.locations[src.id];Game.ovPlayer={x:p.x,y:p.y};Game.districtWorldsV133.positions[w.id]={x:p.x,y:p.y};Game.pendingPath=null;
      Object.values(ensureNeighborhoodStateV134(w)).forEach(h=>{h.localHeat=5;h.security=1;h.gangPressure=1;h.unrest=1});
      updateInterdistrictDispatchUIV12104();updateMultiHopDispatchUIV12104();
      const base=document.getElementById('v12104-interdistrict-panel'),offer=offerMultiHopDispatchV12104(src.id,w);return{src:src.id,sourceDistrict:w.id,offer,baseText:base?.textContent||'',hasDirect:!!base?.querySelector('#v12104-cross-accept'),hasMulti:!!base?.querySelector('#v12104-multi-accept')};
    }''')
    assert setup['offer'] and setup['hasDirect'] and setup['hasMulti'],setup
    off=setup['offer'];assert off['handoffDistrict']!=off['sourceDistrict'] and off['finalDistrict'] not in (off['sourceDistrict'],off['handoffDistrict']),off
    assert len(off['leg1']['options']) and len(off['leg2']['options']),off
    accepted=page.evaluate('''(id)=>{const ok=acceptMultiHopDispatchV12104(id),a=activeMultiHopDispatchV12104();return{ok,id:a?.id,phase:a?.phase,stage:a?.multiHopPlan?.stage,deadline:a?.deadline,source:a?.sourceDistrict,target:a?.targetDistrict,options:a?.options?.length||0,credits:Game.credits}}''',off['id'])
    assert accepted['ok'] and accepted['phase']=='choose_transit' and accepted['stage']==1 and accepted['target']==off['handoffDistrict'],accepted
    first=page.evaluate('''()=>{
      const a=activeMultiHopDispatchV12104(),w=currentDistrictV133();const opts=a.options.filter(o=>!o.blocked).map(o=>{const n=w.transit.find(t=>t.id===o.sourceNodeId),path=n&&findDistrictPathV133(Game.ovPlayer,{x:n.x,y:n.y},w);return{o,len:path?.length||0}}).sort((x,y)=>y.len-x.len);const pick=opts[0];const deadline=a.deadline,ok=chooseInterdistrictTransitV12104(pick.o.linkId);return{ok,link:pick.o.linkId,path:Game.pendingPath?.length||0,deadlineBefore:deadline,deadlineAfter:a.deadline,selected:a.multiHopPlan?.selectedLeg1?.linkId,stage:a.multiHopPlan?.stage,phase:a.phase}}''')
    assert first['ok'] and first['path']>0 and first['selected']==first['link'] and first['deadlineAfter']==first['deadlineBefore'],first
    crossed1=page.evaluate('''()=>{
      const a=activeMultiHopDispatchV12104(),op=a.options.find(o=>o.linkId===a.chosenLinkId),w=currentDistrictV133(),node=w.transit.find(t=>t.id===op.sourceNodeId);Game.ovPlayer={x:node.x,y:node.y};Game.districtWorldsV133.positions[w.id]={x:node.x,y:node.y};Game.pendingPath=null;const deadline=a.deadline,ok=travelDistrictV133(op.linkId,'clear'),after=activeMultiHopDispatchV12104();return{ok,district:currentDistrictV133()?.id,phase:after?.phase,stage:after?.multiHopPlan?.stage,target:after?.targetId,path:Game.pendingPath?.length||0,deadline,deadlineAfter:after?.deadline}}''')
    assert crossed1['ok'] and crossed1['district']==off['handoffDistrict'] and crossed1['phase']=='last_mile' and crossed1['stage']==1 and crossed1['path']>0 and crossed1['deadlineAfter']==crossed1['deadline'],crossed1
    handoff=page.evaluate('''()=>{
      const a=activeMultiHopDispatchV12104(),w=currentDistrictV133(),p=w.locations[a.targetId],before=Game.credits;Game.ovPlayer={x:p.x,y:p.y};Game.districtWorldsV133.positions[w.id]={x:p.x,y:p.y};Game.pendingPath=null;onStreetStepV134(w);updateMultiHopDispatchUIV12104();const b=activeMultiHopDispatchV12104(),panel=document.getElementById('v12104-multihop-panel'),r=panel?.getBoundingClientRect();return{active:!!b,phase:b?.phase,stage:b?.multiHopPlan?.stage,creditsBefore:before,creditsAfter:Game.credits,text:panel?.textContent||'',display:panel?.style.display,width:r?.width||0,left:r?.left||0,right:r?.right||0,scroll:document.documentElement.scrollWidth,inner:innerWidth,stats:ensureDistrictDispatchStateV12104().stats,deadline:b?.deadline}}''')
    assert handoff['active'] and handoff['phase']=='handoff' and handoff['stage']=='handoff' and handoff['creditsAfter']==handoff['creditsBefore'],handoff
    assert 'PHYSICAL HANDOFF COMPLETE' in handoff['text'] and handoff['display']=='block',handoff
    assert handoff['width']<=374.5 and handoff['left']>=-0.5 and handoff['right']<=390.5 and handoff['scroll']<=390,handoff
    page.screenshot(path=str(ROOT/'qa/pwa12-104-city-multihop-logistics-mobile.png'),full_page=True)
    assert page.evaluate('()=>saveGame(3,true)') is True
    restored=page.evaluate('''()=>{ensureDistrictDispatchStateV12104().active=null;Game.pendingPath=null;const ok=loadGame(3);updateMultiHopDispatchUIV12104();const a=activeMultiHopDispatchV12104(),p=document.getElementById('v12104-multihop-panel');return{ok,id:a?.id,phase:a?.phase,stage:a?.multiHopPlan?.stage,deadline:a?.deadline,display:p?.style.display,text:p?.textContent||''}}''')
    assert restored['ok'] and restored['id']==off['id'] and restored['phase']=='handoff' and restored['stage']=='handoff' and restored['deadline']==handoff['deadline'],restored
    secondPrep=page.evaluate('''()=>{const a=activeMultiHopDispatchV12104();a.dynamicDisruptionTriggered=true;a.dynamicDisruptionArm={linkId:'old'};a.dynamicDisruption={status:'pushed',triggeredAt:1,linkId:'old'};const ok=beginSecondLegMultiHopV12104();const b=activeMultiHopDispatchV12104();return{ok,stage:b?.multiHopPlan?.stage,phase:b?.phase,source:b?.sourceDistrict,target:b?.targetDistrict,options:b?.options?.length||0,deadline:b?.deadline,disruptions:b?.multiHopPlan?.disruptions?.length||0,dynamic:!!b?.dynamicDisruption,dynamicFlag:!!b?.dynamicDisruptionTriggered}}''')
    assert secondPrep['ok'] and secondPrep['stage']==2 and secondPrep['phase']=='choose_transit' and secondPrep['source']==off['handoffDistrict'] and secondPrep['target']==off['finalDistrict'],secondPrep
    assert secondPrep['disruptions']>=1 and not secondPrep['dynamic'] and not secondPrep['dynamicFlag'],secondPrep
    second=page.evaluate('''()=>{const a=activeMultiHopDispatchV12104(),w=currentDistrictV133();const opts=a.options.filter(o=>!o.blocked).map(o=>{const n=w.transit.find(t=>t.id===o.sourceNodeId),path=n&&findDistrictPathV133(Game.ovPlayer,{x:n.x,y:n.y},w);return{o,len:path?.length||0}}).sort((x,y)=>y.len-x.len);const pick=opts[0],deadline=a.deadline,ok=chooseInterdistrictTransitV12104(pick.o.linkId);return{ok,link:pick.o.linkId,path:Game.pendingPath?.length||0,deadlineBefore:deadline,deadlineAfter:a.deadline,selected:a.multiHopPlan?.selectedLeg2?.linkId,payout:a.payout,stage:a.multiHopPlan?.stage}}''')
    assert second['ok'] and second['path']>0 and second['selected']==second['link'] and second['deadlineAfter']==second['deadlineBefore'] and second['payout']>0,second
    crossed2=page.evaluate('''()=>{const a=activeMultiHopDispatchV12104(),op=a.options.find(o=>o.linkId===a.chosenLinkId),w=currentDistrictV133(),node=w.transit.find(t=>t.id===op.sourceNodeId);Game.ovPlayer={x:node.x,y:node.y};Game.districtWorldsV133.positions[w.id]={x:node.x,y:node.y};Game.pendingPath=null;const deadline=a.deadline,ok=travelDistrictV133(op.linkId,'clear'),after=activeMultiHopDispatchV12104();return{ok,district:currentDistrictV133()?.id,phase:after?.phase,stage:after?.multiHopPlan?.stage,target:after?.targetId,path:Game.pendingPath?.length||0,deadline,deadlineAfter:after?.deadline}}''')
    assert crossed2['ok'] and crossed2['district']==off['finalDistrict'] and crossed2['phase']=='last_mile' and crossed2['stage']==2 and crossed2['path']>0 and crossed2['deadlineAfter']==crossed2['deadline'],crossed2
    completed=page.evaluate('''()=>{const a=activeMultiHopDispatchV12104(),w=currentDistrictV133(),p=w.locations[a.targetId],before=Game.credits;Game.ovPlayer={x:p.x,y:p.y};Game.districtWorldsV133.positions[w.id]={x:p.x,y:p.y};Game.pendingPath=null;onStreetStepV134(w);const s=ensureDistrictDispatchStateV12104(),last=s.history[0];return{before,after:Game.credits,active:s.active,last:last&&{id:last.id,status:last.status,reward:last.reward,multiHop:!!last.multiHop,stage:last.multiHopPlan?.stage,leg1:last.multiHopPlan?.selectedLeg1?.linkId,leg2:last.multiHopPlan?.selectedLeg2?.linkId,disruptions:last.multiHopPlan?.disruptions?.length||0},stats:s.stats}}''')
    assert completed['active'] is None and completed['last']['id']==off['id'] and completed['last']['status']=='delivered' and completed['last']['multiHop'],completed
    assert completed['last']['leg1']==first['link'] and completed['last']['leg2']==second['link'] and completed['after']==completed['before']+completed['last']['reward'] and completed['last']['reward']>0,completed
    assert completed['stats']['multiHopHandoffs']>=1 and completed['stats']['multiHopDelivered']>=1,completed
    assert not errors,errors
    print('PASS multi-hop logistics browser: direct-run option preserved, two physical crossings, physical handoff, save/load, fresh second-leg disruption state, final delivery, 390x844 UI')
    ctx.close();browser.close()
