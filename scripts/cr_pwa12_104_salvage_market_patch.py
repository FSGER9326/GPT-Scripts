from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve()

# 1) Route the legacy V11 auto-loot hook through the new company salvage intake.
megap=root/'src/legacy/megacity-v11.js'
mega=megap.read_text(encoding='utf-8')
needle="function awardManufacturerLootV11(m){\n ensureV11State();"
replacement="function awardManufacturerLootV11(m){\n ensureV11State();if(typeof window.queueMissionSalvageV135==='function')return window.queueMissionSalvageV135(m);"
if mega.count(needle)!=1:
    raise SystemExit(f'unexpected manufacturer loot seam count={mega.count(needle)}')
mega=mega.replace(needle,replacement,1)
megap.write_text(mega,encoding='utf-8')

# 2) Make city-market price reflect local industrial supply and make rare stock truly one-shot.
cityp=root/'src/legacy/city-life-v13.js'
city=cityp.read_text(encoding='utf-8')
old="return Math.round(m.price*repMult*wealth*(window.heatVendorMultV134B?window.heatVendorMultV134B():1))"
new="return Math.round(m.price*repMult*wealth*(window.heatVendorMultV134B?window.heatVendorMultV134B():1)*(window.marketSupplyMultiplierV135?window.marketSupplyMultiplierV135(shop,m):1))"
if city.count(old)!=1:
    raise SystemExit(f'unexpected shop price seam count={city.count(old)}')
city=city.replace(old,new,1)

old="else purchaseItem(shop,key,price,m.item);\n saveGame(0,true);renderMarketV13(shopId);return true"
new="else purchaseItem(shop,key,price,m.item);\n if(Game.rareStock?.[shopId]?.item===key)delete Game.rareStock[shopId];\n saveGame(0,true);renderMarketV13(shopId);return true"
if city.count(old)!=1:
    raise SystemExit(f'unexpected market purchase seam count={city.count(old)}')
city=city.replace(old,new,1)

old="${isRare?'<div class=\"v13-rare\">LIMITED</div>':''}</div>`}).join('');"
new="${isRare?'<div class=\"v13-rare\">LIMITED · ONE UNIT</div>':''}${window.marketSupplyBadgeV135?window.marketSupplyBadgeV135(s,m):''}</div>`}).join('');"
if city.count(old)!=1:
    raise SystemExit(f'unexpected market card seam count={city.count(old)}')
city=city.replace(old,new,1)
cityp.write_text(city,encoding='utf-8')

# 3) Extend the durable company state with a salvage-exchange ledger. This is additive,
# so older schema-14 saves migrate by defaulting the missing field.
companyp=root/'src/company/company-foundation-v13-5.js'
company=companyp.read_text(encoding='utf-8')
state_needle=" s.maintenance=s.maintenance||{};s.maintenance.weaponWear=s.maintenance.weaponWear||{};s.maintenance.armorWear=s.maintenance.armorWear||{};s.maintenance.pendingRepairs=Array.isArray(s.maintenance.pendingRepairs)?s.maintenance.pendingRepairs:[];"
state_replacement=state_needle+"\n s.salvageExchange=s.salvageExchange&&typeof s.salvageExchange==='object'?s.salvageExchange:{};s.salvageExchange.version=1;s.salvageExchange.pending=Array.isArray(s.salvageExchange.pending)?s.salvageExchange.pending:[];s.salvageExchange.resolved=s.salvageExchange.resolved&&typeof s.salvageExchange.resolved==='object'?s.salvageExchange.resolved:{};s.salvageExchange.stats=s.salvageExchange.stats&&typeof s.salvageExchange.stats==='object'?s.salvageExchange.stats:{generated:0,kept:0,sold:0,stripped:0};"
if company.count(state_needle)!=1:
    raise SystemExit(f'unexpected company state seam count={company.count(state_needle)}')
company=company.replace(state_needle,state_replacement,1)

insert_after="window.processCompanyDayV135=processCompanyDayV135;\n"
if company.count(insert_after)!=1:
    raise SystemExit(f'unexpected process day insertion seam count={company.count(insert_after)}')
