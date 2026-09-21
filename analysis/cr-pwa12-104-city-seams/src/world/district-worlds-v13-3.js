if(typeof window!=='undefined'){
(() => {
'use strict';
const V133_VERSION='13.3';
const V133_DISTRICTS={"ash_blocks":{"name":"Ash Blocks","w":220,"h":170,"grammar":"ash","bg":"#09090a","ground":"#111317","road":"#29282a","secondary":"#222326","alley":"#191c20","accent":"#ff5a35","building":"#241513","roof":"#381d18","open":"#191714","curvature":0.48,"arterialWidth":2.35,"secondaryWidth":1.28,"alleys":11,"buildings":270,"openChance":0.30,"buildingKinds":["tenement","tenement","cluster","ruin","compound","row"],"strategic":[18,76]},"floodline":{"name":"Floodline","w":210,"h":170,"grammar":"flood","bg":"#060a10","ground":"#101922","road":"#23303a","secondary":"#1c2832","alley":"#172129","accent":"#7f63ff","building":"#151328","roof":"#211d38","open":"#0d2028","curvature":0.55,"arterialWidth":2.7,"secondaryWidth":1.6,"alleys":7,"buildings":130,"openChance":0.43,"buildingKinds":["stilt","row","cluster","pump","ruin"],"strategic":[10,92]},"old_market":{"name":"Old Market","w":200,"h":160,"grammar":"market","bg":"#090a0b","ground":"#17191a","road":"#302d2a","secondary":"#292724","alley":"#22201f","accent":"#d7b06c","building":"#25221e","roof":"#393228","open":"#211d18","curvature":0.42,"arterialWidth":2.10,"secondaryWidth":1.08,"alleys":15,"buildings":330,"openChance":0.20,"buildingKinds":["market","row","row","courtyard","arcade","compact"],"strategic":[34,58]},"neon_row":{"name":"Neon Row","w":190,"h":160,"grammar":"neon","bg":"#080711","ground":"#15121b","road":"#252333","secondary":"#211d2b","alley":"#17151f","accent":"#ff38b8","building":"#211125","roof":"#32163b","open":"#1a1322","curvature":0.45,"arterialWidth":3.0,"secondaryWidth":1.6,"alleys":13,"buildings":250,"openChance":0.23,"buildingKinds":["club","row","tower","arcade","compact"],"strategic":[18,52]},"rail_crown":{"name":"Rail Crown","w":220,"h":150,"grammar":"rail","bg":"#090907","ground":"#181714","road":"#302d28","secondary":"#25231f","alley":"#1b1b19","accent":"#ffb23d","building":"#2a1f13","roof":"#3b2b18","open":"#201a14","curvature":0.28,"arterialWidth":3.0,"secondaryWidth":1.8,"alleys":6,"buildings":145,"openChance":0.39,"buildingKinds":["depot","warehouse","row","worker","yardblock"],"strategic":[54,65]},"dock_nine":{"name":"Dock Nine","w":240,"h":170,"grammar":"dock","bg":"#07090a","ground":"#14191d","road":"#2e3336","secondary":"#242a2e","alley":"#1a2023","accent":"#ff9a2f","building":"#251a10","roof":"#3a2816","open":"#151b1d","curvature":0.24,"arterialWidth":3.4,"secondaryWidth":2.0,"alleys":4,"buildings":100,"openChance":0.54,"buildingKinds":["warehouse","warehouse","hangar","customs","shed"],"strategic":[74,76]},"forge_belt":{"name":"Forge Belt","w":240,"h":180,"grammar":"forge","bg":"#080706","ground":"#171513","road":"#302a25","secondary":"#28231f","alley":"#1c1916","accent":"#d76528","building":"#29150c","roof":"#412113","open":"#1d1712","curvature":0.22,"arterialWidth":3.2,"secondaryWidth":1.9,"alleys":5,"buildings":125,"openChance":0.43,"buildingKinds":["factory","factory","hall","tankfarm","worker","shed"],"strategic":[88,84]},"undergrid":{"name":"Undergrid","w":200,"h":180,"grammar":"undergrid","bg":"#03040a","ground":"#0b0d17","road":"#15182a","secondary":"#121625","alley":"#0e111d","accent":"#6c77ff","building":"#0a0b14","roof":"#15172a","open":"#0b0e1b","curvature":0.58,"arterialWidth":2.3,"secondaryWidth":1.4,"alleys":15,"buildings":150,"openChance":0.16,"buildingKinds":["chamber","utility","server","maintenance","vault"],"strategic":[66,54]},"civic_circuit":{"name":"Civic Circuit","w":190,"h":150,"grammar":"civic","bg":"#071019","ground":"#101a24","road":"#283743","secondary":"#21303a","alley":"#19252e","accent":"#45bfff","building":"#122232","roof":"#193247","open":"#152632","curvature":0.24,"arterialWidth":3.2,"secondaryWidth":1.9,"alleys":5,"buildings":150,"openChance":0.34,"buildingKinds":["civic","hospital","office","garage","courtyard"],"strategic":[44,40]},"glass_heights":{"name":"Glass Heights","w":220,"h":170,"grammar":"glass","bg":"#070b12","ground":"#101922","road":"#2a3744","secondary":"#22303b","alley":"#1b2730","accent":"#a78aff","building":"#101a2b","roof":"#18304b","open":"#14252a","curvature":0.62,"arterialWidth":3.15,"secondaryWidth":1.55,"alleys":2,"buildings":95,"openChance":0.64,"buildingKinds":["tower","tower","villa","podium","estate"],"strategic":[42,18]},"helix_financial":{"name":"Helix Financial","w":180,"h":150,"grammar":"helix","bg":"#050b12","ground":"#0d1722","road":"#273745","secondary":"#1d2c39","alley":"#16232d","accent":"#66e6ff","building":"#0c1b2c","roof":"#11324c","open":"#12202a","curvature":0.32,"arterialWidth":3.5,"secondaryWidth":1.9,"alleys":4,"buildings":155,"openChance":0.31,"buildingKinds":["finance","tower","podium","vault","office"],"strategic":[60,24]},"meridian_arcology":{"name":"Meridian Arcology","w":240,"h":190,"grammar":"meridian","bg":"#060b10","ground":"#101820","road":"#2d3740","secondary":"#252e36","alley":"#1b242a","accent":"#d9f7ff","building":"#111b24","roof":"#1b2b35","open":"#182127","curvature":0.18,"arterialWidth":4.2,"secondaryWidth":2.3,"alleys":2,"buildings":90,"openChance":0.49,"buildingKinds":["arcology","arcology","campus","logistics","tower"],"strategic":[75,18]},"crown_spire":{"name":"Crown Spire","w":170,"h":140,"grammar":"crown","bg":"#0b0a07","ground":"#191711","road":"#373329","secondary":"#2e2a22","alley":"#211f1b","accent":"#f2d76b","building":"#262113","roof":"#423817","open":"#211e15","curvature":0.38,"arterialWidth":3.4,"secondaryWidth":1.8,"alleys":2,"buildings":70,"openChance":0.57,"buildingKinds":["embassy","tower","compound","villa","blackoffice"],"strategic":[90,16]}};
const V133_NEIGHBORHOODS={"ash_blocks":["Broken Saint","Red Jack Quarter","Cinder Row","South Ruins","Scrap Mile","Foundry Fringe"],"floodline":["Dry Walk","Pump Ward","Lowwater","Kora's Reach","Drowned Blocks"],"old_market":["Mercenary Arcade","Broker's Walk","Spine Exchange","Lantern Court","Old Station"],"neon_row":["Electric Mile","Chrome Basilica","Velvet District","Mako Strip","Backstage"],"rail_crown":["Crown Exchange","Platform Ward","Freight Spine","Bishop Yard"],"dock_nine":["Pier Six","Bonded Quarter","Customs Ring","Atlas Yard","Container City"],"forge_belt":["Foundry Exchange","Night Line","Furnace Ward","Worker Belt","Petra Works"],"undergrid":["Maintenance Hub","Ghost Line","Relay Deep","Black Node","Old Metro"],"civic_circuit":["Civic Square","Trauma Ward","Records Quarter","Security Row"],"glass_heights":["Skybridge","Executive Gardens","Velvet Lift","North Glass","Ambassador's Row"],"helix_financial":["Exchange","Settlement Row","Helix Plaza","Vault Quarter"],"meridian_arcology":["Contractor Ring","Meridian Core","Logistics Spine","Residential Stack","Internal Armory"],"crown_spire":["Embassy Gallery","Diplomatic Ring","Black Office","Spire Court"]};
const V133_TRANSIT_LINKS=[{"id":"ash_old_gate","type":"border","name":"North Commercial Gate","minutes":18,"from":{"district":"ash_blocks","node":"north_gate","edge":"north"},"to":{"district":"old_market","node":"ash_gate","edge":"south"}},{"id":"ash_flood_gate","type":"border","name":"Lowwater Crossing","minutes":16,"from":{"district":"ash_blocks","node":"flood_gate","edge":"west"},"to":{"district":"floodline","node":"ash_crossing","edge":"east"}},{"id":"old_neon_gate","type":"border","name":"Neon West Walk","minutes":14,"from":{"district":"old_market","node":"neon_gate","edge":"west"},"to":{"district":"neon_row","node":"market_gate","edge":"east"}},{"id":"old_civic_gate","type":"border","name":"Civic South Gate","minutes":15,"from":{"district":"old_market","node":"civic_gate","edge":"north"},"to":{"district":"civic_circuit","node":"market_gate","edge":"south"}},{"id":"old_rail_gate","type":"border","name":"Freight Street Gate","minutes":17,"from":{"district":"old_market","node":"rail_gate","edge":"east"},"to":{"district":"rail_crown","node":"market_gate","edge":"west"}},{"id":"neon_civic_gate","type":"border","name":"Blue Line Street Gate","minutes":13,"from":{"district":"neon_row","node":"civic_gate","edge":"north"},"to":{"district":"civic_circuit","node":"neon_gate","edge":"west"}},{"id":"civic_glass_security","type":"security","name":"Glass Heights Security Gate","minutes":12,"from":{"district":"civic_circuit","node":"glass_checkpoint","edge":"north"},"to":{"district":"glass_heights","node":"civic_checkpoint","edge":"south"},"faction":"meridian"},{"id":"civic_helix_security","type":"security","name":"Helix Access Control","minutes":12,"from":{"district":"civic_circuit","node":"helix_checkpoint","edge":"east"},"to":{"district":"helix_financial","node":"civic_checkpoint","edge":"south"},"faction":"meridian"},{"id":"glass_helix_gate","type":"security","name":"Executive Skyway Gate","minutes":10,"from":{"district":"glass_heights","node":"helix_gate","edge":"east"},"to":{"district":"helix_financial","node":"glass_gate","edge":"west"},"faction":"meridian"},{"id":"helix_meridian_security","type":"security","name":"Meridian Contractor Gate","minutes":14,"from":{"district":"helix_financial","node":"meridian_checkpoint","edge":"east"},"to":{"district":"meridian_arcology","node":"helix_checkpoint","edge":"west"},"faction":"meridian"},{"id":"meridian_crown_security","type":"security","name":"Crown Spire Diplomatic Gate","minutes":11,"from":{"district":"meridian_arcology","node":"crown_checkpoint","edge":"east"},"to":{"district":"crown_spire","node":"meridian_checkpoint","edge":"west"},"faction":"meridian"},{"id":"rail_dock_freight","type":"freight","name":"Dock Freight Line","minutes":16,"cost":90,"from":{"district":"rail_crown","node":"dock_freight","edge":"east"},"to":{"district":"dock_nine","node":"rail_freight","edge":"west"}},{"id":"rail_forge_freight","type":"freight","name":"Foundry Freight Spur","minutes":18,"cost":90,"from":{"district":"rail_crown","node":"forge_freight","edge":"south"},"to":{"district":"forge_belt","node":"rail_freight","edge":"west"}},{"id":"dock_forge_freight","type":"freight","name":"Industrial Cargo Transfer","minutes":15,"cost":80,"from":{"district":"dock_nine","node":"forge_freight","edge":"east"},"to":{"district":"forge_belt","node":"dock_freight","edge":"north"}},{"id":"rail_under_service","type":"border","name":"Infrastructure Service Gate","minutes":15,"from":{"district":"rail_crown","node":"under_gate","edge":"north"},"to":{"district":"undergrid","node":"rail_gate","edge":"west"}},{"id":"old_neon_metro","type":"metro","name":"Old Market ↔ Electric Mile","minutes":9,"cost":45,"from":{"district":"old_market","node":"central_metro"},"to":{"district":"neon_row","node":"electric_metro"}},{"id":"old_civic_metro","type":"metro","name":"Old Market ↔ Civic Square","minutes":8,"cost":40,"from":{"district":"old_market","node":"central_metro"},"to":{"district":"civic_circuit","node":"civic_metro"}},{"id":"old_rail_metro","type":"metro","name":"Old Market ↔ Crown Exchange","minutes":10,"cost":45,"from":{"district":"old_market","node":"central_metro"},"to":{"district":"rail_crown","node":"crown_metro"}},{"id":"civic_glass_metro","type":"metro","name":"Civic Square ↔ Skybridge","minutes":8,"cost":55,"from":{"district":"civic_circuit","node":"civic_metro"},"to":{"district":"glass_heights","node":"skybridge_metro"}},{"id":"civic_helix_metro","type":"metro","name":"Civic Square ↔ Helix Plaza","minutes":7,"cost":55,"from":{"district":"civic_circuit","node":"civic_metro"},"to":{"district":"helix_financial","node":"helix_metro"}},{"id":"under_helix_ghost","type":"hidden","name":"Ghost Utility Route","minutes":12,"from":{"district":"undergrid","node":"ghost_route"},"to":{"district":"helix_financial","node":"utility_basement"},"unlock":"ghost"},{"id":"flood_ash_drain","type":"hidden","name":"Flood Drain Passage","minutes":14,"from":{"district":"floodline","node":"drain_route"},"to":{"district":"ash_blocks","node":"storm_drain"},"unlock":"flood"},{"id":"neon_undergrid_service","type":"hidden","name":"Backstage Service Shaft","minutes":11,"from":{"district":"neon_row","node":"service_shaft"},"to":{"district":"undergrid","node":"neon_service"},"unlock":"chrome"}];
window.V133_DISTRICTS=V133_DISTRICTS;window.V133_NEIGHBORHOODS=V133_NEIGHBORHOODS;window.V133_TRANSIT_LINKS=V133_TRANSIT_LINKS;

const T={PARCEL:0,ART:1,SEC:2,ALLEY:3,PLAZA:4,YARD:5,ROUGH:6,WATER:7,RAIL:8,BRIDGE:9,TUNNEL:10,PARK:11,INDUSTRIAL:12,PED:13,TRANSIT:14,BUILDING:15,WALL:16};
const WALK_COST={[T.ART]:1,[T.SEC]:1.10,[T.ALLEY]:1.28,[T.PLAZA]:1.16,[T.YARD]:1.55,[T.ROUGH]:3.40,[T.RAIL]:1.72,[T.BRIDGE]:1.05,[T.TUNNEL]:1.18,[T.PARK]:1.75,[T.INDUSTRIAL]:1.85,[T.PED]:1.08,[T.TRANSIT]:1.0};
const V133_WORLD_CACHE=new Map();
window.V133_TERRAIN=T;

function hashV133(s){let h=2166136261>>>0;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)}h^=h>>>13;h=Math.imul(h,0x5bd1e995);h^=h>>>15;return h>>>0}
function randV133(...parts){return hashV133(parts.join('|'))/4294967295}
// PWA12.101: static world decoration revisits the same world cells on every camera repaint.
// Cache the 32-bit deterministic hash per world/salt/cell so repeat frames avoid string assembly + FNV-style hashing.
function visualCellRandV101(world,salt,x,y,saltLast=false){
 if(!world||x<0||y<0||x>=world.w||y>=world.h)return randV133(world?.id||'',salt,x,y);
 const caches=world._visualCellRandV101||(world._visualCellRandV101=new Map());let a=caches.get(salt);
 if(!a){a=new Uint32Array(world.w*world.h);caches.set(salt,a)}
 const i=y*world.w+x;let h=a[i];if(h===0){h=hashV133(saltLast?`${world.id}|${x}|${y}|${salt}`:`${world.id}|${salt}|${x}|${y}`);if(h!==0)a[i]=h}
 return h/4294967295
}
window.visualCellRandV101=visualCellRandV101;
function clamp133(v,a,b){return Math.max(a,Math.min(b,v))}
function idx133(w,x,y){return y*w+x}
function dist133(a,b){return Math.hypot(a.x-b.x,a.y-b.y)}
function sectorMeta133(id){return (window.V11_SECTORS||[]).find(s=>s.id===id)||null}
function locDefs133(id){return (window.V13_DISTRICT_LOCATIONS?.[id]||[])}
function locDef133(id){for(const arr of Object.values(window.V13_DISTRICT_LOCATIONS||{})){const q=arr.find(x=>x.id===id);if(q)return q}return null}
function contactDef133(id){return (window.V13_CONTACTS||[]).find(x=>x.id===id)||null}
function shopDef133(id){return (window.V13_SHOPS||[]).find(x=>x.id===id)||null}

function ensureDistrictWorldStateV133(){
 if(!Game.districtWorldsV133||typeof Game.districtWorldsV133!=='object')Game.districtWorldsV133={};
 const s=Game.districtWorldsV133;
 s.activeId=s.activeId&&V133_DISTRICTS[s.activeId]?s.activeId:'old_market';
 s.positions=s.positions||{};
 s.unlockedLinks=s.unlockedLinks||{};
 s.hiddenLinks=s.hiddenLinks||{};
 s.dynamic=s.dynamic||{};
 s.cameraByDistrict=s.cameraByDistrict||{};
 s.discoveredNeighborhoods=s.discoveredNeighborhoods||{};
 refreshHiddenLinksV133();
 return s
}
window.ensureDistrictWorldStateV133=ensureDistrictWorldStateV133;

function refreshHiddenLinksV133(){
 if(!Game.districtWorldsV133)return;
 const s=Game.districtWorldsV133,h=s.hiddenLinks||(s.hiddenLinks={});
 const rel=Game.contactRelations||{};
 if((rel.c2?.trust||0)>=25||(rel.c8?.trust||0)>=25||rel.c22?.known)h.under_helix_ghost=true;
 if(rel.c16?.known||rel.c29?.known||(rel.c16?.trust||0)>=18)h.flood_ash_drain=true;
 if((rel.c4?.trust||0)>=25||rel.c12?.known)h.neon_undergrid_service=true;
}
window.refreshHiddenLinksV133=refreshHiddenLinksV133;

function linksForDistrictV133(id,includeHidden=true){
 ensureDistrictWorldStateV133();
 return V133_TRANSIT_LINKS.filter(l=>{
   const touches=l.from.district===id||l.to.district===id;if(!touches)return false;
   return l.type!=='hidden'||(includeHidden&&Game.districtWorldsV133.hiddenLinks[l.id]);
 })
}
function endpointForV133(link,districtId){return link.from.district===districtId?link.from:link.to}
function otherEndpointV133(link,districtId){return link.from.district===districtId?link.to:link.from}
window.linksForDistrictV133=linksForDistrictV133;

function pointInBounds133(world,x,y){return x>=0&&y>=0&&x<world.w&&y<world.h}
function terrainAt133(world,x,y){return pointInBounds133(world,x,y)?world.terrain[idx133(world.w,x,y)]:T.WALL}
function setTerrain133(world,x,y,v){if(pointInBounds133(world,x,y))world.terrain[idx133(world.w,x,y)]=v}
function walkableTerrain133(v){return WALK_COST[v]!==undefined}
function isWalkableV133(x,y){const w=currentDistrictV133();return !!w&&pointInBounds133(w,x,y)&&walkableTerrain133(terrainAt133(w,x,y))}
window.isWalkable=isWalkableV133;

function placeNeighborhoodsV133(world){
 const names=V133_NEIGHBORHOODS[world.id]||['Central'];
 const centers=[];const margin=Math.max(20,Math.min(world.w,world.h)*.13),cx=world.w/2,cy=world.h/2;
 for(let i=0;i<names.length;i++){
   const angle=(i/names.length)*Math.PI*2+(randV133(world.id,'nangle',i)-.5)*.65;
   const radiusX=world.w*(.23+.11*randV133(world.id,'nrx',i)),radiusY=world.h*(.22+.12*randV133(world.id,'nry',i));
   let x=Math.round(cx+Math.cos(angle)*radiusX+(randV133(world.id,'nx',i)-.5)*world.w*.08);
   let y=Math.round(cy+Math.sin(angle)*radiusY+(randV133(world.id,'ny',i)-.5)*world.h*.08);
   x=clamp133(x,margin,world.w-margin);y=clamp133(y,margin,world.h-margin);
   centers.push({id:`${world.id}_n${i}`,name:names[i],x,y,radius:Math.round(Math.min(world.w,world.h)*(.12+.025*randV133(world.id,'nr',i)))});
 }
 world.neighborhoods=centers;return centers
}

function edgePointV133(world,edge,salt){
 const t=.20+randV133(world.id,salt,'edge')*.60,m=3;
 if(edge==='north')return{x:Math.round(m+t*(world.w-m*2)),y:m};
 if(edge==='south')return{x:Math.round(m+t*(world.w-m*2)),y:world.h-1-m};
 if(edge==='west')return{x:m,y:Math.round(m+t*(world.h-m*2))};
 if(edge==='east')return{x:world.w-1-m,y:Math.round(m+t*(world.h-m*2))};
 return null
}
function nearestNeighborhoodV133(world,p){return [...world.neighborhoods].sort((a,b)=>dist133(a,p)-dist133(b,p))[0]}

function placeTransitAnchorsV133(world){
 const byNode=new Map();
 /* Generate every transit endpoint, including undiscovered hidden routes.
    Visibility/access is handled later so a revealed route never requires
    destructive district regeneration. */
 const physicalLinks=V133_TRANSIT_LINKS.filter(l=>l.from.district===world.id||l.to.district===world.id);
 for(const link of physicalLinks){
   const ep=endpointForV133(link,world.id);if(byNode.has(ep.node))continue;
   let p=edgePointV133(world,ep.edge,ep.node);
   if(!p){
     const n=world.neighborhoods[hashV133(ep.node)%world.neighborhoods.length];
     const a=randV133(world.id,ep.node,'a')*Math.PI*2,r=6+randV133(world.id,ep.node,'r')*12;
     p={x:clamp133(Math.round(n.x+Math.cos(a)*r),6,world.w-7),y:clamp133(Math.round(n.y+Math.sin(a)*r),6,world.h-7)};
   }
   const node={id:ep.node,x:p.x,y:p.y,edge:ep.edge||null,linkIds:[],type:link.type};
   byNode.set(ep.node,node)
 }
 for(const link of physicalLinks){const ep=endpointForV133(link,world.id);byNode.get(ep.node)?.linkIds.push(link.id)}
 world.transit=[...byNode.values()];return world.transit
}

function curvePointsV133(a,b,salt,curvature=.4){
 const dx=b.x-a.x,dy=b.y-a.y,d=Math.max(1,Math.hypot(dx,dy)),nx=-dy/d,ny=dx/d;
 const maxOff=Math.min(d*.26,26)*curvature;
 const off1=(randV133(salt,'curve1')-.5)*2*maxOff;
 const off2=(randV133(salt,'curve2')-.5)*2*maxOff;
 const along1=(.28+(randV133(salt,'along1')-.5)*.10),along2=(.72+(randV133(salt,'along2')-.5)*.10);
 const c1={x:a.x+dx*along1+nx*off1,y:a.y+dy*along1+ny*off1};
 const c2={x:a.x+dx*along2+nx*off2,y:a.y+dy*along2+ny*off2};
 const steps=Math.max(14,Math.ceil(d/2.0)),pts=[];
 for(let i=0;i<=steps;i++){
   const q=i/steps,m=1-q;
   pts.push({
     x:m*m*m*a.x+3*m*m*q*c1.x+3*m*q*q*c2.x+q*q*q*b.x,
     y:m*m*m*a.y+3*m*m*q*c1.y+3*m*q*q*c2.y+q*q*q*b.y
   })
 }
 return pts
}
function paintDiskV133(world,x,y,r,type){
 const rr=Math.ceil(r);for(let dy=-rr;dy<=rr;dy++)for(let dx=-rr;dx<=rr;dx++){if(dx*dx+dy*dy>r*r+.5)continue;const nx=Math.round(x+dx),ny=Math.round(y+dy);if(pointInBounds133(world,nx,ny))setTerrain133(world,nx,ny,type)}
}
function curveBoundsV177(pts){
 let minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity;for(const p of pts){if(p.x<minX)minX=p.x;if(p.y<minY)minY=p.y;if(p.x>maxX)maxX=p.x;if(p.y>maxY)maxY=p.y}return{minX,minY,maxX,maxY}
}
function rasterCurveV133(world,pts,width,type,record=true){
 for(let i=0;i<pts.length-1;i++){
   const a=pts[i],b=pts[i+1],d=Math.max(1,Math.ceil(dist133(a,b)*1.4));
   for(let j=0;j<=d;j++){const t=j/d;paintDiskV133(world,a.x+(b.x-a.x)*t,a.y+(b.y-a.y)*t,Math.max(.55,width*.50),type)}
 }
 if(record){const bounds=curveBoundsV177(pts);world.roadCurves.push({points:pts,width,type,bounds})}
}
function carveEllipseV133(world,cx,cy,rx,ry,type){
 for(let y=Math.floor(cy-ry);y<=Math.ceil(cy+ry);y++)for(let x=Math.floor(cx-rx);x<=Math.ceil(cx+rx);x++){const q=((x-cx)/rx)**2+((y-cy)/ry)**2;if(q<=1)setTerrain133(world,x,y,type)}
}

function farthestPairV133(points){
 let best=null,bd=-1;for(let i=0;i<points.length;i++)for(let j=i+1;j<points.length;j++){const d=dist133(points[i],points[j]);if(d>bd){bd=d;best=[points[i],points[j]]}}return best
}
function neighborhoodEdgePointV133(n,toward,radius=10){
 const dx=toward.x-n.x,dy=toward.y-n.y,d=Math.max(.001,Math.hypot(dx,dy));
 return{x:n.x+dx/d*radius,y:n.y+dy/d*radius}
}
function localRingV133(world,n,ni){
 const g=world.cfg.grammar;
 const nodes=g==='glass'?5:g==='market'||g==='ash'||g==='neon'||g==='undergrid'?7:6;
 const rx=(g==='glass'?13:9)+randV133(world.id,ni,'ringrx')*(g==='glass'?8:5);
 const ry=(g==='glass'?10:7)+randV133(world.id,ni,'ringry')*(g==='glass'?6:4);
 const phase=randV133(world.id,ni,'ringphase')*Math.PI*2,pts=[];
 for(let j=0;j<nodes;j++){
   const a=phase+j/nodes*Math.PI*2+(randV133(world.id,ni,j,'ringj')-.5)*.30;
   pts.push({x:clamp133(n.x+Math.cos(a)*rx,4,world.w-5),y:clamp133(n.y+Math.sin(a)*ry,4,world.h-5)})
 }
 return pts
}
function generateOrganicRoadsV133(world){
 world.roadCurves=[];
 const cfg=world.cfg,g=cfg.grammar,structural=world.transit.length>=2?world.transit:world.neighborhoods;

 // District-scale primary spine. It should CROSS the district, not radiate from a hub.
 const pair=farthestPairV133(structural);
 if(pair)rasterCurveV133(world,curvePointsV133(pair[0],pair[1],`${world.id}:major:0`,cfg.curvature*1.12),cfg.arterialWidth,T.ART);

 // Planned / industrial districts get one additional long axis.
 if(world.neighborhoods.length>=4&&['glass','civic','helix','meridian','dock','forge','rail'].includes(g)){
   const a=world.neighborhoods[1],b=world.neighborhoods[(1+Math.floor(world.neighborhoods.length/2))%world.neighborhoods.length];
   const pa=neighborhoodEdgePointV133(a,b,g==='glass'?14:10),pb=neighborhoodEdgePointV133(b,a,g==='glass'?14:10);
   rasterCurveV133(world,curvePointsV133(pa,pb,`${world.id}:major:1`,cfg.curvature),cfg.arterialWidth*(g==='glass'?.86:.70),T.ART)
 }

 // Local street loops define neighborhoods. This is the main anti-starburst change.
 const rings=world.neighborhoods.map((n,ni)=>localRingV133(world,n,ni));
 rings.forEach((ring,ni)=>{
   const localType=g==='undergrid'?T.TUNNEL:g==='market'&&ni%2===0?T.PED:T.SEC;
   for(let j=0;j<ring.length;j++){
     const a=ring[j],b=ring[(j+1)%ring.length];
     rasterCurveV133(world,curvePointsV133(a,b,`${world.id}:localring:${ni}:${j}`,cfg.curvature*.72),Math.max(.72,cfg.secondaryWidth*.66),localType)
   }
   // Neighborhood center is a plaza/court reached by only one or two short access lanes.
   const n=world.neighborhoods[ni],plazaScale=g==='glass'?1.35:g==='market'?.82:1;
   carveEllipseV133(world,n.x,n.y,(3.3+randV133(world.id,ni,'prx')*2.5)*plazaScale,(2.8+randV133(world.id,ni,'pry')*2.0)*plazaScale,T.PLAZA);
   const accessCount=['ash','market','neon','undergrid'].includes(g)?2:1;
   for(let k=0;k<accessCount;k++){
     const q=ring[(hashV133(`${world.id}:${ni}:access:${k}`))%ring.length];
     rasterCurveV133(world,curvePointsV133(n,q,`${world.id}:court:${ni}:${k}`,cfg.curvature*.40),Math.max(.58,cfg.secondaryWidth*.48),g==='market'?T.PED:T.ALLEY)
   }
 });

 // Connect neighboring districts' internal neighborhoods perimeter-to-perimeter, never center-to-center.
 for(let i=0;i<world.neighborhoods.length;i++){
   const a=world.neighborhoods[i],b=world.neighborhoods[(i+1)%world.neighborhoods.length];
   const pa=neighborhoodEdgePointV133(a,b,g==='glass'?14:10),pb=neighborhoodEdgePointV133(b,a,g==='glass'?14:10);
   rasterCurveV133(world,curvePointsV133(pa,pb,`${world.id}:districtlink:${i}`,cfg.curvature*.95),Math.max(.80,cfg.secondaryWidth*.72),T.SEC)
 }

 // Transit enters through the perimeter of the nearest neighborhood.
 for(const tr of world.transit){
   const n=nearestNeighborhoodV133(world,tr),target=neighborhoodEdgePointV133(n,tr,g==='glass'?14:10);
   rasterCurveV133(world,curvePointsV133(tr,target,`${world.id}:${tr.id}:entry`,cfg.curvature*.92),Math.max(.85,cfg.secondaryWidth*.80),tr.edge?T.SEC:(g==='undergrid'?T.TUNNEL:T.PED))
 }

 // Tangential side lanes branch from local rings rather than firing out from the center.
 rings.forEach((ring,ni)=>{
   const count=g==='glass'?3:g==='crown'||g==='meridian'?4:['ash','market','neon','undergrid'].includes(g)?10:6;
   for(let j=0;j<count;j++){
     const base=ring[hashV133(`${world.id}:${ni}:side:${j}`)%ring.length];
     const n=world.neighborhoods[ni],rad={x:base.x-n.x,y:base.y-n.y},d=Math.max(.01,Math.hypot(rad.x,rad.y));
     const tx=-rad.y/d,ty=rad.x/d,side=randV133(world.id,ni,j,'sidesign')>.5?1:-1;
     const len=(g==='glass'?9:6)+randV133(world.id,ni,j,'sidelen')*(g==='glass'?15:13);
     const bend=(randV133(world.id,ni,j,'sidebend')-.5)*.55;
     const dirx=tx*side*Math.cos(bend)-rad.x/d*Math.sin(bend),diry=ty*side*Math.cos(bend)-rad.y/d*Math.sin(bend);
     const target={x:clamp133(base.x+dirx*len,3,world.w-4),y:clamp133(base.y+diry*len,3,world.h-4)};
     const typ=g==='market'&&j%3===0?T.PED:g==='undergrid'?T.TUNNEL:T.ALLEY;
     rasterCurveV133(world,curvePointsV133(base,target,`${world.id}:sidelane:${ni}:${j}`,cfg.curvature*.58),g==='glass'?.62:.66,typ)
   }
 });

 for(const tr of world.transit)carveEllipseV133(world,tr.x,tr.y,2.5,2.5,T.TRANSIT);
 return world
}
window.generateOrganicRoadsV133=generateOrganicRoadsV133;

function applyDistrictTerrainV133(world){
 const id=world.id;
 if(id==='floodline'){
   for(let k=0;k<3;k++){
     const y0=28+k*48+Math.round((randV133(id,k,'wy')-.5)*14);
     const pts=[];for(let x=-5;x<=world.w+5;x+=3)pts.push({x,y:y0+Math.sin(x*.045+k*1.7)*10+(randV133(id,k,x,'wj')-.5)*3});
     for(const p of pts){for(let r=-4;r<=4;r++)for(let q=-2;q<=2;q++){const x=Math.round(p.x+r),y=Math.round(p.y+q),old=terrainAt133(world,x,y);if(!pointInBounds133(world,x,y))continue;if(walkableTerrain133(old))setTerrain133(world,x,y,T.BRIDGE);else setTerrain133(world,x,y,T.WATER)}}
     world.waterCurves.push({points:pts,width:7})
   }
 }
 if(id==='dock_nine'){
   const shore=Math.round(world.h*.79);for(let y=shore;y<world.h;y++)for(let x=0;x<world.w;x++){const old=terrainAt133(world,x,y);setTerrain133(world,x,y,walkableTerrain133(old)?T.BRIDGE:T.WATER)}
   for(let x=20;x<world.w-20;x+=32){for(let y=shore-8;y<world.h-6;y++)for(let dx=-2;dx<=2;dx++)setTerrain133(world,x+dx,y,T.YARD)}
 }
 if(['rail_crown','forge_belt','dock_nine'].includes(id)){
   const count=id==='rail_crown'?3:2;for(let k=0;k<count;k++){const y=Math.round(world.h*(.24+k*.22));const a={x:0,y:y+(randV133(id,k,'rail')-.5)*10},b={x:world.w-1,y:y+(randV133(id,k,'rail2')-.5)*10};const pts=curvePointsV133(a,b,`${id}:rail:${k}`,.15);rasterCurveV133(world,pts,1.2,T.RAIL);world.railCurves.push({points:pts,width:1.2})}
 }
 if(id==='glass_heights'){
   world.neighborhoods.forEach((n,i)=>{if(i%2===0)carveEllipseV133(world,n.x+8,n.y-7,9+randV133(id,i,'park')*8,7+randV133(id,i,'park2')*7,T.PARK)})
 }
 if(id==='civic_circuit'){
   world.neighborhoods.forEach((n,i)=>{if(i<2)carveEllipseV133(world,n.x,n.y,9,7,T.PLAZA)})
 }
 if(id==='undergrid'){
   for(let i=0;i<world.terrain.length;i++){if(world.terrain[i]===T.ART||world.terrain[i]===T.SEC)world.terrain[i]=T.TUNNEL}
 }
 if(id==='meridian_arcology'){
   world.neighborhoods.forEach((n,i)=>{if(i%2===0)carveEllipseV133(world,n.x,n.y,11,8,T.PLAZA)})
 }
}

function footprintPartsV133(kind,w,h,seed){
 const parts=[];
 if(['warehouse','factory','hall','hangar','arcology','finance','civic','hospital','embassy','blackoffice','vault'].includes(kind)){
   parts.push({x:0,y:0,w,h});
 }else if(['courtyard','compound','estate','campus'].includes(kind)){
   const t=Math.max(2,Math.round(Math.min(w,h)*.25));
   parts.push({x:0,y:0,w,h:t},{x:0,y:h-t,w,h:t},{x:0,y:t,w:t,h:h-2*t},{x:w-t,y:t,w:t,h:h-2*t})
 }else if(['tenement','cluster','market','arcade','worker'].includes(kind)){
   const split=Math.max(2,Math.floor(w*(.48+((seed%13)-6)*.015)));
   parts.push({x:0,y:0,w:split,h},{x:split-1,y:Math.max(1,Math.floor(h*.18)),w:w-split+1,h:Math.max(2,Math.floor(h*.72))})
 }else if(kind==='ruin'){
   parts.push({x:0,y:0,w:Math.max(2,Math.floor(w*.62)),h},{x:Math.floor(w*.55),y:0,w:Math.max(2,Math.floor(w*.45)),h:Math.max(2,Math.floor(h*.45))})
 }else{
   parts.push({x:0,y:0,w,h})
 }
 return parts
}
function canPlaceBuildingV133(world,x,y,w,h){
 if(x<2||y<2||x+w>=world.w-2||y+h>=world.h-2)return false;
 let good=0,total=0;
 for(let yy=y;yy<y+h;yy++)for(let xx=x;xx<x+w;xx++){total++;if(terrainAt133(world,xx,yy)===T.PARCEL)good++}
 return good/total>.88
}
function placeBuildingCellsV133(world,b){
 for(const p of b.parts)for(let yy=b.y+p.y;yy<b.y+p.y+p.h;yy++)for(let xx=b.x+p.x;xx<b.x+p.x+p.w;xx++)setTerrain133(world,xx,yy,T.BUILDING)
}
function distanceToWalkableV133(world,x,y,max=7){
 for(let r=1;r<=max;r++)for(let dy=-r;dy<=r;dy++)for(let dx=-r;dx<=r;dx++){if(Math.abs(dx)!==r&&Math.abs(dy)!==r)continue;const nx=x+dx,ny=y+dy;if(pointInBounds133(world,nx,ny)&&walkableTerrain133(terrainAt133(world,nx,ny)))return r}return max+1
}
function buildingDimsV133(world,kind,key){
 const industrial=['warehouse','factory','hall','hangar','arcology','campus','customs','tankfarm'].includes(kind);
 let minW=industrial?8:3,maxW=industrial?20:kind==='tower'?8:12,minH=industrial?7:3,maxH=industrial?17:kind==='tower'?8:12;
 const g=world.cfg.grammar;
 if(g==='market'){minW=3;maxW=7;minH=3;maxH=8}
 else if(g==='ash'){minW=3;maxW=9;minH=3;maxH=10}
 else if(g==='neon'){minW=3;maxW=7;minH=4;maxH=10}
 else if(g==='glass'){minW=5;maxW=10;minH=5;maxH=10}
 let w=minW+Math.floor(randV133(world.id,key,'bw')*(maxW-minW+1)),h=minH+Math.floor(randV133(world.id,key,'bh')*(maxH-minH+1));
 if(kind==='row'){w=3+Math.floor(randV133(world.id,key,'rw')*4);h=5+Math.floor(randV133(world.id,key,'rh')*6)}
 if(kind==='market'||kind==='arcade'||kind==='compact'){w=3+Math.floor(randV133(world.id,key,'mw')*4);h=3+Math.floor(randV133(world.id,key,'mh')*5)}
 if(kind==='tower'){w=5+Math.floor(randV133(world.id,key,'tw')*4);h=5+Math.floor(randV133(world.id,key,'th')*4)}
 return{w,h}
}
function placeBuildingAtV133(world,kind,cx,cy,visualAngle,key){
 const {w,h}=buildingDimsV133(world,kind,key),x=Math.round(cx-w/2),y=Math.round(cy-h/2);
 if(!canPlaceBuildingV133(world,x,y,w,h))return false;
 const parts=footprintPartsV133(kind,w,h,hashV133(`${world.id}:${key}:shape`)),b={id:`b_${world.id}_${world.buildings.length}`,kind,x,y,w,h,parts,angle:0,seed:hashV133(`${world.id}:${key}:visual`),neighborhood:neighborhoodAtPointV133(world,cx,cy)?.id||null};
 placeBuildingCellsV133(world,b);world.buildings.push(b);return true
}
function streetBuildingSettingsV133(world){
 const g=world.cfg.grammar;
 if(g==='market')return{stride:3,setback:1.6,roads:[T.ART,T.SEC,T.PED],chance:.92};
 if(g==='ash')return{stride:4,setback:2.2,roads:[T.ART,T.SEC,T.ALLEY],chance:.78};
 if(g==='neon')return{stride:3,setback:1.8,roads:[T.ART,T.SEC,T.PED],chance:.88};
 if(g==='glass')return{stride:8,setback:6.5,roads:[T.ART,T.SEC],chance:.62};
 if(['dock','forge','rail'].includes(g))return{stride:7,setback:5.0,roads:[T.ART,T.SEC],chance:.72};
 if(g==='undergrid')return{stride:5,setback:2.6,roads:[T.TUNNEL,T.SEC,T.ALLEY],chance:.72};
 if(['meridian','helix','civic','crown'].includes(g))return{stride:6,setback:4.0,roads:[T.ART,T.SEC],chance:.72};
 return{stride:5,setback:3,roads:[T.ART,T.SEC],chance:.70}
}

function signatureSpecV133(grammar){
 return {
  ash:{kinds:['compound','tenement'],count:1,w:[8,13],h:[7,12]},
  flood:{kinds:['pump','stilt'],count:1,w:[8,13],h:[7,11]},
  market:{kinds:['market','arcade'],count:1,w:[7,11],h:[6,10]},
  neon:{kinds:['club','tower'],count:1,w:[7,10],h:[7,12]},
  rail:{kinds:['depot','warehouse'],count:1,w:[11,18],h:[7,12]},
  dock:{kinds:['warehouse','hangar'],count:3,w:[12,22],h:[8,15]},
  forge:{kinds:['factory','hall'],count:3,w:[12,22],h:[9,16]},
  undergrid:{kinds:['chamber','server'],count:3,w:[9,15],h:[8,13]},
  civic:{kinds:['civic','hospital'],count:1,w:[10,16],h:[8,13]},
  glass:{kinds:['tower','estate'],count:3,w:[7,12],h:[7,12]},
  helix:{kinds:['finance','vault'],count:1,w:[10,16],h:[8,13]},
  meridian:{kinds:['arcology','campus'],count:3,w:[14,24],h:[11,18]},
  crown:{kinds:['embassy','compound'],count:1,w:[10,16],h:[8,13]}
 }[grammar]||{kinds:['compact'],count:1,w:[7,11],h:[6,10]}
}
function placeSignatureBuildingV133(world,n,ni,slot){
 const spec=signatureSpecV133(world.cfg.grammar),kind=spec.kinds[slot%spec.kinds.length];
 for(let a=0;a<28;a++){
   const ang=(slot/spec.count)*Math.PI*2+randV133(world.id,ni,slot,a,'siga')*Math.PI*2;
   const close=['glass','undergrid','dock','forge','meridian'].includes(world.cfg.grammar);
   const rad=(close?7:10)+slot*(close?3.5:5)+randV133(world.id,ni,slot,a,'sigr')*(close?12:18);
   const w=spec.w[0]+Math.floor(randV133(world.id,ni,slot,a,'sigw')*(spec.w[1]-spec.w[0]+1));
   const h=spec.h[0]+Math.floor(randV133(world.id,ni,slot,a,'sigh')*(spec.h[1]-spec.h[0]+1));
   const cx=n.x+Math.cos(ang)*rad,cy=n.y+Math.sin(ang)*rad,x=Math.round(cx-w/2),y=Math.round(cy-h/2);
   if(!canPlaceBuildingV133(world,x,y,w,h))continue;
   const parts=footprintPartsV133(kind,w,h,hashV133(`${world.id}:signature:${ni}:${slot}:${a}`));
   const b={id:`sig_${world.id}_${ni}_${slot}`,kind,x,y,w,h,parts,
     angle:0,
     seed:hashV133(`${world.id}:signature:${ni}:${slot}`),neighborhood:n.id,signature:true};
   placeBuildingCellsV133(world,b);world.buildings.push(b);return true
 }
 return false
}
function placeSignatureStructuresV133(world){
 const spec=signatureSpecV133(world.cfg.grammar);
 world.neighborhoods.forEach((n,ni)=>{for(let s=0;s<spec.count;s++)placeSignatureBuildingV133(world,n,ni,s)});
}
window.placeSignatureStructuresV133=placeSignatureStructuresV133;

function placeBuildingsV133(world){
 const cfg=world.cfg,kinds=cfg.buildingKinds,target=cfg.buildings;world.buildings=[];
 placeSignatureStructuresV133(world);
 const settings=streetBuildingSettingsV133(world);
 // Phase A: street-facing fabric. Buildings are positioned from road tangents,
 // so urban form follows the street network instead of floating independently.
 world.roadCurves.forEach((rc,ri)=>{
   if(!settings.roads.includes(rc.type)||world.buildings.length>=target*.82)return;
   const pts=rc.points;
   for(let i=1;i<pts.length-1&&world.buildings.length<target*.82;i+=settings.stride){
     const p=pts[i],prev=pts[i-1],next=pts[i+1],dx=next.x-prev.x,dy=next.y-prev.y,d=Math.max(.001,Math.hypot(dx,dy)),nx=-dy/d,ny=dx/d;
     for(const side of [-1,1]){
       const key=`street:${ri}:${i}:${side}`;if(randV133(world.id,key,'chance')>settings.chance)continue;
       const kind=kinds[hashV133(`${world.id}:${key}:kind`)%kinds.length],dims=buildingDimsV133(world,kind,key);
       const roadHalf=Math.max(.7,rc.width*.55),offset=roadHalf+settings.setback+Math.max(dims.w,dims.h)*.48;
       const jitter=(randV133(world.id,key,'jitter')-.5)*3.2,cx=p.x+nx*offset*side+(dx/d)*jitter,cy=p.y+ny*offset*side+(dy/d)*jitter;
       let ang=Math.atan2(dy,dx);while(ang>Math.PI/4)ang-=Math.PI/2;while(ang<-Math.PI/4)ang+=Math.PI/2;ang*=world.cfg.grammar==='glass'?.62:.42;
       placeBuildingAtV133(world,kind,cx,cy,ang,key)
     }
   }
 });
 // Phase B: irregular infill keeps neighborhoods dense without restoring a grid.
 const attempts=target*14;
 for(let a=0;a<attempts&&world.buildings.length<target;a++){
   const kind=kinds[hashV133(`${world.id}:infill:kind:${a}`)%kinds.length],{w,h}=buildingDimsV133(world,kind,`infill:${a}`),x=2+Math.floor(randV133(world.id,a,'bx')*(world.w-w-5)),y=2+Math.floor(randV133(world.id,a,'by')*(world.h-h-5));
   if(!canPlaceBuildingV133(world,x,y,w,h))continue;const cx=x+w/2,cy=y+h/2;if(distanceToWalkableV133(world,Math.round(cx),Math.round(cy),11)>11)continue;
   placeBuildingAtV133(world,kind,cx,cy,(randV133(world.id,a,'rot')-.5)*(world.cfg.grammar==='glass'?.18:.10),`infill:${a}`)
 }
 // Preserve urban mass. Left-over parcels are BLOCKED city fabric by default.
 // Only district-appropriate voids become walkable space. This makes streets matter.
 const openScale={
   ash:.34,market:.22,neon:.26,flood:.38,rail:.55,dock:.62,forge:.52,
   undergrid:.24,civic:.42,glass:1.00,helix:.34,meridian:.43,crown:.55
 }[world.cfg.grammar]??.35;
 for(let y=0;y<world.h;y++)for(let x=0;x<world.w;x++){
   if(terrainAt133(world,x,y)!==T.PARCEL)continue;
   const r=randV133(world.id,x,y,'left'),open=r<(cfg.openChance*openScale);
   if(!open)continue; // remain T.PARCEL: blocked anonymous urban fabric
   let v=T.ROUGH;
   if(world.cfg.grammar==='glass')v=T.PARK;
   else if(['dock','forge','rail'].includes(world.cfg.grammar))v=(r<cfg.openChance*openScale*.66?T.YARD:T.INDUSTRIAL);
   else if(world.cfg.grammar==='market')v=(r<cfg.openChance*openScale*.55?T.PED:T.ROUGH);
   else if(world.cfg.grammar==='civic'||world.cfg.grammar==='meridian'||world.cfg.grammar==='crown')v=T.PLAZA;
   else if(world.cfg.grammar==='undergrid')v=T.ROUGH;
   setTerrain133(world,x,y,v)
 }
 return world.buildings
}
window.placeBuildingsV133=placeBuildingsV133;

function neighborhoodAtPointV133(world,x,y){let best=null,bd=1e9;for(const n of world.neighborhoods){const d=Math.hypot(n.x-x,n.y-y);if(d<bd){bd=d;best=n}}return best}
function neighborhoodAtV133(x,y,world=currentDistrictV133()){return world?neighborhoodAtPointV133(world,x,y):null}
window.neighborhoodAtV133=neighborhoodAtV133;

function nearestWalkableCellV133(world,x,y,used=new Set(),preferEntrance=false){
 for(let r=0;r<24;r++)for(let dy=-r;dy<=r;dy++)for(let dx=-r;dx<=r;dx++){
   if(r&&Math.abs(dx)!==r&&Math.abs(dy)!==r)continue;const nx=Math.round(x+dx),ny=Math.round(y+dy),k=`${nx},${ny}`;
   if(!pointInBounds133(world,nx,ny)||used.has(k)||!walkableTerrain133(terrainAt133(world,nx,ny)))continue;
   if(preferEntrance){
     let adjacent=false;for(const[ax,ay]of[[1,0],[-1,0],[0,1],[0,-1]])if(terrainAt133(world,nx+ax,ny+ay)===T.BUILDING){adjacent=true;break}
     if(!adjacent&&r<12)continue
   }
   return{x:nx,y:ny}
 }
 return{x:clamp133(Math.round(x),1,world.w-2),y:clamp133(Math.round(y),1,world.h-2)}
}
function assignLocationsV133(world){
 const used=new Set(world.transit.map(t=>`${t.x},${t.y}`)),defs=locDefs133(world.id);world.locations={};
 defs.forEach((l,i)=>{
   const n=world.neighborhoods[hashV133(`${world.id}:${l.id}:hood`)%world.neighborhoods.length],a=randV133(world.id,l.id,'la')*Math.PI*2,r=4+randV133(world.id,l.id,'lr')*Math.max(9,n.radius*.72);
   const target={x:n.x+Math.cos(a)*r,y:n.y+Math.sin(a)*r},p=nearestWalkableCellV133(world,target.x,target.y,used,l.type==='contact'||l.type==='shop'||l.type==='clinic');
   used.add(`${p.x},${p.y}`);world.locations[l.id]={...p,id:l.id,neighborhood:n.id,sectorId:world.id};
 });
 if(world.id==='old_market'){
   const n=world.neighborhoods[0],p=nearestWalkableCellV133(world,n.x+4,n.y+3,used,true);world.locations.v133_safehouse={...p,id:'v133_safehouse',neighborhood:n.id,sectorId:world.id};used.add(`${p.x},${p.y}`)
 }
 return world.locations
}
window.assignLocationsV133=assignLocationsV133;

function locationKnownV133(id){
 if(id==='v133_safehouse')return true;const l=locDef133(id);if(!l)return false;
 return !!Game.cityLife?.discovered?.[id]||(l.contact&&Game.contactRelations?.[l.contact]?.known)
}
function locationDisplayV133(id){
 if(id==='v133_safehouse')return{id,name:'SAFEHOUSE',type:'safehouse',desc:'Crew headquarters and recovery base.'};
 return locDef133(id)
}

function ensureTransitWalkabilityV133(world){
 for(const tr of world.transit){paintDiskV133(world,tr.x,tr.y,3,T.TRANSIT);const n=nearestNeighborhoodV133(world,tr);rasterCurveV133(world,curvePointsV133(tr,n,`${world.id}:${tr.id}:repair`,world.cfg.curvature*.55),Math.max(1.4,world.cfg.secondaryWidth),tr.edge?T.SEC:T.PED,false)}
}
function rebuildOvMapV133(world){
 Game.ovMap=Array.from({length:world.h},(_,y)=>Array.from({length:world.w},(_,x)=>walkableTerrain133(terrainAt133(world,x,y))?0:1))
}
function buildDistrictMinimapV133(world){
 const c=document.createElement('canvas');c.width=240;c.height=Math.round(240*world.h/world.w);const x=c.getContext('2d'),sx=c.width/world.w,sy=c.height/world.h;
 x.fillStyle=world.cfg.bg;x.fillRect(0,0,c.width,c.height);
 for(let y=0;y<world.h;y+=2)for(let xx=0;xx<world.w;xx+=2){const v=terrainAt133(world,xx,y);let col=walkableTerrain133(v)?world.cfg.ground:'#06090d';if(v===T.WATER)col='#07182a';else if(v===T.ART)col='#49545c';else if(v===T.SEC)col='#35414a';else if(v===T.PLAZA)col='#26343b';else if(v===T.PARK)col='#163024';else if(v===T.RAIL)col='#4c3923';else if(v===T.BUILDING)col=world.cfg.building;x.fillStyle=col;x.fillRect(xx*sx,y*sy,Math.max(1,2*sx),Math.max(1,2*sy))}
 world.minimapCanvas=c
}

function generateDistrictV133(id){
 if(V133_WORLD_CACHE.has(id))return V133_WORLD_CACHE.get(id);
 const cfg=V133_DISTRICTS[id];if(!cfg)throw new Error(`Unknown district ${id}`);
 const world={id,cfg,w:cfg.w,h:cfg.h,terrain:new Uint8Array(cfg.w*cfg.h),roadCurves:[],waterCurves:[],railCurves:[],buildings:[],neighborhoods:[],transit:[],locations:{},signature:null};
 world.terrain.fill(T.PARCEL);placeNeighborhoodsV133(world);placeTransitAnchorsV133(world);generateOrganicRoadsV133(world);applyDistrictTerrainV133(world);placeBuildingsV133(world);ensureTransitWalkabilityV133(world);assignLocationsV133(world);repairConnectivityV133(world);buildDistrictMinimapV133(world);world.signature=districtSignatureV133(world);V133_WORLD_CACHE.set(id,world);return world
}
window.generateDistrictV133=generateDistrictV133;

class MinHeapV133{
 constructor(){this.a=[]}
 get size(){return this.a.length}
 push(n){const a=this.a;a.push(n);let i=a.length-1;while(i>0){const p=(i-1)>>1;if(a[p].score<=n.score)break;a[i]=a[p];i=p}a[i]=n}
 pop(){const a=this.a;if(!a.length)return null;const root=a[0],last=a.pop();if(a.length){let i=0;a[0]=last;while(true){let l=i*2+1,r=l+1,s=i;if(l<a.length&&a[l].score<a[s].score)s=l;if(r<a.length&&a[r].score<a[s].score)s=r;if(s===i)break;[a[i],a[s]]=[a[s],a[i]];i=s}}return root}
}
window.MinHeapV133=MinHeapV133;

function findDistrictPathV133(start,goal,world=currentDistrictV133()){
 if(!world||!start||!goal||!pointInBounds133(world,goal.x,goal.y)||!walkableTerrain133(terrainAt133(world,goal.x,goal.y)))return null;
 if(start.x===goal.x&&start.y===goal.y)return[{x:start.x,y:start.y}];
 const W=world.w,H=world.h,N=W*H,INF=1e20,g=new Float64Array(N),parent=new Int32Array(N),closed=new Uint8Array(N);g.fill(INF);parent.fill(-1);
 const heap=new MinHeapV133(),si=idx133(W,start.x,start.y),gi=idx133(W,goal.x,goal.y),heur=(x,y)=>Math.hypot(goal.x-x,goal.y-y);
 g[si]=0;heap.push({idx:si,score:heur(start.x,start.y)});
 const dirs=[[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]];
 let guard=0;
 while(heap.size&&guard++<N*3){
   const q=heap.pop(),cur=q.idx;if(closed[cur])continue;closed[cur]=1;if(cur===gi)break;
   const cx=cur%W,cy=(cur/W)|0;
   for(const[dx,dy]of dirs){const nx=cx+dx,ny=cy+dy;if(nx<0||ny<0||nx>=W||ny>=H)continue;const tv=terrainAt133(world,nx,ny);if(!walkableTerrain133(tv))continue;if(dx&&dy&&(!walkableTerrain133(terrainAt133(world,cx+dx,cy))||!walkableTerrain133(terrainAt133(world,cx,cy+dy))))continue;
     const ni=idx133(W,nx,ny);if(closed[ni])continue;const diag=dx&&dy?1.414:1,ng=g[cur]+WALK_COST[tv]*diag;if(ng>=g[ni])continue;g[ni]=ng;parent[ni]=cur;heap.push({idx:ni,score:ng+heur(nx,ny)})}
 }
 if(parent[gi]===-1)return null;const path=[];let cur=gi;while(cur!==-1){path.push({x:cur%W,y:(cur/W)|0});if(cur===si)break;cur=parent[cur]}return path.reverse()
}
window.findDistrictPathV133=findDistrictPathV133;window.findPath=findDistrictPathV133;

function requiredNodesV133(world){
 const arr=world.transit.map(x=>({id:`transit:${x.id}`,x:x.x,y:x.y}));
 for(const [id,p]of Object.entries(world.locations))arr.push({id:`loc:${id}`,x:p.x,y:p.y});return arr
}
function carveGuaranteedLaneV133(world,a,b,salt){
 const pts=curvePointsV133(a,b,salt,Math.max(.35,world.cfg.curvature*.72));
 // Supercover sampling: radius >1 cell prevents diagonal pinholes.
 for(let i=0;i<pts.length-1;i++){
   const p=pts[i],q=pts[i+1],d=Math.max(2,Math.ceil(dist133(p,q)*3));
   for(let j=0;j<=d;j++){const u=j/d;paintDiskV133(world,p.x+(q.x-p.x)*u,p.y+(q.y-p.y)*u,1.18,T.ALLEY)}
 }
 world.roadCurves.push({points:pts,width:.68,type:T.ALLEY,repair:true,bounds:curveBoundsV177(pts)})
}
function repairConnectivityV133(world){
 const req=requiredNodesV133(world);if(!req.length)return;
 const root=req[0];
 // Multiple passes are intentional because opening one lane can join several components.
 for(let pass=0;pass<3;pass++){
   let changed=false;
   for(const n of req.slice(1)){
     if(findDistrictPathV133(root,n,world))continue;
     carveGuaranteedLaneV133(world,root,n,`${world.id}:repair:${pass}:${n.id}`);changed=true
   }
   if(!changed)break
 }
 // Last-resort deterministic direct supercover. A required node may never ship disconnected.
 for(const n of req.slice(1)){
   if(findDistrictPathV133(root,n,world))continue;
   const steps=Math.ceil(dist133(root,n)*3);
   for(let i=0;i<=steps;i++){const q=i/Math.max(1,steps);paintDiskV133(world,root.x+(n.x-root.x)*q,root.y+(n.y-root.y)*q,1.45,T.ALLEY)}
 }
}
function organicScoreV133(world){
 let turns=0,diag=0;for(const r of world.roadCurves)for(let i=2;i<r.points.length;i++){const a=r.points[i-2],b=r.points[i-1],c=r.points[i],v1={x:b.x-a.x,y:b.y-a.y},v2={x:c.x-b.x,y:c.y-b.y};const cross=Math.abs(v1.x*v2.y-v1.y*v2.x);if(cross>.08)turns++;if(Math.abs(v2.x)>.2&&Math.abs(v2.y)>.2)diag++}return{turns,diag}
}
function validateWorldV133(world){
 const req=requiredNodesV133(world),root=req[0],unreachable=req.filter(n=>!findDistrictPathV133(root,n,world)).map(n=>n.id),org=organicScoreV133(world);
 return{id:world.id,w:world.w,h:world.h,buildings:world.buildings.length,locations:Object.keys(world.locations).length,transit:world.transit.length,unreachable,organic:org,signature:world.signature}
}
window.validateWorldV133=validateWorldV133;
function districtSignatureV133(world){
 let h=2166136261>>>0;for(let i=0;i<world.terrain.length;i+=Math.max(1,Math.floor(world.terrain.length/4000))){h^=world.terrain[i]+i;h=Math.imul(h,16777619)}
 for(const b of world.buildings.slice(0,80)){h^=hashV133(`${b.kind}:${b.x}:${b.y}:${b.w}:${b.h}`);h=Math.imul(h,16777619)}return(h>>>0).toString(16)
}
window.districtSignatureV133=districtSignatureV133;

function currentDistrictV133(){const s=ensureDistrictWorldStateV133();return V133_WORLD_CACHE.get(s.activeId)||generateDistrictV133(s.activeId)}
window.currentDistrictV133=currentDistrictV133;

function nearestWalkableFromV133(world,p){return nearestWalkableCellV133(world,p.x,p.y,new Set(),false)}
function entryPointV133(world,entryId){
 if(entryId){const tr=world.transit.find(x=>x.id===entryId);if(tr)return{x:tr.x,y:tr.y}}
 const s=ensureDistrictWorldStateV133(),saved=s.positions[world.id];if(saved&&isFinite(saved.x)&&isFinite(saved.y)&&walkableTerrain133(terrainAt133(world,saved.x,saved.y)))return{x:saved.x,y:saved.y};
 const n=world.neighborhoods[0];return nearestWalkableCellV133(world,n.x,n.y)
}
function activateDistrictV133(id,entryId=null){
 if(!V133_DISTRICTS[id])return false;ensureV13State();const state=ensureDistrictWorldStateV133(),old=state.activeId;
 if(old&&old!==id&&Game.ovPlayer&&V133_DISTRICTS[old])state.positions[old]={x:Game.ovPlayer.x,y:Game.ovPlayer.y};
 if(old&&old!==id&&Game.ovCamera&&V133_DISTRICTS[old])state.cameraByDistrict[old]={x:Game.ovCamera.x,y:Game.ovCamera.y,tile:Game.ovTile,follow:Game.ovCamera.follow};
 const world=generateDistrictV133(id);state.activeId=id;Game.cityLife.currentDistrict=id;const p=entryId?entryPointV133(world,entryId):entryPointV133(world,null);Game.ovPlayer={x:p.x,y:p.y};state.positions[id]={x:p.x,y:p.y};rebuildOvMapV133(world);
 window.OV_W_V133=world.w;window.OV_H_V133=world.h;Game.pendingPath=null;Game._v133TravelTarget=null;Game.ovCamera=null;Game.ovStaticDirty=true;updateOverworldHUDV133();return true
}
window.activateDistrictV133=activateDistrictV133;

function megaSectorFromRawV133(data){
 const p=data?.ovPlayer;if(!p)return'old_market';const bounds=window.V132_SECTOR_BOUNDS||{};
 for(const[id,b]of Object.entries(bounds))if(p.x>=b[0]&&p.x<=b[2]&&p.y>=b[1]&&p.y<=b[3])return id;
 return'old_market'
}
function migrateMegaSaveV133(data){
 ensureDistrictWorldStateV133();if(data?.districtWorldsV133){Game.districtWorldsV133=JSON.parse(JSON.stringify(data.districtWorldsV133));ensureDistrictWorldStateV133();return Game.districtWorldsV133.activeId}
 const sid=megaSectorFromRawV133(data),world=generateDistrictV133(sid),p=data?.ovPlayer||{x:0,y:0},b=(window.V132_SECTOR_BOUNDS||{})[sid];
 let target=world.neighborhoods[0];
 if(b){const rx=clamp133((p.x-b[0])/Math.max(1,b[2]-b[0]),0,1),ry=clamp133((p.y-b[1])/Math.max(1,b[3]-b[1]),0,1);target={x:rx*(world.w-1),y:ry*(world.h-1)}}
 const q=nearestWalkableFromV133(world,target);Game.districtWorldsV133.activeId=sid;Game.districtWorldsV133.positions[sid]=q;return sid
}
window.migrateMegaSaveV133=migrateMegaSaveV133;

/* ---------- Rendering ---------- */
function visibleBoundsV133(world){
 const r=frameRectV133()||{width:Game.ovCanvas?.clientWidth||0,height:Game.ovCanvas?.clientHeight||0},t=Game.ovTile,c=Game.ovCamera;
 return{x0:Math.max(0,Math.floor(c.x)-3),y0:Math.max(0,Math.floor(c.y)-3),x1:Math.min(world.w,Math.ceil(c.x+r.width/t)+3),y1:Math.min(world.h,Math.ceil(c.y+r.height/t)+3),W:r.width,H:r.height}
}
function worldToScreenV133(wx,wy){return{x:(wx-Game.ovCamera.x)*Game.ovTile,y:(wy-Game.ovCamera.y)*Game.ovTile}}
function screenToWorldV133(sx,sy){return{x:Math.floor(sx/Game.ovTile+Game.ovCamera.x),y:Math.floor(sy/Game.ovTile+Game.ovCamera.y)}}
window.worldToScreen=worldToScreenV133;window.screenToWorld=screenToWorldV133;

function terrainColorV133(world,v){
 const c=world.cfg;if(v===T.ART)return c.road;if(v===T.SEC)return c.secondary;if(v===T.ALLEY)return c.alley;if(v===T.PLAZA)return c.open;if(v===T.YARD)return '#1b1c1b';if(v===T.ROUGH)return c.ground;if(v===T.WATER)return '#06182a';if(v===T.RAIL)return '#211c19';if(v===T.BRIDGE)return '#2a3032';if(v===T.TUNNEL)return '#101427';if(v===T.PARK)return '#10251b';if(v===T.INDUSTRIAL)return '#181718';if(v===T.PED)return '#201e1d';if(v===T.TRANSIT)return '#202c31';return c.bg
}
function drawRoadCurvesV133(ctx,world,bounds=null){
 const t=Game.ovTile;for(const rc of world.roadCurves){if(rc.points.length<2)continue;const rb=rc.bounds||(rc.bounds=curveBoundsV177(rc.points));if(bounds){const pad=Math.max(1,rc.width*.7);if(rb.maxX+pad<bounds.x0||rb.minX-pad>bounds.x1||rb.maxY+pad<bounds.y0||rb.minY-pad>bounds.y1)continue}ctx.save();ctx.lineCap='round';ctx.lineJoin='round';const roadCol=rc.type===T.ART?world.cfg.road:rc.type===T.SEC?world.cfg.secondary:world.cfg.alley;const visualScale=rc.type===T.ART?(world.cfg.grammar==='glass'?.46:.38):rc.type===T.SEC?.46:rc.type===T.PED?.34:.22;
 const roadW=Math.max(rc.type===T.ALLEY?2:3,rc.width*visualScale*t);
 ctx.globalAlpha=rc.type===T.ART?.94:rc.type===T.SEC?.78:rc.type===T.PED?.66:.52;
 ctx.strokeStyle='rgba(0,0,0,.55)';ctx.lineWidth=roadW+Math.max(2,t*.11);ctx.beginPath();rc.points.forEach((p,i)=>{const s=worldToScreenV133(p.x+.5,p.y+.5);i?ctx.lineTo(s.x,s.y):ctx.moveTo(s.x,s.y)});ctx.stroke();
 ctx.strokeStyle=roadCol;ctx.lineWidth=roadW;ctx.stroke();
 const mat=window.CR14UrbanMaterials?.pattern?.(ctx,world.id,rc.type===T.ART?'road':'walk');if(mat){ctx.save();ctx.globalAlpha=rc.type===T.ART?.28:.20;ctx.strokeStyle=mat;ctx.lineWidth=Math.max(2,roadW*.78);ctx.stroke();ctx.restore()}
 if(rc.type===T.ART){ctx.strokeStyle='rgba(238,207,125,.24)';ctx.lineWidth=Math.max(1,t*.045);ctx.setLineDash([t*.42,t*.62]);ctx.stroke();ctx.setLineDash([])}
 else if(rc.type===T.SEC){ctx.strokeStyle='rgba(210,222,225,.07)';ctx.lineWidth=1;ctx.stroke()}
 ctx.globalAlpha=1;ctx.restore()}
}
function drawBuildingFootprintV133(ctx,b,world){
 const t=Game.ovTile,c=world.cfg,cx=(b.x+b.w/2-Game.ovCamera.x)*t,cy=(b.y+b.h/2-Game.ovCamera.y)*t;
 ctx.save(); // World buildings follow their unrotated collision/interaction footprints.
 const style=world.cfg.grammar,accent=c.accent,seed=b.seed;
 for(const part of b.parts){
   const x=(b.x+part.x-Game.ovCamera.x)*t,y=(b.y+part.y-Game.ovCamera.y)*t,w=part.w*t,h=part.h*t;
   ctx.shadowColor='rgba(0,0,0,.72)';ctx.shadowBlur=Math.min(18,t*.45);ctx.shadowOffsetX=3;ctx.shadowOffsetY=5;
   let grad=ctx.createLinearGradient(x,y,x+w,y+h);grad.addColorStop(0,c.roof);grad.addColorStop(.55,c.building);grad.addColorStop(1,'#05070a');
   ctx.fillStyle=grad;const radius=style==='glass'?Math.min(t*.6,10):style==='crown'?5:2;
   if(ctx.roundRect){ctx.beginPath();ctx.roundRect(x,y,w,h,radius);ctx.fill()}else ctx.fillRect(x,y,w,h);
   const facade=window.CR14UrbanMaterials?.pattern?.(ctx,world.id,'facade');if(facade){ctx.save();ctx.globalAlpha=style==='glass'?.24:.18;ctx.fillStyle=facade;if(ctx.roundRect){ctx.beginPath();ctx.roundRect(x,y,w,h,radius);ctx.fill()}else ctx.fillRect(x,y,w,h);ctx.restore()}
   ctx.shadowBlur=0;ctx.strokeStyle=accent+'35';ctx.lineWidth=1;ctx.strokeRect(x+.5,y+.5,w-1,h-1);
   if(style==='ash'){ctx.fillStyle='rgba(255,90,53,.15)';if(seed%3===0)ctx.fillRect(x+w*.08,y+h*.76,w*.72,2);ctx.fillStyle='rgba(0,0,0,.28)';ctx.fillRect(x+w*.18,y+h*.15,w*.24,h*.14)}
   else if(style==='market'){ctx.fillStyle=['#d06b3d','#d7b06c','#7aa89b','#8a557e'][seed%4]+'99';ctx.fillRect(x,y+h*.74,w,Math.max(2,t*.12));for(let k=1;k<4;k++){ctx.fillStyle='rgba(235,205,135,.24)';ctx.fillRect(x+w*k/4-1,y+h*.18,2,Math.max(2,h*.34))}}
   else if(style==='glass'){const rg=ctx.createLinearGradient(x,y,x+w,y);rg.addColorStop(0,'rgba(90,170,210,.10)');rg.addColorStop(.5,'rgba(180,225,255,.36)');rg.addColorStop(1,'rgba(85,105,175,.10)');ctx.fillStyle=rg;ctx.fillRect(x+w*.08,y+h*.08,w*.84,h*.76);ctx.fillStyle='rgba(150,210,255,.20)';ctx.fillRect(x+w*.15,y+h*.13,w*.06,h*.62)}
   else if(['dock','forge','rail'].includes(style)){ctx.strokeStyle='rgba(255,173,73,.28)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x+w*.1,y+h*.2);ctx.lineTo(x+w*.9,y+h*.2);ctx.stroke();for(let k=0;k<3;k++){ctx.fillStyle='rgba(255,180,80,.14)';ctx.fillRect(x+w*(.18+k*.27),y+h*.48,w*.12,h*.12)}}
   else if(style==='neon'){ctx.shadowColor=accent;ctx.shadowBlur=8;ctx.fillStyle=accent+'aa';ctx.fillRect(x+w*.06,y+h*.18,2,h*.5);ctx.fillRect(x+w*.06,y+h*.18,w*.45,2);ctx.shadowBlur=0}
   else if(style==='undergrid'){ctx.strokeStyle=accent+'45';ctx.strokeRect(x+w*.12,y+h*.12,w*.76,h*.76);ctx.fillStyle=accent+'22';ctx.fillRect(x+w*.25,y+h*.25,w*.5,h*.08)}
   else if(style==='meridian'||style==='helix'||style==='civic'){ctx.fillStyle=accent+'20';ctx.fillRect(x+w*.08,y+h*.10,w*.84,h*.08);ctx.fillStyle='rgba(255,255,255,.08)';ctx.fillRect(x+w*.12,y+h*.30,w*.76,1)}
   else if(style==='crown'){ctx.strokeStyle='#f2d76b55';ctx.strokeRect(x+w*.12,y+h*.12,w*.76,h*.76)}
   else if(style==='flood'){ctx.fillStyle='rgba(80,145,190,.15)';ctx.fillRect(x,y+h*.78,w,h*.12)}
   drawStructuralRoofV169(ctx,world,b,part,x,y,w,h);
   drawRoofWeatheringV170(ctx,world,b,part,x,y,w,h);
   if(typeof drawUrbanGritV170==='function')drawUrbanGritV170(ctx,world,b,part,x,y,w,h);
   drawFacadeWindowsV161(ctx,world,b,part,x,y,w,h,seed);
   drawStreetFrontageV161(ctx,world,b,part,x,y,w,h,seed);
   drawMasonryReturnsV170(ctx,world,b,part,x,y,w,h);
   window.CR14UrbanMaterials?.drawBuildingSign?.(ctx,world.id,b,x,y,w,h,seed);
   // Roof machinery / skylights / vents make large footprints read as structures rather than slabs.
   const units=Math.min(5,1+(seed%5));for(let u=0;u<units;u++){const ux=x+w*(.16+((seed+u*17)%63)/100),uy=y+h*(.16+((seed+u*29)%58)/100),uw=Math.max(2,Math.min(t*.22,w*.12)),uh=Math.max(2,Math.min(t*.16,h*.10));ctx.fillStyle='rgba(4,7,9,.42)';ctx.fillRect(ux,uy,uw,uh);ctx.strokeStyle='rgba(160,190,200,.11)';ctx.strokeRect(ux+.5,uy+.5,uw-1,uh-1)}
   if(b.signature){
     ctx.strokeStyle=accent+'66';ctx.lineWidth=Math.max(1,t*.045);ctx.strokeRect(x+2,y+2,w-4,h-4);
     ctx.fillStyle=accent+'18';ctx.fillRect(x+w*.18,y+h*.18,w*.64,Math.max(2,h*.08));
     if(style==='forge'){for(let s=0;s<3;s++){ctx.fillStyle='rgba(20,15,11,.9)';ctx.beginPath();ctx.arc(x+w*(.26+s*.23),y+h*.30,Math.min(7,t*.16),0,Math.PI*2);ctx.fill();ctx.strokeStyle='rgba(215,101,40,.34)';ctx.stroke()}}
     else if(style==='dock'){ctx.strokeStyle='rgba(255,154,47,.35)';ctx.lineWidth=2;for(let s=0;s<4;s++){ctx.beginPath();ctx.moveTo(x+w*.1+s*w*.2,y+h*.72);ctx.lineTo(x+w*.18+s*w*.2,y+h*.56);ctx.stroke()}}
     else if(style==='undergrid'){ctx.fillStyle=accent+'32';for(let s=0;s<5;s++)ctx.fillRect(x+w*.18+s*w*.12,y+h*.32,w*.055,h*.28)}
     else if(style==='glass'){ctx.fillStyle='rgba(170,225,255,.24)';ctx.fillRect(x+w*.28,y+h*.12,w*.44,h*.66)}
     else if(style==='meridian'){ctx.strokeStyle='rgba(220,248,255,.25)';ctx.strokeRect(x+w*.17,y+h*.17,w*.66,h*.66)}
     else if(style==='flood'){ctx.fillStyle='rgba(80,170,210,.22)';ctx.fillRect(x+w*.20,y+h*.60,w*.60,h*.12)}
   }
 }
 ctx.restore()
}
window.drawBuildingFootprintV133=drawBuildingFootprintV133;

/* PWA12.69: rectilinear service architecture, anchored to the actual collision footprint.
   No new world entities, no independent building rotations, and no simulation time. */
function drawStructuralRoofV169(ctx,world,b,part,x,y,w,h){
 const t=Game.ovTile,g=world.cfg.grammar;
 if(t<19||w<t*1.8||h<t*1.8)return;
 const industry=['dock','forge','rail'].includes(g),corporate=['glass','meridian','helix','civic','crown'].includes(g),
       seed=b.seed>>>0,margin=Math.max(4,t*.12),left=x+margin,top=y+margin,rw=w-margin*2,rh=h-margin*2;
 if(rw<20||rh<20)return;
 ctx.save();
 // Roofs are cast concrete, tar and aged sheet metal instead of flat luminous panels.
 ctx.fillStyle=corporate?'rgba(42,65,72,.25)':industry?'rgba(91,79,66,.24)':g==='neon'?'rgba(29,34,41,.61)':'rgba(82,78,68,.22)';
 ctx.fillRect(left,top,rw,rh);
 const step=Math.max(8,t*(industry?.38:.51));
 ctx.lineWidth=Math.max(.7,t*.017);
 ctx.strokeStyle=corporate?'rgba(155,185,185,.11)':industry?'rgba(191,175,145,.15)':'rgba(170,160,140,.12)';
 ctx.beginPath();for(let sx=left+step;sx<left+rw-3;sx+=step){ctx.moveTo(sx,top+2);ctx.lineTo(sx,top+rh-2)}ctx.stroke();
 // Exposed parapet: light on north / west faces, shadow on the south / east.
 const rim=Math.max(2,t*.072);
 ctx.fillStyle=corporate?'rgba(157,188,194,.32)':'rgba(176,167,145,.29)';ctx.fillRect(x,y,w,rim);ctx.fillRect(x,y,rim,h);
 ctx.fillStyle='rgba(0,0,0,.48)';ctx.fillRect(x+w-rim,y,rim,h);ctx.fillRect(x,y+h-rim,w,rim);
 ctx.strokeStyle='rgba(0,0,0,.39)';ctx.strokeRect(x+rim,y+rim,w-rim*2,h-rim*2);
 // Duct, fan housing and inspection hatch, scaled to real roof area.
 if(w>t*2.6&&h>t*2.5){
   const vx=x+w*.19,vy=y+h*.23,vw=Math.min(w*.18,t*.65),vh=Math.min(h*.14,t*.50);
   ctx.fillStyle='rgba(0,0,0,.42)';ctx.fillRect(vx+t*.065,vy+t*.065,vw,vh);
   ctx.fillStyle=corporate?'rgba(74,112,121,.81)':'rgba(107,105,95,.85)';ctx.fillRect(vx,vy,vw,vh);
   ctx.strokeStyle='rgba(204,204,187,.42)';ctx.strokeRect(vx+.5,vy+.5,vw-1,vh-1);
   ctx.strokeStyle='rgba(14,20,22,.48)';for(let k=1;k<4;k++){const xx=vx+vw*k/4;ctx.beginPath();ctx.moveTo(xx,vy+2);ctx.lineTo(xx,vy+vh-2);ctx.stroke()}
   const hx=x+w*.67,hy=y+h*.67,hw=Math.min(w*.16,t*.60),hh=Math.min(h*.11,t*.45);
   ctx.fillStyle='rgba(3,8,10,.55)';ctx.fillRect(hx+t*.04,hy+t*.045,hw,hh);
   ctx.fillStyle=corporate?'rgba(61,92,105,.67)':'rgba(83,81,70,.74)';ctx.fillRect(hx,hy,hw,hh);
   ctx.strokeStyle='rgba(190,198,187,.31)';ctx.strokeRect(hx+.5,hy+.5,hw-1,hh-1);
 }
 if(!corporate&&seed%3===0){ // A single tar-repair patch, not random neon squares.
   ctx.fillStyle='rgba(12,16,18,.22)';ctx.fillRect(x+w*.38,y+h*.73,w*.21,Math.max(2,t*.085));
 }
 ctx.restore();
}
window.drawStructuralRoofV169=drawStructuralRoofV169;

/* PWA12.70: broad, material-specific roof degradation. All marks are deterministic,
   clipped to the exact unrotated footprint, and generated only in the static pass. */
function drawRoofWeatheringV170(ctx,world,b,part,x,y,w,h){
 const t=Game.ovTile,g=world.cfg.grammar,corp=['glass','meridian','helix','civic','crown'].includes(g),factory=['dock','forge','rail'].includes(g);
 if(t<17||w<t*1.1||h<t*1.1)return;
 const seed=b.seed>>>0,inset=Math.max(3,t*.10),iw=w-2*inset,ih=h-2*inset;
 if(iw<=8||ih<=8)return;
 ctx.save();ctx.beginPath();ctx.rect(x+inset,y+inset,iw,ih);ctx.clip();
 // Roofs get irregular accumulated dirt rather than extra glowing outlines.
 const patches=Math.min(22,Math.max(3,Math.floor(iw*ih/(t*t*1.2))));
 for(let i=0;i<patches;i++){
  const r=randV133(world.id,b.seed,part.x,part.y,'patina',i),r2=randV133(world.id,b.seed,part.x,part.y,'patina-y',i),px=x+inset+iw*r,py=y+inset+ih*r2,rx=Math.max(3,Math.min(t*.70,iw*.24)),ry=Math.max(2,Math.min(t*.32,ih*.12));
  ctx.fillStyle=corp?'rgba(12,22,27,.16)':factory?'rgba(29,18,11,.25)':'rgba(23,19,15,.26)';
  ctx.beginPath();ctx.ellipse(px,py,rx*(.58+r*.8),ry*(.7+r2*.8),r-.5,0,Math.PI*2);ctx.fill();
  if(i%3===0){ctx.strokeStyle=corp?'rgba(183,206,206,.11)':factory?'rgba(154,101,63,.22)':'rgba(154,142,113,.14)';ctx.lineWidth=Math.max(.7,t*.017);ctx.beginPath();ctx.moveTo(px-rx*.55,py-ry*.40);ctx.lineTo(px+rx*.30,py+ry*.22);ctx.stroke()}
 }
 // Real service roofs show drainage flow from north to south and oxidized fasteners.
 const ducts=Math.max(1,Math.min(5,Math.floor(w/(t*1.4))));
 for(let i=0;i<ducts;i++){
  const xx=x+inset+(i+.5)*iw/ducts,yy=y+inset+ih*(.14+.7*randV133(b.seed,i,'drain'));
  ctx.fillStyle='rgba(8,13,14,.52)';ctx.fillRect(xx-t*.045,yy,t*.09,Math.max(2,t*.055));
  ctx.fillStyle=corp?'rgba(62,82,86,.22)':factory?'rgba(120,70,35,.22)':'rgba(111,94,72,.24)';ctx.fillRect(xx-t*.018,yy+t*.04,Math.max(1,t*.035),Math.max(3,ih*.22));
 }
 // Small isolated weatherproofing patches, not a uniform roof-wide grid.
 if(seed%3!==0){ctx.fillStyle='rgba(5,9,11,.24)';ctx.fillRect(x+iw*.24,y+ih*.62,Math.min(t*.53,iw*.29),Math.max(2,t*.11));}
 ctx.restore();
}
window.drawRoofWeatheringV170=drawRoofWeatheringV170;

/* The upper roof and narrow street-facing wall are distinguishable from above.
   The wall band stays *inside* the existing building footprint and does not alter hitboxes. */
function drawMasonryReturnsV170(ctx,world,b,part,x,y,w,h){
 const t=Game.ovTile,g=world.cfg.grammar,corp=['glass','meridian','helix','civic','crown'].includes(g),factory=['dock','forge','rail'].includes(g);
 if(t<20||w<t*1.4||h<t*1.3)return;
 const band=Math.min(t*.29,h*.14),bottom=y+h-band,margin=Math.max(2,t*.065),col=corp?'rgba(49,68,73,.94)':factory?'rgba(70,56,44,.96)':g==='neon'?'rgba(37,35,43,.96)':'rgba(58,52,44,.95)';
 ctx.save();ctx.fillStyle='rgba(0,0,0,.35)';ctx.fillRect(x+margin,bottom-2,w-2*margin,band+2);
 ctx.fillStyle=col;ctx.fillRect(x+margin,bottom,w-2*margin,band-margin*.4);
 ctx.fillStyle='rgba(2,5,6,.55)';ctx.fillRect(x+margin,bottom+band-Math.max(2,t*.07),w-2*margin,Math.max(2,t*.07));
 ctx.fillStyle=corp?'rgba(133,185,188,.19)':factory?'rgba(186,139,93,.18)':'rgba(189,171,139,.17)';
 for(let q=0;q<Math.floor((w-margin*2)/(t*.53));q++){
   const wx=x+margin+t*.21+q*t*.53;if(wx+t*.23>x+w-margin)break;
   ctx.fillRect(wx,bottom+band*.25,t*.23,Math.max(2,band*.43));
   ctx.fillStyle='rgba(3,7,9,.55)';ctx.fillRect(wx+t*.035,bottom+band*.27,Math.max(1,t*.025),Math.max(1,band*.36));
   ctx.fillStyle=corp?'rgba(133,185,188,.19)':factory?'rgba(186,139,93,.18)':'rgba(189,171,139,.17)';
 }
 ctx.restore();
}
window.drawMasonryReturnsV170=drawMasonryReturnsV170;



function buildingEdgeExposureV161(world,b,part){
 const gx=b.x+part.x,gy=b.y+part.y,gw=part.w,gh=part.h;
 const out={north:0,south:0,west:0,east:0};
 for(let i=0;i<gw;i++){if(walkableTerrain133(terrainAt133(world,gx+i,gy-1)))out.north++;if(walkableTerrain133(terrainAt133(world,gx+i,gy+gh)))out.south++;}
 for(let i=0;i<gh;i++){if(walkableTerrain133(terrainAt133(world,gx-1,gy+i)))out.west++;if(walkableTerrain133(terrainAt133(world,gx+gw,gy+i)))out.east++;}
 return out;
}
window.buildingEdgeExposureV161=buildingEdgeExposureV161;

function drawFacadeWindowsV161(ctx,world,b,part,x,y,w,h,seed){
 const t=Game.ovTile,style=world.cfg.grammar,affluent=['glass','helix','meridian','civic','crown'].includes(style),industrial=['dock','forge','rail'].includes(style);
 if(w<t*1.4||h<t*1.4)return;
 const cols=Math.max(2,Math.min(7,Math.floor(w/Math.max(16,t*.58))));
 const rows=Math.max(1,Math.min(5,Math.floor(h/Math.max(14,t*.54))));
 const padX=Math.max(3,t*.12),padY=Math.max(3,t*.12);
 const ww=Math.max(2,(w-padX*2-(cols-1)*t*.10)/cols),wh=Math.max(2,(h-padY*2-(rows-1)*t*.12)/rows);
 const litA=affluent?'rgba(190,235,255,.24)':industrial?'rgba(255,189,104,.18)':'rgba(242,208,131,.16)';
 const litB=affluent?'rgba(111,214,241,.15)':industrial?'rgba(214,120,67,.12)':'rgba(101,215,222,.10)';
 const dim='rgba(8,12,16,.24)';
 ctx.save();
 for(let ry=0;ry<rows;ry++)for(let cx=0;cx<cols;cx++){
   const wx=x+padX+cx*(ww+t*.10),wy=y+padY+ry*(wh+t*.12),r=randV133(world.id,b.seed,part.x,part.y,cx,ry,'window');
   ctx.fillStyle=r>.58?(r>.83?litA:litB):dim;
   ctx.fillRect(wx,wy,ww,wh);
 }
 if(industrial){ctx.strokeStyle='rgba(255,171,92,.10)';ctx.lineWidth=Math.max(1,t*.03);for(let ry=1;ry<rows;ry++){const yy=y+padY+ry*(wh+t*.12)-t*.06;ctx.beginPath();ctx.moveTo(x+padX,yy);ctx.lineTo(x+w-padX,yy);ctx.stroke()}}
 ctx.restore();
}
window.drawFacadeWindowsV161=drawFacadeWindowsV161;

function drawStreetFrontageV161(ctx,world,b,part,x,y,w,h,seed){
 const t=Game.ovTile,style=world.cfg.grammar,accent=world.cfg.accent,exp=buildingEdgeExposureV161(world,b,part);
 const affluent=['glass','helix','meridian','civic','crown'].includes(style),industrial=['dock','forge','rail'].includes(style);
 const signColor=affluent?'rgba(158,230,255,.22)':industrial?'rgba(255,178,89,.23)':'rgba(115,220,232,.20)';
 const trimColor=affluent?'rgba(195,236,255,.16)':industrial?'rgba(174,126,73,.18)':'rgba(229,196,114,.14)';
 const doorway='rgba(2,5,8,.70)';
 function awningNorth(){if(exp.north<Math.max(1,part.w*.25))return;ctx.fillStyle='rgba(0,0,0,.24)';ctx.fillRect(x+t*.10,y+t*.16,w-t*.20,Math.max(2,t*.08));ctx.fillStyle=signColor;ctx.fillRect(x+t*.16,y+t*.10,w-t*.32,Math.max(2,t*.07));for(let i=0;i<Math.max(1,Math.floor((w-t*.35)/(t*.44)));i++){const lx=x+t*.24+i*t*.44;ctx.fillStyle='rgba(255,244,213,.12)';ctx.fillRect(lx,y+t*.18,Math.max(2,t*.16),Math.max(2,t*.06))}}
 function awningSouth(){if(exp.south<Math.max(1,part.w*.25))return;ctx.fillStyle='rgba(0,0,0,.24)';ctx.fillRect(x+t*.10,y+h-Math.max(2,t*.24),w-t*.20,Math.max(2,t*.08));ctx.fillStyle=signColor;ctx.fillRect(x+t*.16,y+h-Math.max(2,t*.30),w-t*.32,Math.max(2,t*.07));for(let i=0;i<Math.max(1,Math.floor((w-t*.35)/(t*.44)));i++){const lx=x+t*.24+i*t*.44;ctx.fillStyle='rgba(255,244,213,.11)';ctx.fillRect(lx,y+h-Math.max(2,t*.22),Math.max(2,t*.16),Math.max(2,t*.06))}}
 function awningWest(){if(exp.west<Math.max(1,part.h*.28))return;ctx.fillStyle='rgba(0,0,0,.22)';ctx.fillRect(x+t*.12,y+t*.10,Math.max(2,t*.08),h-t*.20);ctx.fillStyle=trimColor;ctx.fillRect(x+t*.07,y+t*.14,Math.max(2,t*.06),h-t*.28);}
 function awningEast(){if(exp.east<Math.max(1,part.h*.28))return;ctx.fillStyle='rgba(0,0,0,.22)';ctx.fillRect(x+w-Math.max(2,t*.20),y+t*.10,Math.max(2,t*.08),h-t*.20);ctx.fillStyle=trimColor;ctx.fillRect(x+w-Math.max(2,t*.14),y+t*.14,Math.max(2,t*.06),h-t*.28);}
 awningNorth(); awningSouth(); awningWest(); awningEast();
 // Doorway on the most exposed side.
 const sides=[['north',exp.north],['south',exp.south],['west',exp.west],['east',exp.east]].sort((a,b)=>b[1]-a[1]);
 if(sides[0][1]>0){
   ctx.fillStyle=doorway;ctx.strokeStyle='rgba(191,231,234,.12)';ctx.lineWidth=1;
   if(sides[0][0]==='north'||sides[0][0]==='south'){
     const dw=Math.max(4,Math.min(w*.18,t*.24)),dx=x+w*.5-dw*.5,dy=sides[0][0]==='north'?y+h*.06:y+h-h*.18;
     ctx.fillRect(dx,dy,dw,h*.12);ctx.strokeRect(dx+.5,dy+.5,dw-1,h*.12-1);
     ctx.fillStyle=accent+'24';ctx.fillRect(dx-dw*.35,dy+(sides[0][0]==='north'?h*.13:-h*.03),dw*1.7,Math.max(1,t*.03));
   }else{
     const dh=Math.max(5,Math.min(h*.16,t*.26)),dy=y+h*.5-dh*.5,dx=sides[0][0]==='west'?x+w*.06:x+w-w*.12;
     ctx.fillRect(dx,dy,w*.10,dh);ctx.strokeRect(dx+.5,dy+.5,w*.10-1,dh-1);
     ctx.fillStyle=accent+'22';ctx.fillRect(dx+(sides[0][0]==='west'?w*.10:-w*.08),dy-dh*.20,Math.max(1,t*.03),dh*1.4);
   }
 }
 // Rooftop parapet / service seam to make massing read more clearly.
 ctx.strokeStyle='rgba(0,0,0,.34)';ctx.lineWidth=Math.max(1,t*.04);ctx.strokeRect(x+t*.05,y+t*.05,w-t*.10,h-t*.10);
}
window.drawStreetFrontageV161=drawStreetFrontageV161;



function drawDistrictPropsV133(ctx,world,bounds){
 const t=Game.ovTile,style=world.cfg.grammar;
 for(let y=bounds.y0;y<bounds.y1;y+=2)for(let x=bounds.x0;x<bounds.x1;x+=2){
   const r=randV133(world.id,x,y,'prop'),v=terrainAt133(world,x,y);
   const blockedPropOK=['dock','forge','rail','undergrid','meridian'].includes(style)&&(v===T.PARCEL||v===T.BUILDING);
   if((!walkableTerrain133(v)&&!blockedPropOK)||v===T.ART)continue;const p=worldToScreenV133(x+.5,y+.5);
   if(style==='ash'&&r>.82){ctx.fillStyle=r>.95?'#a94828':'#4a4540';ctx.fillRect(p.x-2,p.y-1,4,2);if(r>.965){ctx.strokeStyle='rgba(255,90,53,.35)';ctx.beginPath();ctx.moveTo(p.x-4,p.y+3);ctx.lineTo(p.x+4,p.y-3);ctx.stroke()}}
   else if(style==='market'&&r>.70&&(v===T.PED||v===T.PLAZA||v===T.ALLEY)){const col=['#b75e3d','#d7b06c','#6f9f8c','#85577d'][hashV133(`${x}:${y}`)%4];ctx.fillStyle=col+'dd';ctx.fillRect(p.x-t*.16,p.y-t*.12,t*.32,t*.24);ctx.fillStyle='rgba(15,12,10,.75)';ctx.fillRect(p.x-t*.13,p.y+t*.12,t*.26,2)}
   else if(style==='glass'&&r>.77&&(v===T.PARK||v===T.PLAZA||v===T.ROUGH)){ctx.fillStyle='rgba(69,126,82,.72)';ctx.beginPath();ctx.arc(p.x,p.y,2.5+(r-.77)*10,0,Math.PI*2);ctx.fill();if(r>.93){ctx.strokeStyle='rgba(150,220,185,.16)';ctx.beginPath();ctx.arc(p.x,p.y,5,0,Math.PI*2);ctx.stroke()}}
   else if(style==='neon'&&r>.86){ctx.fillStyle=world.cfg.accent+'aa';ctx.fillRect(p.x-1,p.y-4,2,8)}
   else if(style==='dock'&&r>.60&&(v===T.YARD||v===T.INDUSTRIAL||v===T.ROUGH)){const cols=['#8d4426','#b45f2b','#6a7e83','#806337'];const col=cols[hashV133(`${x}:${y}:container`)%cols.length];ctx.save();ctx.translate(p.x,p.y);ctx.rotate(((hashV133(`${x}:${y}:rot`)%9)-4)*.035);for(let k=0;k<3;k++){ctx.fillStyle=col;ctx.fillRect(-t*.30+k*t*.20,-t*.10,t*.17,t*.20);ctx.strokeStyle='rgba(0,0,0,.42)';ctx.strokeRect(-t*.30+k*t*.20,-t*.10,t*.17,t*.20)}ctx.restore()}
   else if(style==='forge'&&r>.64&&(v===T.YARD||v===T.INDUSTRIAL||v===T.ROUGH)){ctx.strokeStyle='rgba(215,101,40,.34)';ctx.lineWidth=2;ctx.beginPath();ctx.arc(p.x,p.y,Math.max(3,t*.13),0,Math.PI*2);ctx.stroke();ctx.beginPath();ctx.moveTo(p.x-t*.25,p.y);ctx.lineTo(p.x+t*.25,p.y);ctx.stroke()}
   else if(style==='rail'&&r>.80&&(v===T.YARD||v===T.INDUSTRIAL)){ctx.fillStyle='rgba(190,124,55,.22)';ctx.fillRect(p.x-t*.28,p.y-t*.07,t*.56,t*.14)}
   else if(style==='undergrid'&&r>.62&&(v===T.TUNNEL||v===T.ALLEY||v===T.ROUGH)){ctx.shadowColor=world.cfg.accent;ctx.shadowBlur=5;ctx.fillStyle=world.cfg.accent+'55';ctx.fillRect(p.x-2,p.y-2,4,4);ctx.shadowBlur=0;if(r>.92){ctx.strokeStyle=world.cfg.accent+'24';ctx.beginPath();ctx.moveTo(p.x-8,p.y);ctx.lineTo(p.x+8,p.y);ctx.stroke()}}
   else if((style==='meridian'||style==='helix'||style==='civic')&&r>.82&&v===T.PLAZA){ctx.strokeStyle=world.cfg.accent+'22';ctx.beginPath();ctx.arc(p.x,p.y,Math.max(3,t*.14),0,Math.PI*2);ctx.stroke()}
   else if(style==='flood'&&r>.82){ctx.fillStyle='rgba(90,180,210,.28)';ctx.fillRect(p.x-3,p.y,6,1)}
 }
}window.drawDistrictPropsV133=drawDistrictPropsV133;



function drawAnonymousUrbanFabricV133(ctx,world,bounds){
 const t=Game.ovTile,c=world.cfg,style=c.grammar;
 ctx.save();

 // Base city mass. Adjacent logical cells share exactly the same fill, so they merge
 // into continuous blocks instead of showing the navigation grid.
 const base=style==='ash'?'#17100f':
   style==='market'?'#171614':
   style==='neon'?'#130d17':
   style==='undergrid'?'#080a13':
   style==='glass'?'#0c141b':
   style==='civic'||style==='helix'||style==='meridian'?'#0c151d':
   style==='crown'?'#1a170f':
   style==='dock'||style==='forge'||style==='rail'?'#151310':
   style==='flood'?'#0d1016':'#111419';

 ctx.fillStyle=base;
 for(let y=bounds.y0;y<bounds.y1;y++)for(let x=bounds.x0;x<bounds.x1;x++){
   const v=terrainAt133(world,x,y);
   if(v!==T.PARCEL&&v!==T.BUILDING)continue;
   const p=worldToScreenV133(x,y);
   ctx.fillRect(Math.floor(p.x),Math.floor(p.y),Math.ceil(t)+1,Math.ceil(t)+1);
 }

 // Street-facing edge highlight: only draw block edges where urban mass meets walkable space.
 // This makes the blocks read as continuous architecture rather than a tiled field.
 const edgeColor=style==='glass'?'rgba(105,180,215,.16)':
   style==='neon'?'rgba(255,56,184,.14)':
   style==='ash'?'rgba(177,73,43,.13)':
   style==='market'?'rgba(210,172,104,.12)':
   style==='crown'?'rgba(242,215,107,.13)':
   'rgba(108,157,174,.10)';
 ctx.strokeStyle=edgeColor;ctx.lineWidth=Math.max(1,t*.035);
 ctx.beginPath();
 for(let y=bounds.y0;y<bounds.y1;y++)for(let x=bounds.x0;x<bounds.x1;x++){
   const v=terrainAt133(world,x,y);if(v!==T.PARCEL&&v!==T.BUILDING)continue;
   const p=worldToScreenV133(x,y),px=p.x,py=p.y;
   if(walkableTerrain133(terrainAt133(world,x,y-1))){ctx.moveTo(px,py);ctx.lineTo(px+t,py)}
   if(walkableTerrain133(terrainAt133(world,x+1,y))){ctx.moveTo(px+t,py);ctx.lineTo(px+t,py+t)}
   if(walkableTerrain133(terrainAt133(world,x,y+1))){ctx.moveTo(px+t,py+t);ctx.lineTo(px,py+t)}
   if(walkableTerrain133(terrainAt133(world,x-1,y))){ctx.moveTo(px,py+t);ctx.lineTo(px,py)}
 }
 ctx.stroke();

 // District-specific anonymous roof texture. Sparse and large enough not to expose cells.
 const spacing=style==='market'?5:style==='ash'?7:style==='neon'?6:style==='glass'?13:9;
 for(let y=bounds.y0;y<bounds.y1;y+=spacing)for(let x=bounds.x0;x<bounds.x1;x+=spacing){
   if(terrainAt133(world,x,y)!==T.PARCEL)continue;
   const r=randV133(world.id,x,y,'anonroof');if(r<.38)continue;
   const p=worldToScreenV133(x+.5,y+.5);
   if(style==='market'){
     const col=['#8d4938','#9a7442','#426f69','#6f465f'][hashV133(`${x}:${y}:m`)%4];
     ctx.fillStyle=col+'55';ctx.fillRect(p.x-t*.42,p.y-t*.20,t*.84,Math.max(2,t*.10));
   }else if(style==='ash'){
     ctx.fillStyle=r>.78?'rgba(150,57,33,.18)':'rgba(76,72,66,.16)';
     ctx.fillRect(p.x-t*.36,p.y-t*.18,t*.72,Math.max(2,t*.12));
   }else if(style==='neon'){
     ctx.shadowColor=c.accent;ctx.shadowBlur=5;ctx.fillStyle=c.accent+'38';
     ctx.fillRect(p.x-t*.28,p.y-t*.03,t*.56,Math.max(1,t*.045));ctx.shadowBlur=0;
   }else if(style==='undergrid'){
     ctx.strokeStyle=c.accent+'22';ctx.strokeRect(p.x-t*.28,p.y-t*.18,t*.56,t*.36);
   }else if(['dock','forge','rail'].includes(style)){
     ctx.fillStyle='rgba(214,133,60,.12)';ctx.fillRect(p.x-t*.30,p.y-t*.12,t*.60,t*.24);
   }else if(style==='glass'){
     ctx.fillStyle='rgba(110,185,215,.12)';ctx.fillRect(p.x-t*.16,p.y-t*.16,t*.32,t*.32);
   }else{
     ctx.fillStyle='rgba(130,170,185,.08)';ctx.fillRect(p.x-t*.22,p.y-t*.12,t*.44,t*.24);
   }
 }
 ctx.restore()
}
window.drawAnonymousUrbanFabricV133=drawAnonymousUrbanFabricV133;

function drawEnvironmentRegionsV133(ctx,world,bounds){
 const t=Game.ovTile,W=bounds.W,H=bounds.H;
 // PWA12.99: neighborhood-scale environmental surfaces can be much larger than a tile,
 // but regions wholly outside the visible world bounds cannot contribute pixels. Keep a
 // conservative 15% + 1 tile margin so edge gradients/geometry remain visually identical.
 const visibleNeighborhoods=world.neighborhoods.filter(n=>{const r=n.radius*1.15+1;return !(n.x+r<bounds.x0||n.x-r>bounds.x1||n.y+r<bounds.y0||n.y-r>bounds.y1)});
 // Neighborhood-scale surfaces hide the logical grid and give each district a broad material identity.
 if(world.cfg.grammar==='glass'){
   // landscaped estates / corporate gardens
   for(const n of visibleNeighborhoods){
     const p=worldToScreenV133(n.x,n.y),rx=n.radius*t*1.08,ry=n.radius*t*.82;const g=ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,Math.max(rx,ry));g.addColorStop(0,'rgba(26,78,48,.48)');g.addColorStop(.72,'rgba(12,51,31,.34)');g.addColorStop(1,'rgba(7,28,20,0)');ctx.fillStyle=g;ctx.beginPath();ctx.ellipse(p.x,p.y,rx,ry,0,0,Math.PI*2);ctx.fill();
     // private garden paths and water feature
     ctx.strokeStyle='rgba(160,205,190,.13)';ctx.lineWidth=Math.max(1,t*.08);ctx.beginPath();ctx.ellipse(p.x,p.y,rx*.64,ry*.46,.18,0,Math.PI*2);ctx.stroke();
     ctx.fillStyle='rgba(80,150,190,.22)';ctx.beginPath();ctx.ellipse(p.x+rx*.12,p.y-ry*.08,Math.max(4,t*.34),Math.max(3,t*.21),0,0,Math.PI*2);ctx.fill();
   }
 }else if(world.cfg.grammar==='undergrid'){
   // service chambers should read as rooms, not empty black ground
   for(const n of visibleNeighborhoods){
     const p=worldToScreenV133(n.x,n.y),rw=n.radius*t*.78,rh=n.radius*t*.56;
     ctx.fillStyle='rgba(19,20,40,.42)';ctx.fillRect(p.x-rw,p.y-rh,rw*2,rh*2);
     ctx.strokeStyle=world.cfg.accent+'28';ctx.lineWidth=Math.max(1,t*.05);ctx.strokeRect(p.x-rw,p.y-rh,rw*2,rh*2);
     for(let i=-2;i<=2;i++){ctx.fillStyle=world.cfg.accent+'18';ctx.fillRect(p.x+i*rw*.25-t*.07,p.y-rh*.44,t*.14,rh*.88)}
   }
 }else if(world.cfg.grammar==='ash'){
   for(const n of visibleNeighborhoods){const p=worldToScreenV133(n.x,n.y),r=n.radius*t*.95;const g=ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,r);g.addColorStop(0,'rgba(72,28,18,.18)');g.addColorStop(1,'rgba(30,11,8,0)');ctx.fillStyle=g;ctx.fillRect(p.x-r,p.y-r,r*2,r*2)}
 }else if(world.cfg.grammar==='market'){
   for(const n of visibleNeighborhoods){const p=worldToScreenV133(n.x,n.y),r=n.radius*t*.80;const g=ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,r);g.addColorStop(0,'rgba(126,92,48,.10)');g.addColorStop(1,'rgba(50,36,18,0)');ctx.fillStyle=g;ctx.fillRect(p.x-r,p.y-r,r*2,r*2)}
 }else if(world.cfg.grammar==='neon'){
   for(const n of visibleNeighborhoods){const p=worldToScreenV133(n.x,n.y),r=n.radius*t*.7;const g=ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,r);g.addColorStop(0,world.cfg.accent+'13');g.addColorStop(1,'transparent');ctx.fillStyle=g;ctx.fillRect(p.x-r,p.y-r,r*2,r*2)}
 }else if(['dock','forge','rail'].includes(world.cfg.grammar)){
   for(const n of visibleNeighborhoods){
     const p=worldToScreenV133(n.x,n.y),rw=n.radius*t*.92,rh=n.radius*t*.54;
     ctx.fillStyle='rgba(61,48,33,.13)';ctx.fillRect(p.x-rw,p.y-rh,rw*2,rh*2);ctx.strokeStyle='rgba(211,142,67,.10)';ctx.strokeRect(p.x-rw,p.y-rh,rw*2,rh*2);
     if(world.cfg.grammar==='dock'){
       // container-yard lanes
       for(let k=-2;k<=2;k++){ctx.strokeStyle='rgba(255,154,47,.10)';ctx.beginPath();ctx.moveTo(p.x-rw*.82,p.y+k*rh*.24);ctx.lineTo(p.x+rw*.82,p.y+k*rh*.24);ctx.stroke()}
       // gantry silhouette
       ctx.strokeStyle='rgba(255,174,81,.16)';ctx.lineWidth=Math.max(1,t*.05);ctx.beginPath();ctx.moveTo(p.x-rw*.62,p.y-rh*.58);ctx.lineTo(p.x-rw*.62,p.y-rh*.96);ctx.lineTo(p.x+rw*.40,p.y-rh*.96);ctx.lineTo(p.x+rw*.40,p.y-rh*.58);ctx.stroke()
     }else if(world.cfg.grammar==='forge'){
       // pipe manifold and tank circles
       ctx.strokeStyle='rgba(215,101,40,.18)';ctx.lineWidth=Math.max(1,t*.06);ctx.beginPath();ctx.moveTo(p.x-rw*.75,p.y);ctx.lineTo(p.x+rw*.75,p.y);ctx.stroke();
       for(let k=-2;k<=2;k++){ctx.beginPath();ctx.arc(p.x+k*rw*.28,p.y-rh*.28,Math.max(3,t*.20),0,Math.PI*2);ctx.stroke()}
     }else{
       for(let k=-2;k<=2;k++){ctx.strokeStyle='rgba(240,179,91,.10)';ctx.beginPath();ctx.moveTo(p.x-rw*.8,p.y+k*rh*.20);ctx.lineTo(p.x+rw*.8,p.y+k*rh*.20);ctx.stroke()}
     }
   }
 }else if(['civic','helix','meridian','crown'].includes(world.cfg.grammar)){
   for(const n of visibleNeighborhoods){
     const p=worldToScreenV133(n.x,n.y),r=n.radius*t*.62;const g=ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,r);g.addColorStop(0,world.cfg.accent+'0c');g.addColorStop(1,'transparent');ctx.fillStyle=g;ctx.beginPath();ctx.ellipse(p.x,p.y,r,r*.68,0,0,Math.PI*2);ctx.fill();
     if(world.cfg.grammar==='meridian'){
       ctx.strokeStyle='rgba(220,248,255,.14)';ctx.lineWidth=Math.max(1,t*.045);ctx.strokeRect(p.x-r*.72,p.y-r*.44,r*1.44,r*.88);
       ctx.strokeStyle='rgba(220,248,255,.07)';for(let k=-2;k<=2;k++){ctx.beginPath();ctx.moveTo(p.x-r*.62,p.y+k*r*.14);ctx.lineTo(p.x+r*.62,p.y+k*r*.14);ctx.stroke()}
     }
   }
 }
 // Floodline has continuous water channels rather than blue square cells.
 if(world.waterCurves?.length){
   ctx.save();ctx.lineCap='round';ctx.lineJoin='round';
   for(const wc of world.waterCurves){const wb=wc.bounds||(wc.bounds=curveBoundsV177(wc.points)),pad=Math.max(1,wc.width*.65);if(wb.maxX+pad<bounds.x0||wb.minX-pad>bounds.x1||wb.maxY+pad<bounds.y0||wb.minY-pad>bounds.y1)continue;ctx.strokeStyle='rgba(7,29,48,.98)';ctx.lineWidth=wc.width*t;ctx.beginPath();wc.points.forEach((p,i)=>{const s=worldToScreenV133(p.x,p.y);i?ctx.lineTo(s.x,s.y):ctx.moveTo(s.x,s.y)});ctx.stroke();ctx.strokeStyle='rgba(76,154,198,.15)';ctx.lineWidth=Math.max(2,wc.width*t*.10);ctx.stroke()}
   ctx.restore()
 }
 // Industrial rail bands are rendered as continuous tracks.
 if(world.railCurves?.length){
   ctx.save();ctx.lineCap='round';for(const rc of world.railCurves){const rb=rc.bounds||(rc.bounds=curveBoundsV177(rc.points)),pad=Math.max(1,rc.width);if(rb.maxX+pad<bounds.x0||rb.minX-pad>bounds.x1||rb.maxY+pad<bounds.y0||rb.minY-pad>bounds.y1)continue;ctx.strokeStyle='rgba(30,27,26,.96)';ctx.lineWidth=Math.max(4,rc.width*t*1.7);ctx.beginPath();rc.points.forEach((p,i)=>{const s=worldToScreenV133(p.x,p.y);i?ctx.lineTo(s.x,s.y):ctx.moveTo(s.x,s.y)});ctx.stroke();ctx.strokeStyle='rgba(174,129,72,.28)';ctx.lineWidth=Math.max(1,t*.06);ctx.setLineDash([t*.18,t*.18]);ctx.stroke();ctx.setLineDash([])}ctx.restore()
 }
}
function drawDistrictDetailV136(ctx,world,bounds){
 const t=Game.ovTile,style=world.cfg.grammar,accent=world.cfg.accent,seed=hashV133(`${world.id}:v136detail`);ctx.save();
 const spanX=Math.max(1,bounds.x1-bounds.x0),spanY=Math.max(1,bounds.y1-bounds.y0);
 if(style==='neon'){for(let i=0;i<14;i++){const x=bounds.x0+((seed+i*17)%spanX),y=bounds.y0+((seed+i*31)%spanY),v=terrainAt133(world,x,y);if(!walkableTerrain133(v))continue;const p=worldToScreenV133(x+.5,y+.5),w=Math.max(5,t*(.35+(i%3)*.12));ctx.shadowColor=i%2?accent:'#ff55c8';ctx.shadowBlur=7;ctx.fillStyle=i%2?accent+'bb':'#ff55c8aa';ctx.fillRect(p.x-w/2,p.y-t*.35,w,Math.max(2,t*.08));ctx.shadowBlur=0}}
 else if(style==='ash'){for(let i=0;i<11;i++){const x=bounds.x0+((seed+i*23)%spanX),y=bounds.y0+((seed+i*37)%spanY),p=worldToScreenV133(x+.5,y+.5);ctx.strokeStyle='rgba(167,84,48,.22)';ctx.beginPath();ctx.moveTo(p.x-t*.55,p.y-t*.28);ctx.lineTo(p.x+t*.55,p.y+t*.18);ctx.stroke();ctx.fillStyle='rgba(92,64,49,.55)';ctx.fillRect(p.x-2,p.y-2,4,4)}}
 else if(style==='market'){for(let i=0;i<16;i++){const x=bounds.x0+((seed+i*19)%spanX),y=bounds.y0+((seed+i*11)%spanY),v=terrainAt133(world,x,y);if(!walkableTerrain133(v))continue;const p=worldToScreenV133(x+.5,y+.5),cols=['#b75e3d','#d7b06c','#6f9f8c','#85577d'];ctx.fillStyle=cols[i%4]+'88';ctx.beginPath();ctx.moveTo(p.x-t*.25,p.y);ctx.lineTo(p.x,p.y-t*.18);ctx.lineTo(p.x+t*.25,p.y);ctx.closePath();ctx.fill()}}
 else if(style==='dock'){for(let i=0;i<10;i++){const x=bounds.x0+((seed+i*27)%spanX),y=bounds.y0+((seed+i*13)%spanY),p=worldToScreenV133(x+.5,y+.5);ctx.strokeStyle='rgba(255,154,47,.25)';ctx.strokeRect(p.x-t*.35,p.y-t*.14,t*.7,t*.28);ctx.beginPath();ctx.moveTo(p.x-t*.28,p.y);ctx.lineTo(p.x+t*.28,p.y);ctx.stroke()}}
 else if(style==='forge'){for(let i=0;i<9;i++){const x=bounds.x0+((seed+i*29)%spanX),y=bounds.y0+((seed+i*17)%spanY),p=worldToScreenV133(x+.5,y+.5);ctx.strokeStyle='rgba(215,101,40,.28)';ctx.lineWidth=Math.max(1,t*.05);ctx.beginPath();ctx.arc(p.x,p.y,Math.max(3,t*.2),0,Math.PI*2);ctx.stroke();ctx.beginPath();ctx.moveTo(p.x+t*.2,p.y);ctx.lineTo(p.x+t*.55,p.y);ctx.stroke()}}
 else if(style==='rail'){ctx.strokeStyle='rgba(230,170,80,.18)';ctx.lineWidth=2;for(let i=0;i<5;i++){const y=bounds.y0+((seed+i*17)%spanY),a=worldToScreenV133(bounds.x0,y),b=worldToScreenV133(bounds.x1,y);ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke()}}
 else if(style==='undergrid'){ctx.strokeStyle=accent+'25';ctx.lineWidth=2;for(let i=0;i<10;i++){const x=bounds.x0+((seed+i*13)%spanX),y=bounds.y0+((seed+i*21)%spanY),p=worldToScreenV133(x+.5,y+.5);ctx.beginPath();ctx.arc(p.x,p.y,Math.max(3,t*.13),0,Math.PI*2);ctx.stroke();ctx.beginPath();ctx.moveTo(p.x-t*.3,p.y);ctx.lineTo(p.x+t*.3,p.y);ctx.stroke()}}
 else if(style==='flood'){ctx.strokeStyle='rgba(91,170,211,.19)';for(let i=0;i<9;i++){const y=bounds.y0+((seed+i*19)%spanY),a=worldToScreenV133(bounds.x0,y),b=worldToScreenV133(bounds.x1,y);ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.bezierCurveTo((a.x+b.x)*.35,a.y+4,(a.x+b.x)*.65,b.y-4,b.x,b.y);ctx.stroke()}}
 else if(style==='glass'){for(let i=0;i<9;i++){const x=bounds.x0+((seed+i*19)%spanX),y=bounds.y0+((seed+i*23)%spanY),p=worldToScreenV133(x+.5,y+.5);ctx.fillStyle='rgba(65,128,83,.28)';ctx.beginPath();ctx.arc(p.x,p.y,Math.max(3,t*.13),0,Math.PI*2);ctx.fill();ctx.strokeStyle='rgba(180,225,255,.12)';ctx.strokeRect(p.x-t*.23,p.y-t*.23,t*.46,t*.46)}}
 else if(['meridian','helix','civic','crown'].includes(style)){for(let i=0;i<8;i++){const x=bounds.x0+((seed+i*31)%spanX),y=bounds.y0+((seed+i*17)%spanY),p=worldToScreenV133(x+.5,y+.5);ctx.strokeStyle=accent+'22';ctx.strokeRect(p.x-t*.28,p.y-t*.28,t*.56,t*.56);ctx.fillStyle=accent+'16';ctx.fillRect(p.x-t*.18,p.y-t*.04,t*.36,Math.max(1,t*.08))}}
 ctx.restore()
}
window.drawDistrictDetailV136=drawDistrictDetailV136;

