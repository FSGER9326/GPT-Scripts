"""Real Chromium reachability, inherited route leverage, persistence and mobile layout for RECONCILIATION WINDOW."""
from pathlib import Path
import mimetypes, os
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'qa'/'pwa12_136_reconciliation_window';QA.mkdir(parents=True,exist_ok=True)
HTML=(ROOT/'index.html').read_text(encoding='utf-8')
SHIM="""<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"""
HTML=HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1).replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')

def serve(route):
    url=route.request.url
    if not url.startswith('http://cr.local/'): return route.abort()
    rel=url[len('http://cr.local/'):].split('?',1)[0] or 'index.html';fp=ROOT/rel
    if fp.is_file(): route.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream')
    else: route.fulfill(status=404,body=b'NOT FOUND')

cases=[
    ('desktop',{'width':1440,'height':900},'civic','c9','civic_circuit','loc_contact_c9','loc_civic_surplus',0,'quiet_census_clean_access','follow_principal',0),
    ('mobile',{'width':390,'height':844},'market','c23','old_market','loc_contact_c23','loc_old_hidden_1',1,'quiet_census_public_proof','burn_source_map',1),
]
only=os.environ.get('CR_RECONCILIATION_VIEWPORT');cases=[c for c in cases if not only or c[0]==only]
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'])
    for label,viewport,branch,contact_id,district,contact_loc,qc_loc,qc_button,modifier,decision,rw_button in cases:
        ctx=browser.new_context(viewport=viewport,device_scale_factor=1);p=ctx.new_page();errors=[]
        p.on('pageerror',lambda e:errors.append(str(e)));p.route('http://cr.local/**',serve)
        p.set_content(HTML,wait_until='domcontentloaded');p.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
        setup=p.evaluate(f'''()=>{{
          startNewGame('Reconciliation QA','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');
          activateDistrictV133('old_market',null);const mira=Game.contacts.find(c=>c.id==='c1');Game.ovPlayer={{x:mira.x,y:mira.y}};
          const hood=generateDistrictV133('old_market').neighborhoods[0];ensureNeighborhoodStateV134(generateDistrictV133('old_market'));
          const clash={{id:'qa_rw_clash_{label}',name:'Street Clash · Old Market',sectorId:'old_market',contact:'c1',v134StreetEncounter:true,v134StreetActorType:'security',v134StreetNeighborhood:hood.id,v134ContactSupport:{{id:'c1',name:'MIRA',tier:2,label:'LOCAL BACKUP'}}}};
          Game.missionHistory.push({{...clash,day:Game.day}});if(!CR14MarketEyesV14.registerStreetWin(clash))throw new Error('Market Eyes did not queue');
          const pending=CR14MarketEyesV14.pending();if(!CR14MarketEyesV14.resolveChoice(pending,'trace'))throw new Error('Market Eyes trace choice failed');
          const job=CR14MarketEyesV14.ensureMission();if(!job)throw new Error('SECOND ANGLE missing');Game.missionHistory.push({{...job,day:Game.day}});Events.emit('mission:success',job);
          activateDistrictV133('{district}',null);const cw=generateDistrictV133('{district}'),cp=cw.locations['{contact_loc}'];Game.ovPlayer={{x:cp.x,y:cp.y}};Game.cityLife.currentLocation='{contact_loc}';renderContactDossierV13('{contact_id}');showScreen('v13-contact-screen');
          return {{paperLead:CR14PaperGhostsV14.lead()?.id,paperButtons:[...document.querySelectorAll('.v14-paper-choice')].filter(b=>!b.disabled).length}};
        }}''')
        assert setup['paperLead'] and setup['paperButtons']==1,(label,setup)
        p.locator('.v14-paper-choice').click();p.wait_for_timeout(80)
        paper=p.evaluate(f'''()=>({{branch:CR14PaperGhostsV14.resolution()?.branch,quiet:CR14QuietCensusV14.lead()?.id||null,discovered:!!Game.cityLife.discovered['{qc_loc}']}})''')
        assert paper['branch']==branch and paper['quiet'] and paper['discovered'],(label,paper)
        qc_local=p.evaluate(f'''()=>{{
          activateDistrictV133('{district}',null);const w=generateDistrictV133('{district}'),pt=w.locations['{qc_loc}'];Game.ovPlayer={{x:pt.x,y:pt.y}};Game.cityLife.currentLocation='{qc_loc}';renderDistrictHubV13('{district}');showScreen('v13-city-life-screen');CR14QuietCensusV14.renderLocationCase();
          return {{at:CR14QuietCensusV14.atTarget('{branch}'),enabled:[...document.querySelectorAll('.v14-qc-choice')].filter(b=>!b.disabled).length}};
        }}''')
        assert qc_local['at'] and qc_local['enabled']==2,(label,qc_local)
        p.locator('.v14-qc-choice').nth(qc_button).click();p.wait_for_timeout(100)
        qc=p.evaluate('''()=>({out:CR14QuietCensusV14.resolution(),rwLead:CR14ReconciliationWindowV14.ensureLead()})''')
        assert qc['out']['nextModifier']==modifier and qc['out']['nextHook']=='quiet_census_reconciliation_window',(label,qc)
        assert qc['rwLead'] and qc['rwLead']['locationId']=='loc_helix_hidden_1',(label,qc)
        remote=p.evaluate('''()=>{
          activateDistrictV133('helix_financial',null);Game.ovPlayer={x:1,y:1};Game.cityLife.currentLocation='loc_helix_hidden_1';renderDistrictHubV13('helix_financial');showScreen('v13-city-life-screen');CR14ReconciliationWindowV14.renderLocationCase();
          const card=document.querySelector('.v14-reconciliation-window');return {at:CR14ReconciliationWindowV14.atTarget(),text:card?.textContent||'',enabled:[...card?.querySelectorAll('button')||[]].filter(b=>!b.disabled).length,discovered:!!Game.cityLife.discovered.loc_helix_hidden_1};
        }''')
        assert remote['discovered'] and not remote['at'] and 'RECONCILIATION WINDOW' in remote['text'] and remote['enabled']==0,(label,remote)
        local=p.evaluate('''()=>{
          const w=generateDistrictV133('helix_financial'),pt=w.locations.loc_helix_hidden_1;Game.ovPlayer={x:pt.x,y:pt.y};Game.cityLife.currentLocation='loc_helix_hidden_1';renderDistrictHubV13('helix_financial');showScreen('v13-city-life-screen');CR14ReconciliationWindowV14.renderLocationCase();
          const card=document.querySelector('.v14-reconciliation-window'),r=card.getBoundingClientRect(),buttons=[...card.querySelectorAll('button')];return {at:CR14ReconciliationWindowV14.atTarget(),enabled:buttons.filter(b=>!b.disabled).length,text:card.textContent,right:r.right,left:r.left,width:r.width,screenWidth:document.querySelector('#v13-city-life-screen').scrollWidth,windowWidth:innerWidth,buttonHeights:buttons.map(b=>b.getBoundingClientRect().height)};
        }''')
        assert local['at'] and local['enabled']==2 and 'RECONCILIATION WINDOW' in local['text'],(label,local)
        assert local['right']<=local['windowWidth']+1 and local['left']>=-1,(label,local)
        assert all(h>=44 for h in local['buttonHeights']),(label,local)
        if label=='mobile': assert local['screenWidth']<=local['windowWidth']+1,(label,local)
        p.screenshot(path=str(QA/f'reconciliation-window-{branch}-{label}-choice.png'),full_page=True)
        pre=p.evaluate('''()=>({heat:Game.heat.meridian,hour:Game.hour})''')
        p.locator('.v14-rw-choice').nth(rw_button).click();p.wait_for_timeout(100)
        result=p.evaluate('''()=>({out:CR14ReconciliationWindowV14.resolution(),heat:Game.heat.meridian,text:document.querySelector('.v14-reconciliation-window')?.textContent||''})''')
        out=result['out'];assert out and out['decision']==decision and out['accessModifier']==modifier,(label,result)
        assert out['contractorName']=='QUIET CENSUS CIVIC ANALYTICS' and 'SETTLEMENT RECORD' in result['text'],(label,result)
        if decision=='follow_principal':
            assert out['principalTrace'] is True and out['sourceMapBurned'] is False and out['sourceProtection']=='exposed' and out['nextHook']=='quiet_census_principal_trace',(label,out)
            assert result['heat']==min(100,pre['heat']+2),(label,pre,result)
        else:
            assert out['principalTrace'] is False and out['sourceMapBurned'] is True and out['sourceProtection']=='hardened' and out['nextHook']=='quiet_census_source_shelter',(label,out)
            assert result['heat']==min(100,pre['heat']+2),(label,pre,result)
        p.screenshot(path=str(QA/f'reconciliation-window-{branch}-{label}-outcome.png'),full_page=True)
        before=p.evaluate('''()=>({journal:JSON.stringify(Game.journal),heat:Game.heat.meridian,discovered:!!Game.cityLife.discovered.loc_helix_hidden_1,decision:CR14ReconciliationWindowV14.resolution()?.decision,modifier:CR14ReconciliationWindowV14.resolution()?.accessModifier,trace:CR14ReconciliationWindowV14.resolution()?.principalTrace,burned:CR14ReconciliationWindowV14.resolution()?.sourceMapBurned})''')
        p.evaluate('()=>saveGame(1,false)');p.evaluate('()=>ChromeRequiemV14Boot.bridge.flush()')
        p.evaluate('''()=>{Game.journal=[];Game.heat.meridian=99;Game.cityLife.discovered.loc_helix_hidden_1=false;}''')
        assert p.evaluate('()=>ChromeRequiemV14Boot.runtime.load(1)') is True,(label,'load failed')
        after=p.evaluate('''()=>({journal:JSON.stringify(Game.journal),heat:Game.heat.meridian,discovered:!!Game.cityLife.discovered.loc_helix_hidden_1,decision:CR14ReconciliationWindowV14.resolution()?.decision,modifier:CR14ReconciliationWindowV14.resolution()?.accessModifier,trace:CR14ReconciliationWindowV14.resolution()?.principalTrace,burned:CR14ReconciliationWindowV14.resolution()?.sourceMapBurned})''')
        assert after==before,(label,before,after)
        assert not errors,(label,errors)
        print('PASS',label,branch,modifier,decision,'Market Eyes -> Paper Ghosts -> Quiet Census -> Settlement Vault Annex -> save/load',flush=True)
        ctx.close()
    browser.close()
print('PASS PWA12.136 RECONCILIATION WINDOW browser full-chain reachability, physical gating, rendered branching, persistence, and responsive layout',flush=True)
os._exit(0)