feature=r'''

/* PWA12.104 progression candidate — field salvage intake + local supply scarcity.
   Recovered gear keeps canonical combat stats; recovery condition affects only the
   economic choice between KEEP, SELL and STRIP, avoiding another stat-tier ladder. */
const V135_SALVAGE_AFFINITY=Object.freeze({
 kestrel:['optic_reflex','optic_marksman','stock_stabilizer'],
 helix:['optic_smart','under_laser','optic_reflex'],
 mako:['optic_reflex','under_laser','stock_cqb'],
 redline:['muzzle_heavy','muzzle_comp','stock_cqb'],
 sable:['muzzle_suppressor','stock_stabilizer','optic_reflex'],
 atlas:['muzzle_heavy','under_grip','stock_stabilizer','optic_marksman']
});
function salvageExchangeStateV135(){return ensureCompanyStateV135().salvageExchange}
function salvageManufacturerV135(m){
 const explicit=m?.lootManufacturer;if(explicit&&window.V11_MANUFACTURERS?.[explicit])return explicit;
 const sector=(window.V11_SECTORS||[]).find(s=>s.id===m?.sectorId),industry=(sector?.industry||[]).filter(id=>window.V11_MANUFACTURERS?.[id]);
 if(!industry.length)return null;return industry[hashV135(`${m?.id||'mission'}|industry`)%industry.length]
}
function salvageBasePriceV135(kind,key){
 if(kind==='weapon')return Math.max(1,Number(WEAPON_PRICES?.[key]||ITEMS?.[key]?.price||500));
 return Math.max(1,Number(window.V11_ATTACHMENTS?.[key]?.price||350))
}
function salvageQualityV135(condition){return condition>=88?'CLEAN':condition>=72?'SERVICEABLE':condition>=55?'FIELD-WORN':'BATTLEWORN'}
function salvageOfferForMissionV135(m){
 if(!m?.id)return null;const manufacturer=salvageManufacturerV135(m);if(!manufacturer)return null;
 const seed=hashV135(`${m.id}|${m.sectorId||''}|${m.worldLocation||''}|${manufacturer}|salvage`),diff=clampV135(Number(m.diff)||1,1,3),chance=m.worldLocation?100:60+diff*5;
 if((seed%100)>=chance)return null;
 const specs=(window.V11_WEAPON_SPECS||[]).filter(x=>x[2]===manufacturer),owned=new Set(Game.stash?.weapons||[]),unowned=specs.filter(x=>!owned.has(x[0]));
 const weaponChance=m.worldLocation?52:18+diff*8,weaponRoll=(seed>>>8)%100;let kind='attachment',key=null;
 if(weaponRoll<weaponChance&&unowned.length)key=unowned[(seed>>>13)%unowned.length][0],kind='weapon';
 if(!key){const affinity=(V135_SALVAGE_AFFINITY[manufacturer]||[]).filter(id=>window.V11_ATTACHMENTS?.[id]),pool=affinity.length?affinity:Object.keys(window.V11_ATTACHMENTS||{});if(!pool.length)return null;key=pool[(seed>>>13)%pool.length]}
 const condition=clampV135(45+((seed>>>18)%41)+(m.worldLocation?4:0)+diff*2,45,96),base=salvageBasePriceV135(kind,key),sellValue=Math.max(40,Math.round(base*(.17+.30*(condition/100))*(1+diff*.035))),stripValue=Math.max(1,Math.round((kind==='weapon'?base/520:base/300)*(.55+condition/200)));
 const sector=(window.V11_SECTORS||[]).find(s=>s.id===m.sectorId),name=kind==='weapon'?(ITEMS?.[key]?.name||key):(window.V11_ATTACHMENTS?.[key]?.name||key),mfr=window.V11_MANUFACTURERS?.[manufacturer];
 return{id:`v135salv_${hashV135(m.id+'|'+key).toString(36)}`,sourceMissionId:m.id,missionName:m.name||'Operation',day:Game.day||1,kind,key,manufacturer,manufacturerName:mfr?.name||manufacturer,origin:m.area||sector?.name||m.worldLocation||'UNKNOWN AO',condition,quality:salvageQualityV135(condition),basePrice:base,sellValue,stripValue}
}
function queueMissionSalvageV135(m){
 if(!m?.id)return false;const x=salvageExchangeStateV135();if(x.resolved[m.id]||x.pending.some(d=>d.sourceMissionId===m.id))return false;const docket=salvageOfferForMissionV135(m);
 if(!docket){x.resolved[m.id]={action:'none',day:Game.day||1};return false}
 x.pending.unshift(docket);x.stats.generated=(x.stats.generated||0)+1;
 if(typeof addJournal==='function')addJournal('main','Field Salvage Intake',`${docket.name||docket.key} recovered from ${docket.origin}. Decide whether to keep, sell or strip it at the safehouse.`);
 toast?.(`SALVAGE INTAKE: ${docket.kind==='weapon'?(ITEMS?.[docket.key]?.name||docket.key):(window.V11_ATTACHMENTS?.[docket.key]?.name||docket.key)}`);return docket
}
function resolveMissionSalvageV135(id,action){
 const x=salvageExchangeStateV135(),i=x.pending.findIndex(d=>d.id===id);if(i<0||!['keep','sell','strip'].includes(action))return false;const d=x.pending[i],label=d.kind==='weapon'?(ITEMS?.[d.key]?.name||d.key):(window.V11_ATTACHMENTS?.[d.key]?.name||d.key);
 if(action==='keep'){
   if(d.kind==='weapon'){Game.stash=Game.stash||{weapons:[],armor:[]};Game.stash.weapons=Array.isArray(Game.stash.weapons)?Game.stash.weapons:[];if(Game.stash.weapons.includes(d.key)){toast?.('That weapon is already in the armory. Sell or strip this recovery instead.');return false}Game.stash.weapons.push(d.key)}
   else{Game.armory=Game.armory||{attachments:{}};Game.armory.attachments=Game.armory.attachments||{};Game.armory.attachments[d.key]=(Game.armory.attachments[d.key]||0)+1}
   x.stats.kept=(x.stats.kept||0)+1;
 }else if(action==='sell'){Game.credits=(Game.credits||0)+d.sellValue;x.stats.sold=(x.stats.sold||0)+1}
 else{Game.salvage=(Game.salvage||0)+d.stripValue;x.stats.stripped=(x.stats.stripped||0)+1}
 x.pending.splice(i,1);x.resolved[d.sourceMissionId]={action,day:Game.day||1,key:d.key,kind:d.kind,condition:d.condition,value:action==='sell'?d.sellValue:action==='strip'?d.stripValue:0};
 if(typeof addJournal==='function')addJournal('main','Salvage Disposition',`${label}: ${action==='keep'?'retained in company inventory':action==='sell'?`sold for ¢${d.sellValue}`:`stripped for ⚙${d.stripValue} repair salvage`}.`);
 updateOverworldHUD?.();saveGame(0,true);return true
}
function marketSupplyContextV135(shop,m){
 const sector=(window.V11_SECTORS||[]).find(s=>s.id===shop?.sectorId),industry=sector?.industry||[];if(!shop||!m||!sector)return{mult:1,label:'STANDARD SUPPLY',kind:'standard'};
 if(m.type==='weapon'){
   const mid=m.item?.manufacturer||ITEMS?.[m.key]?.manufacturer;if(!mid)return{mult:1,label:'STANDARD SUPPLY',kind:'standard'};const local=industry.includes(mid);return local?{mult:.92,label:'LOCAL INDUSTRY · −8%',kind:'local'}:{mult:1.12,label:'IMPORTED · +12%',kind:'import'}
 }
 if(m.type==='attachment'){
   const aid=m.attachmentId||String(m.key||'').replace(/^att:/,''),local=industry.some(mid=>(V135_SALVAGE_AFFINITY[mid]||[]).includes(aid));return local?{mult:.96,label:'LOCAL COMPONENT · −4%',kind:'local'}:{mult:1.06,label:'IMPORT COMPONENT · +6%',kind:'import'}
 }
 return{mult:1,label:'STANDARD SUPPLY',kind:'standard'}
}
function marketSupplyMultiplierV135(shop,m){return marketSupplyContextV135(shop,m).mult}
function marketSupplyBadgeV135(shop,m){const c=marketSupplyContextV135(shop,m);return c.kind==='standard'?'':`<div class="v135-supply ${c.kind}">${c.label}</div>`}
function renderSalvageExchangeV135(){
 const inner=document.getElementById('modal-inner');if(!inner)return null;inner.querySelector('#v135-salvage-exchange')?.remove();const x=salvageExchangeStateV135(),host=document.createElement('div');host.id='v135-salvage-exchange';host.className='v135-salvage-exchange';
 const cards=x.pending.map(d=>{const name=d.kind==='weapon'?(ITEMS?.[d.key]?.name||d.key):(window.V11_ATTACHMENTS?.[d.key]?.name||d.key),owned=d.kind==='weapon'&&(Game.stash?.weapons||[]).includes(d.key);return`<div class="v135-salvage-card" data-salvage="${d.id}"><div class="v135-salvage-copy"><strong>${name}</strong><span>${d.manufacturerName} · ${d.kind.toUpperCase()} · ${d.quality} ${d.condition}%</span><small>${d.origin} · ${d.missionName}</small></div><div class="v135-salvage-actions"><button class="btn small" data-salvage-action="keep" ${owned?'disabled':''}>${owned?'OWNED':'KEEP'}</button><button class="btn small" data-salvage-action="sell">SELL · ¢${d.sellValue}</button><button class="btn small" data-salvage-action="strip">STRIP · ⚙${d.stripValue}</button></div></div>`}).join('');
 host.innerHTML=`<div class="v135-maint-title">SALVAGE INTAKE <span class="v135-salvage-count">${x.pending.length} PENDING · ⚙${Game.salvage||0}</span></div><div class="v135-salvage-rule">Recovery condition changes resale and parts yield only. KEEP services the item into its normal canonical combat profile.</div>${cards||'<div class="v135-salvage-empty">No field recoveries awaiting disposition.</div>'}`;
 const company=inner.querySelector('#v135-company-panel');if(company)company.insertAdjacentElement('afterend',host);else{const safe=inner.querySelector('.safe-grid');if(safe)safe.insertAdjacentElement('beforebegin',host);else inner.appendChild(host)};
 host.querySelectorAll('[data-salvage-action]').forEach(b=>b.onclick=()=>{const card=b.closest('[data-salvage]');if(card&&resolveMissionSalvageV135(card.dataset.salvage,b.dataset.salvageAction))openSafehouse()});return host
}
Object.assign(window,{salvageExchangeStateV135,salvageOfferForMissionV135,queueMissionSalvageV135,resolveMissionSalvageV135,marketSupplyContextV135,marketSupplyMultiplierV135,marketSupplyBadgeV135,renderSalvageExchangeV135});
'''
company=company.replace(insert_after,insert_after+feature,1)

