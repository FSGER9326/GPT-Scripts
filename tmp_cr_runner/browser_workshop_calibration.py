from pathlib import Path
import sys, json, time
from playwright.sync_api import sync_playwright

ROOT=Path(sys.argv[1]).resolve()
BASE=sys.argv[2] if len(sys.argv)>2 else 'http://127.0.0.1:8765'
QA=ROOT/'qa'; QA.mkdir(exist_ok=True)
results=[]
def check(name,ok,details=None):
    row={'name':name,'ok':bool(ok),'details':details}
    results.append(row)
    print(('PASS' if ok else 'FAIL'),name, '' if details is None else json.dumps(details,ensure_ascii=False))
    if not ok: raise AssertionError(f'{name}: {details}')

def boot(page):
    errors=[]
    page.on('pageerror',lambda e: errors.append(str(e)))
    page.goto(BASE+'/',wait_until='domcontentloaded',timeout=60000)
    page.wait_for_function("window.ChromeRequiemV14Boot && window.ChromeRequiemV14Boot.ready===true",timeout=60000)
    page.wait_for_timeout(250)
    check('boot has no page errors',not errors,errors)
    return errors

def init_game(page):
    return page.evaluate("""() => {
      if(!Game.roster?.length){
        const ck=Object.keys(CLASSES||{})[0], bk=Object.keys(BACKGROUNDS||{})[0];
        startNewGame('QA_CAL',ck,bk);
      }
      Game.activeMission=null;
      Game.safehouse=Game.safehouse||{}; Game.safehouse.workshop=2;
      Game.credits=5000; Game.salvage=20;
      if(typeof Game.time==='number') Game.time=480;
      if(typeof Game.day==='number') Game.day=Math.max(1,Game.day||1);
      const u=Game.roster[0];
      if(!u.weapon){const wk=Object.keys(ITEMS).find(k=>ITEMS[k]?.type==='weapon');if(wk)u.weapon=wk}
      applySkillsToUnit(u);
      return {name:u.name,weapon:u.weapon,day:Game.day,time:Game.time,diag:runDiagnosticsV14Calibration()};
    }""")

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    ctx=browser.new_context(viewport={'width':412,'height':915},device_scale_factor=1)
    page=ctx.new_page(); boot(page); init=init_game(page)
    check('module diagnostics 8/8',init['diag']['passed']==init['diag']['total']==8,init['diag'])

    gate=page.evaluate("""() => {
      const api=WorkshopCalibrationV14,u=Game.roster[0],w=u.weapon;
      Game.safehouse.workshop=1; const blocked=api.canRefit(u,w,'breach');
      Game.safehouse.workshop=2; const allowed=api.canRefit(u,w,'breach');
      Game.activeMission={id:'qa-active'}; const missionBlocked=api.canRefit(u,w,'breach'); Game.activeMission=null;
      return {blocked,allowed,missionBlocked};
    }""")
    check('Workshop 1 blocks tactical calibration',not gate['blocked']['ok'],gate)
    check('Workshop 2 permits tactical calibration',gate['allowed']['ok'],gate)
    check('active mission blocks refit',not gate['missionBlocked']['ok'],gate)

    normal=page.evaluate("""async () => {
      const api=WorkshopCalibrationV14,u=Game.roster[0],w=u.weapon;
      Game.safehouse.workshop=2; Game.credits=5000; Game.salvage=20; Game.activeMission=null;
      if(typeof Game.time==='number')Game.time=480;
      applySkillsToUnit(u);
      const base={damage:u.damage,range:u.range,crit:u.critChance,move:u.move,armor:u.armor,maxAp:u.maxAp,apCost:(ITEMS[w]?.ap||ITEMS[w]?.apCost||null)};
      const q=api.quote(u,w,'breach'),credits0=Game.credits,salvage0=Game.salvage,day0=Game.day,time0=Game.time;
      const realAdvance=window.advanceTime; let seenMinutes=null;
      window.advanceTime=function(m){seenMinutes=m;return realAdvance(m)};
      const ok=api.setProfile(u,w,'breach'); window.advanceTime=realAdvance;
      const breach={damage:u.damage,range:u.range,crit:u.critChance,move:u.move,armor:u.armor,maxAp:u.maxAp};
      const credits1=Game.credits,salvage1=Game.salvage,day1=Game.day,time1=Game.time;
      const snap=JSON.stringify(breach); applySkillsToUnit(u); const repeat1=JSON.stringify({damage:u.damage,range:u.range,crit:u.critChance,move:u.move,armor:u.armor,maxAp:u.maxAp}); applySkillsToUnit(u); const repeat2=JSON.stringify({damage:u.damage,range:u.range,crit:u.critChance,move:u.move,armor:u.armor,maxAp:u.maxAp});
      const alt=Object.keys(ITEMS).find(k=>ITEMS[k]?.type==='weapon'&&k!==w); let away=null,back=null;
      if(alt){u.weapon=alt;applySkillsToUnit(u);away=api.currentProfileId(u,alt);u.weapon=w;applySkillsToUnit(u);back=api.currentProfileId(u,w)}
      return {w,base,q,ok,breach,credits0,credits1,salvage0,salvage1,seenMinutes,day0,time0,day1,time1,snap,repeat1,repeat2,alt,away,back};
    }""")
    check('BREACH installs',normal['ok'],normal)
    check('exact quoted credits spent',normal['credits0']-normal['credits1']==normal['q']['credits'],normal)
    check('exact quoted salvage spent',normal['salvage0']-normal['salvage1']==normal['q']['salvage'],normal)
    check('refit calls normal action-time with exact minutes',normal['seenMinutes']==normal['q']['minutes'],normal)
    check('BREACH exact derived delta',normal['breach']['damage']==normal['base']['damage']+2 and normal['breach']['range']==max(1,normal['base']['range']-1) and normal['breach']['crit']==max(0,normal['base']['crit']-5),normal)
    check('BREACH leaves non-target stats unchanged',normal['breach']['move']==normal['base']['move'] and normal['breach']['armor']==normal['base']['armor'] and normal['breach']['maxAp']==normal['base']['maxAp'],normal)
    check('derived recalculation is idempotent',normal['snap']==normal['repeat1']==normal['repeat2'],normal)
    if normal['alt']:
        check('calibration is per weapon when equipped away',normal['away']=='field',normal)
        check('calibration returns when weapon re-equipped',normal['back']=='breach',normal)

    swaps=page.evaluate("""() => {
      const api=WorkshopCalibrationV14,u=Game.roster[0],w=u.weapon;
      Game.credits=5000;Game.salvage=20;Game.safehouse.workshop=2;Game.activeMission=null;
      applySkillsToUnit(u);
      const breach={damage:u.damage,range:u.range,crit:u.critChance};
      const qP=api.quote(u,w,'precision'); const okP=api.setProfile(u,w,'precision');
      const precision={damage:u.damage,range:u.range,crit:u.critChance,id:api.currentProfileId(u,w),stored:{...(u.weaponCalibrationV14||{})}};
      const okF=api.setProfile(u,w,'field');
      const field={damage:u.damage,range:u.range,crit:u.critChance,id:api.currentProfileId(u,w),stored:{...(u.weaponCalibrationV14||{})}};
      return {breach,qP,okP,precision,okF,field};
    }""")
    check('PRECISION replaces BREACH',swaps['okP'] and swaps['precision']['id']=='precision',swaps)
    check('profiles do not stack',swaps['precision']['damage']==swaps['field']['damage']-1 and swaps['precision']['range']==swaps['field']['range']+1 and swaps['precision']['crit']==swaps['field']['crit']+6,swaps)
    check('FIELD ZERO removes stored weapon entry',swaps['okF'] and swaps['field']['id']=='field' and len(swaps['field']['stored'])==0,swaps)

    attach=page.evaluate("""() => {
      const api=WorkshopCalibrationV14,u=Game.roster[0],w=u.weapon;
      Game.credits=5000;Game.salvage=20;Game.safehouse.workshop=2;Game.activeMission=null;
      api.setProfile(u,w,'breach'); applySkillsToUnit(u); const before={d:u.damage,r:u.range,c:u.critChance};
      Game.armory=Game.armory||{};Game.armory.attachments=Game.armory.attachments||{};
      let installed=null;
      if(typeof V11_ATTACHMENTS==='object'&&typeof installAttachmentV11==='function'){
        for(const id of Object.keys(V11_ATTACHMENTS)){
          Game.armory.attachments[id]=Math.max(1,Game.armory.attachments[id]||0);
          try{if(installAttachmentV11(u,id)){installed=id;break}}catch(e){}
        }
      }
      applySkillsToUnit(u); const withA={d:u.damage,r:u.range,c:u.critChance,profile:api.currentProfileId(u,w)};
      if(installed&&typeof removeAttachmentV11==='function')removeAttachmentV11(u,V11_ATTACHMENTS[installed]?.slot||installed);
      applySkillsToUnit(u); const removed={d:u.damage,r:u.range,c:u.critChance,profile:api.currentProfileId(u,w)};
      return {installed,before,withA,removed};
    }""")
    check('attachment flow preserves calibration identity',attach['withA']['profile']=='breach' and attach['removed']['profile']=='breach',attach)
    if attach['installed']:
        check('attachment equip/remove changes or restores derived weapon state',attach['withA']!=attach['removed'],attach)

    save=page.evaluate("""async () => {
      const api=WorkshopCalibrationV14,u=Game.roster[0],w=u.weapon;Game.credits=5000;Game.salvage=20;Game.safehouse.workshop=2;Game.activeMission=null;
      if(api.currentProfileId(u,w)!=='breach'){ if(api.currentProfileId(u,w)!=='field')api.setProfile(u,w,'field'); api.setProfile(u,w,'breach'); }
      applySkillsToUnit(u); const expected={id:api.currentProfileId(u,w),d:u.damage,r:u.range,c:u.critChance};
      const saveResult=saveGame(1,true); const beforeKeys={};for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);beforeKeys[k]=localStorage.getItem(k)}
      u.weaponCalibrationV14[w]='precision';applySkillsToUnit(u);
      const loadResult=await Promise.resolve(loadGame(1)); await new Promise(r=>setTimeout(r,100));
      const lu=Game.roster[0];applySkillsToUnit(lu); const restored={id:api.currentProfileId(lu,lu.weapon),d:lu.damage,r:lu.range,c:lu.critChance,hasMirror:Object.prototype.hasOwnProperty.call(lu,'calibrationProfileV14')};
      return {expected,saveResult,loadResult,restored,keys:Object.keys(beforeKeys)};
    }""")
    check('save/load restores calibration',save['restored']['id']==save['expected']['id'] and save['restored']['d']==save['expected']['d'] and save['restored']['r']==save['expected']['r'] and save['restored']['c']==save['expected']['c'],save)
    check('serialized runtime has one calibration authority',not save['restored']['hasMirror'],save)

    combat=page.evaluate("""() => {
      const api=WorkshopCalibrationV14,u=Game.roster[0];applySkillsToUnit(u);
      let err=null,unit=null,returned=null;
      const mission={id:'qa-calibration-bridge',name:'Calibration Bridge',difficulty:1,reward:0,enemyCount:1,enemyTypes:['raider']};
      try{if(typeof buildGrid==='function')buildGrid(mission);returned=createCombatUnits(mission);const arr=Array.isArray(returned)?returned:(Game.units||Game.combatUnits||[]);unit=arr.find(x=>x.name===u.name||x.rosterId===u.id||x.sourceId===u.id||x.team==='player'||x.faction==='player')||arr[0]||null}catch(e){err=String(e)}
      return {err,roster:{name:u.name,id:u.id,damage:u.damage,range:u.range,crit:u.critChance},unit:unit?{name:unit.name,id:unit.id,damage:unit.damage,range:unit.range,crit:unit.critChance,team:unit.team,faction:unit.faction}:null,returnedType:Array.isArray(returned)?'array':typeof returned};
    }""")
    check('combat-unit bridge executes',combat['err'] is None and combat['unit'] is not None,combat)
    check('combat unit inherits calibrated weapon stats',combat['unit']['damage']==combat['roster']['damage'] and combat['unit']['range']==combat['roster']['range'] and combat['unit']['crit']==combat['roster']['crit'],combat)

    ui=page.evaluate("""() => {
      Game.selectedCrewIndex=0;Game.crewTab='inventory';showScreen('crew');const body=document.getElementById('crew-body');body.innerHTML='';renderInventory(body);
      const panel=body.querySelector('.v14-calibration-panel'),cards=[...body.querySelectorAll('.v14-cal-card')],buttons=[...body.querySelectorAll('.v14-cal-card button')];
      const pr=panel?.getBoundingClientRect();return {panel:!!panel,cards:cards.length,buttons:buttons.length,panelWidth:pr?.width||0,viewport:document.documentElement.clientWidth,docScroll:document.documentElement.scrollWidth,bodyScroll:body.scrollWidth,bodyClient:body.clientWidth,buttonHeights:buttons.map(b=>b.getBoundingClientRect().height)};
    }""")
    check('Pixel 7 workshop panel renders all profiles',ui['panel'] and ui['cards']==3 and ui['buttons']==3,ui)
    check('Pixel 7 has zero horizontal overflow',ui['docScroll']<=ui['viewport'] and ui['bodyScroll']<=ui['bodyClient']+1,ui)
    check('Pixel 7 calibration buttons are >=44px',min(ui['buttonHeights'] or [0])>=44,ui)
    page.screenshot(path=str(QA/'pwa12-104-workshop-calibration-mobile.png'),full_page=True)
    ctx.close()

    # Failure-path context: pre-commit rollback then post-commit lockout.
    ctx2=browser.new_context(viewport={'width':1280,'height':800}); page2=ctx2.new_page(); boot(page2); init_game(page2)
    failures=page2.evaluate("""() => {
      const api=WorkshopCalibrationV14,u=Game.roster[0],w=u.weapon;Game.safehouse.workshop=2;Game.credits=5000;Game.salvage=20;Game.activeMission=null;
      if(api.currentProfileId(u,w)!=='field'){u.weaponCalibrationV14={};applySkillsToUnit(u)}
      const c0=Game.credits,s0=Game.salvage,id0=api.currentProfileId(u,w),realApply=window.applySkillsToUnit;
      window.applySkillsToUnit=function(){throw new Error('qa-precommit')}; const preResult=api.setProfile(u,w,'breach'); window.applySkillsToUnit=realApply;
      const pre={result:preResult,credits:Game.credits,salvage:Game.salvage,id:api.currentProfileId(u,w),expected:{c0,s0,id0}};
      const realAdvance=window.advanceTime; let q=api.quote(u,w,'breach'); window.advanceTime=function(){throw new Error('qa-time')}; const postResult=api.setProfile(u,w,'breach'); window.advanceTime=realAdvance;
      const post={result:postResult,credits:Game.credits,salvage:Game.salvage,id:api.currentProfileId(u,w),faulted:api.isTimeFaulted(),next:api.canRefit(u,w,'precision'),q};
      return {pre,post};
    }""")
    check('pre-commit derived-stat failure rolls back resources/profile',failures['pre']['result'] is False and failures['pre']['credits']==failures['pre']['expected']['c0'] and failures['pre']['salvage']==failures['pre']['expected']['s0'] and failures['pre']['id']==failures['pre']['expected']['id0'],failures)
    check('post-commit time failure keeps installed refit and costs',failures['post']['result'] is True and failures['post']['id']=='breach' and failures['post']['credits']==failures['pre']['expected']['c0']-failures['post']['q']['credits'] and failures['post']['salvage']==failures['pre']['expected']['s0']-failures['post']['q']['salvage'],failures)
    check('time-processing fault locks further refits until reload',failures['post']['faulted'] and not failures['post']['next']['ok'] and 'locked' in failures['post']['next']['reason'].lower(),failures)
    ctx2.close();browser.close()

report={'passed':sum(1 for r in results if r['ok']),'total':len(results),'results':results}
(QA/'pwa12-104-workshop-calibration-browser.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('BROWSER_QA',json.dumps({'passed':report['passed'],'total':report['total']}))
