"""Pixel-7 browser integration for PWA12.104 salvage-market progression candidate."""
from pathlib import Path
import mimetypes,sys,json
from playwright.sync_api import sync_playwright
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
(ROOT/'qa').mkdir(exist_ok=True)
HTML=(ROOT/'index.html').read_text(encoding='utf-8').replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')
SHIM="""<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"""
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    ctx=browser.new_context(viewport={'width':412,'height':915},device_scale_factor=1)
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
      startNewGame('Salvage QA','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');Game.credits=50000;Game.salvage=0;
      const find=(kind,prefix)=>{for(let i=0;i<3000;i++){const m={id:`${prefix}_${i}`,name:`${kind} recovery ${i}`,lootManufacturer:'kestrel',worldLocation:'rhine',sectorId:'glass_heights',area:'GLASS HEIGHTS',diff:3};const d=salvageOfferForMissionV135(m);if(d?.kind===kind)return{m,d}}return null};
      const weapon=find('weapon','qa_weapon');if(!weapon)throw new Error('no deterministic weapon offer found');
      const first=queueMissionSalvageV135(weapon.m),again=queueMissionSalvageV135(weapon.m);openSafehouse();
      const host=document.getElementById('v135-salvage-exchange'),modal=document.getElementById('modal-inner'),hr=host.getBoundingClientRect(),mr=modal.getBoundingClientRect();
      return{weapon,first:!!first,again,pending:salvageExchangeStateV135().pending.length,ui:{width:Math.round(hr.width),modalWidth:Math.round(mr.width),overflow:host.scrollWidth-host.clientWidth,rightOverflow:Math.max(0,Math.round(hr.right-mr.right)),buttons:host.querySelectorAll('[data-salvage-action]').length}};
    }''')
    assert setup['first'] and setup['again'] is False and setup['pending']==1,setup
    assert setup['ui']['overflow']<=1 and setup['ui']['rightOverflow']<=1 and setup['ui']['buttons']==3,setup
    page.screenshot(path=str(ROOT/'qa/pwa12-104-salvage-market-mobile.png'),full_page=True)

    persist=page.evaluate('''()=>{const before=salvageExchangeStateV135().pending[0];const saved=saveGame(1,true);Game.companyV135.salvageExchange.pending=[];const ok=loadGame(1);const after=salvageExchangeStateV135().pending[0];return{saved,ok,before:before?.id,after:after?.id,source:after?.sourceMissionId}}''')
    assert persist['saved'] and persist['ok'] and persist['before']==persist['after']==setup['weapon']['d']['id'],persist

    migration=page.evaluate('''()=>{saveGame(2,true);const key='chrome_requiem_v13_2',data=JSON.parse(localStorage.getItem(key));delete data.companyV135.salvageExchange;localStorage.setItem(key,JSON.stringify(data));const ok=loadGame(2),x=salvageExchangeStateV135();return{ok,version:x.version,pending:x.pending.length,resolved:Object.keys(x.resolved).length,stats:!!x.stats}}''')
    assert migration=={'ok':True,'version':1,'pending':0,'resolved':0,'stats':True},migration

    # Re-queue the deterministic weapon after the synthetic old-save migration and KEEP it without auto-equipping.
    kept=page.evaluate('''q=>{const beforeWeapon=Game.roster[0].weapon,offer=queueMissionSalvageV135(q.m),d=salvageExchangeStateV135().pending.find(x=>x.sourceMissionId===q.m.id),credits=Game.credits,salvage=Game.salvage,ok=resolveMissionSalvageV135(d.id,'keep');const u=Game.roster[0],notAuto=u.weapon===beforeWeapon,owned=Game.stash.weapons.includes(d.key);u.weapon=d.key;applySkillsToUnit(u);const equipped={key:u.weapon,damage:u.damage,range:u.range,crit:u.critChance};u.weapon=beforeWeapon;applySkillsToUnit(u);const unequipped={key:u.weapon,damage:u.damage,range:u.range,crit:u.critChance};u.weapon=d.key;applySkillsToUnit(u);return{offer:!!offer,ok,owned,notAuto,creditsSame:Game.credits===credits,salvageSame:Game.salvage===salvage,key:d.key,equipped,unequipped}}''',setup['weapon'])
    assert kept['offer'] and kept['ok'] and kept['owned'] and kept['notAuto'] and kept['creditsSame'] and kept['salvageSame'],kept
    assert kept['equipped']['key']==kept['key'] and kept['unequipped']['key']!=kept['key'],kept

    attachment=page.evaluate('''()=>{const u=Game.roster[0],platform=ITEMS[u.weapon]?.platform||ITEMS[u.weapon]?.baseWeapon;for(let i=0;i<4000;i++){const m={id:`qa_attachment_${i}`,name:`attachment recovery ${i}`,lootManufacturer:'kestrel',worldLocation:'rhine',sectorId:'glass_heights',area:'GLASS HEIGHTS',diff:2};const d=salvageOfferForMissionV135(m),a=d&&V11_ATTACHMENTS[d.key];if(d?.kind==='attachment'&&a?.platforms?.includes(platform))return{m,d,slot:a.slot,platform}}throw new Error('no compatible deterministic attachment offer found')}''')
    attach_result=page.evaluate('''q=>{const u=Game.roster[0],before=Game.armory.attachments[q.d.key]||0;queueMissionSalvageV135(q.m);const d=salvageExchangeStateV135().pending.find(x=>x.sourceMissionId===q.m.id);const kept=resolveMissionSalvageV135(d.id,'keep'),owned=Game.armory.attachments[q.d.key]||0,installed=installAttachmentV11(u,u.weapon,q.d.key),slot=V11_ATTACHMENTS[q.d.key].slot,mod=u.weaponMods[u.weapon]?.[slot];const tmp=document.createElement('div');document.body.appendChild(tmp);renderWeaponBenchV11(tmp);const remove=tmp.querySelector(`[data-remove="${slot}"]`);if(remove)remove.click();const removed=!u.weaponMods[u.weapon]?.[slot];tmp.remove();const reinstalled=installAttachmentV11(u,u.weapon,q.d.key);return{kept,before,owned,installed,mod,removed,reinstalled,slot,damage:u.damage,range:u.range,crit:u.critChance}}''',attachment)
    assert attach_result['kept'] and attach_result['owned']==attach_result['before']+1 and attach_result['installed'] and attach_result['mod']==attachment['d']['key'],attach_result
    assert attach_result['removed'] and attach_result['reinstalled'],attach_result

    combat=page.evaluate('''()=>{const u=Game.roster[0],m={id:'qa_combat_bridge',name:'Combat bridge',type:'eliminate',objective:'eliminate',diff:1,enemies:['Guard'],sectorId:'glass_heights',reward:0,xp:0};Game.activeMission=m;buildGrid(m);createCombatUnitsV135(m);const cu=Game.units.find(x=>x.team==='player'&&x.rosterRef===u);return{found:!!cu,weapon:cu?.weapon,damage:cu?.damage,range:cu?.range,crit:cu?.critChance,roster:{weapon:u.weapon,damage:u.damage,range:u.range,crit:u.critChance}}}''')
    assert combat['found'] and combat['weapon']==combat['roster']['weapon'] and combat['damage']==combat['roster']['damage'] and combat['range']==combat['roster']['range'] and combat['crit']==combat['roster']['crit'],combat

    strip=page.evaluate('''()=>{const u=Game.roster[0];let q=null;for(let i=0;i<4000;i++){const m={id:`qa_strip_${i}`,name:'Strip recovery',lootManufacturer:'atlas',worldLocation:'detroit',sectorId:'dock_nine',area:'DOCK NINE',diff:2},d=salvageOfferForMissionV135(m);if(d){q={m,d};break}}if(!q)throw new Error('no strip offer');queueMissionSalvageV135(q.m);const d=salvageExchangeStateV135().pending.find(x=>x.sourceMissionId===q.m.id),before=Game.salvage,ok=resolveMissionSalvageV135(d.id,'strip'),after=Game.salvage,key=equipmentKeyV135(u.weapon,u,'weapon'),s=ensureCompanyStateV135();s.maintenance.weaponWear[key]=18;const quote=repairQuoteV135([key]);Game.credits=50000;const beforeRepair=Game.salvage,repair=repairEquipmentV135([key]),afterRepair=Game.salvage,wear=s.maintenance.weaponWear[key];return{ok,strip:d.stripValue,before,after,quote,repair,beforeRepair,afterRepair,wear}}''')
    assert strip['ok'] and strip['after']-strip['before']==strip['strip'] and strip['repair'],strip
    assert strip['beforeRepair']-strip['afterRepair']==strip['quote']['salvage'] and strip['wear']==0,strip

    sold=page.evaluate('''()=>{let q=null;for(let i=0;i<4000;i++){const m={id:`qa_sell_${i}`,name:'Sell recovery',lootManufacturer:'mako',worldLocation:'lagos',sectorId:'neon_row',area:'NEON ROW',diff:1},d=salvageOfferForMissionV135(m);if(d){q={m,d};break}}queueMissionSalvageV135(q.m);const d=salvageExchangeStateV135().pending.find(x=>x.sourceMissionId===q.m.id),before=Game.credits,ok=resolveMissionSalvageV135(d.id,'sell');return{ok,sell:d.sellValue,before,after:Game.credits}}''')
    assert sold['ok'] and sold['after']-sold['before']==sold['sell'],sold

    market=page.evaluate('''()=>{Game.credits=50000;Game.rep.meridian=0;Game.rep.spine=0;Game.heat.meridian=0;Game.heat.spine=0;renderMarketV13('s_needle');showScreen('v13-market-screen');const labels=[...document.querySelectorAll('#v13-market-grid .v135-supply')].map(x=>x.textContent.trim());const local=marketSupplyContextV135(shopDefV13('s_needle'),{key:'sable_shade',type:'weapon',item:ITEMS.sable_shade}),imported=marketSupplyContextV135(shopDefV13('s_needle'),{key:'kestrel_falcon',type:'weapon',item:ITEMS.kestrel_falcon});Game.rareStock={s_needle:{item:'rifle_mk2',expires:Game.day+1}};Game.rareStockDay=Game.day;renderMarketV13('s_needle');const rareBefore=!!document.querySelector('#v13-market-grid [data-key="rifle_mk2"]'),buy=buyMarketItemV13('s_needle','rifle_mk2'),rareGone=!Game.rareStock.s_needle;renderMarketV13('s_needle');const rareAfter=!!document.querySelector('#v13-market-grid [data-key="rifle_mk2"]');return{labels,local,imported,rareBefore,buy,rareGone,rareAfter}}''')
    assert market['local']['mult']==0.92 and market['imported']['mult']==1.12,market
    assert any('LOCAL INDUSTRY' in x for x in market['labels']) and any('IMPORTED' in x for x in market['labels']),market
    assert market['rareBefore'] and market['buy'] and market['rareGone'] and not market['rareAfter'],market

    stats=page.evaluate('''()=>{const x=salvageExchangeStateV135();return{x,diag:runDiagnosticsV135(),overflow:Math.max(document.documentElement.scrollWidth-document.documentElement.clientWidth,0)}}''')
    assert stats['diag']['passed']==stats['diag']['total'],stats['diag']
    assert not errors,errors
    print(json.dumps({'setup':setup,'kept':kept,'attachment':attachment,'attach_result':attach_result,'combat':combat,'strip':strip,'sold':sold,'market':market,'stats':stats},indent=2))
    print('PASS PWA12.104 salvage-market browser: deterministic recovery, KEEP/SELL/STRIP, save/load migration, weapon swap, attachment install/remove, combat bridge, repair salvage sink, local/import pricing, one-shot rare stock, Pixel 7 UI')
    ctx.close();browser.close()