old="function openSafehouseV135(){const r=V135_BASE.openSafehouse();migrateCompanyRosterV135();assignAllDeadlinesV135();renderCompanyPanelV135();return r}"
new="function openSafehouseV135(){const r=V135_BASE.openSafehouse();migrateCompanyRosterV135();assignAllDeadlinesV135();renderCompanyPanelV135();renderSalvageExchangeV135();return r}"
if company.count(old)!=1:
    raise SystemExit(f'unexpected safehouse seam count={company.count(old)}')
company=company.replace(old,new,1)
companyp.write_text(company,encoding='utf-8')

# 4) Add responsive styling to the existing company stylesheet. No new source marker is required.
cssp=root/'src/styles/13-v13-5.css'
css=cssp.read_text(encoding='utf-8')
marker='/* PWA12.104 SALVAGE MARKET CANDIDATE 01 */'
if marker in css:
    raise SystemExit('candidate CSS already present')
css += r'''

/* PWA12.104 SALVAGE MARKET CANDIDATE 01 */
.v135-salvage-exchange{margin:10px 0;padding:10px;border:1px solid rgba(228,173,76,.32);background:rgba(10,14,18,.78)}
.v135-salvage-count{float:right;font-size:7px;color:#e4ad4c;font-weight:700;letter-spacing:.8px}
.v135-salvage-rule{font-size:7px;line-height:1.5;color:#78909a;margin:4px 0 8px}
.v135-salvage-card{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;align-items:center;padding:8px 0;border-top:1px solid rgba(120,144,154,.18)}
.v135-salvage-card:first-of-type{border-top:0}
.v135-salvage-copy{min-width:0;display:flex;flex-direction:column;gap:2px}
.v135-salvage-copy strong{font-family:'Orbitron',sans-serif;font-size:8px;color:#e9f3f6;white-space:normal;overflow-wrap:anywhere}
.v135-salvage-copy span,.v135-salvage-copy small{font-size:7px;color:#78909a;line-height:1.35}
.v135-salvage-actions{display:flex;gap:4px;flex-wrap:wrap;justify-content:flex-end}
.v135-salvage-actions .btn{font-size:7px;padding:5px 7px;white-space:nowrap}
.v135-salvage-empty{padding:8px 0;font-size:7px;color:#627680}
.v135-supply{margin-top:5px;font-family:'Orbitron',sans-serif;font-size:6px;letter-spacing:.65px;opacity:.9}
.v135-supply.local{color:#65e6a3}.v135-supply.import{color:#e4ad4c}
@media(max-width:720px){
 .v135-salvage-card{grid-template-columns:1fr;align-items:stretch}
 .v135-salvage-actions{justify-content:stretch;display:grid;grid-template-columns:repeat(3,minmax(0,1fr))}
 .v135-salvage-actions .btn{width:100%;min-width:0;padding:7px 3px;white-space:normal;line-height:1.2}
 .v135-salvage-count{float:none;display:block;margin-top:3px}
}
'''
cssp.write_text(css,encoding='utf-8')

print('patched salvage intake and market scarcity candidate into',root)
