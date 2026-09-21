"""Chromium integration: interior risk/reward, checkpoint resume and one-time payout."""
from pathlib import Path
import json,mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text().replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')

def document(storage=None):
    shim="""<script>const __s=new Map(Object.entries(%s));const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});window.__testStorage=__s;</script>""" % json.dumps(storage or {})
    return HTML.replace('<head>','<head><base href="http://cr.local/">'+shim,1)

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    context=browser.new_context(viewport={'width':1280,'height':850})
    errors=[]
    def route(r):
        rel=r.request.url.split('http://cr.local/',1)[-1].split('?',1)[0] or 'index.html';fp=ROOT/rel
        r.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream') if fp.is_file() else r.fulfill(status=404,body=b'not found')
    context.route('http://cr.local/**',route)
    def openpage(storage=None):
        p=context.new_page();p.on('pageerror',lambda e:errors.append(str(e)))
        p.set_content(document(storage),wait_until='domcontentloaded')
        p.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
        return p
    start="""()=>{
        startNewGame('Intelligence QA','Hacker','street');
        document.getElementById('story-modal')?.classList.remove('open');showScreen('combat');
        const m={id:'intel_choice_qa',type:'heist',objective:'heist',_v12ObjectiveAssigned:true,
          name:'Blacksite ledger',desc:'QA test',contact:null,diff:2,
          enemies:['Guard','Enforcer','Drone'],reward:600,xp:70,targetFaction:'meridian',
          factionRepGain:0,factionRepLoss:{}};
        Game.activeMission=m;initCombat(m);Game.objective.completed=true;checkWinLose();
        return{credits:Game.credits,clock:[Game.day,Game.hour],missionCount:Game.missionHistory.length,
          stage:CR14MultiStageOperations.active.index,
          route:CR14MultiStageOperations.active.routeConsole,intel:CR14MultiStageOperations.active.intelConsole};
    }"""
    def position(p,kind):
        return p.evaluate("""kind=>{
          const op=CR14MultiStageOperations.active;
          const c=kind==='intel'?op.intelConsole:op.routeConsole;
          const u=Game.units.find(x=>x.team==='player'&&x.className==='Hacker')||Game.units.find(x=>x.team==='player');
          const old=Game.grid.find(v=>v.unit===u);if(old)old.unit=null;
          const cell=Game.grid.find(v=>v.x===c.x&&v.y===c.y);
          if(cell.unit&&cell.unit!==u)throw Error('Console occupied');
          u.x=c.x;u.y=c.y;cell.unit=u;Game.selectedUnit=u;Game.turn='player';u.ap=3;
          const action=objectiveActionAvailable(u);
          return{label:action?.label,chosen:kind,coord:c,ap:u.ap};
        }""",kind)
    # The intel path must forfeit maintenance extraction, survive two checkpoint generations,
    # and pay the original reward plus intel EXACTLY once after final exfil.
    first=openpage();initial=first.evaluate(start)
    assert initial['stage']==1 and initial['route'] and initial['intel'],initial
    avail=position(first,'intel')
    assert avail['label'] and 'INTEL' in avail['label'],avail
    (ROOT/'qa').mkdir(exist_ok=True)
    first.screenshot(path=str(ROOT/'qa/pwa12-64-interior-intel-choice-desktop.png'))
    picked=first.evaluate("""()=>{const u=Game.selectedUnit,a=objectiveActionAvailable(u);
      if(!a||!a.run())throw Error('intel could not be stolen');
      return{ap:u.ap,active:CR14MultiStageOperations.active,credits:Game.credits,
      time:[Game.day,Game.hour],status:document.getElementById('operation-stage-strip').textContent,
      routeBlocked:document.querySelector('[data-operation-console="locked"]')!=null};} """)
    assert picked['ap']==2 and picked['active']['intelExtracted'] and not picked['active']['extractionRerouted'] and picked['routeBlocked'],picked
    assert picked['credits']==initial['credits'] and picked['time']==initial['clock'],picked
    first.evaluate('()=>{Game.objective.completed=true;Game.objective.exfil=null;checkWinLose()}')
    assert first.evaluate('()=>CR14MultiStageOperations.active?.index')==2
    first.evaluate('()=>ChromeRequiemV14Boot.bridge.flush()')
    stored=first.evaluate('()=>Object.fromEntries(window.__testStorage)')
    first.close()
    second=openpage(stored)
    assert second.evaluate('()=>ChromeRequiemV14Boot.runtime.load(0)') is True
    restored=second.evaluate("""()=>({active:CR14MultiStageOperations.active,shape:Game.arenaShapeV14,
      credits:Game.credits,history:Game.missionHistory.length,clock:[Game.day,Game.hour],
      checkpoint:CR14MultiStageOperations.exportCheckpoint()})""")
    assert restored['active']['index']==2 and restored['active']['intelExtracted'] and not restored['active']['extractionRerouted'],restored
    assert restored['shape']=='entrance' and restored['credits']==initial['credits'] and restored['history']==0 and restored['clock']==initial['clock'],restored
    assert restored['checkpoint']['intelExtracted'] and not restored['checkpoint']['extractionRerouted'],restored
    end=second.evaluate("""()=>{const m=Game.activeMission;Game.objective.completed=true;Game.objective.exfilReady=true;
      for(const u of Game.units.filter(x=>x.team==='enemy')){u.hp=0;u.dead=true;const c=Game.grid.find(v=>v.unit===u);if(c)c.unit=null;}
      checkWinLose();return {credits:Game.credits,history:Game.missionHistory.filter(x=>x.id===m.id),
        journal:Game.journal.filter(j=>j.id==='intel_'+m.id),active:CR14MultiStageOperations.active,
        checkpoint:CR14MultiStageOperations.exportCheckpoint()};}""")
    assert end['credits']==initial['credits']+780 and len(end['history'])==1 and end['history'][0]['reward']==780,end
    assert len(end['journal'])==1 and end['active'] is None and end['checkpoint'] is None,end
    again=second.evaluate("""()=>{checkWinLose();return {credits:Game.credits,history:Game.missionHistory.filter(x=>x.id==='intel_choice_qa').length}}""")
    assert again['credits']==end['credits'] and again['history']==1,again
    second.close()
    # Control: choosing the maintenance route locks intel and preserves the base payout.
    third=openpage();base=third.evaluate(start);choice=position(third,'route');assert 'REROUTE' in (choice['label'] or ''),choice
    routed=third.evaluate("""()=>{const u=Game.selectedUnit;const a=objectiveActionAvailable(u);a.run();return CR14MultiStageOperations.active;}""")
    assert routed['extractionRerouted'] and not routed['intelExtracted'],routed
    third.evaluate('()=>{Game.objective.completed=true;Game.objective.exfil=null;checkWinLose()}')
    assert third.evaluate('()=>Game.arenaShapeV14')=='corridor'
    routeEnd=third.evaluate("""()=>{Game.objective.completed=true;Game.objective.exfilReady=true;
      for(const u of Game.units.filter(x=>x.team==='enemy')){u.hp=0;u.dead=true;}
      checkWinLose();return{credits:Game.credits,h:Game.missionHistory.filter(x=>x.id==='intel_choice_qa').length};}""")
    assert routeEnd['credits']==base['credits']+600 and routeEnd['h']==1,routeEnd
    third.close()
    assert not errors,errors
    print('PASS PWA12.64 intel vs maintenance exfil, 1 AP Hacker action, checkpoint resume, one-time +180 intel payout and ledger, no premature time/reward; route path retains base payout')
    browser.close()