/* PWA12.41: world-anchored environmental grit, static-pass only. */
function drawGrittyStreetFabricV141(ctx,world,b){
 const t=Game.ovTile,grammar=world.cfg.grammar,industrial=['dock','forge','rail'].includes(grammar),affluent=['glass','helix','meridian','crown','civic'].includes(grammar);
 if(t<17)return;
 ctx.save();
 for(let y=Math.floor(b.y0/3)*3;y<b.y1;y+=3)for(let x=Math.floor(b.x0/3)*3;x<b.x1;x+=3){
  if(!walkableTerrain133(terrainAt133(world,x,y)))continue;
  const r=visualCellRandV101(world,'grit',x,y),p=worldToScreenV133(x+.5,y+.5);
  ctx.lineWidth=Math.max(.65,t*.023);ctx.strokeStyle=affluent?'rgba(108,151,169,.16)':'rgba(7,8,9,.48)';
  ctx.beginPath();ctx.moveTo(p.x-t*.68,p.y-t*.27);ctx.lineTo(p.x-t*.17,p.y-t*(.11+r*.19));ctx.lineTo(p.x+t*(.18+r*.17),p.y+t*.09);ctx.stroke();
  if(r>.4){ctx.fillStyle=affluent?'rgba(83,120,142,.13)':'rgba(4,7,9,.34)';ctx.fillRect(p.x-t*.48,p.y+t*.28,t*(.33+r*.32),t*.13);ctx.strokeStyle='rgba(167,175,170,.10)';ctx.strokeRect(p.x-t*.48,p.y+t*.28,t*(.33+r*.32),t*.13)}
  if(r>.78&&!affluent){ctx.fillStyle='rgba(3,11,18,.57)';ctx.beginPath();ctx.ellipse(p.x+t*.16,p.y+t*.37,t*.34,t*.105,-.16,0,Math.PI*2);ctx.fill();ctx.fillStyle=world.cfg.accent+'30';ctx.fillRect(p.x-t*.03,p.y+t*.33,t*.25,Math.max(1,t*.018))}
  if(r<.2&&industrial){ctx.fillStyle='rgba(5,8,9,.75)';ctx.fillRect(p.x-t*.25,p.y-t*.2,t*.46,t*.12);ctx.strokeStyle='rgba(173,146,83,.32)';for(let j=0;j<3;j++){ctx.beginPath();ctx.moveTo(p.x-t*.21+j*t*.13,p.y-t*.2);ctx.lineTo(p.x-t*.21+j*t*.13,p.y-t*.08);ctx.stroke()}}
  if(r>.89&&!affluent){ctx.fillStyle='rgba(72,67,57,.64)';ctx.fillRect(p.x+t*.27,p.y-t*.24,t*.12,t*.16);ctx.fillStyle='rgba(129,111,80,.38)';ctx.fillRect(p.x+t*.28,p.y-t*.25,t*.09,t*.025)}
 }
 ctx.restore();
}
window.drawGrittyStreetFabricV141=drawGrittyStreetFabricV141;

