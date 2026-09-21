"""Real Chromium: completed-area checkpoint survives fresh runtime and preserves economics."""
from pathlib import Path
import mimetypes
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text(encoding='utf-8').replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
def document(storage):
    shim="""<script>const __s=new Map(Object.entries(%s));const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});window.__testStorage=__s;</script>""" % json.dumps(storage)
    return HTML.replace('<head>','<head><base href="http://cr.local/">'+shim,1)
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    context=browser.new_context(viewport={'width':1280,'height':850})
    errors=[]
    def route(r):
        path=r.request.url.split('http://cr.local/',1)[-1].split('?',1)[0] or 'index.html'
        fp=ROOT/path
        return r.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream') if fp.is_file() else r.fulfill(status=404,body=b'not found')
    context.route('http://cr.local/**',route)
    first=context.new_page();first.on('pageerror',lambda e:errors.append(str(e)))
    first.set_content(document({}),wait_until='domcontentloaded')
    first.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
    before=first.evaluate("""()=>{
      startNewGame('Checkpoint QA','Hacker','street');
      document.getElementById('story-modal')?.classList.remove('open');
      showScreen('combat');
      const m={id:'checkpoint_qa_61',type:'heist',objective:'heist',_v12ObjectiveAssigned:true,
        name:'Blacksite archive',desc:'Test case',contact:null,diff:2,
        enemies:['Guard','Enforcer','Drone'],reward:600,xp:70,targetFaction:'meridian',
        factionRepGain:0,factionRepLoss:{}};
      Game.activeMission=m;initCombat(m);
      const u=Game.units.find(x=>x.team==='player');u.hp=61;
      u.statuses={marked:2};u.inventory={...u.inventory,qaPayload:3};
      Game.alerted=true;
      // Complete a full perimeter stage and enter the next area: the checkpoint
      // is created only after the stage boundary has been entered successfully.
      Game.objective.completed=true;checkWinLose();
      return {credits:Game.credits,clock:[Game.day,Game.hour],history:Game.missionHistory.length,
        op:CR14MultiStageOperations.active,stage:Game.arenaShapeV14,
        hp:Game.units.find(x=>x.team==='player').hp,
        inventory:Game.units.find(x=>x.team==='player').inventory.qaPayload,
        marked:Game.units.find(x=>x.team==='player').statuses.marked};
    }""")
    assert before['op']['index']==1 and before['stage']=='rooms' and before['hp']==61,before
    first.evaluate('()=>ChromeRequiemV14Boot.bridge.flush()')
    envelope=first.evaluate("""async()=>{
      const e=await ChromeRequiemV14Boot.bridge.resolveEnvelope(0);
      return {stage:e?.payload?.operationCheckpointV14?.index,mission:e?.payload?.operationCheckpointV14?.mission?.id,
        crew:e?.payload?.operationCheckpointV14?.crew};
    }""")
    assert envelope['stage']==1 and envelope['mission']=='checkpoint_qa_61',envelope
    saved=first.evaluate('()=>Object.fromEntries(window.__testStorage)')
    first.close()
    # New browser tab, new JS runtime, same origin-backed IndexedDB/localStorage.
    second=context.new_page();second.on('pageerror',lambda e:errors.append(str(e)))
    second.set_content(document(saved),wait_until='domcontentloaded')
    second.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
    loaded=second.evaluate('()=>ChromeRequiemV14Boot.runtime.load(0)')
    assert loaded is True,loaded
    after=second.evaluate("""()=>({credits:Game.credits,clock:[Game.day,Game.hour],
      history:Game.missionHistory.length,op:CR14MultiStageOperations.active,
      stage:Game.arenaShapeV14,hp:Game.units.find(x=>x.team==='player').hp,
      inventory:Game.units.find(x=>x.team==='player').inventory.qaPayload,
      marked:Game.units.find(x=>x.team==='player').statuses.marked,
      activeMission:Game.activeMission?.id,enemies:Game.units.filter(u=>u.team==='enemy').length})""")
    assert after['op']['index']==1 and after['stage']=='rooms' and after['activeMission']=='checkpoint_qa_61',after
    for k in ('credits','clock','history','hp','inventory','marked'):
        assert before[k]==after[k],(k,before,after)
    assert after['enemies']==4 and before['op']['securitySuppressed'] is False,after
    (ROOT/'qa').mkdir(exist_ok=True)
    second.screenshot(path=str(ROOT/'qa/pwa12-61-resumed-interior.png'))
    # Extraction-choice consequences must survive another checkpoint generation.
    second.evaluate("""()=>{
      const c=Game.grid.find(v=>v.operationRouteConsoleV14);const u=Game.units.find(v=>v.team==='player');
      const from=Game.grid.find(v=>v.unit===u);if(from)from.unit=null;
      u.x=c.x;u.y=c.y;Game.grid.find(v=>v.x===u.x&&v.y===u.y).unit=u;
      Game.selectedUnit=u;Game.turn='player';u.ap=3;
      const a=objectiveActionAvailable(u);if(!a||!a.run())throw Error('route unavailable');
      Game.objective.completed=true;Game.objective.exfil=null;checkWinLose();
    }""")
    assert second.evaluate('()=>CR14MultiStageOperations.active?.index===2 && CR14MultiStageOperations.active.extractionRerouted && Game.arenaShapeV14==="corridor"')
    second.evaluate('()=>ChromeRequiemV14Boot.bridge.flush()')
    saved=second.evaluate('()=>Object.fromEntries(window.__testStorage)')
    second.close()
    third=context.new_page();third.on('pageerror',lambda e:errors.append(str(e)))
    third.set_content(document(saved),wait_until='domcontentloaded')
    third.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
    assert third.evaluate('()=>ChromeRequiemV14Boot.runtime.load(0)') is True
    ex=third.evaluate("""()=>({stage:CR14MultiStageOperations.active?.index,
      rerouted:CR14MultiStageOperations.active?.extractionRerouted,
      shape:Game.arenaShapeV14,credits:Game.credits,history:Game.missionHistory.length,
      hp:Game.units.find(x=>x.team==='player').hp,clock:[Game.day,Game.hour]})""")
    assert ex['stage']==2 and ex['rerouted'] and ex['shape']=='corridor',ex
    assert ex['credits']==before['credits'] and ex['history']==before['history'] and ex['clock']==before['clock'] and ex['hp']==61,ex
    third.screenshot(path=str(ROOT/'qa/pwa12-61-resumed-extraction.png'))
    # Final completion must pay once and remove the durable operation checkpoint.
    result=third.evaluate("""()=>{
      const m=Game.activeMission;Game.objective.completed=true;Game.objective.exfilReady=true;
      for(const u of Game.units.filter(x=>x.team==='enemy')){u.hp=0;u.dead=true;const c=Game.grid.find(v=>v.unit===u);if(c)c.unit=null;}
      checkWinLose();return {payout:Game.credits,history:Game.missionHistory.filter(x=>x.id===m.id).length,
        checkpoint:CR14MultiStageOperations.exportCheckpoint(),active:CR14MultiStageOperations.active};
    }""")
    assert result['payout']==before['credits']+600 and result['history']==1 and result['checkpoint'] is None and result['active'] is None,result
    assert not errors,errors
    print('PASS PWA12.61 fresh-runtime fallback checkpoint resume: area 2 and 3, alarm/HP/status/inventory/route, single payout, unchanged world time')
    third.close();browser.close()
