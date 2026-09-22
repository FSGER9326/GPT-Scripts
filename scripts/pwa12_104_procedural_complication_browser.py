#!/usr/bin/env python3
from pathlib import Path
import mimetypes,sys
from playwright.sync_api import sync_playwright
ROOT=Path(sys.argv[1]).resolve();QA=ROOT/'qa';QA.mkdir(parents=True,exist_ok=True)
HTML=(ROOT/'index.html').read_text(encoding='utf-8')
SHIM="""<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"""
HTML=HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1).replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
QUIET_APPROACH='v134b_ap_forged'

def open_game(browser):
 p=browser.new_page(viewport={'width':1280,'height':900},device_scale_factor=1);errors=[];missing=[];p.on('pageerror',lambda e:errors.append(e.stack or str(e)))
 def route(r):
  u=r.request.url
  if not u.startswith('http://cr.local/'):return r.abort()
  rel=u[len('http://cr.local/'):].split('?',1)[0] or 'index.html';fp=ROOT/rel
  if fp.is_file():r.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream')
  else:missing.append(rel);r.fulfill(status=404,body=b'NOT FOUND')
 p.route('http://cr.local/**',route);p.set_content(HTML,wait_until='domcontentloaded');p.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000);return p,errors,missing

def setup(p,label):
 d=p.evaluate('''(label)=>{let z=null;for(let a=0;a<5&&!z;a++){startNewGame(label+a,'Hacker','street');document.getElementById('story-modal')?.classList.remove('open');for(const c of Game.contacts||[]){for(const m of c.missions||[]){if(m.v140Complication?.version===1&&m.v140Complication.enabled){z={c,m};break}}if(z)break}}if(!z)return{error:'no enabled complication'};const{c,m}=z;Game.contactRelations[c.id]??={};Game.contactRelations[c.id].known=true;Game.credits=Math.max(10000,Game.credits||0);if(Game.districtWorldsV133?.activeId!==c.sectorId)activateDistrictV133(c.sectorId,null);Game.ovPlayer={x:c.x,y:c.y};const before={id:m.id,contact:c.id,reward:m.reward,xp:m.xp,q:JSON.parse(JSON.stringify(m.v140Complication))};saveGame(4,true);m.v140Complication.seed=(m.v140Complication.seed+1)>>>0;m.v140Complication.runtimeTriggered=true;const ok=loadGame(4),c2=Game.contacts.find(x=>x.id===c.id),m2=c2?.missions?.find(x=>x.id===m.id);if(!ok||!m2)return{error:'save/load lost mission'};const persist={seed:m2.v140Complication.seed,kind:m2.v140Complication.kind,runtimeTriggered:m2.v140Complication.runtimeTriggered??null};if(Game.districtWorldsV133?.activeId!==c2.sectorId)activateDistrictV133(c2.sectorId,null);Game.ovPlayer={x:c2.x,y:c2.y};renderContactDossierV13(c2.id);showScreen('v13-contact-screen');const card=document.querySelector(`#v13-contracts [data-m="${m2.id}"]`),chip=card?.querySelector('.v140-risk-chip')?.textContent||'';return{id:m2.id,contact:c2.id,before,persist,card:!!card,chip}}''',label)
 assert not d.get('error'),d;assert d['card'] and d['chip'].startswith('RISK'),d;assert d['persist']['seed']==d['before']['q']['seed'] and d['persist']['kind']==d['before']['q']['kind'] and d['persist']['runtimeTriggered'] is None,d;return d

def brief(p,d):
 p.locator(f'#v13-contracts [data-m="{d["id"]}"]').click(timeout=8000);p.wait_for_function("()=>Game.screen==='v10-briefing'&&!!Game.pendingMission",timeout=8000)
 q=p.evaluate('''()=>({id:Game.pendingMission.id,reward:Game.pendingMission.reward,xp:Game.pendingMission.xp,q:Game.pendingMission.v140Complication,text:document.querySelector('.v140-complication-brief')?.textContent||'',forged:!!document.querySelector('.v134b-approach[data-id="v134b_ap_forged"]:not([disabled])')})''')
 assert q['id']==d['id'] and q['reward']==d['before']['reward'] and q['xp']==d['before']['xp'],q;assert q['q']['enabled'] and 'RISK ' in q['text'] and 'MITIGATION' in q['text'] and q['forged'],q;return q