/* PWA12.70: medium-scale resurfacing, road-edge cracking and rain grime.
   4x4 world lattice ensures marks are spatially stable as camera pans. */
function drawMunicipalWearV170(ctx,world,bounds){
 const t=Game.ovTile,g=world.cfg.grammar,corp=['glass','meridian','helix','civic','crown'].includes(g);
 if(t<18)return;
 ctx.save();
 for(let y=Math.floor(bounds.y0/4)*4;y<bounds.y1;y+=4)for(let x=Math.floor(bounds.x0/4)*4;x<bounds.x1;x+=4){
  const v=terrainAt133(world,x,y);if(![T.ART,T.SEC,T.ALLEY,T.PED,T.PLAZA,T.TRANSIT].includes(v))continue;
  const r=visualCellRandV101(world,'pavement-restoration',x,y,true),p=worldToScreenV133(x+.5,y+.5);
  if(r>.35){
   const rw=t*(.8+r*.45),rh=t*(.28+r*.31),px=p.x-rw*.48,py=p.y+rh*.12;
   ctx.fillStyle=corp?'rgba(19,29,32,.33)':'rgba(10,13,15,.48)';ctx.fillRect(px,py,rw,rh);
   ctx.strokeStyle=corp?'rgba(115,145,147,.17)':'rgba(111,102,83,.24)';ctx.lineWidth=Math.max(.7,t*.02);ctx.strokeRect(px+.5,py+.5,rw-1,rh-1);
   if(r>.67){ctx.strokeStyle='rgba(146,130,105,.13)';ctx.beginPath();ctx.moveTo(px+rw*.12,py+rh*.67);ctx.lineTo(px+rw*.45,py+rh*.57);ctx.lineTo(px+rw*.87,py+rh*.79);ctx.stroke()}
  }
  if(r>.76&&!corp){
   const puddle=ctx.createLinearGradient(p.x-t*.35,p.y,p.x+t*.47,p.y+t*.25);
   puddle.addColorStop(0,'rgba(3,12,15,.05)');puddle.addColorStop(.42,'rgba(4,15,19,.52)');puddle.addColorStop(1,'rgba(8,23,27,.08)');
   ctx.fillStyle=puddle;ctx.beginPath();ctx.ellipse(p.x,p.y+t*.38,t*.43,t*.115,-.12,0,Math.PI*2);ctx.fill();
   ctx.strokeStyle=world.cfg.accent+'34';ctx.lineWidth=Math.max(1,t*.035);ctx.beginPath();ctx.moveTo(p.x-t*.12,p.y+t*.35);ctx.lineTo(p.x+t*.24,p.y+t*.33);ctx.stroke();
  }
 }
 ctx.restore();
}
window.drawMunicipalWearV170=drawMunicipalWearV170;


