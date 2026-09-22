from pathlib import Path
import json, os
from playwright.sync_api import sync_playwright

BASE=os.environ.get('CR_BASE_URL','http://127.0.0.1:8765')
OUT=Path(os.environ.get('CR_QA_DIR','qa'))
OUT.mkdir(parents=True,exist_ok=True)

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={"width":390,"height":844})
    errors=[]
    page.on('pageerror',lambda e: errors.append(str(e)))
    page.goto(BASE,wait_until='domcontentloaded',timeout=60000)
    page.wait_for_function("typeof Game!=='undefined' && typeof window.assignRecoverySupportV14==='function' && typeof window.startRecoveryV14==='function'",timeout=60000)
    page.evaluate("""() => {
      const lead={name:'LEAD',className:'Agent',v135RosterId:'qa:lead',loyalty:6,injuries:[],traits:[]};
      const patient={name:'MOTH',className:'Hacker',v135RosterId:'qa:moth',loyalty:2,injuries:['broken_arm'],traits:[],originFaction:'chrome',originContactId:'c-med'};
      const bonded={name:'ROOK',className:'Heavy',v135RosterId:'qa:rook',loyalty:4,injuries:[],traits:[],originFaction:'iron',originContactId:'c-other'};
      const strained={name:'VALE',className:'Sniper',v135RosterId:'qa:vale',loyalty:3,injuries:[],traits:[],originFaction:'meridian',originContactId:'c-vale'};
      Game.roster=[lead,patient,bonded,strained];Game.day=1;
      Game.companyV135={...(Game.companyV135||{}),activeIds:['qa:lead','qa:moth','qa:rook','qa:vale'],reserveIds:[],recoveryV14:{version:1,cases:{},history:[]},recoverySupportV14:{version:1,assignments:{},history:[]}};
      window.migrateCompanyRosterV135?.();
      const c=window.ensureCompanyStateV135();c.activeIds=['qa:lead','qa:moth','qa:rook','qa:vale'];c.reserveIds=[];
    }""")
    start=page.evaluate("""() => {const u=Game.roster.find(x=>x.v135RosterId==='qa:moth');const c=window.startRecoveryV14(u);const co=window.ensureCompanyStateV135();return {due:c?.dueDay,active:co.activeIds.slice(),reserve:co.reserveIds.slice()}}""")
    assert isinstance(start['due'],(int,float)) and start['due']>2,start
    assert 'qa:moth' not in start['active'] and 'qa:moth' in start['reserve'],start
    original_due=start['due']
    candidates=page.evaluate("""() => window.recoverySupportCandidatesV14('qa:moth').map(x=>({id:x.id,name:x.u.name,bonded:x.bonded,strained:x.strained,reason:x.reason,loyalty:x.loyalty}))""")
    assert any(x['id']=='qa:rook' and x['bonded'] for x in candidates),candidates
    assert any(x['id']=='qa:vale' and x['strained'] for x in candidates),candidates
    page.evaluate("""() => window.openSafehouse()""")
    page.wait_for_selector('#v14-recovery-panel',timeout=10000)
    page.evaluate("""() => window.renderRecoverySupportV14()""")
    panel=page.locator('#v14-recovery-support')
    assert panel.count()==1
    select=panel.locator('select')
    button=panel.locator('button')
    assert select.count()==1 and button.count()==1
    sb=select.bounding_box();bb=button.bounding_box()
    assert sb and sb['height']>=44,sb
    assert bb and bb['height']>=44,bb
    assert not page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
    select.select_option('qa:rook')
    page.screenshot(path=str(OUT/'pwa12-142-recovery-bonds-mobile-choice.png'),full_page=True)
    button.click()
    page.wait_for_function("!!window.recoverySupportAssignmentV14('qa:moth')")
    assigned=page.evaluate("""() => {const a=window.recoverySupportAssignmentV14('qa:moth'),c=window.recoveryCaseV14(Game.roster.find(x=>x.v135RosterId==='qa:moth')),co=window.ensureCompanyStateV135();return{a,c,active:co.activeIds.slice(),reserve:co.reserveIds.slice()}}""")
    assert assigned['c']['dueDay']==original_due-1,assigned
    assert assigned['a']['helperId']=='qa:rook' and assigned['a']['bonded'] and not assigned['a']['strained'],assigned
    assert 'qa:rook' not in assigned['active'] and 'qa:rook' in assigned['reserve'],assigned
    assigned_due=assigned['c']['dueDay']
    deploy=page.evaluate("""() => window.deployableActiveCrewV135().map(x=>x.v135RosterId)""")
    assert 'qa:moth' not in deploy and 'qa:rook' not in deploy,deploy
    forced=page.evaluate("""() => {const c=window.ensureCompanyStateV135();c.activeIds.push('qa:rook');c.reserveIds=c.reserveIds.filter(x=>x!=='qa:rook');window.normalizeRecoverySupportV14();return{active:c.activeIds.slice(),reserve:c.reserveIds.slice()}}""")
    assert 'qa:rook' not in forced['active'] and 'qa:rook' in forced['reserve'],forced
    briefing=page.evaluate("""() => {let b=document.getElementById('v10-brief-body');if(!b){document.body.insertAdjacentHTML('beforeend','<div id="v10-brief-body"><div class="v10-brief-actions"></div></div>');b=document.getElementById('v10-brief-body')}else b.innerHTML='<div class="v10-brief-actions"></div>';window.decorateRecoverySupportBriefingV14();return b.innerText}""")
    assert 'RECOVERY DETAIL' in briefing and 'ROOK' in briefing and 'MOTH' in briefing,briefing
    page.evaluate("""async () => {await Promise.resolve(window.saveGame(0,true));const s=window.ensureRecoverySupportV14();s.assignments={};await Promise.resolve(window.loadGame(0));await new Promise(r=>setTimeout(r,100));}""")
    page.wait_for_function("!!window.recoverySupportAssignmentV14('qa:moth')",timeout=10000)
    restored=page.evaluate("""() => window.recoverySupportAssignmentV14('qa:moth')""")
    assert restored and restored['helperId']=='qa:rook',restored
    result=page.evaluate("""due => {Game.day=due;window.processRecoveryV14(due);window.normalizeRecoverySupportV14();const rook=Game.roster.find(x=>x.v135RosterId==='qa:rook'),moth=Game.roster.find(x=>x.v135RosterId==='qa:moth'),c=window.ensureCompanyStateV135();return{rookLoyalty:rook.loyalty,mothInjuries:moth.injuries.slice(),active:c.activeIds.slice(),assignment:window.recoverySupportAssignmentV14('qa:moth')}}""",assigned_due)
    assert result['rookLoyalty']==4,result
    assert 'broken_arm' not in result['mothInjuries'] and result['assignment'] is None,result
    assert 'qa:rook' in result['active'],result
    strained=page.evaluate("""() => {const moth=Game.roster.find(x=>x.v135RosterId==='qa:moth'),vale=Game.roster.find(x=>x.v135RosterId==='qa:vale'),co=window.ensureCompanyStateV135();moth.injuries=['broken_arm'];if(!co.activeIds.includes('qa:moth'))co.activeIds.push('qa:moth');co.reserveIds=co.reserveIds.filter(x=>x!=='qa:moth');Game.day=10;const c=window.startRecoveryV14(moth);const a=window.assignRecoverySupportV14('qa:moth','qa:vale');return{caseDue:c?.dueDay,assigned:a,valeLoyalty:vale.loyalty}}""")
    assert strained['assigned'] and strained['assigned']['strained'],strained
    assert strained['assigned']['dueDay']==strained['caseDue']-1,strained
    strained_due=strained['assigned']['dueDay']
    end=page.evaluate("""due => {Game.day=due;window.processRecoveryV14(due);window.normalizeRecoverySupportV14();const vale=Game.roster.find(x=>x.v135RosterId==='qa:vale'),s=window.ensureRecoverySupportV14();return{loyalty:vale.loyalty,history:s.history.slice(0,4),assignment:window.recoverySupportAssignmentV14('qa:moth')}}""",strained_due)
    assert end['loyalty']==2,end
    assert end['assignment'] is None,end
    assert any(x.get('helperId')=='qa:vale' and x.get('outcome')=='recovered' and x.get('loyaltyChange')==-1 for x in end['history']),end
    diag=page.evaluate("window.runDiagnosticsRecoverySupportV14()")
    assert diag['passed']==diag['total'],diag
    relevant_errors=[e for e in errors if 'recovery bonds' in e.lower()]
    assert not relevant_errors,relevant_errors
    browser.close()

print(json.dumps({'status':'PASS','viewport':'390x844','standard_due_day':original_due,'bonded_due_day':assigned_due,'verified':['relationship-gated helper candidates','choice UI reachability','dual roster exclusion','forced reserve normalization','mission briefing consequence','slot save/load restoration','bonded no-cost completion','strained -1 loyalty completion','44px mobile controls','no horizontal overflow']},indent=2))