def stage(p,d):
 p.locator(f'.v134b-approach[data-id="{QUIET_APPROACH}"]').click(timeout=5000);p.locator('#v10-brief-deploy').click(timeout=5000);p.wait_for_function('(id)=>Game.contractApproachesV134B?.plan?.missionId===id',arg=d['id'],timeout=5000)
 r=p.evaluate('''()=>{const n=currentPlannedNodeV134B();if(!n)return{error:'no node'};Game.ovPlayer={x:n.x,y:n.y};return{ok:completeMissionApproachV134B({kind:'v134b',id:n.id}),id:n.id,ready:Game.contractApproachesV134B?.plan?.ready}}''');assert not r.get('error') and r['ok'] and r['ready'],r;p.wait_for_selector('#v134b-stage-modal.open #v134b-stage-deploy',timeout=5000)

def deploy(p,d):
 p.locator('#v134b-stage-deploy').click(timeout=5000);p.wait_for_function('(id)=>Game.activeMission?.id===id&&Game.screen===\'combat\'',arg=d['id'],timeout=15000)
 return p.evaluate('''()=>{const m=Game.activeMission;return{id:m.id,reward:m.reward,xp:m.xp,q:m.v140Complication,approach:m.v134bApproach,staged:!!m.v134bStaged,alerted:!!Game.alerted,aware:Game.units.filter(u=>u.team==='enemy').map(u=>({a:u.awareness,on:!!u.alerted})),shape:Game.arenaShapeV14||null}}''')

def run(browser,mitigated):
 p,errors,missing=open_game(browser);d=setup(p,'C04M' if mitigated else 'C04U');q=brief(p,d)
 if not mitigated:p.screenshot(path=str(QA/'candidate04_complication_briefing.png'),full_page=True)
 if mitigated:
  cost=q['q']['mitigationCost'];cash=p.evaluate('()=>Game.credits');p.locator('.v140-mitigate').click(timeout=5000);post=p.evaluate('''()=>({cash:Game.credits,q:Game.pendingMission.v140Complication,button:!!document.querySelector('.v140-mitigate')})''');assert post['q']['mitigated'] and post['q']['mitigationPaid']==cost and post['cash']==cash-cost and not post['button'],post
  persisted=p.evaluate('''(id)=>{const ok=loadGame(0),m=Game.contacts.flatMap(c=>c.missions||[]).find(x=>x.id===id);return{ok,cash:Game.credits,q:m?.v140Complication}}''',d['id']);assert persisted['ok'] and persisted['q']['mitigated'] and persisted['q']['mitigationPaid']==cost and persisted['cash']==post['cash'],persisted
  p.evaluate('''(x)=>{const c=Game.contacts.find(c=>c.id===x.contact);Game.contactRelations[c.id]??={};Game.contactRelations[c.id].known=true;if(Game.districtWorldsV133?.activeId!==c.sectorId)activateDistrictV133(c.sectorId,null);Game.ovPlayer={x:c.x,y:c.y};renderContactDossierV13(c.id);showScreen('v13-contact-screen')}''',d);brief(p,d)
 stage(p,d)
 if not mitigated:
  lock=p.evaluate('''(id)=>{const m=Game.contacts.flatMap(c=>c.missions||[]).find(x=>x.id===id),cash=Game.credits,r=mitigateComplicationV140(m);return{r,cash,after:Game.credits,locked:mitigationLockedV140(m),mitigated:m.v140Complication.mitigated}}''',d['id']);assert lock['locked'] and lock['r'] is False and lock['cash']==lock['after'] and not lock['mitigated'],lock
 c=deploy(p,d);assert c['approach']==QUIET_APPROACH and c['staged'] and c['reward']==d['before']['reward'] and c['xp']==d['before']['xp'],c
 if mitigated:assert c['alerted'] is False and not c['q'].get('runtimeTriggered',False) and c['aware'] and all(x['a']==0 and not x['on'] for x in c['aware']),c
 else:assert c['alerted'] and c['q'].get('runtimeTriggered') is True and c['q'].get('runtimeApproach')==QUIET_APPROACH and c['aware'] and all(x['a']==100 and x['on'] for x in c['aware']),c
 p.screenshot(path=str(QA/('candidate04_complication_mitigated_combat.png' if mitigated else 'candidate04_complication_unmitigated_combat.png')),full_page=True);assert not errors and not missing,(errors,missing);p.close();return c

with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage']);u=run(b,False);m=run(b,True);print('PASS procedural complication browser transitions',{'unmitigated':{'id':u['id'],'kind':u['q']['kind'],'approach':u['approach'],'alerted':u['alerted'],'shape':u['shape']},'mitigated':{'id':m['id'],'kind':m['q']['kind'],'cost':m['q']['mitigationPaid'],'approach':m['approach'],'alerted':m['alerted'],'shape':m['shape']}},flush=True);b.close()