/* PWA12.62: stronger landmark readability and ground-story texture for the overworld. */
function drawStreetMicroDetailsV162(ctx,world,bounds){
 const t=Game.ovTile,grammar=world.cfg.grammar,industrial=['dock','forge','rail'].includes(grammar),affluent=['glass','helix','meridian','civic','crown'].includes(grammar);
 if(t<16)return;
 ctx.save();
 for(let y=bounds.y0;y<bounds.y1;y++)for(let x=bounds.x0;x<bounds.x1;x++){
  const v=terrainAt133(world,x,y);if(![T.ART,T.SEC,T.ALLEY,T.PED,T.PLAZA,T.TRANSIT,T.BRIDGE].includes(v))continue;
  const p=worldToScreenV133(x,y),cx=p.x+t*.5,cy=p.y+t*.5,r=visualCellRandV101(world,'microdetail',x,y);
  if((v===T.ART||v===T.SEC||v===T.TRANSIT||v===T.BRIDGE)){
   if(r>.70){ctx.fillStyle='rgba(0,0,0,.16)';ctx.fillRect(p.x+t*.14,p.y+t*.14,t*(.18+r*.14),Math.max(1,t*.035));}
   if(r>.78){ctx.strokeStyle=affluent?'rgba(188,226,241,.10)':industrial?'rgba(228,157,82,.12)':'rgba(232,199,133,.10)';ctx.lineWidth=Math.max(1,t*.028);ctx.beginPath();ctx.moveTo(p.x+t*.18,cy+t*.18);ctx.lineTo(p.x+t*.82,cy+t*.18);ctx.stroke();}
   if(r>.86){ctx.fillStyle='rgba(4,8,12,.34)';ctx.beginPath();ctx.ellipse(cx+t*.07,cy+t*.22,t*.16,t*.05,-.14,0,Math.PI*2);ctx.fill();ctx.fillStyle=world.cfg.accent+'24';ctx.fillRect(cx+t*.01,cy+t*.20,t*.16,Math.max(1,t*.02));}
   if(r<.17){ctx.strokeStyle='rgba(233,202,118,.12)';ctx.lineWidth=Math.max(.75,t*.022);ctx.strokeRect(p.x+t*.28,p.y+t*.28,t*.18,t*.10)}
   if(r>.94){ctx.fillStyle='rgba(0,0,0,.28)';ctx.fillRect(cx-t*.08,cy-t*.08,t*.16,t*.16);ctx.strokeStyle='rgba(174,188,196,.14)';ctx.strokeRect(cx-t*.08+.5,cy-t*.08+.5,t*.16-1,t*.16-1)}
  }else if(v===T.PLAZA||v===T.PED){
   if(r>.66){ctx.strokeStyle=affluent?'rgba(197,234,247,.08)':'rgba(225,199,143,.09)';ctx.lineWidth=Math.max(.8,t*.022);ctx.beginPath();ctx.moveTo(p.x+t*.18,p.y+t*.25);ctx.lineTo(p.x+t*.82,p.y+t*.25);ctx.moveTo(p.x+t*.25,p.y+t*.74);ctx.lineTo(p.x+t*.75,p.y+t*.74);ctx.stroke();}
   if(r>.88){ctx.fillStyle='rgba(3,8,11,.42)';ctx.fillRect(cx-t*.12,cy+t*.08,t*.24,Math.max(1,t*.06));ctx.fillStyle=world.cfg.accent+'20';ctx.fillRect(cx-t*.08,cy+t*.10,t*.16,Math.max(1,t*.02));}
  }else if(v===T.ALLEY){
   if(r>.58){ctx.fillStyle='rgba(5,8,10,.54)';ctx.beginPath();ctx.ellipse(cx+t*.05,cy+t*.18,t*.18,t*.06,-.20,0,Math.PI*2);ctx.fill();}
   if(r>.81){ctx.fillStyle='rgba(80,74,66,.62)';ctx.fillRect(cx-t*.12,cy-t*.05,t*.18,t*.10);ctx.fillStyle='rgba(133,119,94,.28)';ctx.fillRect(cx-t*.10,cy-t*.03,t*.14,Math.max(1,t*.02));}
  }
 }
 ctx.restore();
}
window.drawStreetMicroDetailsV162=drawStreetMicroDetailsV162;

