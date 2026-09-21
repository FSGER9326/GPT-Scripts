if(typeof window!=='undefined'){
(() => {
'use strict';
const V11_VERSION=11, V11_SAVE_KEY='chrome_requiem_v11_';

/* ================= CITY / SECTORS ================= */
const V11_SECTORS=[
 {id:'glass_heights',name:'GLASS HEIGHTS',tier:'rich',x0:0,y0:0,x1:7,y1:4,allegiance:'meridian',controller:'OLD-MONEY CONSORTIA',wealth:5,security:4,color:'#9d7cff',reward:1.22,industry:['kestrel'],desc:'Private skybridges, biometric lobbies and old corporate families. Crime here wears a legal department.'},
 {id:'helix_financial',name:'HELIX FINANCIAL WARD',tier:'rich',x0:8,y0:0,x1:13,y1:4,allegiance:'meridian',controller:'HELIX CONSORTIUM',wealth:5,security:5,color:'#66e6ff',reward:1.28,industry:['helix'],desc:'Trading floors and data vaults stacked above streets cleaned every six minutes by autonomous security.'},
 {id:'meridian_arcology',name:'MERIDIAN ARCOLOGY',tier:'corp',x0:14,y0:0,x1:18,y1:4,allegiance:'meridian',controller:'MERIDIAN CORP',wealth:5,security:5,color:'#e8faff',reward:1.38,industry:['kestrel','helix'],desc:'A city inside the city. Corporate citizenship, internal courts, private transit and armed response in under ninety seconds.'},
 {id:'crown_spire',name:'CROWN SPIRE',tier:'corp',x0:19,y0:0,x1:23,y1:4,allegiance:'meridian',controller:'EXTRATERRITORIAL ZONE',wealth:5,security:5,color:'#f2d76b',reward:1.42,industry:['atlas'],desc:'Embassies, black-budget offices and executive landing decks. Most residents never touch street level.'},
 {id:'neon_row',name:'NEON ROW',tier:'middle',x0:0,y0:5,x1:5,y1:9,allegiance:'chrome',controller:'CHILDREN OF CHROME',wealth:3,security:2,color:'#ff38b8',reward:1.08,industry:['mako'],desc:'Clubs, body shops, illicit clinics and chrome temples. Every alley is an advertisement for becoming somebody else.'},
 {id:'old_market',name:'OLD MARKET',tier:'middle',x0:6,y0:5,x1:10,y1:10,allegiance:'spine',controller:'SPINE BROKERS',wealth:3,security:2,color:'#b5b0a7',reward:1.02,industry:['sable'],desc:'Neutral ground by tradition, not law. Fixers, smugglers and information brokers keep the peace because business requires it.'},
 {id:'civic_circuit',name:'CIVIC CIRCUIT',tier:'middle',x0:11,y0:5,x1:15,y1:10,allegiance:'meridian',controller:'CITY SECURITY AUTHORITY',wealth:4,security:4,color:'#45bfff',reward:1.18,industry:['helix'],desc:'Hospitals, transit command, courts and municipal datacenters. Cameras are everywhere and almost none belong to the city.'},
 {id:'rail_crown',name:'RAIL CROWN',tier:'middle',x0:16,y0:5,x1:20,y1:9,allegiance:'iron',controller:'IRON TRANSIT UNION',wealth:3,security:3,color:'#ffb23d',reward:1.10,industry:['atlas','redline'],desc:'Freight mag-lines, bonded warehouses and union blocks. Whoever controls the switches controls half the city supply chain.'},
 {id:'undergrid',name:'THE UNDERGRID',tier:'poor',x0:21,y0:5,x1:23,y1:9,allegiance:'wraiths',controller:'WRAITH CELLS',wealth:1,security:1,color:'#6c77ff',reward:.96,industry:['sable'],desc:'Server heat, forgotten tunnels and illegal fiber. The Wraiths disappear here faster than security can render a warrant.'},
 {id:'ash_blocks',name:'ASH BLOCKS',tier:'poor',x0:0,y0:10,x1:5,y1:15,allegiance:'iron',controller:'RED JACKS GANG',wealth:1,security:1,color:'#ff5a35',reward:.94,industry:['redline'],desc:'Collapsed public housing and improvised markets. The Red Jacks tax power, water and anybody carrying a clean weapon.'},
 {id:'floodline',name:'FLOODLINE',tier:'poor',x0:6,y0:11,x1:11,y1:15,allegiance:'wraiths',controller:'GLASS KNIVES',wealth:1,security:1,color:'#7f63ff',reward:.98,industry:['sable'],desc:'Storm barriers failed decades ago. Residents live above the waterline; gangs and smugglers own everything beneath it.'},
 {id:'dock_nine',name:'DOCK NINE',tier:'industrial',x0:12,y0:11,x1:17,y1:15,allegiance:'iron',controller:'IRON SYNDICATE',wealth:2,security:2,color:'#ff9a2f',reward:1.08,industry:['atlas','redline'],desc:'Container stacks, fabrication yards and union muscle. Guns arrive as machine parts and leave with serials burned off.'},
 {id:'forge_belt',name:'FORGE BELT',tier:'industrial',x0:18,y0:10,x1:23,y1:15,allegiance:'iron',controller:'FOUNDRY CLANS',wealth:2,security:3,color:'#d76528',reward:1.12,industry:['redline','atlas'],desc:'Foundries, recycler furnaces and weapons subcontractors. The air tastes metallic and nothing here is truly civilian.'}
];
window.V11_SECTORS=V11_SECTORS;
function getSectorV11(x,y){return V11_SECTORS.find(s=>x>=s.x0&&x<=s.x1&&y>=s.y0&&y<=s.y1)||V11_SECTORS[5]}
window.getSectorV11=getSectorV11;
const V11PrevGetDistrict=getDistrict;
getDistrict=function(x,y){const s=getSectorV11(x,y);return{name:s.name,control:s.controller,faction:s.allegiance,sector:s,tier:s.tier,wealth:s.wealth,security:s.security}};

const V11_EXTRA_CONTACTS=[
 {id:'c6',name:'RAZOR',role:'Gang Broker · Ash Blocks',x:2,y:13,color:'#ff5a35',faction:'iron',missions:[]},
 {id:'c7',name:'YUKI TAN',role:'Arms Liaison · Glass Heights',x:5,y:2,color:'#66e6ff',faction:'meridian',missions:[]},
 {id:'c8',name:'HEXA',role:'Wraith Courier · Undergrid',x:22,y:7,color:'#737dff',faction:'wraiths',missions:[]},
 {id:'c9',name:'MARLOWE',role:'Corporate Fixer · Civic Circuit',x:13,y:8,color:'#45bfff',faction:'meridian',missions:[]},
 {id:'c10',name:'MOTHER BELL',role:'Chrome Confessor · Neon Row',x:3,y:7,color:'#ff38b8',faction:'chrome',missions:[]},
 {id:'c11',name:'FEN',role:'Dock Smuggler · Dock Nine',x:15,y:13,color:'#ff9a2f',faction:'iron',missions:[]}
];

/* ================= MANUFACTURERS / ARMORY ================= */
const V11_MANUFACTURERS={
 kestrel:{name:'KESTREL DYNAMICS',short:'KST',color:'#6ed8ff',doctrine:'Precision machining · superior range · conservative damage profile',faction:'meridian'},
 helix:{name:'HELIX ARMAMENTS',short:'HLX',color:'#55ffb0',doctrine:'Integrated smart optics · high critical potential',faction:'meridian'},
 mako:{name:'MAKO DEFENSE',short:'MKO',color:'#ffbf45',doctrine:'Compact actions · aggressive cyclic rate · street-serviceable',faction:'chrome'},
 redline:{name:'REDLINE ORDNANCE',short:'RDL',color:'#ff554f',doctrine:'Overpressure loads · brutal damage · short optimal envelope',faction:'iron'},
 sable:{name:'SABLE WORKS',short:'SBL',color:'#9c79ff',doctrine:'Low-signature actions · suppressed doctrine · covert handling',faction:'wraiths'},
 atlas:{name:'ATLAS INDUSTRIAL ARMS',short:'ATL',color:'#e4d26b',doctrine:'Heavy receivers · dependable range · industrial durability',faction:'iron'}
};
window.V11_MANUFACTURERS=V11_MANUFACTURERS;

const V11_WEAPON_SPECS=[
 ['kestrel_kite9','pistol','kestrel','KITE-9',6,5,1,8,520],['kestrel_raven','rifle','kestrel','RAVEN-4',9,7,2,8,1450],['kestrel_needle','sniper','kestrel','NEEDLE-7',16,9,2,12,2350],
 ['helix_orbit','pistol','helix','ORBIT',7,5,1,10,650],['helix_mantis','smg','helix','MANTIS',6,4,1,10,1050],['helix_specter','rifle','helix','SPECTER',10,6,2,12,1850],
 ['mako_shiver','smg','mako','SHIVER',5,4,1,5,750],['mako_riot','pistol','mako','RIOT-6',6,4,1,5,430],['mako_lancer','rifle','mako','LANCER',7,5,1,4,1300],
 ['redline_judge','pistol','redline','JUDGE',11,3,1,2,720],['redline_reaver','rifle','redline','REAVER',15,4,2,2,1700],['redline_hammer','shotgun','redline','HAMMER-12',18,2,2,0,1500],
 ['sable_whisper','pistol','sable','WHISPER',6,4,1,9,780],['sable_ghost','smg','sable','GHOST-5',5,3,1,9,1150],['sable_veil','rifle','sable','VEIL',8,5,2,10,1950],
 ['atlas_bulldog','shotgun','atlas','BULLDOG',16,3,2,3,1350],['atlas_longarm','rifle','atlas','LONGARM',12,6,2,4,1650],['atlas_mammoth','sniper','atlas','MAMMOTH',20,8,2,4,2550]
];

window.V11_WEAPON_SPECS=V11_WEAPON_SPECS;
const V11_ATTACHMENTS={
 optic_reflex:{name:'REFLEX DOT',slot:'optic',price:320,platforms:['pistol','smg','rifle','shotgun'],effects:{crit:6},desc:'+6% Crit. Fast sight picture.'},
 optic_marksman:{name:'MARKSMAN 4×',slot:'optic',price:620,platforms:['rifle','sniper'],effects:{range:1,crit:5},desc:'+1 Range, +5% Crit.'},
 optic_smart:{name:'SMARTLINK ARRAY',slot:'optic',price:820,platforms:['pistol','smg','rifle','sniper','shotgun'],effects:{crit:10},desc:'+10% Crit. Neural-assisted lead calculation.'},
 muzzle_suppressor:{name:'GHOST SUPPRESSOR',slot:'muzzle',price:560,platforms:['pistol','smg','rifle','sniper'],effects:{dmg:-1,noise:.34},desc:'Massively reduces gunshot awareness; −1 damage.'},
 muzzle_comp:{name:'VECTOR COMP',slot:'muzzle',price:460,platforms:['pistol','smg','rifle'],effects:{dmg:1,crit:3},desc:'+1 Damage, +3% Crit.'},
 muzzle_heavy:{name:'BREACH BARREL',slot:'muzzle',price:590,platforms:['rifle','sniper','shotgun'],effects:{dmg:2},desc:'+2 Damage.'},
 under_grip:{name:'GYRO FOREGRIP',slot:'under',price:410,platforms:['smg','rifle','shotgun'],effects:{crit:6},desc:'+6% Crit.'},
 under_laser:{name:'VISIBLE/IR LASE',slot:'under',price:520,platforms:['pistol','smg','rifle'],effects:{crit:8},desc:'+8% Crit.'},
 stock_stabilizer:{name:'STABILIZER STOCK',slot:'stock',price:490,platforms:['smg','rifle','sniper'],effects:{range:1},desc:'+1 Range.'},
 stock_cqb:{name:'CQB STOCK',slot:'stock',price:390,platforms:['smg','rifle','shotgun'],effects:{dmg:1,range:-1},desc:'+1 Damage, −1 Range.'}
};
window.V11_ATTACHMENTS=V11_ATTACHMENTS;

function weaponPlatformV11(k){const w=ITEMS[k]||{};return w.platform||w.baseWeapon||(['pistol','smg','rifle','sniper','shotgun'].includes(k)?k:null)}
function weaponModsForV11(u,k=u?.weapon){u.weaponMods=u.weaponMods||{};u.weaponMods[k]=u.weaponMods[k]||{};return u.weaponMods[k]}
function attachmentUsedCountV11(id){let n=0;for(const u of Game.roster||[])for(const mods of Object.values(u.weaponMods||{}))for(const v of Object.values(mods||{}))if(v===id)n++;return n}
function attachmentAvailableV11(id){return Math.max(0,(Game.armory?.attachments?.[id]||0)-attachmentUsedCountV11(id))}

const CRArtV136={
 version:'13.6',
 semantic:{
  contact:{color:'#55d9ff',shape:'contact',label:'CONTACT'},weapons:{color:'#ffb64d',shape:'weapons',label:'ARMS'},
  armor:{color:'#8fb8d8',shape:'armor',label:'ARMOR'},clinic:{color:'#65e6a3',shape:'clinic',label:'CLINIC'},
  data:{color:'#ad77ff',shape:'data',label:'DATA'},market:{color:'#e6c56e',shape:'market',label:'MARKET'},
  landmark:{color:'#57cbdc',shape:'landmark',label:'SITE'},hidden:{color:'#7b68ad',shape:'hidden',label:'HIDDEN'},
  safehouse:{color:'#f2d76b',shape:'safehouse',label:'HQ'},metro:{color:'#54d8ff',shape:'metro',label:'METRO'},
  security:{color:'#ff7668',shape:'security',label:'GATE'},freight:{color:'#f1a54e',shape:'freight',label:'FREIGHT'},
  route:{color:'#9a82ff',shape:'route',label:'ROUTE'},district:{color:'#8db5c3',shape:'district',label:'GATE'}
 },
 manufacturers:{
  kestrel:{edge:'#72ddff',fill:'#101f2b',language:'precision'},helix:{edge:'#62ffc0',fill:'#0d221d',language:'smart'},
  mako:{edge:'#ffbe48',fill:'#241b0c',language:'compact'},redline:{edge:'#ff6258',fill:'#28100f',language:'brutal'},
  sable:{edge:'#aa84ff',fill:'#1a1329',language:'stealth'},atlas:{edge:'#e8d568',fill:'#24220f',language:'heavy'}
 },
 districts:{
  ash_blocks:{motif:'patched'},old_market:{motif:'awnings'},neon_row:{motif:'signage'},glass_heights:{motif:'landscape'},
  helix_financial:{motif:'finance'},meridian_arcology:{motif:'arcology'},crown_spire:{motif:'diplomatic'},
  floodline:{motif:'waterworks'},undergrid:{motif:'conduit'},dock_nine:{motif:'cargo'},forge_belt:{motif:'industrial'},
  rail_crown:{motif:'rail'},civic_circuit:{motif:'municipal'}
 }
};
window.CRArtV136=CRArtV136;

function weaponSvgV136(key,mods={}){
 const external=Object.keys(mods||{}).length===0?window.CRAssets?.url?.('weapons',key):null;
 if(external){const label=String(ITEMS[key]?.name||key).replace(/"/g,'&quot;');return `<img src="${external}" alt="${label}" class="v14-weapon-asset" loading="lazy" decoding="async">`;}
 const w=ITEMS[key]||{},p=weaponPlatformV11(key)||'rifle',mid=w.manufacturer||String(key).split('_')[0],m=V11_MANUFACTURERS[mid]||{short:'STD',name:'Independent',color:'#8fa8b8'},art=CRArtV136.manufacturers[mid]||{edge:m.color||'#8fa8b8',fill:'#111b22',language:'field'},c=art.edge,h=Math.abs(hashString(key)),v=h%4;
 let body='',details='';
 if(p==='pistol')body=v===0?`<path d="M10 18H59L72 22V27H45L42 39H31L29 27H10Z"/>`:v===1?`<path d="M8 17H61L75 21V27H48L44 38H34L32 28H11L8 24Z"/>`:v===2?`<path d="M13 16H62L73 20V26L48 28L44 40H33L30 28H11Z"/>`:`<path d="M9 19H65L75 22V26H49L45 38H35L31 27H9Z"/>`;
 else if(p==='smg')body=v%2?`<path d="M7 15H70L80 20V26H51L48 38H37L35 27H8Z"/><path d="M18 27L7 36H23L33 27Z"/>`:`<path d="M5 18H72L82 22V27H53L48 39H36L34 28H6Z"/><path d="M14 18L5 12H27L33 18Z"/>`;
 else if(p==='shotgun')body=v%2?`<path d="M4 18H84L94 22V27H50L46 39H35L33 27H4Z"/><path d="M15 18L4 10H26L33 18Z"/>`:`<path d="M3 16H80L94 21V27H50L45 39H34L31 27H5Z"/><rect x="53" y="13" width="25" height="4" rx="2"/>`;
 else if(p==='sniper')body=v%2?`<path d="M2 18H89L97 21V25H52L48 39H38L36 25H2Z"/><path d="M16 18L4 9H27L35 18Z"/>`:`<path d="M1 17H91L98 20V24H54L48 38H38L35 25H3Z"/><path d="M13 17L5 11H29L37 17Z"/>`;
 else body=v===0?`<path d="M3 17H83L93 21V26H50L46 39H37L35 26H3Z"/><path d="M16 17L5 9H25L35 17Z"/>`:v===1?`<path d="M4 16H79L91 20V27H51L47 39H36L33 27H6Z"/><path d="M15 16L4 11H27L36 16Z"/>`:v===2?`<path d="M2 18H86L95 22V26H51L47 38H38L35 27H4Z"/><rect x="17" y="12" width="18" height="5" rx="2"/>`:`<path d="M4 17H82L92 21V25H50L45 39H36L33 26H4Z"/><path d="M9 17L2 12H25L33 17Z"/>`;
 if(art.language==='precision')details+=`<path d="M21 14H48" stroke="${c}" stroke-width="2"/><rect x="55" y="12" width="16" height="4" rx="2"/>`;
 else if(art.language==='smart')details+=`<rect x="44" y="8" width="16" height="7" rx="2"/><circle cx="52" cy="11.5" r="2.3"/><path d="M66 15L75 9"/>`;
 else if(art.language==='compact')details+=`<path d="M11 27L3 34H18L25 27Z"/><rect x="61" y="18" width="9" height="9" rx="2"/>`;
 else if(art.language==='brutal')details+=`<path d="M69 17L79 12L84 17M72 27L83 32" stroke-width="2.3"/><rect x="19" y="24" width="15" height="5"/>`;
 else if(art.language==='stealth')details+=`<rect x="79" y="18" width="18" height="8" rx="4"/><path d="M20 15H64" stroke-dasharray="3 2"/>`;
 else if(art.language==='heavy')details+=`<rect x="16" y="13" width="58" height="5" rx="2"/><path d="M48 27H62L59 41H51Z"/>`;
 const att=Object.values(mods||{}).map(id=>V11_ATTACHMENTS[id]).filter(Boolean);let overlay='';
 for(const a of att){const n=(a.name||'').toUpperCase();
  if(a.slot==='optic')overlay+=n.includes('4×')||n.includes('RANGE')?`<rect x="41" y="6" width="25" height="7" rx="2"/><circle cx="45" cy="9.5" r="4"/><circle cx="64" cy="9.5" r="3"/>`:`<rect x="44" y="8" width="14" height="7" rx="2"/><path d="M47 8V5H55V8"/>`;
  if(a.slot==='muzzle')overlay+=n.includes('SUPPRESS')||n.includes('SUBSONIC')?`<rect x="81" y="18" width="17" height="8" rx="4"/>`:`<path d="M82 18H98V26H82L88 22Z"/>`;
  if(a.slot==='under')overlay+=n.includes('GRIP')||n.includes('WEIGHT')?`<path d="M50 26H61L58 41H52Z"/>`:`<rect x="53" y="27" width="15" height="5" rx="1"/>`;
  if(a.slot==='stock')overlay+=n.includes('FOLD')?`<path d="M7 18L0 11H12L19 18Z"/>`:`<path d="M6 18L0 8H13L22 18Z"/>`;
 }
 const gid=`wg${h%997}`;
 return `<svg viewBox="0 0 100 44" aria-label="${m.name||'Weapon'} ${w.name||key}"><defs><linearGradient id="${gid}" x1="0" y1="0" x2="1" y2="1"><stop stop-color="${art.fill}"/><stop offset="1" stop-color="#06090c"/></linearGradient></defs><g fill="url(#${gid})" stroke="${c}" stroke-width="1.45" stroke-linejoin="round">${body}</g><g fill="none" stroke="${c}" stroke-width="1.05" opacity=".85">${details}</g><g fill="#172733" stroke="${c}" stroke-width="1.05">${overlay}</g><circle cx="${68+(h%8)}" cy="23" r="1.8" fill="${c}"/><path d="M6 31H27" stroke="${c}" stroke-opacity=".35"/><text x="5" y="42.5" font-family="monospace" font-size="5.2" fill="${c}">${m.short||String(mid).slice(0,3).toUpperCase()}</text></svg>`;
}
window.weaponSvgV136=weaponSvgV136;
function weaponSvgV11(key,mods={}){return weaponSvgV136(key,mods)}
window.weaponSvgV11=weaponSvgV11;

function registerManufacturedWeaponsV11(){
 for(const [id,base,mfg,model,dmg,range,ap,crit,price] of V11_WEAPON_SPECS){
  const b=ITEMS[base];if(!b)continue;ITEMS[id]={...b,name:`${V11_MANUFACTURERS[mfg].name.split(' ')[0]} ${model}`,icon:id,dmg,range,ap,crit,manufacturer:mfg,platform:base,baseWeapon:base,attachmentSlots:['optic','muzzle','under','stock'],inherentNoise:mfg==='sable'?.52:1,desc:`${V11_MANUFACTURERS[mfg].doctrine}.`};WEAPON_PRICES[id]=price;ICONS[id]=weaponSvgV11(id,{});
 }
}
registerManufacturedWeaponsV11();

function attachmentIconV136(id,a){
 const external=window.CRAssets?.url?.('attachments',id);
 if(external){const label=String(a?.name||id).replace(/"/g,'&quot;');return `<img src="${external}" alt="${label}" class="v14-attachment-asset" loading="lazy" decoding="async">`;}
 const key=String(id||a?.name||'attachment').toLowerCase(),slot=a?.slot||'under',c=slot==='optic'?'#55dfff':slot==='muzzle'?'#b878ff':slot==='under'?'#ffb14c':'#58e6a2';let g='';
 if(slot==='optic'){
  if(/thermal|spectral/.test(key))g=`<rect x="13" y="8" width="25" height="13" rx="3"/><circle cx="21" cy="14.5" r="5"/><path d="M28 10V19M32 10V19M36 10V19"/>`;
  else if(/range|marksman|4x|prism/.test(key))g=`<rect x="9" y="10" width="33" height="10" rx="4"/><circle cx="12" cy="15" r="6"/><circle cx="40" cy="15" r="5"/><path d="M22 10V6H31V10"/>`;
  else if(/smart/.test(key))g=`<rect x="15" y="7" width="22" height="14" rx="3"/><path d="M20 12H32M26 8V20"/><circle cx="26" cy="14" r="3"/>`;
  else g=`<rect x="16" y="7" width="20" height="14" rx="3"/><path d="M20 7V3H32V7"/><circle cx="26" cy="14" r="4"/>`;
 }else if(slot==='muzzle'){
  if(/suppress|subsonic/.test(key))g=`<rect x="7" y="10" width="37" height="12" rx="6"/><path d="M14 12V20M21 12V20M28 12V20M35 12V20"/>`;
  else if(/breach/.test(key))g=`<path d="M7 10H43V22H7L13 16Z"/><path d="M36 10L43 5M36 22L43 27"/>`;
  else if(/vent|comp/.test(key))g=`<rect x="8" y="10" width="35" height="12" rx="3"/><path d="M15 10L19 5M24 10L28 5M33 10L37 5"/>`;
  else g=`<path d="M8 9H42V23H8L15 16Z"/><path d="M18 11V21M28 11V21"/>`;
 }else if(slot==='under'){
  if(/bipod/.test(key))g=`<rect x="11" y="7" width="28" height="7" rx="2"/><path d="M19 14L10 29M31 14L40 29M16 27H8M34 27H42"/>`;
  else if(/launcher/.test(key))g=`<rect x="7" y="8" width="36" height="12" rx="5"/><circle cx="36" cy="14" r="5"/><path d="M17 20L14 29H22L25 20"/>`;
  else if(/sensor|laser/.test(key))g=`<rect x="8" y="8" width="34" height="11" rx="3"/><circle cx="35" cy="13.5" r="4"/><path d="M11 23H40M13 26H37" stroke-dasharray="3 2"/>`;
  else if(/weight/.test(key))g=`<rect x="8" y="8" width="34" height="10" rx="2"/><path d="M13 18H37L34 29H16Z"/>`;
  else g=`<rect x="10" y="7" width="30" height="8" rx="2"/><path d="M20 15H31L28 29H22Z"/>`;
 }else{
  if(/fold/.test(key))g=`<path d="M8 13H28L43 5V11L31 17L43 24V29L27 20H8Z"/>`;
  else if(/precision|stabil/.test(key))g=`<path d="M6 12H29L44 5V27L29 20H6Z"/><path d="M29 12H42M29 20H42"/>`;
  else if(/shock/.test(key))g=`<path d="M7 11H28L43 5V27L28 21H7Z"/><path d="M31 9L38 14L31 19"/>`;
  else g=`<path d="M8 12H29L43 6V26L29 20H8Z"/><path d="M34 9V23"/>`;
 }
 return `<svg viewBox="0 0 50 32" aria-label="${a?.name||id}"><g fill="#0d1820" stroke="${c}" stroke-width="1.35" stroke-linejoin="round">${g}</g><path d="M5 29H45" stroke="${c}" stroke-opacity=".24"/><circle cx="5" cy="29" r="1.2" fill="${c}"/></svg>`;
}
window.attachmentIconV136=attachmentIconV136;
function attachmentIconV11(a){const id=Object.entries(V11_ATTACHMENTS||{}).find(([,x])=>x===a)?.[0]||a?.name||'';return attachmentIconV136(id,a)}
window.attachmentIconV11=attachmentIconV11;

function ensureV11Actors(){
 for(const c of V11_EXTRA_CONTACTS)if(!Game.contacts.some(x=>x.id===c.id))Game.contacts.push({...c,missions:[]});
 const vendors=[
  {id:'v_kestrel',name:'KESTREL GALLERY',type:'weapon',x:6,y:2,color:'#6ed8ff',stock:['kestrel_kite9','kestrel_raven','kestrel_needle']},
  {id:'v_helix',name:'HELIX SYSTEMS ARMORY',type:'weapon',x:12,y:2,color:'#55ffb0',stock:['helix_orbit','helix_mantis','helix_specter']},
  {id:'v_mako',name:'MAKO STREET DEPOT',type:'weapon',x:2,y:8,color:'#ffbf45',stock:['mako_riot','mako_shiver','mako_lancer']},
  {id:'v_sable',name:'SABLE QUIET ROOM',type:'weapon',x:9,y:8,color:'#9c79ff',stock:['sable_whisper','sable_ghost','sable_veil']},
  {id:'v_redline',name:'REDLINE FOUNDRY SALES',type:'weapon',x:20,y:12,color:'#ff554f',stock:['redline_judge','redline_reaver','redline_hammer']},
  {id:'v_atlas',name:'ATLAS INDUSTRIAL ARMS',type:'weapon',x:16,y:13,color:'#e4d26b',stock:['atlas_bulldog','atlas_longarm','atlas_mammoth']}
 ];
 for(const v of vendors)if(!Game.vendors.some(x=>x.id===v.id))Game.vendors.push({...v,stock:[...v.stock]});
}

/* ================= FACTION CAREERS ================= */
const V11_FACTION_RANKS=[
 {min:-999,name:'BLACKLISTED',perk:'Hostile or burned relationship.'},{min:0,name:'OUTSIDER',perk:'Standard contracts and public vendors.'},
 {min:10,name:'KNOWN QUANTITY',perk:'Faction fixers begin offering repeat work.'},{min:30,name:'ASSET',perk:'Faction procurement and specialist contracts.'},
 {min:55,name:'OPERATIVE',perk:'Global faction operations become available.'},{min:80,name:'INNER CIRCLE',perk:'Signature weapon procurement and endgame jobs.'}
];
window.V11_FACTION_RANKS=V11_FACTION_RANKS;
function factionRankV11(f){const r=Game.rep?.[f]||0;let out=V11_FACTION_RANKS[0];for(const x of V11_FACTION_RANKS)if(r>=x.min)out=x;return out}
function factionRankIndexV11(f){return V11_FACTION_RANKS.indexOf(factionRankV11(f))}
window.factionRankV11=factionRankV11;
const V11_SIGNATURE={meridian:'kestrel_needle',wraiths:'sable_veil',iron:'atlas_mammoth',chrome:'mako_lancer',spine:'helix_specter'};
function checkFactionPromotionsV11(){
 Game.factionPromotions=Game.factionPromotions||{};
 for(const f of Object.keys(FACTIONS)){const idx=factionRankIndexV11(f),old=Game.factionPromotions[f]??1;if(idx>old){for(let i=old+1;i<=idx;i++)if(i>=2)addJournal('main',`${FACTIONS[f].name}: ${V11_FACTION_RANKS[i].name}`,`Your standing with ${FACTIONS[f].name} has advanced. ${V11_FACTION_RANKS[i].perk}`);toast(`${FACTIONS[f].short}: ${V11_FACTION_RANKS[idx].name}`)}Game.factionPromotions[f]=Math.max(old,idx)}
}
window.checkFactionPromotionsV11=checkFactionPromotionsV11;
function claimFactionProcurementV11(f){
 if((Game.rep[f]||0)<80)return false;Game.factionClaims=Game.factionClaims||{};if(Game.factionClaims[f])return false;
 const k=V11_SIGNATURE[f];if(k&&!Game.stash.weapons.includes(k))Game.stash.weapons.push(k);Game.factionClaims[f]=true;addJournal('main','Inner Circle Procurement',`${FACTIONS[f].name} issued ${ITEMS[k]?.name||k} from restricted inventory.`);toast(`SIGNATURE WEAPON: ${ITEMS[k]?.name||k}`);saveGame(0,true);renderFactions();return true;
}

window.claimFactionProcurementV11=claimFactionProcurementV11;
/* ================= WORLD NETWORK ================= */
const V11_WORLD_LOCATIONS=[
 {id:'rhine',name:'RHINE FREEPORT',region:'EUROPE · RHINE-RUHR',x:48,y:30,color:'#67d9ff',act:1,cost:450,hours:8,manufacturer:'kestrel',faction:null,rep:0,danger:2,desc:'Autonomous freight enclaves stitched between old industrial cities. Smuggling, corporate deniability and excellent rail access.'},
 {id:'tokyo',name:'TOKYO BAY ARCOLOGY',region:'PACIFIC · JAPAN',x:83,y:35,color:'#ff68c8',act:2,cost:900,hours:14,manufacturer:'helix',faction:'meridian',rep:20,danger:4,desc:'Vertical corporate territory built into the bay. Contract work is precise, expensive and watched from every angle.'},
 {id:'lagos',name:'LAGOS VERTICAL',region:'AFRICA · GULF OF GUINEA',x:50,y:62,color:'#ffbf45',act:2,cost:720,hours:12,manufacturer:'mako',faction:'chrome',rep:10,danger:3,desc:'Hyper-dense trade towers, fabrication markets and private power grids. Fast money, faster weapons.'},
 {id:'singapore',name:'SINGAPORE ORBITAL GATE',region:'SE ASIA · STRAIT',x:76,y:59,color:'#55ffb0',act:2,cost:1100,hours:16,manufacturer:'helix',faction:'meridian',rep:30,danger:4,desc:'Earthside logistics for orbital industry. Corporate customs has military hardware and no sense of humor.'},
 {id:'saopaulo',name:'SÃO PAULO VERTICAL ZONE',region:'SOUTH AMERICA · BRAZIL',x:34,y:75,color:'#ff554f',act:2,cost:850,hours:15,manufacturer:'redline',faction:'iron',rep:20,danger:4,desc:'Megablocks, cartel logistics and aftermarket arms factories spread across a city that never stopped growing.'},
 {id:'detroit',name:'DETROIT ARSENAL BELT',region:'NORTH AMERICA · GREAT LAKES',x:25,y:36,color:'#e4d26b',act:3,cost:1250,hours:13,manufacturer:'atlas',faction:'iron',rep:35,danger:5,desc:'Automated plants and defense contractors surrounded by fortified labor districts. Heavy hardware is the local language.'},
 {id:'reykjavik',name:'REYKJAVÍK DATA HAVEN',region:'NORTH ATLANTIC · ICELAND',x:39,y:15,color:'#9c79ff',act:2,cost:980,hours:11,manufacturer:'sable',faction:'wraiths',rep:30,danger:3,desc:'Cold datacenters, sovereign compute vaults and quiet professionals. Most operations here are over before anybody hears a shot.'}
];
window.V11_WORLD_LOCATIONS=V11_WORLD_LOCATIONS;
function worldUnlockedV11(l){return (Game.act||1)>=l.act&&(!l.faction||(Game.rep[l.faction]||0)>=l.rep)}
function generateWorldMissionV11(l){
 const templates=[
  {type:'heist',name:'EXTRATERRITORIAL DATA HEIST',desc:'Breach three secure nodes and exfiltrate the package.',base:1650,en:['Enforcer','Drone','Heavy']},
  {type:'bounty',name:'INTERNATIONAL PRIORITY TARGET',desc:'A protected target crossed borders. Remove them before local security closes the window.',base:1850,en:['Enforcer','Enforcer','Boss']},
  {type:'sabotage',name:'FOREIGN INFRASTRUCTURE HIT',desc:'Destroy critical infrastructure without letting the client appear in the chain of custody.',base:1750,en:['Guard','Heavy','Drone']},
  {type:'eliminate',name:'BLACK-BAG CLEANUP',desc:'A deniable team failed. Remove survivors and recover anything that identifies the sponsor.',base:1550,en:['Guard','Enforcer','Heavy']}
 ];
 const t=templates[Math.floor(seededRandom()*templates.length)],diff=Math.min(3,Math.max(2,l.danger-1)),target=['meridian','wraiths','iron','chrome'][Math.floor(seededRandom()*4)];
 return{id:`world_${l.id}_${Game.day}_${Math.floor(seededRandom()*99999)}`,contact:null,type:t.type,objective:t.type,name:`${l.name} // ${t.name}`,desc:t.desc,enemies:[...t.en,...Array.from({length:Math.max(0,diff-2)},()=>diff===3?'Enforcer':'Guard')],diff,reward:t.base+diff*350,xp:130+diff*55,targetFaction:target,factionRepGain:0,factionRepLoss:{[target]:-(4+diff)},worldLocation:l.id,lootManufacturer:l.manufacturer,area:l.name};
}
window.generateWorldMissionV11=generateWorldMissionV11;
function launchWorldContractV11(id){
 ensureV11State();const l=V11_WORLD_LOCATIONS.find(x=>x.id===id);if(!l||!worldUnlockedV11(l)){toast('Global route locked.');return false}if(Game.credits<l.cost){toast('Not enough credits for transit and forged clearances.');return false}
 Game.credits-=l.cost;advanceTime(l.hours*60);Game.world.current=l.id;Game.world.trips=(Game.world.trips||0)+1;addJournal('main',`Deployment: ${l.name}`,`Paid ¢${l.cost} for transit, forged manifests and local transport. Global contract initiated.`);const m=generateWorldMissionV11(l);saveGame(0,true);startMission(m);return true;
}
window.launchWorldContractV11=launchWorldContractV11;

/* ================= STATE / WORLD ACTORS ================= */
function ensureV11State(){
 ResponsiveSystemsV14.ensureState();Game.armory=Game.armory||{attachments:{}};Game.armory.attachments=Game.armory.attachments||{};
 Game.world=Game.world||{current:'city',trips:0,completed:0,visited:[]};Game.world.visited=Game.world.visited||[];
 Game.city=Game.city||{visited:[]};Game.factionPromotions=Game.factionPromotions||{};Game.factionClaims=Game.factionClaims||{};
 for(const u of Game.roster||[]){u.weaponMods=u.weaponMods||{}}
 ensureV11Actors();
 const s=getSectorV11(Game.ovPlayer?.x||0,Game.ovPlayer?.y||0);if(s&&!Game.city.visited.includes(s.id))Game.city.visited.push(s.id);
}
window.ensureV11State=ensureV11State;

/* ================= UI ================= */
function injectV11UI(){
 ensureV11State();const app=document.getElementById('app'),ow=document.getElementById('overworld-screen');if(!app)return;
 if(!document.getElementById('v11-city-screen')){const s=document.createElement('div');s.id='v11-city-screen';s.className='screen';s.innerHTML=`<div class="v11-screen-head"><div><div class="v11-screen-title">MEGACITY ATLAS</div><div class="v11-screen-sub">Socio-economic sectors · territorial control · local risk</div></div><div class="spacer"></div><button class="btn small" id="v11-city-back">◀ CITY</button></div><div class="v11-scroll" id="v11-city-body"></div>`;app.appendChild(s);s.querySelector('#v11-city-back').onclick=()=>showScreen('overworld-screen')}
 if(!document.getElementById('v11-world-screen')){const s=document.createElement('div');s.id='v11-world-screen';s.className='screen';s.innerHTML=`<div class="v11-screen-head"><div><div class="v11-screen-title">GLOBAL CONTRACT NETWORK</div><div class="v11-screen-sub">Off-city operations · international transit · manufacturer access</div></div><div class="spacer"></div><button class="btn small" id="v11-world-back">◀ CITY</button></div><div class="v11-scroll" id="v11-world-body"></div>`;app.appendChild(s);s.querySelector('#v11-world-back').onclick=()=>showScreen('overworld-screen')}
 const tb=document.querySelector('#overworld-screen>.topbar');if(tb&&!document.getElementById('ov-city-v11')){const fac=document.getElementById('ov-fac-btn');const b=document.createElement('button');b.className='btn small';b.id='ov-city-v11';b.textContent='CITY';b.onclick=()=>{renderCityAtlasV11();showScreen('v11-city-screen')};tb.insertBefore(b,fac);const w=document.createElement('button');w.className='btn small';w.id='ov-world-v11';w.textContent='WORLD';w.onclick=()=>{renderWorldNetworkV11();showScreen('v11-world-screen')};tb.insertBefore(w,fac)}
 const drawer=document.getElementById('v10-mobile-drawer');if(drawer&&!drawer.querySelector('[data-v11-city]')){const anchor=drawer.querySelector('[data-v10-go="journal"]');const c=document.createElement('button');c.className='btn';c.dataset.v11City='1';c.textContent='MEGACITY ATLAS';c.onclick=()=>{drawer.classList.remove('open');renderCityAtlasV11();showScreen('v11-city-screen')};drawer.insertBefore(c,anchor);const w=document.createElement('button');w.className='btn';w.dataset.v11World='1';w.textContent='GLOBAL NETWORK';w.onclick=()=>{drawer.classList.remove('open');renderWorldNetworkV11();showScreen('v11-world-screen')};drawer.insertBefore(w,anchor)}
 const menu=document.getElementById('menu-box');if(menu&&!document.getElementById('menu-diag-v11')){const b=document.createElement('button');b.className='btn';b.id='menu-diag-v11';b.textContent='◇ V11 SYSTEM DIAGNOSTICS';b.onclick=()=>{const d=runDiagnosticsV11();toast(`V11 diagnostics ${d.passed}/${d.total}`)};menu.insertBefore(b,document.getElementById('menu-quit'))}
 const tag=document.getElementById('intro-tag');if(tag&&!tag.dataset.v11){tag.dataset.v11='1';tag.textContent=tag.textContent.replace(/· V10\b/,'· V11');if(!/V11/.test(tag.textContent))tag.textContent+=' · V11'}
}
function routeToSectorV11(id){
 const s=V11_SECTORS.find(x=>x.id===id);if(!s)return false;showScreen('overworld-screen');initOverworld();let best=null;
 for(let y=s.y0;y<=s.y1;y++)for(let x=s.x0;x<=s.x1;x++)if(isWalkable(x,y)){const d=Math.abs(x-(s.x0+s.x1)/2)+Math.abs(y-(s.y0+s.y1)/2);if(!best||d<best.d)best={x,y,d}}
 if(!best)return false;const p=findPath(Game.ovPlayer,{x:best.x,y:best.y});if(p&&p.length>1){Game.pendingPath=p;toast(`Route set: ${s.name}`);return true}toast('No route found.');return false;
}
function renderCityAtlasV11(){
 ensureV11State();const body=document.getElementById('v11-city-body'),cur=getSectorV11(Game.ovPlayer.x,Game.ovPlayer.y);body.innerHTML=`<div class="v11-sector-grid">${V11_SECTORS.map(s=>`<div class="v11-sector ${s.id===cur.id?'current':''}" style="--v11-accent:${s.color}"><div class="v11-sector-name">${s.name}${s.id===cur.id?' · CURRENT':''}</div><div class="v11-tier">${s.tier.toUpperCase()} · ${s.controller}</div><div class="v11-sector-desc">${s.desc}</div><div class="v11-sector-meta"><div class="v11-meta">WEALTH<b>${'◆'.repeat(s.wealth)}${'◇'.repeat(5-s.wealth)}</b></div><div class="v11-meta">SECURITY<b>${'◆'.repeat(s.security)}${'◇'.repeat(5-s.security)}</b></div><div class="v11-meta">ARMS<b>${s.industry.map(x=>V11_MANUFACTURERS[x].short).join(' / ')}</b></div></div><div class="v11-sector-actions"><button class="btn small" data-route="${s.id}">SET ROUTE</button></div></div>`).join('')}</div>`;body.querySelectorAll('[data-route]').forEach(b=>b.onclick=()=>routeToSectorV11(b.dataset.route))}
window.renderCityAtlasV11=renderCityAtlasV11;

function renderWorldNetworkV11(){
 ensureV11State();const body=document.getElementById('v11-world-body');const nodes=V11_WORLD_LOCATIONS.map(l=>`<div class="v11-node ${l.x>68?'right':''}" style="left:${l.x}%;top:${l.y}%;--node:${l.color}"><span>${l.name}</span></div>`).join('');
 body.innerHTML=`<div class="v11-world-layout"><div class="v11-globe">${nodes}</div><div class="v11-world-list">${V11_WORLD_LOCATIONS.map(l=>{const unlock=worldUnlockedV11(l),m=V11_MANUFACTURERS[l.manufacturer];let req=`ACT ${l.act}`;if(l.faction)req+=` · ${FACTIONS[l.faction].short} REP ${l.rep}`;return`<div class="v11-world-card ${unlock?'':'locked'}" style="--loc:${l.color}"><div class="v11-world-name">${l.name}</div><div class="v11-world-region">${l.region}</div><div class="v11-world-desc">${l.desc}</div><div class="v11-world-meta">THREAT <b>${'◆'.repeat(l.danger)}</b><br>TRANSIT <b>¢${l.cost} · ${l.hours}h</b><br>LOCAL ARMS <b style="color:${m.color}">${m.name}</b></div>${unlock?`<button class="btn primary" data-world="${l.id}" style="width:100%">DEPLOY GLOBAL CONTRACT</button>`:`<div class="v11-lock">LOCKED · ${req}</div>`}</div>`}).join('')}</div></div>`;body.querySelectorAll('[data-world]').forEach(b=>b.onclick=()=>launchWorldContractV11(b.dataset.world))}
window.renderWorldNetworkV11=renderWorldNetworkV11;

/* Sector overlay on city */
function drawSectorOverlayV11(){
 if(Game.screen!=='overworld-screen'||!Game.ovCtx||!PerformanceV14.metrics()?.overworld)return;const ctx=Game.ovCtx,m=PerformanceV14.metrics().overworld;ctx.save();ctx.font=`700 ${Math.max(6,Math.min(9,m.tile*.22))}px Orbitron`;ctx.textAlign='center';ctx.textBaseline='middle';
 for(const s of V11_SECTORS){const x=m.offX+s.x0*m.tile,y=m.offY+s.y0*m.tile,w=(s.x1-s.x0+1)*m.tile,h=(s.y1-s.y0+1)*m.tile;ctx.strokeStyle=s.color+'55';ctx.lineWidth=1;ctx.strokeRect(x+.5,y+.5,w-1,h-1);ctx.fillStyle=s.color+'10';ctx.fillRect(x,y,w,h);if(w>70&&h>45){ctx.fillStyle=s.color+'aa';ctx.fillText(s.name,x+w/2,y+h/2)}}
 ctx.restore();
}
const V11PrevOverworldLoop=overworldLoop;
overworldLoop=function(t){V11PrevOverworldLoop(t);drawSectorOverlayV11()};

/* ================= MISSIONS BY DISTRICT ================= */
const V11PrevGenerateMissions=generateMissions;
generateMissions=function(){
 ensureV11State();V11PrevGenerateMissions();
 for(const c of Game.contacts){const s=getSectorV11(c.x,c.y);for(const m of c.missions||[]){m.sectorId=s.id;m.area=s.name;m.reward=Math.round(m.reward*s.reward);m.desc=`${m.desc} AO: ${s.name}. ${s.tier.toUpperCase()} sector · Security ${s.security}/5.`}}
};
const V11PrevBrief=showMissionBriefingV10;
showMissionBriefingV10=function(m){V11PrevBrief(m);const body=document.getElementById('v10-brief-body');if(!body)return;const l=m.worldLocation?V11_WORLD_LOCATIONS.find(x=>x.id===m.worldLocation):null,s=!l?V11_SECTORS.find(x=>x.id===m.sectorId)||getSectorV11(Game.ovPlayer.x,Game.ovPlayer.y):null;const chip=document.createElement('div');chip.className='v11-theater';chip.innerHTML=`OPERATION THEATER <span class="v11-sector-chip">${l?l.name:s.name}</span> · ${l?'GLOBAL DEPLOYMENT':`${s.tier.toUpperCase()} / SEC ${s.security}`}`;body.insertBefore(chip,body.firstChild)};
const V11PrevInitCombat=initCombat;
initCombat=function(m){const r=V11PrevInitCombat(m);const combat=document.getElementById('combat'),s=m.worldLocation?null:(V11_SECTORS.find(x=>x.id===m.sectorId)||getSectorV11(Game.ovPlayer.x,Game.ovPlayer.y));combat.dataset.v11Tier=m.worldLocation?'world':(s?.tier==='industrial'?'poor':s?.tier||'middle');return r};

/* ================= WEAPON BENCH / ATTACHMENTS ================= */
function attachmentCompatibleV11(a,weaponKey){const p=weaponPlatformV11(weaponKey);return !!p&&a.platforms.includes(p)}
function installAttachmentV11(u,weaponKey,id){
 ensureV11State();const a=V11_ATTACHMENTS[id];if(!u||!a||!attachmentCompatibleV11(a,weaponKey))return false;const mods=weaponModsForV11(u,weaponKey),old=mods[a.slot];
 if(old===id)return true;if(attachmentAvailableV11(id)<=0){toast('No free copy of that attachment.');return false}mods[a.slot]=id;applySkillsToUnit(u);toast(`${a.name} installed.`);saveGame(0,true);return true;
}
window.installAttachmentV11=installAttachmentV11;
function removeAttachmentV11(u,weaponKey,slot){const mods=weaponModsForV11(u,weaponKey);if(!mods[slot])return false;delete mods[slot];applySkillsToUnit(u);saveGame(0,true);return true}
function buyAttachmentV11(id){const a=V11_ATTACHMENTS[id];if(!a||Game.credits<a.price){toast('Not enough credits.');return false}Game.credits-=a.price;Game.armory.attachments[id]=(Game.armory.attachments[id]||0)+1;toast(`${a.name} added to armory.`);updateOverworldHUD();saveGame(0,true);return true}
function renderWeaponBenchV11(body){
 ensureV11State();const u=Game.roster[Game.selectedCrewIndex];if(!u)return;const w=ITEMS[u.weapon]||{},p=weaponPlatformV11(u.weapon),mods=weaponModsForV11(u,u.weapon),m=V11_MANUFACTURERS[w.manufacturer]||{name:'LEGACY / UNBRANDED',color:'#8fa8b8',doctrine:'Standard city-market weapon.'};
 const bench=document.createElement('div');bench.className='v11-bench';if(!p){bench.innerHTML=`<div class="v11-weapon-name">${w.name||u.weapon}</div><div class="v11-weapon-stats">This weapon platform does not accept ballistic attachments.</div>`;body.appendChild(bench);return}
 const slots=['optic','muzzle','under','stock'];bench.innerHTML=`<div class="v11-bench-head"><div class="v11-weapon-hero">${weaponSvgV11(u.weapon,mods)}</div><div class="v11-weapon-data"><div class="v11-weapon-name">${w.name}</div><div class="v11-mfg" style="color:${m.color}">${m.name} · ${p.toUpperCase()} PLATFORM</div><div class="v11-weapon-stats">DMG ${u.damage} · RANGE ${u.range} · AP ${w.ap||1} · CRIT ${u.critChance}%<br>${m.doctrine}</div></div></div><div class="v11-mod-grid">${slots.map(slot=>{const iid=mods[slot],ia=iid?V11_ATTACHMENTS[iid]:null,opts=Object.entries(V11_ATTACHMENTS).filter(([id,a])=>a.slot===slot&&attachmentCompatibleV11(a,u.weapon));return`<div class="v11-mod-slot"><h5>${slot.toUpperCase()}</h5><div class="installed">${ia?ia.name:'EMPTY'}</div>${ia?`<button class="btn small" data-remove="${slot}">REMOVE</button>`:''}<div class="v11-mod-options">${opts.map(([id,a])=>`<button class="btn small" data-install="${id}" ${attachmentAvailableV11(id)<=0&&mods[slot]!==id?'disabled':''}>${a.name} ×${Game.armory.attachments[id]||0}</button>`).join('')}</div></div>`}).join('')}</div>`;
 bench.querySelectorAll('[data-install]').forEach(b=>b.onclick=()=>{if(installAttachmentV11(u,u.weapon,b.dataset.install)){renderCrewScreen()}});
 bench.querySelectorAll('[data-remove]').forEach(b=>b.onclick=()=>{removeAttachmentV11(u,u.weapon,b.dataset.remove);renderCrewScreen()});body.appendChild(bench);
}
window.renderWeaponBenchV11=renderWeaponBenchV11;
const V11PrevRenderInventory=renderInventory;
renderInventory=function(body){V11PrevRenderInventory(body);renderWeaponBenchV11(body)};

const V11PrevApplySkills=applySkillsToUnit;
applySkillsToUnit=function(u){V11PrevApplySkills(u);const w=ITEMS[u.weapon]||{};if(w.crit)u.critChance+=(w.crit||0);const mods=weaponModsForV11(u,u.weapon);for(const id of Object.values(mods)){const a=V11_ATTACHMENTS[id];if(!a)continue;const e=a.effects||{};u.damage+=e.dmg||0;u.range=Math.max(1,u.range+(e.range||0));u.critChance+=e.crit||0;u.move=Math.max(1,u.move+(e.move||0))}u.damage=Math.max(1,u.damage);u.critChance=Math.max(0,u.critChance)};
const V11PrevMakeNoise=makeNoise;
makeNoise=function(x,y,amount=50){const shooter=Game.units?.find(u=>u.team==='player'&&u.x===x&&u.y===y&&u.hp>0),w=shooter?ITEMS[shooter.weapon]:null,modOwner=shooter?.rosterRef||shooter,mods=shooter?weaponModsForV11(modOwner,shooter.weapon):{},sup=Object.values(mods).map(id=>V11_ATTACHMENTS[id]).find(a=>a?.effects?.noise);let mult=w?.inherentNoise||1;if(sup)mult*=sup.effects.noise;return V11PrevMakeNoise(x,y,amount*mult)};

/* weapon vendors gain attachment inventory */
const V11PrevOpenVendor=openVendor;
openVendor=function(vendor){const r=V11PrevOpenVendor(vendor);if(vendor?.type==='weapon'&&vendor?.type!=='hire'){ensureV11State();const g=document.getElementById('vendor-grid');for(const [id,a] of Object.entries(V11_ATTACHMENTS)){const el=document.createElement('div');el.className='vendor-item v11-att-vendor';el.innerHTML=`<div class="v11-att-icon">${attachmentIconV11(a)}</div><div class="vi-info"><div class="vi-name">${a.name}</div><div class="vi-desc">${a.slot.toUpperCase()} · ${a.desc}</div><div class="vi-price">¢ ${a.price}</div></div>`;el.onclick=()=>{if(buyAttachmentV11(id))openVendor(vendor)};g.appendChild(el)}}return r};

/* ================= FACTION UI ================= */
const V11PrevRenderFactions=renderFactions;
renderFactions=function(){V11PrevRenderFactions();ensureV11State();checkFactionPromotionsV11();const body=document.getElementById('faction-body'),wrap=document.createElement('div');wrap.className='v11-career-wrap';wrap.innerHTML=`<div class="v11-career-title">FACTION CAREERS / PROCUREMENT</div><div class="v11-career-grid">${Object.entries(FACTIONS).map(([f,def])=>{const rep=Game.rep[f]||0,r=factionRankV11(f),idx=factionRankIndexV11(f),next=V11_FACTION_RANKS[idx+1],pct=next?Math.max(0,Math.min(100,((rep-r.min)/(next.min-r.min))*100)):100,claim=(rep>=80&&!Game.factionClaims[f]);return`<div class="v11-career" style="--fac:${def.color}"><h4>${def.name}</h4><div class="v11-career-rank">${r.name} · REP ${rep>=0?'+':''}${rep}</div><p>${r.perk}${next?` Next: ${next.name} @ ${next.min}.`:' Maximum standing reached.'}</p><div class="v11-rankbar"><i style="width:${pct}%"></i></div>${claim?`<button class="btn small" data-claim="${f}" style="width:100%;margin-top:7px">CLAIM INNER-CIRCLE WEAPON</button>`:Game.factionClaims[f]?'<div style="font:700 7px Orbitron;color:#00ff88;margin-top:7px">SIGNATURE PROCUREMENT CLAIMED</div>':''}</div>`}).join('')}</div>`;body.appendChild(wrap);wrap.querySelectorAll('[data-claim]').forEach(b=>b.onclick=()=>claimFactionProcurementV11(b.dataset.claim))};

/* ================= STORY EXPANSION ================= */
STORY.v11_city_layers={text:`Mira projects the city over the table — not as streets, but as prices.\n\n“Stop thinking of it as one city. Glass Heights buys laws. Meridian Arcology writes them. Ash Blocks survives underneath them. Dock Nine moves the hardware, the Undergrid moves the secrets, and Old Market sells introductions between people who pretend they never met.”\n\nShe taps the map. “Every contract has an address. Addresses have class, security and owners. Learn the layers or die between them.”`,choices:[{text:'— “Show me who owns what.” —',flag:'v11_city_layers_seen',journal:{type:'main',title:'City of Layers',desc:'Mira taught you to read the megacity as wealth, security and territorial control.',status:'Use the CITY atlas'}}]};
STORY.v11_arms_race={text:`Yuki Tan lays three rifles on a white cloth. None share a single screw.\n\n“Kestrel sells certainty. Redline sells fear. Sable sells absence. Helix sells the idea the gun is smarter than its owner.”\n\nShe slides a case of optics and muzzle assemblies toward you.\n\n“Stop buying guns. Start building platforms.”`,choices:[{text:'— Open the armory case. —',flag:'v11_arms_race_seen',journal:{type:'main',title:'The Arms Race',desc:'Manufacturer weapon platforms and modular attachments are now part of your procurement strategy.',status:'Customize weapons in CREW → GEAR'}}]};
STORY.v11_faction_crossroads={text:`Five encrypted invitations arrive inside the same minute.\n\nMeridian calls you an “external strategic asset.” The Wraiths call you “trusted enough.” Iron offers a chair at a table with armed guards. The Children promise a new body. Oracle sends only an address and the words: YOU ARE EXPENSIVE NOW.\n\nYou have crossed the line between freelancer and political actor.`,choices:[{text:'— Work every angle. —',flag:'v11_crossroads_independent',onChoose:()=>{Game.rep.spine=(Game.rep.spine||0)+5},journal:{type:'main',title:'No Single Flag',desc:'You refused to become anybody’s property. Every faction remains a possible ladder—or enemy.',status:'Advance faction careers independently'}},{text:'— Power requires patrons. —',flag:'v11_crossroads_patron',onChoose:()=>{const f=Object.keys(Game.rep).sort((a,b)=>(Game.rep[b]||0)-(Game.rep[a]||0))[0];Game.rep[f]=(Game.rep[f]||0)+8},journal:{type:'main',title:'Patronage',desc:'You leaned into your strongest faction relationship. The city noticed.',status:'Reach INNER CIRCLE standing'}}]};
STORY.v11_world_open={text:`Oracle’s brass key opens a room beneath Old Market.\n\nInside is not a vault. It is a departure board.\n\nRhine Freeport. Tokyo Bay. Lagos. Singapore. São Paulo. Detroit. Reykjavík.\n\n“Chrome City was never the board,” Oracle says behind you. “It was the interview.”\n\nA dozen international contracts begin bidding for your crew before he finishes the sentence.`,choices:[{text:'— “Book the route.” —',flag:'v11_world_open_seen',journal:{type:'main',title:'The World Opens',desc:'Your crew can now take international deployments through the GLOBAL CONTRACT NETWORK.',status:'Open WORLD from the city HUD'}}]};
STORY.v11_world_aftermath={text:`The return flight crosses the city before dawn. For the first time, the towers below look small.\n\nMira sends a single message: YOU LEFT LOCAL.\n\nThen another: THAT MEANS LOCAL PROBLEMS CAN FOLLOW YOU ANYWHERE.\n\nYour crew is no longer a neighborhood outfit. Manufacturers, security services and faction leadership now treat you as something exportable.`,choices:[{text:'— Keep going. —',flag:'v11_world_aftermath_seen',journal:{type:'main',title:'No Longer Local',desc:'Completing an international operation changed how the city sees your crew.',status:'Pursue global and faction endgame contracts'}}]};
function progressStoryV11(){
 const wins=Game.missionHistory?.length||0,repMax=Math.max(...Object.values(Game.rep||{}),0);let key=null,flag=null;
 if(wins>=3&&!Game.storyFlags.v11_city_layers_queued){key='v11_city_layers';flag='v11_city_layers_queued'}
 else if(wins>=5&&!Game.storyFlags.v11_arms_race_queued){key='v11_arms_race';flag='v11_arms_race_queued'}
 else if(repMax>=55&&!Game.storyFlags.v11_crossroads_queued){key='v11_faction_crossroads';flag='v11_crossroads_queued'}
 else if((Game.act||1)>=2&&wins>=8&&!Game.storyFlags.v11_world_open_queued){key='v11_world_open';flag='v11_world_open_queued'}
 else if((Game.world?.completed||0)>=1&&!Game.storyFlags.v11_world_aftermath_queued){key='v11_world_aftermath';flag='v11_world_aftermath_queued'}
 if(key){Game.storyFlags[flag]=true;setTimeout(()=>playStory(key),2350)}
}

/* ================= LOOT / GLOBAL RESOLUTION ================= */
function awardManufacturerLootV11(m){
 ensureV11State();let mfg=m?.lootManufacturer;if(!mfg){const s=V11_SECTORS.find(x=>x.id===m?.sectorId);if(s?.industry?.length)mfg=s.industry[Math.floor(seededRandom()*s.industry.length)]}
 if(!mfg)return;const weapons=V11_WEAPON_SPECS.filter(x=>x[2]===mfg).map(x=>x[0]);if((m?.worldLocation||seededRandom()<.20)&&weapons.length){const k=weapons[Math.floor(seededRandom()*weapons.length)];if(!Game.stash.weapons.includes(k)){Game.stash.weapons.push(k);addJournal('main','Recovered Weapon',`${ITEMS[k].name} recovered from the operation.`);toast(`LOOT: ${ITEMS[k].name}`);return}}
 if(m?.worldLocation||seededRandom()<.42){const ids=Object.keys(V11_ATTACHMENTS),id=ids[Math.floor(seededRandom()*ids.length)];Game.armory.attachments[id]=(Game.armory.attachments[id]||0)+1;toast(`LOOT: ${V11_ATTACHMENTS[id].name}`)}
}
const V11PrevFinalizeSuccess=finalizeMissionSuccess;
finalizeMissionSuccess=function(){const m=Game.activeMission;V11PrevFinalizeSuccess();if(m?.worldLocation){Game.world.completed=(Game.world.completed||0)+1;if(!Game.world.visited.includes(m.worldLocation))Game.world.visited.push(m.worldLocation);Game.world.current='city';const l=V11_WORLD_LOCATIONS.find(x=>x.id===m.worldLocation);addJournal('main',`Global Contract Complete: ${l?.name||m.worldLocation}`,`International deployment completed. Your network and procurement reach expanded.`)}awardManufacturerLootV11(m);checkFactionPromotionsV11();progressStoryV11();saveGame(0,true)};

/* ================= SAVE / LOAD ================= */
const V11PrevSerialize=serializeGame;
serializeGame=function(){ensureV11State();const d=JSON.parse(V11PrevSerialize());d.version=V11_VERSION;d.armory=Game.armory;d.world=Game.world;d.city=Game.city;d.factionPromotions=Game.factionPromotions;d.factionClaims=Game.factionClaims;return JSON.stringify(d)};
let v11AutosavePending=false,v11AutosaveHandle=0;
function flushAutosaveV11(){if(!v11AutosavePending)return false;v11AutosavePending=false;v11AutosaveHandle=0;try{localStorage.setItem(V11_SAVE_KEY+'0',serializeGame());return true}catch(e){toast('Save failed: '+e.message);return false}}
function saveV11Immediate(slot,quiet=false){try{localStorage.setItem(V11_SAVE_KEY+slot,serializeGame());if(!quiet)toast(slot===0?'Autosaved':'Game saved.');return true}catch(e){toast('Save failed: '+e.message);return false}}
saveGame=function(slot,quiet=false){if(slot===0&&quiet){v11AutosavePending=true;if(!v11AutosaveHandle){const cb=()=>flushAutosaveV11();v11AutosaveHandle=typeof requestIdleCallback==='function'?requestIdleCallback(cb,{timeout:700}):setTimeout(cb,0)}return true}return saveV11Immediate(slot,quiet)};
window.addEventListener('pagehide',flushAutosaveV11);
function loadV11Data(data){const extra={armory:data.armory,world:data.world,city:data.city,factionPromotions:data.factionPromotions,factionClaims:data.factionClaims};const ok=ResponsiveSystemsV14.loadData(data);if(ok){Game.armory=extra.armory||{attachments:{}};Game.world=extra.world||{current:'city',trips:0,completed:0,visited:[]};Game.city=extra.city||{visited:[]};Game.factionPromotions=extra.factionPromotions||{};Game.factionClaims=extra.factionClaims||{};ensureV11State();Game.roster.forEach(u=>applySkillsToUnit(u));buildOverworldMap();renderOverworldStatic();drawMinimap?.();injectV11UI();toast(`Loaded v${data.version||10} save.`)}return ok}
loadGame=function(slot){try{const raw=localStorage.getItem(V11_SAVE_KEY+slot)||localStorage.getItem(ResponsiveSystemsV14.saveKey+slot)||localStorage.getItem(PerformanceV14.saveKey+slot)||localStorage.getItem(MercenaryIntelligenceV14.saveKey+slot)||localStorage.getItem(V7_SAVE_KEY+slot)||localStorage.getItem(SAVE_KEY+slot);if(!raw){toast('Empty slot.');return false}return loadV11Data(JSON.parse(raw))}catch(e){toast('Load failed: '+e.message);return false}};
renderLoadMenu=function(){const el=document.getElementById('load-slots');el.innerHTML='';[0,1,2].forEach(slot=>{const raw=localStorage.getItem(V11_SAVE_KEY+slot)||localStorage.getItem(ResponsiveSystemsV14.saveKey+slot)||localStorage.getItem(PerformanceV14.saveKey+slot)||localStorage.getItem(MercenaryIntelligenceV14.saveKey+slot)||localStorage.getItem(V7_SAVE_KEY+slot)||localStorage.getItem(SAVE_KEY+slot),card=document.createElement('button');card.className='btn';card.style.cssText='width:100%;margin-bottom:6px;text-align:left;padding:10px 14px;';const label=slot===0?'AUTOSAVE':`SLOT ${slot}`;if(raw){try{const d=JSON.parse(raw),date=new Date(d.savedAt||Date.now());card.innerHTML=`<b>${label}</b> — ${d.playerName||'Unknown'} (${d.playerClass||'?'}) · Day ${d.day||1} · ¢${d.credits||0} · ⚙${d.salvage||0}<br><span style="opacity:.6;font-size:9px;">v${d.version||4} · ${date.toLocaleString()}</span>`;card.onclick=()=>loadGame(slot)}catch(e){card.innerHTML=`<b>${label}</b> — corrupt`}}else{card.innerHTML=`<b>${label}</b> — empty`;card.disabled=true}el.appendChild(card)})};

const V11PrevStartNew=startNewGame;
startNewGame=function(name,className,background){Game.armory={attachments:{optic_reflex:1,muzzle_suppressor:1,under_grip:1}};Game.world={current:'city',trips:0,completed:0,visited:[]};Game.city={visited:[]};Game.factionPromotions={};Game.factionClaims={};const r=V11PrevStartNew(name,className,background);ensureV11State();generateMissions();buildOverworldMap();saveGame(0,true);return r};

/* ================= DIAGNOSTICS / API ================= */
function runDiagnosticsV11(){
 ensureV11State();const r=[],add=(n,ok,d='')=>r.push({name:n,ok:!!ok,details:d});
 try{
  add('sector atlas',V11_SECTORS.length>=12,`${V11_SECTORS.length} sectors`);
  add('economic strata',new Set(V11_SECTORS.map(s=>s.tier)).size>=5,[...new Set(V11_SECTORS.map(s=>s.tier))].join(', '));
  add('manufacturers',Object.keys(V11_MANUFACTURERS).length>=6);
  add('manufactured weapons',V11_WEAPON_SPECS.length>=18);
  add('attachments',Object.keys(V11_ATTACHMENTS).length>=10);
  add('dynamic weapon SVG',/svg/.test(weaponSvgV11('kestrel_raven',{optic:'optic_marksman',muzzle:'muzzle_suppressor'})));
  add('faction careers',V11_FACTION_RANKS.length>=6);
  add('world network',V11_WORLD_LOCATIONS.length>=7);
  add('world mission generator',!!generateWorldMissionV11(V11_WORLD_LOCATIONS[0]).worldLocation);
  add('persistent modules',!!Game.armory&&!!Game.world&&!!Game.city);
  add('performance module retained',!!window.ChromeRequiem?.modules?.Performance?.stats);
 }catch(e){add('exception',false,e.message)}
 const passed=r.filter(x=>x.ok).length;console.table?.(r);return{version:V11_VERSION,passed,total:r.length,results:r}
}
window.runDiagnosticsV11=runDiagnosticsV11;
window.ChromeRequiem=window.ChromeRequiem||{};window.ChromeRequiem.version=V11_VERSION;window.ChromeRequiem.modules=Object.assign(window.ChromeRequiem.modules||{},{
 CityV11:{sectors:V11_SECTORS,getSector:getSectorV11,render:renderCityAtlasV11},
 ArmoryV11:{manufacturers:V11_MANUFACTURERS,attachments:V11_ATTACHMENTS,weaponSvg:weaponSvgV11,install:installAttachmentV11},
 FactionsV11:{ranks:V11_FACTION_RANKS,check:checkFactionPromotionsV11},
 WorldV11:{locations:V11_WORLD_LOCATIONS,launch:launchWorldContractV11},
 DiagnosticsV11:{run:runDiagnosticsV11}
});

injectV11UI();ensureV11State();checkFactionPromotionsV11();
})()
}
;


const armoryCityCallV14=(name,...args)=>{
 const fn=globalThis[name];
 if(typeof fn!=='function')throw new Error(`ArmoryCityV14 missing legacy implementation: ${name}`);
 return fn(...args);
};
const ArmoryCityV14=Object.freeze({
 version:'11',
 get sectors(){return globalThis.V11_SECTORS},
 get manufacturers(){return globalThis.V11_MANUFACTURERS},
 get weaponSpecs(){return globalThis.V11_WEAPON_SPECS},
 get attachments(){return globalThis.V11_ATTACHMENTS},
 get worldLocations(){return globalThis.V11_WORLD_LOCATIONS},
 get factionRanks(){return globalThis.V11_FACTION_RANKS},
 ensureState:(...args)=>armoryCityCallV14('ensureV11State',...args),
 getSector:(...args)=>armoryCityCallV14('getSectorV11',...args),
 weaponSvg:(...args)=>armoryCityCallV14('weaponSvgV11',...args),
 installAttachment:(...args)=>armoryCityCallV14('installAttachmentV11',...args),
 generateWorldMission:(...args)=>armoryCityCallV14('generateWorldMissionV11',...args),
 launchWorldContract:(...args)=>armoryCityCallV14('launchWorldContractV11',...args),
 diagnostics:(...args)=>armoryCityCallV14('runDiagnosticsV11',...args)
});
globalThis.ChromeRequiemV14Domains ||= {};
globalThis.ChromeRequiemV14Domains.armoryCity=ArmoryCityV14;
