"""Browser integration for physical post-clash Street Favors."""
from pathlib import Path
import mimetypes,sys
from playwright.sync_api import sync_playwright
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
(ROOT/'qa').mkdir(exist_ok=True)
HTML=(ROOT/'index.html').read_text().replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
SHIM="""<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"""
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    ctx=browser.new_context(viewport={'width':412,'height':915})
    errors=[]
    def route(r):
        relative=r.request.url.split('http://cr.local/',1)[-1].split('?',1)[0] or 'index.html'
        path=ROOT/relative
        if path.is_file(): r.fulfill(status=200,body=path.read_bytes(),content_type=mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
        else: r.fulfill(status=404,body=b'not found')
    ctx.route('http://cr.local/**',route)
    page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content(HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1),wait_until='domcontentloaded')
    page.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
    setup=page.evaluate('''()=>{
      startNewGame('Street Favor QA','Hacker','street');
      document.getElementById('story-modal')?.classList.remove('open');
      const c=Game.contacts[0],def=V13_CONTACTS.find(x=>x.id===c.id),target=Object.keys(FACTIONS).find(f=>f!==def.faction);
      Game.contactRelations[c.id].known=true;Game.contactRelations[c.id].trust=50;Game.heat[target]=30;Game.activeMission=null;
      const s=ensureLivingStreetsStateV134();s.contactFavors={};s.contactFavorHistory={};s.neighborhoods[def.sectorId]=s.neighborhoods[def.sectorId]||{};
      s.neighborhoods[def.sectorId].favor_qa={id:'favor_qa',name:'Favor QA',security:2,prosperity:2,unrest:1,gangPressure:3,localHeat:20,secrets:0,controller:'local',events:0};
      const m={id:'favor_source_alpha',name:'QA Street Clash',v134StreetEncounter:true,v134ContactSupport:{id:c.id,name:c.name,tier:2,label:'LOCAL BACKUP'},contact:c.id,sectorId:def.sectorId,v134StreetNeighborhood:'favor_qa',v134StreetActorType:'gang',targetFaction:target,diff:2};
      settleStreetCombatV134(m,true);
      Game.districtWorldsV133=Game.districtWorldsV133||{};Game.districtWorldsV133.activeId=def.sectorId;Game.ovPlayer={x:c.x,y:c.y};
      renderContactDossierV13(c.id);showScreen('v13-contact-screen');
      const favor=streetFavorStateV134(c.id),buttons=[...document.querySelectorAll('#v134-street-favor-card button')];
      return{id:c.id,sector:def.sectorId,target,contactFaction:def.faction,source:m,near:CR14MultiStageOperations.nearContact(c.id),favor,buttons:buttons.length,enabled:buttons.filter(b=>!b.disabled).length,local:s.neighborhoods[def.sectorId].favor_qa.localHeat,targetHeat:Game.heat[target]};
    }''')
    assert setup['near'] and setup['favor']['sourceMissionId']=='favor_source_alpha',setup
    assert setup['buttons']==2 and setup['enabled']==2,setup
    assert setup['local']==28 and setup['targetHeat']==35,setup
    duplicate=page.evaluate('m=>({again:awardStreetFavorV134(m),count:Object.keys(Game.livingStreetsV134.contactFavors).length,history:Object.keys(Game.livingStreetsV134.contactFavorHistory).length})',setup['source'])
    assert duplicate=={'again':False,'count':1,'history':1},duplicate
    page.screenshot(path=str(ROOT/'qa/pwa12-105-street-favor-mobile.png'),full_page=True)
    saved=page.evaluate('()=>saveGame(1,true)');assert saved is True
    restored=page.evaluate('''id=>{Game.livingStreetsV134.contactFavors={};const ok=loadGame(1);const c=Game.contacts.find(x=>x.id===id),def=V13_CONTACTS.find(x=>x.id===id);Game.districtWorldsV133.activeId=def.sectorId;Game.ovPlayer={x:c.x,y:c.y};renderContactDossierV13(id);return{ok,pending:!!streetFavorStateV134(id),near:CR14MultiStageOperations.nearContact(id)}}''',setup['id'])
    assert restored=={'ok':True,'pending':True,'near':True},restored
    remote=page.evaluate('''id=>{Game.ovPlayer={x:-999,y:-999};renderContactDossierV13(id);const bs=[...document.querySelectorAll('#v134-street-favor-card button')];return{near:CR14MultiStageOperations.nearContact(id),buttons:bs.length,disabled:bs.filter(b=>b.disabled).length,direct:resolveStreetFavorV134(id,'cover'),pending:!!streetFavorStateV134(id)}}''',setup['id'])
    assert remote=={'near':False,'buttons':2,'disabled':2,'direct':False,'pending':True},remote
    cover=page.evaluate('''q=>{const c=Game.contacts.find(x=>x.id===q.id),def=V13_CONTACTS.find(x=>x.id===q.id);Game.districtWorldsV133.activeId=def.sectorId;Game.ovPlayer={x:c.x,y:c.y};const h=Game.livingStreetsV134.neighborhoods[q.sector].favor_qa,before=[h.localHeat,Game.heat[q.target]];const ok=resolveStreetFavorV134(q.id,'cover');return{ok,before,after:[h.localHeat,Game.heat[q.target]],pending:!!streetFavorStateV134(q.id),again:resolveStreetFavorV134(q.id,'cover')}}''',setup)
    assert cover['ok'] and cover['before']==[28,35] and cover['after']==[16,27] and not cover['pending'] and cover['again'] is False,cover
    follow=page.evaluate('''q=>{const c=Game.contacts.find(x=>x.id===q.id),def=V13_CONTACTS.find(x=>x.id===q.id);const m={id:'favor_source_beta',name:'Second Clash',v134StreetEncounter:true,v134ContactSupport:{id:q.id,name:c.name,tier:2,label:'LOCAL BACKUP'},contact:q.id,sectorId:q.sector,v134StreetNeighborhood:'favor_qa',v134StreetActorType:'hunter',targetFaction:q.target,diff:2};settleStreetCombatV134(m,true);Game.districtWorldsV133.activeId=def.sectorId;Game.ovPlayer={x:c.x,y:c.y};const ok=resolveStreetFavorV134(q.id,'countermove');const job=c.missions.find(x=>x.v134StreetFavorFollowUp);return{ok,pending:!!streetFavorStateV134(q.id),job:job&&{id:job.id,sectorId:job.sectorId,targetFaction:job.targetFaction,contact:job.contact,diff:job.diff,reward:job.reward,repGain:job.factionRepGain,repLoss:job.factionRepLoss[q.target],source:job.v134StreetFavorSource}}}''',setup)
    assert follow['ok'] and not follow['pending'],follow
    assert follow['job']=={'id':'v134favor_favor_source_beta','sectorId':setup['sector'],'targetFaction':setup['target'],'contact':setup['id'],'diff':3,'reward':990,'repGain':7,'repLoss':-7,'source':'favor_source_beta'},follow
    persist=page.evaluate('''q=>{saveGame(2,true);const c=Game.contacts.find(x=>x.id===q.id);c.missions=c.missions.filter(m=>!m.v134StreetFavorFollowUp);const ok=loadGame(2);const restored=Game.contacts.find(x=>x.id===q.id).missions.find(m=>m.v134StreetFavorFollowUp);return{ok,restored:restored?.id||null,sector:restored?.sectorId||null}}''',setup)
    assert persist=={'ok':True,'restored':'v134favor_favor_source_beta','sector':setup['sector']},persist
    same=page.evaluate('''q=>{const c=Game.contacts.find(x=>x.id===q.id),def=V13_CONTACTS.find(x=>x.id===q.id),s=ensureLivingStreetsStateV134();s.contactFavors[q.id]={contactId:q.id,sourceMissionId:'same_side',district:q.sector,neighborhood:'favor_qa',targetFaction:def.faction,actorType:'security',sourceDiff:2,earnedDay:Game.day};s.contactFavorHistory.same_side={contactId:q.id,status:'banked',day:Game.day};Game.districtWorldsV133.activeId=def.sectorId;Game.ovPlayer={x:c.x,y:c.y};renderContactDossierV13(q.id);const bs=[...document.querySelectorAll('#v134-street-favor-card button')];const counter=resolveStreetFavorV134(q.id,'countermove'),still=!!streetFavorStateV134(q.id),cover=resolveStreetFavorV134(q.id,'cover');return{buttons:bs.length,firstDisabled:bs[0].disabled,secondDisabled:bs[1].disabled,counter,still,cover,pending:!!streetFavorStateV134(q.id)}}''',setup)
    assert same=={'buttons':2,'firstDisabled':False,'secondDisabled':True,'counter':False,'still':True,'cover':True,'pending':False},same
    defeat=page.evaluate('''q=>{const c=Game.contacts.find(x=>x.id===q.id);const m={id:'favor_source_loss',name:'Lost Clash',v134StreetEncounter:true,v134ContactSupport:{id:q.id,name:c.name,tier:2,label:'LOCAL BACKUP'},contact:q.id,sectorId:q.sector,v134StreetNeighborhood:'favor_qa',v134StreetActorType:'gang',targetFaction:q.target,diff:2};settleStreetCombatV134(m,false);return{pending:!!streetFavorStateV134(q.id),history:!!Game.livingStreetsV134.contactFavorHistory[m.id]}}''',setup)
    assert defeat=={'pending':False,'history':False},defeat
    compat=page.evaluate('''()=>{const s=ensureLivingStreetsStateV134();delete s.contactFavors;delete s.contactFavorHistory;const again=ensureLivingStreetsStateV134();return{favors:typeof again.contactFavors==='object',history:typeof again.contactFavorHistory==='object'}}''')
    assert compat=={'favors':True,'history':True},compat
    assert not errors,errors
    print('PASS PWA12.105 browser: physical favor, remote lock, cover choice, countermove mission, same-side guard, defeat guard, save/load, mobile UI')
    ctx.close();browser.close()