function drawDistrictLandmarkVisualsV162(ctx,world,bounds){
 const t=Game.ovTile,style=world.cfg.grammar,markers=allMarkersV133(world);ctx.save();
 for(const m of markers){
  if(m.x<bounds.x0-3||m.y<bounds.y0-3||m.x>bounds.x1+3||m.y>bounds.y1+3)continue;
  const p=worldToScreenV133(m.x+.5,m.y+.5),color=(m.style?.color)||world.cfg.accent,rr=Math.max(10,Math.min(20,t*.46)),gy=p.y+t*.16;
  const g=ctx.createRadialGradient(p.x,gy,0,p.x,gy,rr*2.4);g.addColorStop(0,color+'2d');g.addColorStop(.45,color+'10');g.addColorStop(1,'transparent');ctx.fillStyle=g;ctx.beginPath();ctx.ellipse(p.x,gy,rr*1.55,rr*.68,0,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle=color+'42';ctx.lineWidth=Math.max(1,t*.03);ctx.beginPath();ctx.moveTo(p.x,p.y-rr*1.75);ctx.lineTo(p.x,p.y-rr*.28);ctx.stroke();
  ctx.strokeStyle='rgba(255,255,255,.08)';ctx.beginPath();ctx.moveTo(p.x,p.y-rr*1.5);ctx.lineTo(p.x,p.y-rr*.72);ctx.stroke();
  if(m.kind==='safehouse'){
   ctx.fillStyle='rgba(3,7,9,.80)';ctx.fillRect(p.x-rr*.84,p.y-rr*1.56,rr*1.68,rr*.46);ctx.strokeStyle=color+'55';ctx.strokeRect(p.x-rr*.84+.5,p.y-rr*1.56+.5,rr*1.68-1,rr*.46-1);ctx.fillStyle=color+'36';ctx.fillRect(p.x-rr*.62,p.y-rr*1.43,rr*1.24,Math.max(2,t*.05));
  }else if(m.kind==='transit'){
   ctx.strokeStyle=color+'40';ctx.beginPath();ctx.moveTo(p.x-rr*.9,p.y+rr*.45);ctx.lineTo(p.x-rr*.4,p.y+rr*.12);ctx.lineTo(p.x+rr*.4,p.y+rr*.12);ctx.lineTo(p.x+rr*.9,p.y+rr*.45);ctx.stroke();
  }else if(m.style?.type==='contact'||m.def?.contact){
   ctx.fillStyle=color+'22';ctx.fillRect(p.x-rr*.65,p.y-rr*1.18,rr*.22,rr*.82);ctx.fillRect(p.x+rr*.43,p.y-rr*1.18,rr*.22,rr*.82);
  }else if(m.style?.type==='market'||m.def?.type==='shop'){
   ctx.strokeStyle=color+'35';ctx.beginPath();ctx.moveTo(p.x-rr*.72,p.y-rr*.95);ctx.lineTo(p.x-rr*.26,p.y-rr*1.28);ctx.lineTo(p.x+rr*.26,p.y-rr*1.28);ctx.lineTo(p.x+rr*.72,p.y-rr*.95);ctx.stroke();
  }
 }
 for(const bld of world.buildings){
  if(!bld.signature)continue;if(bld.x+bld.w<bounds.x0||bld.y+bld.h<bounds.y0||bld.x>bounds.x1||bld.y>bounds.y1)continue;
  const x=(bld.x-Game.ovCamera.x)*t,y=(bld.y-Game.ovCamera.y)*t,w=bld.w*t,h=bld.h*t,cx=x+w*.5,roofY=y+t*.14;
  ctx.save(); // Signature architecture aligns with the orthogonal building silhouette.
  if(['market','neon','ash'].includes(style)){
    ctx.fillStyle='rgba(3,7,9,.78)';ctx.fillRect(cx-w*.10,roofY-h*.02,w*.20,Math.max(3,t*.18));ctx.strokeStyle=world.cfg.accent+'55';ctx.strokeRect(cx-w*.22,roofY-h*.08,w*.44,Math.max(5,t*.28));ctx.fillStyle=world.cfg.accent+'25';ctx.fillRect(cx-w*.18,roofY-h*.04,w*.36,Math.max(2,t*.07));
  }else if(['dock','forge','rail'].includes(style)){
    ctx.strokeStyle='rgba(198,145,86,.30)';ctx.lineWidth=Math.max(1,t*.04);ctx.beginPath();ctx.moveTo(cx-w*.18,roofY+t*.06);ctx.lineTo(cx-w*.18,roofY-h*.22);ctx.lineTo(cx+w*.10,roofY-h*.22);ctx.lineTo(cx+w*.10,roofY+t*.04);ctx.stroke();ctx.beginPath();ctx.moveTo(cx-w*.18,roofY-h*.16);ctx.lineTo(cx+w*.18,roofY-h*.28);ctx.stroke();
  }else{
    ctx.strokeStyle=world.cfg.accent+'38';ctx.lineWidth=Math.max(1,t*.03);ctx.beginPath();ctx.moveTo(cx,roofY+t*.04);ctx.lineTo(cx,roofY-h*.24);ctx.stroke();ctx.beginPath();ctx.arc(cx,roofY-h*.26,Math.max(2,t*.09),0,Math.PI*2);ctx.stroke();
  }
  ctx.restore();
 }
 ctx.restore();
}
window.drawDistrictLandmarkVisualsV162=drawDistrictLandmarkVisualsV162;



/* PWA12.63 — macro-scale urban art. All decoration is world-anchored, clipped
   to the visible map, and rendered only into the frozen-world static layer. */
function drawUrbanDepthV163(ctx,world,bounds){
 const t=Game.ovTile,style=world.cfg.grammar;
 if(t<20)return;
 const commercial=style==='market'||style==='neon',industrial=['dock','forge','rail','ash'].includes(style),
       clean=['glass','meridian','helix','civic','crown'].includes(style);
 const rw=3,rh=2;
 ctx.save();
 // These are anonymous rooftops, not navigation cells or collision objects.
 // Require a fully blocked patch so nothing is painted across a walkable path.
 for(let gy=Math.floor(bounds.y0/6)*6;gy<bounds.y1;gy+=6)for(let gx=Math.floor(bounds.x0/6)*6;gx<bounds.x1;gx+=6){
  const roll=randV133(world.id,'roofscape',gx,gy);
  if(roll<.23)continue;
  let solid=true;
  for(let iy=0;iy<rh&&solid;iy++)for(let ix=0;ix<rw;ix++){
   const v=terrainAt133(world,gx+ix,gy+iy);
   if(v!==T.PARCEL&&v!==T.BUILDING){solid=false;break}
  }
  if(!solid)continue;
  const p=worldToScreenV133(gx,gy),x=p.x+t*.11,y=p.y+t*.12,w=t*2.7,h=t*1.72;
  ctx.fillStyle='rgba(0,0,0,.29)';ctx.fillRect(x+5,y+7,w,h);
  ctx.fillStyle=commercial?'rgba(70,62,56,.55)':industrial?'rgba(65,55,46,.60)':clean?'rgba(45,66,76,.65)':'rgba(48,56,65,.58)';
  ctx.fillRect(x,y,w,h);
  ctx.strokeStyle=commercial?'rgba(190,159,114,.30)':industrial?'rgba(169,130,92,.27)':'rgba(120,181,201,.28)';
  ctx.lineWidth=1.2;ctx.strokeRect(x+.6,y+.6,w-1.2,h-1.2);
  ctx.fillStyle='rgba(0,0,0,.30)';ctx.fillRect(x+t*.12,y+t*.18,w-t*.24,h-t*.36);
  // Roof service cores: silhouettes big enough to read at the default camera zoom.
  const bx=x+w*.12,by=y+h*.20;
  ctx.fillStyle=industrial?'rgba(126,112,91,.58)':'rgba(114,139,145,.50)';
  ctx.fillRect(bx,by,w*.24,h*.32);ctx.fillRect(x+w*.58,y+h*.48,w*.25,h*.23);
  ctx.fillStyle='rgba(0,0,0,.48)';ctx.fillRect(bx+t*.04,by+t*.05,w*.18,h*.12);
  ctx.strokeStyle='rgba(190,205,201,.18)';ctx.beginPath();ctx.moveTo(bx+w*.28,by+h*.11);ctx.lineTo(x+w*.63,by+h*.11);ctx.lineTo(x+w*.63,y+h*.45);ctx.stroke();
  if(roll>.73){
   ctx.fillStyle=commercial?'rgba(214,171,108,.38)':industrial?'rgba(215,128,75,.32)':'rgba(111,212,225,.32)';
   ctx.fillRect(x+w*.08,y+h*.87,w*.56,Math.max(2,t*.075));
   ctx.fillStyle='rgba(5,8,11,.54)';ctx.fillRect(x+w*.65,y+h*.12,w*.22,h*.20);
  }
 }
 ctx.restore();
}
window.drawUrbanDepthV163=drawUrbanDepthV163;

function drawStreetLightingV163(ctx,world,bounds){
 const t=Game.ovTile,style=world.cfg.grammar,commercial=style==='market'||style==='neon',
       industrial=['dock','forge','rail','ash'].includes(style),affluent=['glass','meridian','helix','civic','crown'].includes(style),
       lamp=commercial?(style==='neon'?'#fa56bf':'#f2b979'):industrial?'#e0a35f':affluent?'#8ccfe7':'#91b7d9';
 if(t<18)return;
 ctx.save();
 // Sparse persistent practical-light sources, placed on existing walkable tiles.
 for(let gy=Math.floor(bounds.y0/5)*5;gy<bounds.y1;gy+=5)for(let gx=Math.floor(bounds.x0/5)*5;gx<bounds.x1;gx+=5){
  if(randV133(world.id,'lantern',gx,gy)<.36)continue;
  const v=terrainAt133(world,gx,gy);if(!walkableTerrain133(v)||v===T.WATER)continue;
  const screen=worldToScreenV133(gx+.5,gy+.5),x=screen.x,y=screen.y;
  const radius=t*(commercial?2.3:industrial?1.75:2.0);
  const g=ctx.createRadialGradient(x,y,1,x,y,radius);
  g.addColorStop(0,commercial?'rgba(236,166,113,.19)':affluent?'rgba(126,210,230,.15)':'rgba(212,154,102,.15)');
  g.addColorStop(.36,commercial?'rgba(213,126,109,.095)':affluent?'rgba(93,158,185,.070)':'rgba(166,124,91,.070)');
  g.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=g;ctx.fillRect(x-radius,y-radius,radius*2,radius*2);
  ctx.fillStyle='rgba(4,8,10,.74)';ctx.fillRect(x-t*.045,y-t*.29,Math.max(1,t*.09),t*.27);
  ctx.fillStyle=lamp;ctx.globalAlpha=.72;ctx.fillRect(x-t*.10,y-t*.32,t*.2,Math.max(2,t*.065));ctx.globalAlpha=1;
  // A short, restrained reflected streak reads as wet pavement, not an animated overlay.
  ctx.fillStyle=lamp;ctx.globalAlpha=.12;ctx.fillRect(x-t*.09,y+t*.15,t*.17,Math.max(1,t*.035));ctx.globalAlpha=1;
 }
 ctx.restore();
}
window.drawStreetLightingV163=drawStreetLightingV163;


function drawSiteCanopiesV163(ctx,world,bounds){
 const t=Game.ovTile;if(t<27)return;
 ctx.save();
 for(const m of allMarkersV133(world)){
  if(m.x<bounds.x0-4||m.x>bounds.x1+4||m.y<bounds.y0-4||m.y>bounds.y1+4)continue;
  const typ=m.kind==='safehouse'?'safehouse':m.kind==='transit'?'transit':m.style?.type;
  if(!['safehouse','transit','contact','clinic','weapons','market','data'].includes(typ))continue;
  const p=worldToScreenV133(m.x+.5,m.y+.5),accent=m.style?.color||world.cfg.accent;
  const ww=t*(typ==='safehouse'?2.30:1.88),hh=t*.52;
  const x=p.x-ww*.5,y=p.y-t*2.00;
  // A street-front hardware canopy and projected nameplate, not a new collidable structure.
  ctx.fillStyle='rgba(0,0,0,.43)';ctx.fillRect(x+3,y+5,ww,hh);
  ctx.fillStyle='rgba(10,18,22,.90)';ctx.fillRect(x,y,ww,hh);
  ctx.strokeStyle=accent+'91';ctx.lineWidth=1.25;ctx.strokeRect(x+.5,y+.5,ww-1,hh-1);
  ctx.fillStyle=accent+'54';ctx.fillRect(x+4,y+hh-4,ww-8,2);
  ctx.strokeStyle=accent+'54';ctx.lineWidth=1.25;
  ctx.beginPath();ctx.moveTo(x+4,y+hh);ctx.lineTo(p.x-t*.22,p.y-t*.63);ctx.moveTo(x+ww-4,y+hh);ctx.lineTo(p.x+t*.22,p.y-t*.63);ctx.stroke();
  const txt=typ==='safehouse'?'CREW SAFEHOUSE':typ==='transit'?'TRANSIT GATE':typ==='contact'?'LOCAL CONTACT':typ==='clinic'?'CLINIC':typ==='weapons'?'ARMS':'STREET MARKET';
  ctx.font=`700 ${Math.max(7,Math.min(11,t*.23))}px Share Tech Mono, monospace`;
  ctx.fillStyle=accent;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(txt,p.x,y+hh*.48,ww-9);
 }
 ctx.restore();
}
window.drawSiteCanopiesV163=drawSiteCanopiesV163;

function drawSiteForecourtsV163(ctx,world,bounds){
 const t=Game.ovTile;
 if(t<20)return;
 ctx.save();
 for(const m of allMarkersV133(world)){
  if(m.x<bounds.x0-4||m.x>bounds.x1+4||m.y<bounds.y0-4||m.y>bounds.y1+4)continue;
  const p=worldToScreenV133(m.x+.5,m.y+.5),x=p.x,y=p.y,color=m.style?.color||world.cfg.accent;
  const radius=t*1.48;
  const light=ctx.createRadialGradient(x,y,0,x,y,radius);
  light.addColorStop(0,color+'32');light.addColorStop(.42,color+'12');light.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=light;
  ctx.fillRect(x-radius,y-radius,radius*2,radius*2);
  // Wayfinding and approach markings are on the accessible forecourt itself.
  // No tiles are altered; the marker and actual interactions remain authoritative.
  ctx.strokeStyle=color+'48';ctx.lineWidth=Math.max(1,t*.035);
  const r=t*.57;ctx.beginPath();ctx.arc(x,y,r,Math.PI*.18,Math.PI*.82);ctx.stroke();
  ctx.beginPath();ctx.moveTo(x-r*.75,y+t*.65);ctx.lineTo(x-r*.25,y+t*.65);
  ctx.moveTo(x+r*.25,y+t*.65);ctx.lineTo(x+r*.75,y+t*.65);ctx.stroke();
  ctx.fillStyle=color+'36';ctx.fillRect(x-t*.23,y+t*.85,t*.46,Math.max(2,t*.06));
 }
 ctx.restore();
}
window.drawSiteForecourtsV163=drawSiteForecourtsV163;


const STATIC_BACKDROP_CACHE_V193=new Map();
function staticBackdropV193(world,W,H){
 const dpr=Math.max(1,window.devicePixelRatio||1),key=`${world.id}|${world.cfg.ground}|${world.cfg.bg}|${world.cfg.accent}|${W}|${H}|${dpr}`;
 let c=STATIC_BACKDROP_CACHE_V193.get(key);if(c)return c;
 c=document.createElement('canvas');c.width=Math.max(1,Math.round(W*dpr));c.height=Math.max(1,Math.round(H*dpr));
 const x=c.getContext('2d');x.setTransform(dpr,0,0,dpr,0,0);
 const bg=x.createRadialGradient(W*.5,H*.18,0,W*.5,H*.18,Math.max(W,H)*.9);bg.addColorStop(0,world.cfg.ground);bg.addColorStop(.64,world.cfg.bg);bg.addColorStop(1,'#010305');x.fillStyle=bg;x.fillRect(0,0,W,H);
 x.fillStyle=world.cfg.accent+'07';x.fillRect(0,0,W,H);
 x.save();for(let i=0;i<55;i++){const hx=randV133(world.id,i,'texturex')*W,hy=randV133(world.id,i,'texturey')*H,rr=8+randV133(world.id,i,'texturer')*34;x.fillStyle=i%3===0?'rgba(255,255,255,.010)':'rgba(0,0,0,.025)';x.beginPath();x.arc(hx,hy,rr,0,Math.PI*2);x.fill()}x.restore();
 STATIC_BACKDROP_CACHE_V193.set(key,c);if(STATIC_BACKDROP_CACHE_V193.size>24)STATIC_BACKDROP_CACHE_V193.delete(STATIC_BACKDROP_CACHE_V193.keys().next().value);return c
}
window.staticBackdropV193=staticBackdropV193;

const STATIC_VIGNETTE_CACHE_V195=new Map();
function staticVignetteV195(W,H){
 const dpr=Math.max(1,window.devicePixelRatio||1),key=`${W}|${H}|${dpr}`;
 let c=STATIC_VIGNETTE_CACHE_V195.get(key);if(c)return c;
 c=document.createElement('canvas');c.width=Math.max(1,Math.round(W*dpr));c.height=Math.max(1,Math.round(H*dpr));
 const x=c.getContext('2d');x.setTransform(dpr,0,0,dpr,0,0);
 const vig=x.createRadialGradient(W/2,H/2,0,W/2,H/2,Math.max(W,H)*.82);vig.addColorStop(0,'transparent');vig.addColorStop(.72,'transparent');vig.addColorStop(1,'rgba(0,0,0,.52)');x.fillStyle=vig;x.fillRect(0,0,W,H);
 STATIC_VIGNETTE_CACHE_V195.set(key,c);if(STATIC_VIGNETTE_CACHE_V195.size>8)STATIC_VIGNETTE_CACHE_V195.delete(STATIC_VIGNETTE_CACHE_V195.keys().next().value);return c
}
window.staticVignetteV195=staticVignetteV195;

function renderDistrictStaticV133(){
 const world=currentDistrictV133();if(!Game.ovCanvas||!Game.ovStaticCtx||!world)return;
 const b=visibleBoundsV133(world),ctx=Game.ovStaticCtx,t=Game.ovTile,W=b.W,H=b.H;
 ctx.clearRect(0,0,W,H);
 ctx.drawImage(staticBackdropV193(world,W,H),0,0,W,H);
 // The navigation grid stays invisible. Dense anonymous parcels merge into continuous city blocks.
 drawAnonymousUrbanFabricV133(ctx,world,b);
 drawUrbanDepthV163(ctx,world,b);
 drawEnvironmentRegionsV133(ctx,world,b);
 // Sparse special surfaces that genuinely need cell precision.
 for(let y=b.y0;y<b.y1;y++)for(let x=b.x0;x<b.x1;x++){const v=terrainAt133(world,x,y);if(v!==T.PLAZA&&v!==T.YARD&&v!==T.INDUSTRIAL&&v!==T.BRIDGE&&v!==T.TUNNEL)continue;const p=worldToScreenV133(x,y);let col='rgba(29,34,37,.30)';if(v===T.PLAZA)col='rgba(65,67,65,.22)';else if(v===T.YARD||v===T.INDUSTRIAL)col='rgba(45,39,31,.18)';else if(v===T.BRIDGE)col='rgba(53,65,71,.42)';else if(v===T.TUNNEL)col='rgba(19,23,40,.40)';ctx.fillStyle=col;ctx.fillRect(p.x,p.y,t+1,t+1)}
 drawRoadCurvesV133(ctx,world,b);
 drawGrittyStreetFabricV141(ctx,world,b);
 drawMunicipalWearV170(ctx,world,b);
 drawStreetMicroDetailsV162(ctx,world,b);
 for(const build of world.buildings){if(build.x+build.w<b.x0||build.y+build.h<b.y0||build.x>b.x1||build.y>b.y1)continue;drawBuildingFootprintV133(ctx,build,world)}
 drawDistrictPropsV133(ctx,world,b);
 drawStreetLightingV163(ctx,world,b);
 drawSiteForecourtsV163(ctx,world,b);
 drawSiteCanopiesV163(ctx,world,b);
 drawDistrictLandmarkVisualsV162(ctx,world,b);
 window.CR14UrbanIdentity?.drawStatic?.(ctx,world,b);
 drawDistrictDetailV136(ctx,world,b);
 // neighborhood identity labels
 for(const n of world.neighborhoods){const p=worldToScreenV133(n.x,n.y);if(p.x<-100||p.y<-40||p.x>W+100||p.y>H+40)continue;ctx.save();ctx.font=`800 ${Math.max(7,Math.min(12,t*.24))}px Orbitron`;ctx.textAlign='center';ctx.fillStyle=world.cfg.accent+'38';ctx.fillText(n.name.toUpperCase(),p.x,p.y);ctx.restore()}
 ctx.drawImage(staticVignetteV195(W,H),0,0,W,H);
 Game.ovStaticDirty=false;Game._v133StaticKey=`${world.id}|${Game.ovCamera.x.toFixed(3)}|${Game.ovCamera.y.toFixed(3)}|${t.toFixed(2)}|${W}|${H}`
}
window.renderDistrictStaticV133=renderDistrictStaticV133;window.renderOverworldStatic=renderDistrictStaticV133;

function shopSemanticV136(l){
 if(l?.type==='clinic')return'clinic';
 const shop=(window.V13_SHOPS||[]).find(s=>s.id===l?.shop),txt=`${shop?.name||l?.name||''} ${shop?.specialty||l?.desc||''}`.toLowerCase(),stock=(shop?.stock||[]).join(' ').toLowerCase();
 // Broad-purpose dealers keep a MARKET identity even if a few guns, armor or electronics are mixed into stock.
 if(/general mercenary supplies|pharmacy|medical supplies|salvage|contraband|general supplies|street supplies|scaveng|trade stall/.test(txt))return'market';
 // Explicit dealer identity wins over secondary stock.
 if(/arms|armory|weapon|ammo|gun|rifle|pistol|firearm|arsenal/.test(txt))return'weapons';
 if(/armor|outfit|protect|riot|aegis/.test(txt))return'armor';
 if(/data|sensor|optic|matrix|exploit|electronics/.test(txt))return'data';
 // Stock is only the fallback when the dealer's declared specialty is ambiguous.
 if(/(kestrel_|helix_|mako_|redline_|sable_|atlas_)/.test(stock))return'weapons';
 if(/armor_/.test(stock))return'armor';
 if(/optic|sensor|emp/.test(stock))return'data';
 return'market'
}
window.shopSemanticV136=shopSemanticV136;
function semanticMarkerV136(kind,l=null){
 if(kind==='safehouse')return{...CRArtV136.semantic.safehouse,type:'safehouse',text:'HQ'};
 if(kind==='transit'){const links=(l?.linkIds||[]).map(id=>V133_TRANSIT_LINKS.find(x=>x.id===id)).filter(Boolean),types=[...new Set(links.map(x=>x.type))],type=types.includes('metro')?'metro':types.includes('security')?'security':types.includes('freight')?'freight':types.includes('hidden')?'route':'district';return{...CRArtV136.semantic[type],type,text:type==='metro'?'M':type==='freight'?'F':type==='security'?'S':type==='route'?'?':'G'}}
 if(l?.contact){const c=contactDef133(l.contact),color=FACTIONS?.[c?.faction]?.color||CRArtV136.semantic.contact.color,parts=(c?.name||l.name||'?').split(/\s+/);return{...CRArtV136.semantic.contact,color,type:'contact',text:(parts[0][0]+(parts[1]?.[0]||parts[0][1]||'')).toUpperCase(),contact:c}}
 if(l?.type==='clinic')return{...CRArtV136.semantic.clinic,type:'clinic',text:'+'};
 if(l?.type==='shop'){const type=shopSemanticV136(l);return{...CRArtV136.semantic[type],type,text:type==='weapons'?'W':type==='armor'?'A':type==='data'?'D':'$'}}
 if(l?.type==='hidden')return{...CRArtV136.semantic.hidden,type:'hidden',text:'?'};
 return{...CRArtV136.semantic.landmark,type:'landmark',text:'◇'}
}
window.semanticMarkerV136=semanticMarkerV136;
function markerStyle133(kind,l=null){return semanticMarkerV136(kind,l)}
function drawSemanticGlyphV136(ctx,style,r){
 const c=style.color,type=style.type||style.shape;ctx.strokeStyle=c;ctx.fillStyle=c;ctx.lineWidth=Math.max(1,Math.min(2,r*.18));ctx.lineCap='round';ctx.lineJoin='round';
 if(type==='contact'){ctx.beginPath();ctx.arc(0,0,r*.72,0,Math.PI*2);ctx.stroke();ctx.beginPath();ctx.arc(0,-r*.18,r*.22,0,Math.PI*2);ctx.stroke();ctx.beginPath();ctx.moveTo(-r*.38,r*.38);ctx.quadraticCurveTo(0,r*.08,r*.38,r*.38);ctx.stroke()}
 else if(type==='weapons'){ctx.beginPath();ctx.moveTo(-r*.62,-r*.18);ctx.lineTo(r*.48,-r*.18);ctx.lineTo(r*.72,0);ctx.lineTo(r*.14,r*.12);ctx.lineTo(r*.02,r*.52);ctx.lineTo(-r*.25,r*.50);ctx.lineTo(-r*.18,r*.12);ctx.lineTo(-r*.62,r*.10);ctx.closePath();ctx.stroke()}
 else if(type==='armor'){ctx.beginPath();ctx.moveTo(0,-r*.68);ctx.lineTo(r*.55,-r*.42);ctx.lineTo(r*.45,r*.26);ctx.lineTo(0,r*.68);ctx.lineTo(-r*.45,r*.26);ctx.lineTo(-r*.55,-r*.42);ctx.closePath();ctx.stroke()}
 else if(type==='clinic'){ctx.fillRect(-r*.16,-r*.62,r*.32,r*1.24);ctx.fillRect(-r*.62,-r*.16,r*1.24,r*.32)}
 else if(type==='data'){ctx.beginPath();ctx.arc(0,0,r*.2,0,Math.PI*2);ctx.stroke();for(let i=0;i<4;i++){const a=i*Math.PI/2,ex=Math.cos(a)*r*.62,ey=Math.sin(a)*r*.62;ctx.beginPath();ctx.moveTo(Math.cos(a)*r*.2,Math.sin(a)*r*.2);ctx.lineTo(ex,ey);ctx.stroke();ctx.beginPath();ctx.arc(ex,ey,r*.12,0,Math.PI*2);ctx.fill()}}
 else if(type==='market'){ctx.strokeRect(-r*.55,-r*.35,r*1.1,r*.75);ctx.beginPath();ctx.moveTo(-r*.68,-r*.35);ctx.lineTo(-r*.45,-r*.65);ctx.lineTo(r*.45,-r*.65);ctx.lineTo(r*.68,-r*.35);ctx.stroke()}
 else if(type==='safehouse'){ctx.beginPath();ctx.moveTo(0,-r*.7);ctx.lineTo(r*.62,-r*.38);ctx.lineTo(r*.5,r*.35);ctx.lineTo(0,r*.7);ctx.lineTo(-r*.5,r*.35);ctx.lineTo(-r*.62,-r*.38);ctx.closePath();ctx.stroke();ctx.font=`900 ${Math.max(6,r*.58)}px Orbitron`;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('HQ',0,1)}
 else if(type==='metro'){ctx.strokeRect(-r*.58,-r*.58,r*1.16,r*1.16);ctx.font=`900 ${Math.max(7,r*.85)}px Orbitron`;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('M',0,1)}
 else if(type==='security'){ctx.beginPath();ctx.moveTo(0,-r*.68);ctx.lineTo(r*.56,-r*.42);ctx.lineTo(r*.42,r*.38);ctx.lineTo(0,r*.68);ctx.lineTo(-r*.42,r*.38);ctx.lineTo(-r*.56,-r*.42);ctx.closePath();ctx.stroke();ctx.beginPath();ctx.moveTo(-r*.28,0);ctx.lineTo(r*.28,0);ctx.stroke()}
 else if(type==='freight'){ctx.strokeRect(-r*.65,-r*.4,r*1.15,r*.68);ctx.beginPath();ctx.moveTo(r*.5,-r*.15);ctx.lineTo(r*.72,r*.05);ctx.lineTo(r*.72,r*.28);ctx.lineTo(r*.48,r*.28);ctx.stroke();ctx.beginPath();ctx.arc(-r*.3,r*.35,r*.13,0,Math.PI*2);ctx.arc(r*.4,r*.35,r*.13,0,Math.PI*2);ctx.stroke()}
 else if(type==='route'||type==='hidden'){ctx.beginPath();ctx.arc(0,0,r*.58,Math.PI*.12,Math.PI*1.55);ctx.stroke();ctx.beginPath();ctx.moveTo(-r*.18,-r*.12);ctx.quadraticCurveTo(0,-r*.48,r*.25,-r*.22);ctx.quadraticCurveTo(r*.45,0,r*.08,r*.25);ctx.stroke();ctx.beginPath();ctx.arc(0,r*.48,r*.06,0,Math.PI*2);ctx.fill()}
 else{ctx.beginPath();ctx.moveTo(0,-r*.65);ctx.lineTo(r*.65,0);ctx.lineTo(0,r*.65);ctx.lineTo(-r*.65,0);ctx.closePath();ctx.stroke();ctx.beginPath();ctx.arc(0,0,r*.13,0,Math.PI*2);ctx.fill()}
}
window.drawSemanticGlyphV136=drawSemanticGlyphV136;
const MARKER_TEXT_METRICS_V133=new Map();
function cachedMarkerTextWidthV133(ctx,text){const key=ctx.font+'\n'+text;let w=MARKER_TEXT_METRICS_V133.get(key);if(w===undefined){w=ctx.measureText(text).width;MARKER_TEXT_METRICS_V133.set(key,w)}return w}
function drawMarker133(ctx,x,y,label,style,hover=false){
 const p=worldToScreenV133(x+.5,y+.5),t=Game.ovTile,r=Math.max(9,Math.min(15,t*.34))+(hover?2.5:0);ctx.save();ctx.translate(p.x,p.y);ctx.shadowColor=style.color;ctx.shadowBlur=hover?24:14;ctx.fillStyle='rgba(3,8,12,.94)';ctx.strokeStyle=style.color;ctx.lineWidth=1.4;ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.globalAlpha=.28;ctx.lineWidth=2;ctx.beginPath();ctx.arc(0,0,r+4,0,Math.PI*2);ctx.stroke();ctx.globalAlpha=1;ctx.shadowBlur=0;drawSemanticGlyphV136(ctx,style,r*.88);
 if(['contact','weapons','armor','clinic','data','market'].includes(style.type)&&t>=20){const badge=style.type==='contact'?(style.text||'CT'):style.type==='weapons'?'ARMS':style.type==='armor'?'ARM':style.type==='clinic'?'MED':style.type==='data'?'DATA':'SHOP';ctx.font=`800 ${Math.max(5.5,r*.38)}px Orbitron`;ctx.textAlign='center';ctx.textBaseline='middle';const bw=Math.max(r*1.55,cachedMarkerTextWidthV133(ctx,badge)+7);ctx.fillStyle='rgba(2,6,9,.9)';ctx.fillRect(-bw/2,r*.58,bw,Math.max(8,r*.62));ctx.strokeStyle=style.color;ctx.strokeRect(-bw/2+.5,r*.58+.5,bw-1,Math.max(8,r*.62)-1);ctx.fillStyle=style.color;ctx.fillText(badge,0,r*.89)}
 if(t>=24||hover){ctx.font=`700 ${Math.max(7,Math.min(10,t*.22))}px Share Tech Mono`;ctx.textAlign='center';ctx.textBaseline='alphabetic';const w=cachedMarkerTextWidthV133(ctx,label);ctx.fillStyle='rgba(1,4,8,.88)';ctx.fillRect(-w/2-6,r+6,w+12,15);ctx.fillStyle=style.color;ctx.fillText(label,0,r+17)}ctx.restore()
}

function transitVisible133(tr){
 const link=V133_TRANSIT_LINKS.find(l=>tr.linkIds.includes(l.id));if(!link)return true;return link.type!=='hidden'||Game.districtWorldsV133.hiddenLinks[link.id]
}
const MARKER_MODEL_CACHE_V133=new Map();
function markerStateKeyV133(world){
 // Marker geometry is immutable for a generated district. Only discovery and
 // hidden-route visibility can change which marker models belong in the frame.
 // Keep the signature primitive so active camera/movement frames avoid rebuilding
 // labels/styles and repeating contact/shop/transit lookups when state is stable.
 let key=world.id;
 for(const id of Object.keys(world.locations))key+=locationKnownV133(id)?'|1':'|0';
 for(const tr of world.transit)key+=transitVisible133(tr)?'|1':'|0';
 return key
}
function allMarkersV133(world){
 const key=markerStateKeyV133(world),cached=MARKER_MODEL_CACHE_V133.get(world.id);
 if(cached?.key===key)return cached.markers;
 const a=[];for(const[id,p]of Object.entries(world.locations)){if(locationKnownV133(id)){const l=locationDisplayV133(id),kind=id==='v133_safehouse'?'safehouse':'location';a.push({kind,id,x:p.x,y:p.y,label:l?.name||id,def:l,style:markerStyle133(kind,l)})}}
 for(const tr of world.transit)if(transitVisible133(tr))a.push({kind:'transit',id:tr.id,x:tr.x,y:tr.y,label:transitLabelV133(tr),def:tr,style:markerStyle133('transit',tr)});
 MARKER_MODEL_CACHE_V133.set(world.id,{key,markers:a});return a
}
function transitLabelV133(tr){const links=tr.linkIds.map(id=>V133_TRANSIT_LINKS.find(x=>x.id===id)).filter(Boolean);const types=[...new Set(links.map(x=>x.type))];return types.includes('metro')?'METRO':types.includes('security')?'SECURITY GATE':types.includes('freight')?'FREIGHT':types.includes('hidden')?'HIDDEN ROUTE':'DISTRICT GATE'}
function markerAtV133(world,x,y){return allMarkersV133(world).find(m=>Math.hypot(m.x-x,m.y-y)<=1.1)||null}

function drawMinimapV133(ctx,W,H,world,frameRect,markers){
 const mobile=W<700,mw=mobile?Math.min(126,W*.31):182,mh=mw*world.h/world.w,x=W-mw-11,y=11;
 Game._v133MiniRect={x,y,w:mw,h:mh};ctx.save();ctx.fillStyle='rgba(3,8,13,.92)';ctx.fillRect(x-4,y-4,mw+8,mh+18);ctx.strokeStyle=world.cfg.accent+'66';ctx.strokeRect(x-4.5,y-4.5,mw+9,mh+9);ctx.drawImage(world.minimapCanvas,x,y,mw,mh);
 const sx=mw/world.w,sy=mh/world.h;for(const m of (markers||allMarkersV133(world))){const st=m.style||semanticMarkerV136(m.kind,m.def),mx=x+m.x*sx,my=y+m.y*sy,rr=st.type==='contact'?3.8:3.15;ctx.save();ctx.translate(mx,my);ctx.strokeStyle=st.color;ctx.fillStyle=st.color;ctx.lineWidth=1;
 if(st.type==='clinic'){ctx.fillRect(-.7,-rr,1.4,rr*2);ctx.fillRect(-rr,-.7,rr*2,1.4)}
 else if(st.type==='contact'){ctx.beginPath();ctx.arc(0,0,rr,0,Math.PI*2);ctx.stroke();ctx.beginPath();ctx.arc(0,0,.8,0,Math.PI*2);ctx.fill()}
 else if(st.type==='weapons'){ctx.beginPath();ctx.moveTo(-rr,1);ctx.lineTo(rr,-1);ctx.stroke();ctx.fillRect(-rr,-1,rr*1.3,1.6)}
 else if(st.type==='metro'){ctx.strokeRect(-rr,-rr,rr*2,rr*2);ctx.fillRect(-.6,-rr+1,1.2,rr*2-2)}
 else if(st.type==='security'||st.type==='armor'){ctx.beginPath();ctx.moveTo(0,-rr);ctx.lineTo(rr,0);ctx.lineTo(0,rr);ctx.lineTo(-rr,0);ctx.closePath();ctx.stroke()}
 else if(st.type==='data'){ctx.beginPath();ctx.arc(0,0,rr,0,Math.PI*2);ctx.stroke();ctx.fillRect(-.7,-.7,1.4,1.4)}
 else{ctx.fillRect(-rr/2,-rr/2,rr,rr)}ctx.restore()}
 ctx.fillStyle='#fff';ctx.shadowColor=world.cfg.accent;ctx.shadowBlur=7;ctx.fillRect(x+Game.ovPlayer.x*sx-2,y+Game.ovPlayer.y*sy-2,4,4);ctx.shadowBlur=0;
 const wrap=frameRect||document.querySelector('#overworld-screen .wrap').getBoundingClientRect(),vw=wrap.width/Game.ovTile*sx,vh=wrap.height/Game.ovTile*sy;ctx.strokeStyle=world.cfg.accent;ctx.setLineDash([4,3]);ctx.strokeRect(x+Game.ovCamera.x*sx,y+Game.ovCamera.y*sy,vw,vh);ctx.setLineDash([]);
 ctx.fillStyle='#6f8995';ctx.font='700 6px Orbitron';ctx.fillText(`${world.cfg.name.toUpperCase()} // ${world.w}×${world.h}`,x,y+mh+11);ctx.restore()
}

function drawDistrictDynamicV133(frameRect){
 const world=currentDistrictV133(),ctx=Game.ovCtx,r=frameRect||document.querySelector('#overworld-screen .wrap').getBoundingClientRect(),W=r.width,H=r.height,t=Game.ovTile;ctx.clearRect(0,0,W,H);if(Game.ovStaticCanvas)ctx.drawImage(Game.ovStaticCanvas,0,0,W,H);
 const now=(((Game.day||1)-1)*24+(Game.hour||0))*6;
 // Atmosphere by district
 ctx.save();if(['neon_row','floodline','dock_nine'].includes(world.id)){ctx.strokeStyle=world.id==='neon_row'?'rgba(230,90,240,.08)':'rgba(100,170,220,.10)';for(let i=0;i<20;i++){const x=(i*137+now*70)%W,y=(i*83+now*190)%H;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x-2,y+7);ctx.stroke()}}else if(['ash_blocks','forge_belt'].includes(world.id)){for(let i=0;i<9;i++){const x=(i*173+now*12)%W,y=H-((i*91+now*28)%H);ctx.fillStyle='rgba(215,101,40,.08)';ctx.beginPath();ctx.arc(x,y,4+(i%3)*2,0,Math.PI*2);ctx.fill()}}ctx.restore();
 if(Game.pendingPath?.length){ctx.save();ctx.strokeStyle='rgba(67,215,232,.57)';ctx.lineWidth=2;ctx.setLineDash([5,5]);ctx.beginPath();Game.pendingPath.forEach((q,i)=>{const p=worldToScreenV133(q.x+.5,q.y+.5);i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y)});ctx.stroke();ctx.setLineDash([]);Game.pendingPath.forEach((q,i)=>{if(!i)return;const p=worldToScreenV133(q.x+.5,q.y+.5),last=i===Game.pendingPath.length-1;if(!last&&(p.x<-4||p.y<-4||p.x>W+4||p.y>H+4))return;ctx.fillStyle=last?'#e4ad4c':'rgba(67,215,232,.75)';ctx.beginPath();ctx.arc(p.x,p.y,last?3.5:1.8,0,Math.PI*2);ctx.fill()});ctx.restore()}
 const hover=Game.hoverTile,markers=allMarkersV133(world);for(const m of markers){const p=worldToScreenV133(m.x,m.y);if(p.x<-40||p.y<-40||p.x>W+40||p.y>H+40)continue;drawMarker133(ctx,m.x,m.y,m.label,m.style||markerStyle133(m.kind,m.def),hover&&Math.hypot(hover.x-m.x,hover.y-m.y)<=1)}
 const pp=worldToScreenV133(Game.ovPlayer.x+.5,Game.ovPlayer.y+.5),pulse=.5+Math.sin(now*5)*.5;ctx.save();ctx.shadowColor=world.cfg.accent;ctx.shadowBlur=14+pulse*8;ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(pp.x,pp.y,Math.max(5,t*.18)+pulse,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;ctx.strokeStyle=world.cfg.accent;ctx.lineWidth=2;ctx.beginPath();ctx.arc(pp.x,pp.y,Math.max(8,t*.27)+pulse*2,0,Math.PI*2);ctx.stroke();ctx.restore();
 if(hover&&pointInBounds133(world,hover.x,hover.y)){const p=worldToScreenV133(hover.x,hover.y);ctx.strokeStyle=isWalkableV133(hover.x,hover.y)?'#d8f7ff':'#d95c5c';ctx.strokeRect(p.x+1,p.y+1,t-2,t-2)}
 window.drawLivingStreetsV134?.(ctx,world,W,H,t,hover);
 window.drawLocationSitesV14?.(ctx,world,W,H,t,hover);
 drawMinimapV133(ctx,W,H,world,r,markers)
}

function frameRectV133(){
 const cached=Game._v133FrameRect;if(cached?.width>0&&cached?.height>0)return cached;
 const wrap=document.querySelector('#overworld-screen .wrap');return cacheOverworldFrameRectV133(wrap)
}
function ensureCameraV133(){
 const world=currentDistrictV133(),r=frameRectV133()||{width:Game.ovCanvas?.clientWidth||0,height:Game.ovCanvas?.clientHeight||0},mobile=r.width<700,state=ensureDistrictWorldStateV133(),saved=state.cameraByDistrict[world.id];
 if(!Game.ovCamera||Game.ovCamera.districtId!==world.id)Game.ovCamera={districtId:world.id,x:saved?.x||0,y:saved?.y||0,tx:saved?.x||0,ty:saved?.y||0,tile:saved?.tile||(mobile?28:36),follow:saved?.follow!==false};
 Game.ovTile=Game.ovCamera.tile;clampCameraV133(r);return Game.ovCamera
}
function clampCameraV133(frameRect=null){
 const world=currentDistrictV133();if(!Game.ovCamera)return;const r=frameRect||frameRectV133();if(!r)return;const vx=r.width/Game.ovTile,vy=r.height/Game.ovTile,maxX=Math.max(0,world.w-vx),maxY=Math.max(0,world.h-vy);
 for(const k of ['x','tx'])Game.ovCamera[k]=clamp133(Number.isFinite(Game.ovCamera[k])?Game.ovCamera[k]:0,0,maxX);
 for(const k of ['y','ty'])Game.ovCamera[k]=clamp133(Number.isFinite(Game.ovCamera[k])?Game.ovCamera[k]:0,0,maxY)
}
function centerCameraV133(instant=false){
 ensureCameraV133();const r=frameRectV133();if(!r)return;const vx=r.width/Game.ovTile,vy=r.height/Game.ovTile;Game.ovCamera.tx=Game.ovPlayer.x-vx/2+.5;Game.ovCamera.ty=Game.ovPlayer.y-vy/2+.5;Game.ovCamera.follow=true;clampCameraV133(r);if(instant){Game.ovCamera.x=Game.ovCamera.tx;Game.ovCamera.y=Game.ovCamera.ty;Game.ovStaticDirty=true}updateCameraModeV133()
}
function zoomAtV133(factor,sx=null,sy=null){
 scheduleOverworldFrameV133(0);ensureCameraV133();const r=frameRectV133();if(!r)return;const mobile=r.width<700,min=mobile?18:20,max=mobile?48:58,old=Game.ovTile,nw=clamp133(old*factor,min,max);if(Math.abs(nw-old)<.05)return;if(sx==null){sx=r.width/2;sy=r.height/2}const wx=Game.ovCamera.x+sx/old,wy=Game.ovCamera.y+sy/old;Game.ovTile=Game.ovCamera.tile=nw;Game.ovCamera.x=Game.ovCamera.tx=wx-sx/nw;Game.ovCamera.y=Game.ovCamera.ty=wy-sy/nw;Game.ovCamera.follow=false;clampCameraV133(r);Game.ovStaticDirty=true;updateCameraModeV133()
}
window.centerCameraV133=centerCameraV133;window.zoomAtV133=zoomAtV133;

function cacheOverworldFrameRectV133(wrap,rect=null){
 if(!wrap)return Game._v133FrameRect||null;const r=rect||wrap.getBoundingClientRect();const width=r.width||wrap.clientWidth||0,height=r.height||wrap.clientHeight||0;if(width>0&&height>0)Game._v133FrameRect={width,height};return Game._v133FrameRect
}
function ensureOverworldFrameObserverV133(wrap){
 if(!wrap||Game._v133FrameObserver||typeof ResizeObserver==='undefined')return;Game._v133FrameObserver=new ResizeObserver(entries=>{const box=entries[0]?.contentRect;if(!box)return;const prev=Game._v133FrameRect;Game._v133FrameRect={width:box.width,height:box.height};if(!prev||Math.abs(prev.width-box.width)>.5||Math.abs(prev.height-box.height)>.5){Game.ovStaticDirty=true;if(Game.screen==='overworld-screen'&&!document.hidden)scheduleOverworldFrameV133(0)}});Game._v133FrameObserver.observe(wrap)
}
function resizeOverworldV133(){
 const wrap=document.querySelector('#overworld-screen .wrap');if(!wrap||!Game.ovCanvas)return;const r=cacheOverworldFrameRectV133(wrap),dpr=Math.min(window.devicePixelRatio||1,2);ensureOverworldFrameObserverV133(wrap);Game.ovCanvas.width=Math.round(r.width*dpr);Game.ovCanvas.height=Math.round(r.height*dpr);Game.ovCanvas.style.width=r.width+'px';Game.ovCanvas.style.height=r.height+'px';Game.ovCanvas.style.transform='none';Game.ovCtx.setTransform(dpr,0,0,dpr,0,0);
 if(!Game.ovStaticCanvas)Game.ovStaticCanvas=document.createElement('canvas');Game.ovStaticCanvas.width=Game.ovCanvas.width;Game.ovStaticCanvas.height=Game.ovCanvas.height;Game.ovStaticCtx=Game.ovStaticCanvas.getContext('2d');Game.ovStaticCtx.setTransform(dpr,0,0,dpr,0,0);ensureCameraV133();clampCameraV133();Game.ovStaticDirty=true
}
window.resizeOverworld=resizeOverworldV133;

function ensureV133UI(){
 const app=document.getElementById('app'),wrap=document.querySelector('#overworld-screen .wrap');if(!app||!wrap)return;
 if(!document.getElementById('v133-district-badge')){const e=document.createElement('div');e.id='v133-district-badge';wrap.appendChild(e)}
 if(!document.getElementById('v133-map-controls')){const e=document.createElement('div');e.id='v133-map-controls';e.innerHTML=`<button class="btn small" id="v133-zoom-out">−</button><button class="btn small" id="v133-zoom-in">＋</button><button class="btn small wide" id="v133-follow">FOLLOW</button><button class="btn small wide" id="v133-city-map">CITY</button><button class="btn small wide" id="v133-dossier">INFO</button>`;wrap.appendChild(e);
   document.getElementById('v133-zoom-out').onclick=()=>zoomAtV133(.82);document.getElementById('v133-zoom-in').onclick=()=>zoomAtV133(1.22);document.getElementById('v133-follow').onclick=()=>centerCameraV133(false);document.getElementById('v133-city-map').onclick=()=>openStrategicCityMapV133();document.getElementById('v133-dossier').onclick=()=>openCityLifeV13()}
 if(!document.getElementById('v133-camera-mode')){const e=document.createElement('div');e.id='v133-camera-mode';wrap.appendChild(e)}
 if(!document.getElementById('v133-route-card')){const e=document.createElement('div');e.id='v133-route-card';wrap.appendChild(e)}
 if(!document.getElementById('v133-transit-modal')){const e=document.createElement('div');e.id='v133-transit-modal';e.innerHTML='<div class="v133-transit-box" id="v133-transit-box"></div>';wrap.appendChild(e)}
 if(!document.getElementById('v133-strategic-city-screen')){const e=document.createElement('div');e.id='v133-strategic-city-screen';e.className='screen';e.innerHTML=`<div class="v13-screenhead"><div><div class="v13-title">CHROME CITY // TRANSIT INTELLIGENCE</div><div class="v13-sub">DISTRICTS · ACCESS · CONTROL · ROUTES</div></div><div class="spacer"></div><button class="btn small" id="v133-strategic-back">◀ DISTRICT</button></div><div class="v133-strategic-shell"><div id="v133-strategic-map"></div><div class="v133-strategic-info" id="v133-strategic-info"></div></div>`;app.appendChild(e);document.getElementById('v133-strategic-back').onclick=()=>{showScreen('overworld-screen');initOverworldV133()}}
 updateCameraModeV133()
}
function updateCameraModeV133(){const e=document.getElementById('v133-camera-mode');if(e)e.innerHTML=`CAMERA <b>${Game.ovCamera?.follow!==false?'FOLLOW':'FREE'}</b> · ${Math.round(Game.ovTile||0)}PX`}
function updateRouteCardV133(){
 const e=document.getElementById('v133-route-card');if(!e)return;if(!Game.pendingPath?.length){e.style.display='none';return}e.style.display='block';const t=Game._v133TravelTarget;e.innerHTML=`<b>ACTIVE ROUTE</b>${t?.label||'Street route'} · ${Math.max(0,Game.pendingPath.length-1)} blocks remaining`
}

function openDistrictLocationV133(id){
 if(id==='v133_safehouse'){openSafehouse();return true}const l=locDef133(id);if(!l)return false;Game.cityLife.currentLocation=id;Game.cityLife.currentDistrict=currentDistrictV133().id;
 if(l.contact){window.renderContactDossierV13?.(l.contact);showScreen('v13-contact-screen')}
 else if(l.shop){const s=shopDef133(l.shop);if(s?.type==='clinic'){window.renderClinicV13?.(s.id);showScreen('v13-clinic-screen')}else{window.renderMarketV13?.(s.id);showScreen('v13-market-screen')}}
 else{window.renderDistrictHubV13?.(currentDistrictV133().id);showScreen('v13-city-life-screen')}
 return true
}
function routeToPointV133(p,target=null){
 const world=currentDistrictV133(),path=findDistrictPathV133(Game.ovPlayer,p,world);if(!path||path.length<2){if(path?.length===1&&target?.kind==='location')openDistrictLocationV133(target.id);else if(path?.length===1&&target?.kind==='transit')openTransitNodeV133(target.id);else toast('No route.');return false}
 Game.pendingPath=path;Game._v133TravelTarget=target;Game.ovCamera.follow=true;scheduleOverworldFrameV133(0);if(path.length>60&&Math.random()<.18)Game.storyFlags._pendingTravelEvent=path.length;updateRouteCardV133();updateCameraModeV133();return true
}
function routeToLocationV133(id){const p=currentDistrictV133().locations[id];if(!p)return false;const l=locationDisplayV133(id);return routeToPointV133(p,{kind:'location',id,label:l?.name||id})}
function routeToTransitNodeV133(id){const tr=currentDistrictV133().transit.find(x=>x.id===id);if(!tr)return false;return routeToPointV133(tr,{kind:'transit',id,label:transitLabelV133(tr)})}
window.routeToLocationV133=routeToLocationV133;window.routeToTransitNodeV133=routeToTransitNodeV133;

function accessForLinkV133(link){
 ensureDistrictWorldStateV133();if(link.type==='hidden'&&!Game.districtWorldsV133.hiddenLinks[link.id])return{allowed:false,reason:'Route not discovered.'};
 if(link.type==='security'){
   const rep=Game.rep?.[link.faction]||0,n=Game.notoriety||0;if(n<58||rep>=25)return{allowed:true,mode:'clear'};
   const bribe=Math.round(600+n*16),hacker=Game.roster?.some(u=>u.className==='Hacker'||u.className==='AgentEX');return{allowed:false,reason:`Checkpoint flags your crew. Notoriety ${n}; ${FACTIONS?.[link.faction]?.short||link.faction} rep ${rep}.`,bribe,hack:hacker}
 }
 if(link.type==='metro'&&(Game.notoriety||0)>=90)return{allowed:false,reason:'City transit has your crew on an active security watchlist.',bribe:850};
 return{allowed:true,mode:'clear'}
}
function canUseTransitV133(node){const tr=typeof node==='string'?currentDistrictV133().transit.find(x=>x.id===node):node;if(!tr)return false;return tr.linkIds.some(id=>accessForLinkV133(V133_TRANSIT_LINKS.find(x=>x.id===id)).allowed)}
window.canUseTransitV133=canUseTransitV133;

function travelDistrictV133(linkId,mode='clear'){
 const link=V133_TRANSIT_LINKS.find(x=>x.id===linkId);if(!link)return false;const current=currentDistrictV133().id,ep=endpointForV133(link,current),to=otherEndpointV133(link,current);if(!ep||!to)return false;
 const access=accessForLinkV133(link);let cost=link.cost||0;if(!access.allowed){if(mode==='bribe'&&access.bribe){cost+=access.bribe}else if(mode==='hack'&&access.hack){addNotorietyV12?.(3,'checkpoint intrusion')}else{toast(access.reason||'Access denied.');return false}}
 if(Game.credits<cost){toast('Not enough credits.');return false}Game.credits-=cost;advanceTime(link.minutes||12);Game.districtWorldsV133.unlockedLinks[link.id]=true;activateDistrictV133(to.district,to.node);showScreen('overworld-screen');initOverworldV133();toast(`${V133_DISTRICTS[current].name} → ${V133_DISTRICTS[to.district].name}`);saveGame(0,true);return true
}
window.travelDistrictV133=travelDistrictV133;

function renderTransitModalV133(tr){
 const box=document.getElementById('v133-transit-box'),modal=document.getElementById('v133-transit-modal');if(!box||!modal)return;const world=currentDistrictV133(),links=tr.linkIds.map(id=>V133_TRANSIT_LINKS.find(x=>x.id===id)).filter(Boolean).filter(l=>l.type!=='hidden'||Game.districtWorldsV133.hiddenLinks[l.id]);
 const type=transitLabelV133(tr);box.style.setProperty('--accent',world.cfg.accent);box.innerHTML=`<h2>${type}</h2><div class="sub">${world.cfg.name} // ${tr.id.replaceAll('_',' ').toUpperCase()}</div>${links.map(l=>{const other=otherEndpointV133(l,world.id),a=accessForLinkV133(l);return`<div class="v133-transit-choice"><b>${l.name}</b><small>${V133_DISTRICTS[other.district].name} · ${l.type.toUpperCase()} · ${l.minutes||12} MIN${l.cost?` · ¢${l.cost}`:''}<br>${a.allowed?'ACCESS AVAILABLE':a.reason}</small><div class="v133-transit-actions">${a.allowed?`<button class="btn small" data-link="${l.id}" data-mode="clear">TRAVEL</button>`:''}${!a.allowed&&a.bribe?`<button class="btn small" data-link="${l.id}" data-mode="bribe">BRIBE ¢${a.bribe}</button>`:''}${!a.allowed&&a.hack?`<button class="btn small" data-link="${l.id}" data-mode="hack">HACK GATE</button>`:''}</div></div>`}).join('')}<div class="v133-transit-actions"><button class="btn small" id="v133-transit-close">CANCEL</button></div>`;
 box.querySelectorAll('[data-link]').forEach(b=>b.onclick=()=>{modal.classList.remove('open');travelDistrictV133(b.dataset.link,b.dataset.mode)});box.querySelector('#v133-transit-close').onclick=()=>modal.classList.remove('open');modal.classList.add('open')
}
window.renderTransitModalV133=renderTransitModalV133;
function openTransitNodeV133(id){const tr=currentDistrictV133().transit.find(x=>x.id===id);if(!tr)return false;renderTransitModalV133(tr);return true}

const PAN133={pointers:new Map(),start:null,drag:false,pinch:null};
function beginPanV133(e){if(Game.screen!=='overworld-screen')return;scheduleOverworldFrameV133(0);Game.ovCanvas.setPointerCapture?.(e.pointerId);PAN133.pointers.set(e.pointerId,{x:e.clientX,y:e.clientY,lx:e.offsetX,ly:e.offsetY});if(PAN133.pointers.size===1){ensureCameraV133();PAN133.drag=false;PAN133.start={x:e.clientX,y:e.clientY,cx:Game.ovCamera.x,cy:Game.ovCamera.y}}else if(PAN133.pointers.size===2){const a=[...PAN133.pointers.values()];PAN133.pinch={distance:Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y),tile:Game.ovTile};PAN133.drag=true}}
function movePanV133(e){
 // Passive mouse hover only changes visible state when the world tile changes.
 // Avoid waking the frozen overworld renderer for every raw high-polling pointer sample.
 if(!PAN133.pointers.has(e.pointerId)){
   if(e.pointerType==='mouse'){
     // PointerEvent offset coordinates are already local to the canvas. Using them
     // avoids a getBoundingClientRect() layout read on every passive hover sample.
     const sx=Number.isFinite(e.offsetX)?e.offsetX:null,sy=Number.isFinite(e.offsetY)?e.offsetY:null;
     let px=sx,py=sy;if(px===null||py===null){const r=Game.ovCanvas.getBoundingClientRect();px=e.clientX-r.left;py=e.clientY-r.top}
     const next=screenToWorldV133(px,py),prev=Game.hoverTile;
     if(!prev||prev.x!==next.x||prev.y!==next.y){Game.hoverTile=next;scheduleOverworldFrameV133(0)}
   }
   return
 }
 scheduleOverworldFrameV133(0);
 PAN133.pointers.set(e.pointerId,{x:e.clientX,y:e.clientY,lx:e.offsetX,ly:e.offsetY});
 if(PAN133.pointers.size>=2){const a=[...PAN133.pointers.values()],d=Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y),mid={x:(a[0].lx+a[1].lx)/2,y:(a[0].ly+a[1].ly)/2};if(PAN133.pinch?.distance)zoomAtV133((PAN133.pinch.tile*(d/PAN133.pinch.distance))/Game.ovTile,mid.x,mid.y);PAN133.drag=true;return}
 if(!PAN133.start)return;const dx=e.clientX-PAN133.start.x,dy=e.clientY-PAN133.start.y;if(Math.hypot(dx,dy)>5)PAN133.drag=true;if(PAN133.drag){Game.ovCamera.follow=false;Game.ovCamera.x=Game.ovCamera.tx=PAN133.start.cx-dx/Game.ovTile;Game.ovCamera.y=Game.ovCamera.ty=PAN133.start.cy-dy/Game.ovTile;clampCameraV133();Game.ovStaticDirty=true;updateCameraModeV133()}
}
function endPanV133(e){const was=PAN133.drag,count=PAN133.pointers.size;PAN133.pointers.delete(e.pointerId);if(PAN133.pointers.size<2)PAN133.pinch=null;if(PAN133.pointers.size===0){PAN133.start=null;PAN133.drag=false;if(!was&&count===1)handleMapTapV133(e.clientX,e.clientY)}}
window.beginPanV133=beginPanV133;window.movePanV133=movePanV133;window.endPanV133=endPanV133;

function handleMapTapV133(clientX,clientY){
 const world=currentDistrictV133(),rect=Game.ovCanvas.getBoundingClientRect(),sx=clientX-rect.left,sy=clientY-rect.top,m=Game._v133MiniRect;
 if(m&&sx>=m.x&&sx<=m.x+m.w&&sy>=m.y&&sy<=m.y+m.h){ensureCameraV133();const wx=(sx-m.x)/m.w*world.w,wy=(sy-m.y)/m.h*world.h,vx=rect.width/Game.ovTile,vy=rect.height/Game.ovTile;Game.ovCamera.x=Game.ovCamera.tx=wx-vx/2;Game.ovCamera.y=Game.ovCamera.ty=wy-vy/2;Game.ovCamera.follow=false;clampCameraV133();Game.ovStaticDirty=true;updateCameraModeV133();return}
 const q=screenToWorldV133(sx,sy);if(!pointInBounds133(world,q.x,q.y))return;Game.hoverTile=q;if(window.handleMissionApproachTapV134B?.(q))return;if(window.handleLivingStreetTapV134?.(q))return;const mark=markerAtV133(world,q.x,q.y);if(mark){const d=Math.hypot(Game.ovPlayer.x-mark.x,Game.ovPlayer.y-mark.y);if(d<=2.1){mark.kind==='transit'?openTransitNodeV133(mark.id):openDistrictLocationV133(mark.id)}else{mark.kind==='transit'?routeToTransitNodeV133(mark.id):routeToLocationV133(mark.id)}return}
 if(!isWalkableV133(q.x,q.y)){toast('Blocked.');return}routeToPointV133(q,{kind:'point',label:`${q.x},${q.y}`})
}
window.handleMapTapV133=handleMapTapV133;

function installInputV133(){
 const old=document.getElementById('overworld');if(!old)return;let c=old;if(!old.dataset.v133Input||old.dataset.v132Input){const clone=old.cloneNode(false);clone.id='overworld';delete clone.dataset.v132Input;delete clone.dataset.v133Bound;old.replaceWith(clone);c=clone;Game.ovCanvas=clone;Game.ovCtx=clone.getContext('2d');c.dataset.v133Input='1'}
 if(c.dataset.v133Bound)return;c.dataset.v133Bound='1';c.style.touchAction='none';c.addEventListener('pointerdown',beginPanV133);c.addEventListener('pointermove',movePanV133);c.addEventListener('pointerup',endPanV133);c.addEventListener('pointercancel',endPanV133);c.addEventListener('wheel',e=>{e.preventDefault();const r=c.getBoundingClientRect();zoomAtV133(e.deltaY<0?1.12:.89,e.clientX-r.left,e.clientY-r.top)},{passive:false})
}

function setHUDTextV133(el,value){if(!el)return false;const next=String(value);if(el.textContent===next)return false;el.textContent=next;return true}
function setHUDHTMLV133(el,value){if(!el||el.innerHTML===value)return false;el.innerHTML=value;return true}
function updateOverworldHUDV133(){
 const world=currentDistrictV133(),hood=neighborhoodAtV133(Game.ovPlayer.x,Game.ovPlayer.y,world),cr=document.getElementById('ov-credits'),day=document.getElementById('ov-day'),tm=document.getElementById('ov-time'),rep=document.getElementById('ov-rep');
 setHUDTextV133(cr,Game.credits.toLocaleString());setHUDTextV133(day,Game.day);setHUDTextV133(tm,`${String(Math.floor(Game.hour)).padStart(2,'0')}:${String(Math.round((Game.hour%1)*60)).padStart(2,'0')}`);setHUDTextV133(rep,Object.values(Game.rep||{}).reduce((a,b)=>a+b,0));
 const loc=document.getElementById('ov-location'),dn=document.getElementById('dl-name'),dc=document.getElementById('dl-control'),badge=document.getElementById('v133-district-badge'),meta=sectorMeta133(world.id);
 setHUDTextV133(loc,`${world.cfg.name} // ${hood?.name||'TRANSIT'} · ${Game.ovPlayer.x},${Game.ovPlayer.y}`);
 setHUDTextV133(dn,(hood?.name||world.cfg.name).toUpperCase());setHUDTextV133(dc,`${meta?.controller||'LOCAL'} · SEC ${meta?.security||0}/5`);
 setHUDHTMLV133(badge,`<b>${world.cfg.name.toUpperCase()}</b><span>${(hood?.name||'TRANSIT').toUpperCase()} · ${world.w}×${world.h}</span>`);
 updateRouteCardV133()
}
window.updateOverworldHUD=updateOverworldHUDV133;

let LASTMOVE133=0,LASTIDLEFRAME133=0,IDLETIMER133=null;
function cancelOverworldScheduleV133(){
 if(IDLETIMER133!==null){clearTimeout(IDLETIMER133);IDLETIMER133=null}
 if(Game.ovAnim){cancelAnimationFrame(Game.ovAnim);Game.ovAnim=null}
}
function scheduleOverworldFrameV133(delay=0){
 if(Game.screen!=='overworld-screen'||document.hidden)return;
 if(delay>0){
   if(IDLETIMER133!==null)return;
   IDLETIMER133=setTimeout(()=>{IDLETIMER133=null;if(Game.screen==='overworld-screen'&&!document.hidden&&!Game.ovAnim)Game.ovAnim=requestAnimationFrame(overworldLoopV133)},delay);
   return
 }
 if(IDLETIMER133!==null){clearTimeout(IDLETIMER133);IDLETIMER133=null}
 if(!Game.ovAnim)Game.ovAnim=requestAnimationFrame(overworldLoopV133)
}
window.requestOverworldRenderV133=()=>{if(Game.screen==='overworld-screen'&&!document.hidden)overworldLoopV133(performance.now())};
function overworldLoopV133(t){
 // Do not keep a background RAF alive while menus, combat, or a hidden browser
 // tab is active. initOverworldV133()/visibilitychange explicitly restart it.
 Game.ovAnim=null;
 if(Game.screen!=='overworld-screen'||document.hidden)return
 const world=currentDistrictV133();ensureCameraV133();if(Game.ovCanvas&&Game.ovCanvas.style.transform!=='none')Game.ovCanvas.style.transform='none';
 // Read layout once per frame. This used to query + measure the same wrapper
 // twice on follow-camera frames, forcing redundant layout work on mobile.
 const wrapEl=document.getElementById('overworld-screen')?.querySelector('.wrap'),r=Game._v133FrameRect||cacheOverworldFrameRectV133(wrapEl)||{width:Game.ovCanvas?.clientWidth||0,height:Game.ovCanvas?.clientHeight||0};
 if(Game.ovCamera.follow&&!PAN133.drag){const vx=r.width/Game.ovTile,vy=r.height/Game.ovTile;Game.ovCamera.tx=Game.ovPlayer.x-vx/2+.5;Game.ovCamera.ty=Game.ovPlayer.y-vy/2+.5;clampCameraV133()}
 const ox=Game.ovCamera.x,oy=Game.ovCamera.y;Game.ovCamera.x+=(Game.ovCamera.tx-Game.ovCamera.x)*.18;Game.ovCamera.y+=(Game.ovCamera.ty-Game.ovCamera.y)*.18;if(Math.abs(Game.ovCamera.x-Game.ovCamera.tx)<.002)Game.ovCamera.x=Game.ovCamera.tx;if(Math.abs(Game.ovCamera.y-Game.ovCamera.ty)<.002)Game.ovCamera.y=Game.ovCamera.ty;if(Math.abs(ox-Game.ovCamera.x)>.002||Math.abs(oy-Game.ovCamera.y)>.002)Game.ovStaticDirty=true;
 if(!Game._v134EventOpen&&Game.pendingPath?.length>1&&t-LASTMOVE133>55){LASTMOVE133=t;const n=Game.pendingPath[1];Game.ovPlayer.x=n.x;Game.ovPlayer.y=n.y;Game.pendingPath.shift();Game.districtWorldsV133.positions[world.id]={x:n.x,y:n.y};advanceTime(.25);window.onStreetStepV134?.(world);updateOverworldHUDV133();
   if(Game.pendingPath&&Game.pendingPath.length<=1){Game.pendingPath=null;const target=Game._v133TravelTarget;Game._v133TravelTarget=null;updateRouteCardV133();if(target?.kind==='v134b')setTimeout(()=>window.completeMissionApproachV134B?.(target),100);else if(target?.kind==='v134')setTimeout(()=>window.completeLivingStreetTargetV134?.(target),100);else if(target?.kind==='location')setTimeout(()=>openDistrictLocationV133(target.id),100);else if(target?.kind==='transit')setTimeout(()=>openTransitNodeV133(target.id),100);else if(Game.storyFlags._pendingTravelEvent){delete Game.storyFlags._pendingTravelEvent;setTimeout(()=>triggerTravelEvent(),160)}}
 }
 const key=`${world.id}|${Game.ovCamera.x.toFixed(3)}|${Game.ovCamera.y.toFixed(3)}|${Game.ovTile.toFixed(2)}|${r.width}|${r.height}`;
 if(Game.ovStaticDirty||Game._v133StaticKey!==key)renderDistrictStaticV133();
 // Dynamic world state is frozen while idle. Render continuously only while
 // movement/camera work is active; otherwise stop scheduling frames entirely.
 // Input, resize, visibility and route-start paths explicitly invalidate/wake it.
 const cameraMoving=Math.abs(Game.ovCamera.x-Game.ovCamera.tx)>.002||Math.abs(Game.ovCamera.y-Game.ovCamera.ty)>.002;
 const active=!!(Game.pendingPath?.length>1||PAN133.drag||cameraMoving||Game.ovStaticDirty);
 drawDistrictDynamicV133(r);LASTIDLEFRAME133=t;
 // True frozen-world invalidation: after the final settled frame, do not keep
 // either RAF or timer work alive. Active movement/camera work remains full-rate.
 if(active)scheduleOverworldFrameV133(0)
 // Legacy PWA12.15 contract marker (superseded): scheduleOverworldFrameV133(active?0:100)
}
window.overworldLoop=overworldLoopV133;

// Browsers throttle background RAFs, but explicitly cancelling the district loop
// also avoids layout/draw work during visibility transitions and makes the CPU
// contract deterministic. Resume only when the overworld is actually active.
if(!window.__v133VisibilityPerfBound){
 window.__v133VisibilityPerfBound=true;
 document.addEventListener('visibilitychange',()=>{
   if(document.hidden){cancelOverworldScheduleV133();return}
   if(Game.screen==='overworld-screen')scheduleOverworldFrameV133(0)
 })
}

function initOverworldV133(){
 ensureV13State();ensureDistrictWorldStateV133();ensureV133UI();if(!V133_WORLD_CACHE.has(Game.districtWorldsV133.activeId))generateDistrictV133(Game.districtWorldsV133.activeId);activateDistrictV133(Game.districtWorldsV133.activeId,null);
 installInputV133();resizeOverworldV133();ensureCameraV133();if(Game.ovCamera.follow!==false)centerCameraV133(true);window.ensureLivingStreetsStateV134?.();window.ensureNeighborhoodStateV134?.(currentDistrictV133());window.ensureStreetActorsV134?.(currentDistrictV133());window.ensureInteractablesV134?.(currentDistrictV133());window.ensureV134UI?.();updateOverworldHUDV133();document.getElementById('overworld').style.transform='none';
 cancelOverworldScheduleV133();scheduleOverworldFrameV133(0)
}
window.initOverworld=initOverworldV133;window.initOverworldV133=initOverworldV133;window.buildOverworldMap=()=>{const w=currentDistrictV133();rebuildOvMapV133(w);Game.ovStaticDirty=true;return Game.ovMap};

/* ---------- Strategic City Map ---------- */
function strategicLinksForV133(id){return V133_TRANSIT_LINKS.filter(l=>(l.from.district===id||l.to.district===id)&&(l.type!=='hidden'||Game.districtWorldsV133.hiddenLinks[l.id]))}
function routeToStrategicDistrictV133(targetId){
 const current=currentDistrictV133().id,links=strategicLinksForV133(current).filter(l=>otherEndpointV133(l,current).district===targetId);
 if(!links.length){toast('No direct known transit from this district.');return false}const link=links[0],ep=endpointForV133(link,current);showScreen('overworld-screen');initOverworldV133();setTimeout(()=>routeToTransitNodeV133(ep.node),40);return true
}
function renderStrategicCityMapV133(selected=null){
 ensureDistrictWorldStateV133();const map=document.getElementById('v133-strategic-map'),info=document.getElementById('v133-strategic-info');if(!map||!info)return;const current=Game.districtWorldsV133.activeId,sel=selected||current;
 const edges=V133_TRANSIT_LINKS.filter(l=>l.type!=='hidden'||Game.districtWorldsV133.hiddenLinks[l.id]);
 map.innerHTML=`<svg viewBox="0 0 100 100" preserveAspectRatio="none">${edges.map(l=>{const a=V133_DISTRICTS[l.from.district].strategic,b=V133_DISTRICTS[l.to.district].strategic,col=l.type==='security'?'#d9f7ff':l.type==='metro'?'#43d7e8':l.type==='freight'?'#e4ad4c':l.type==='hidden'?'#7f63ff':'#59737e';return`<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}" stroke="${col}" stroke-opacity="${l.type==='hidden'?'.55':'.33'}" stroke-width="${l.type==='metro'?'.55':'.35'}" stroke-dasharray="${l.type==='hidden'?'2 2':'0'}"/>`}).join('')}</svg>`+Object.entries(V133_DISTRICTS).map(([id,d])=>{const meta=sectorMeta133(id),known=locDefs133(id).filter(l=>locationKnownV133(l.id)).length,jobs=(Game.contacts||[]).filter(c=>c.sectorId===id).reduce((n,c)=>n+(c.missions?.length||0),0);return`<button class="v133-city-node ${id===current?'current':''}" data-d="${id}" style="left:${d.strategic[0]}%;top:${d.strategic[1]}%;--node:${meta?.color||d.accent}"><i class="dot"></i><b>${d.name}</b><small>${meta?.controller||'LOCAL'} · SEC ${meta?.security||0}/5<br>${known} sites · ${jobs} jobs</small></button>`}).join('');
 map.querySelectorAll('[data-d]').forEach(e=>e.onclick=()=>renderStrategicCityMapV133(e.dataset.d));
 const d=V133_DISTRICTS[sel],meta=sectorMeta133(sel),local=strategicLinksForV133(sel),fromCurrent=sel===current?[]:strategicLinksForV133(current).filter(l=>otherEndpointV133(l,current).district===sel);
 info.innerHTML=`<div class="v13-section-title">${d.name}</div><div class="v133-info-card" style="--accent:${meta?.color||d.accent}"><h4>${meta?.controller||'LOCAL CONTROL'} · SECURITY ${meta?.security||0}/5</h4><p>${meta?.desc||''}</p></div><div class="v13-section-title">KNOWN CONNECTIONS</div>${local.map(l=>{const other=otherEndpointV133(l,sel);return`<div class="v133-link-row"><div class="v133-link-icon">${l.type==='metro'?'M':l.type==='freight'?'F':l.type==='security'?'S':l.type==='hidden'?'?':'→'}</div><div class="v133-link-main"><b>${V133_DISTRICTS[other.district].name}</b><small>${l.name} · ${l.type.toUpperCase()} · ${l.minutes} MIN</small></div></div>`}).join('')||'<div class="v133-info-card"><p>No known connections.</p></div>'}${fromCurrent.length?`<div class="v13-section-title" style="margin-top:12px">FROM CURRENT DISTRICT</div><div class="v133-info-card"><h4>PHYSICAL ROUTE AVAILABLE</h4><p>Chrome City does not teleport you between districts. Route to the appropriate gate/station in ${V133_DISTRICTS[current].name}.</p><button class="btn small" id="v133-route-strategic" style="margin-top:7px">ROUTE TO TRANSIT</button></div>`:''}`;
 document.getElementById('v133-route-strategic')?.addEventListener('click',()=>routeToStrategicDistrictV133(sel))
}
window.renderStrategicCityMapV133=renderStrategicCityMapV133;
function openStrategicCityMapV133(){ensureV133UI();renderStrategicCityMapV133();showScreen('v133-strategic-city-screen')}
window.openStrategicCityMapV133=openStrategicCityMapV133;

/* Make v13 dossier travel buttons route through the current physical district. */
const V133PrevDistrictHub=window.renderDistrictHubV13;
if(V133PrevDistrictHub)window.renderDistrictHubV13=function(id){const r=V133PrevDistrictHub(id);requestAnimationFrame(()=>{const a=document.getElementById('v13-travel-location');if(a){a.id='v133-travel-location';a.onclick=()=>{const loc=Game.cityLife.currentLocation;if(loc&&currentDistrictV133().locations[loc]){showScreen('overworld-screen');initOverworldV133();routeToLocationV133(loc)}else toast('Location is in another district. Use city transit.')}}const b=document.getElementById('v13-route-district');if(b){b.id='v133-route-district';b.onclick=()=>{if(id===currentDistrictV133().id){showScreen('overworld-screen');initOverworldV133()}else{openStrategicCityMapV133();renderStrategicCityMapV133(id)}}}});return r};

/* ---------- Save migration / lifecycle ---------- */
const V133PrevSerialize=serializeGame;
serializeGame=function(){
 ensureDistrictWorldStateV133();const state=Game.districtWorldsV133;if(state.activeId&&Game.ovPlayer)state.positions[state.activeId]={x:Game.ovPlayer.x,y:Game.ovPlayer.y};if(Game.ovCamera)state.cameraByDistrict[state.activeId]={x:Game.ovCamera.x,y:Game.ovCamera.y,tile:Game.ovTile,follow:Game.ovCamera.follow};
 const d=JSON.parse(V133PrevSerialize());d.version=V133_VERSION;d.districtWorldsV133=JSON.parse(JSON.stringify(state));d.ovPlayer=Game.ovPlayer;return JSON.stringify(d)
};
const V133PrevLoad=loadGame;
loadGame=function(slot){
 let data=null;for(const p of ['chrome_requiem_v13_'+slot,'chrome_requiem_v12_'+slot,'chrome_requiem_v11_'+slot,'chrome_requiem_v10_'+slot,'chrome_requiem_v9_'+slot,'chrome_requiem_v8_'+slot,'chrome_requiem_v7_'+slot,'chrome_requiem_save_'+slot]){const raw=localStorage.getItem(p);if(raw){try{data=JSON.parse(raw)}catch(e){}break}}
 const ok=V133PrevLoad(slot);if(ok){V133_WORLD_CACHE.clear();migrateMegaSaveV133(data);ensureDistrictWorldStateV133();const sid=Game.districtWorldsV133.activeId,saved=Game.districtWorldsV133.positions?.[sid];if(saved)Game.ovPlayer={x:saved.x,y:saved.y};activateDistrictV133(sid,null);ensureV133UI();initOverworldV133();saveGame(0,true)}return ok
};
const V133PrevNew=startNewGame;
startNewGame=function(name,className,background){
 const r=V133PrevNew(name,className,background);V133_WORLD_CACHE.clear();Game.districtWorldsV133={activeId:'old_market',positions:{},unlockedLinks:{},hiddenLinks:{},dynamic:{},cameraByDistrict:{},discoveredNeighborhoods:{}};ensureDistrictWorldStateV133();activateDistrictV133('old_market',null);
 const w=currentDistrictV133(),hq=w.locations.v133_safehouse;if(hq){Game.ovPlayer={x:hq.x,y:hq.y};Game.districtWorldsV133.positions.old_market={x:hq.x,y:hq.y}}
 return r
};

/* ---------- Initialization ---------- */
function validateDistrictWorldsV133(){
 const rows=[];let totalLoc=0,totalBuildings=0,bad=0;for(const id of Object.keys(V133_DISTRICTS)){const w=generateDistrictV133(id),v=validateWorldV133(w);rows.push(v);totalLoc+=v.locations;totalBuildings+=v.buildings;if(v.unreachable.length||v.organic.diag<5)bad++}
 return{districts:rows.length,totalLocations:totalLoc,totalBuildings,bad,rows}
}
window.validateDistrictWorldsV133=validateDistrictWorldsV133;

function runDiagnosticsV133(){
 ensureDistrictWorldStateV133();const rows=[],add=(n,ok,d='')=>rows.push({name:n,ok:!!ok,details:d});try{
  const all=validateDistrictWorldsV133();add('13 separate district worlds',all.districts===13,all.districts);add('all generated worlds valid',all.bad===0,all.bad);add('82+ City Life locations physical',all.totalLocations>=82,all.totalLocations);add('organic road geometry',all.rows.every(r=>r.organic.diag>=5));add('multi-cell building population',all.totalBuildings>1000,all.totalBuildings);add('binary heap routing',typeof MinHeapV133==='function');add('physical transit',V133_TRANSIT_LINKS.length>=20,V133_TRANSIT_LINKS.length);add('strategic map',typeof renderStrategicCityMapV133==='function');add('v13.2 camera UX retained',typeof beginPanV133==='function'&&typeof zoomAtV133==='function');add('v13.1 recovery retained',!!ChromeRequiem.modules?.BlackMagicRecoveryV131);add('v13 City Life retained',!!ChromeRequiem.modules?.CityLifeV13);add('v12 tactical retained',!!ChromeRequiem.modules?.TacticalV12);add('v9 performance retained',!!ChromeRequiem.modules?.Performance?.stats)
 }catch(e){add('exception',false,e.message)}
 return{version:V133_VERSION,passed:rows.filter(x=>x.ok).length,total:rows.length,results:rows}
}
window.runDiagnosticsV133=runDiagnosticsV133;

window.ChromeRequiem.version=V133_VERSION;
window.ChromeRequiem.modules.DistrictWorldsV133={districts:V133_DISTRICTS,neighborhoods:V133_NEIGHBORHOODS,transit:V133_TRANSIT_LINKS,activate:activateDistrictV133,generate:generateDistrictV133,diagnostics:runDiagnosticsV133};

/* Defer full UI init until game start/load, but prepare state. */
ensureV13State();ensureDistrictWorldStateV133();ensureV133UI();
})();
}



// v14 explicit domain API. Legacy globals remain installed above for compatibility.
const districtCallV14=(name,...args)=>{
 const fn=globalThis[name];
 if(typeof fn!=='function')throw new Error(`DistrictWorldsV14 missing legacy implementation: ${name}`);
 return fn(...args);
};
const DistrictWorldsV14=Object.freeze({
 version:'13.3',
 get districts(){return globalThis.V133_DISTRICTS},
 get neighborhoods(){return globalThis.V133_NEIGHBORHOODS},
 get transit(){return globalThis.V133_TRANSIT_LINKS},
 get terrain(){return globalThis.V133_TERRAIN},
 ensureState:(...args)=>districtCallV14('ensureDistrictWorldStateV133',...args),
 generateDistrict:(...args)=>districtCallV14('generateDistrictV133',...args),
 findPath:(...args)=>districtCallV14('findDistrictPathV133',...args),
 activate:(...args)=>districtCallV14('activateDistrictV133',...args),
 current:(...args)=>districtCallV14('currentDistrictV133',...args),
 routeToLocation:(...args)=>districtCallV14('routeToLocationV133',...args),
 routeToTransit:(...args)=>districtCallV14('routeToTransitNodeV133',...args),
 travel:(...args)=>districtCallV14('travelDistrictV133',...args),
 neighborhoodAt:(...args)=>districtCallV14('neighborhoodAtV133',...args),
 validate:(...args)=>districtCallV14('validateDistrictWorldsV133',...args),
 diagnostics:(...args)=>districtCallV14('runDiagnosticsV133',...args)
});
globalThis.ChromeRequiemV14Domains ||= {};
globalThis.ChromeRequiemV14Domains.world ||= {};
globalThis.ChromeRequiemV14Domains.world.districts=DistrictWorldsV14;

/* PWA12.70: deterministic grime and infrastructure details; visual only. */
function drawUrbanGritV170(ctx,world,b,part,x,y,w,h){
 const t=Game.ovTile,seed=b.seed>>>0,g=world.cfg.grammar;if(t<17)return;ctx.save();
 // Drainage streaks and roof-edge dirt build believable scale without obscuring gameplay.
 const streaks=Math.min(7,2+(seed%6));
 for(let i=0;i<streaks;i++){const px=x+w*(.08+(((seed+i*37)%83)/100)),len=Math.min(h*.42,t*(.25+((seed+i*11)%20)/50));ctx.fillStyle=i%3===0?'rgba(116,68,39,.13)':'rgba(0,0,0,.16)';ctx.fillRect(px,y+Math.max(2,t*.06),Math.max(1,t*.025),len)}
 // Service conduit with brackets on non-corporate roofs.
 if(!['glass','meridian','helix','civic','crown'].includes(g)&&w>t*2.1){const yy=y+h*.43;ctx.strokeStyle='rgba(44,52,50,.72)';ctx.lineWidth=Math.max(1,t*.045);ctx.beginPath();ctx.moveTo(x+w*.12,yy);ctx.lineTo(x+w*.78,yy);ctx.lineTo(x+w*.84,yy+h*.12);ctx.stroke();ctx.fillStyle='rgba(156,132,91,.24)';for(let k=1;k<4;k++)ctx.fillRect(x+w*(.12+k*.16),yy-1,Math.max(1,t*.035),Math.max(3,t*.11))}
 // Industrial roofs get exhaust staining around machinery.
 if(['dock','forge','rail'].includes(g)){ctx.fillStyle='rgba(0,0,0,.13)';ctx.beginPath();ctx.ellipse(x+w*.26,y+h*.27,Math.max(5,w*.14),Math.max(3,h*.08),0,0,Math.PI*2);ctx.fill()}
 ctx.restore();
}
window.drawUrbanGritV170=drawUrbanGritV170;
