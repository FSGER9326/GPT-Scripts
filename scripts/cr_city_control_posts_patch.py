from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve()
module=root/'src/world/district-control-posts-pwa12-104-city-candidate-07.js'
module.write_text(r'''if(typeof window!=='undefined'){
(() => {
'use strict';
const VERSION='pwa12.104-city-candidate.07';
const QUIET=new Set(['OPEN ACCESS','FRIENDLY CORRIDOR','FRIENDLY FREIGHT','PRIORITY CLEARANCE','COVERT BYPASS','CONTACT COVER','INCIDENT CLEARED']);
function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
function copy(v){return v==null?v:JSON.parse(JSON.stringify(v))}
function nowMin(){return Math.round((((Game.day||1)-1)*24+(Game.hour||0))*60)}
function currentWorld(){return window.currentDistrictV133?.()||null}
function link(id){return (window.V133_TRANSIT_LINKS||[]).find(x=>x.id===id)||null}
function endpoint(l,d){return l?.from?.district===d?l.from:l?.to?.district===d?l.to:null}
function other(l,d){return l?.from?.district===d?l.to:l?.to?.district===d?l.from:null}
function state(){
 const s=window.ensureLivingStreetsStateV134?.()||(Game.livingStreetsV134=Game.livingStreetsV134||{});
 s.controlPosts=s.controlPosts||{version:1,approach:null,engaged:null,clearances:{},suppressed:{},activeCombat:null,history:[],stats:{seen:0,cleared:0,complied:0,spoofed:0,fights:0,retreated:0,crossings:0}};
 const x=s.controlPosts;x.clearances=x.clearances||{};x.suppressed=x.suppressed||{};x.history=x.history||[];x.stats=x.stats||{};
 for(const k of ['seen','cleared','complied','spoofed','fights','retreated','crossings'])x.stats[k]=x.stats[k]||0;
 return x
}
function nearestHood(world,p){let best=null,bd=Infinity;for(const n of world?.neighborhoods||[]){const d=Math.hypot((p?.x||0)-n.x,(p?.y||0)-n.y);if(d<bd){bd=d;best=n.id}}return best}
function hoodState(post){const w=window.generateDistrictV133?.(post?.district);if(!w)return null;return window.ensureNeighborhoodStateV134?.(w)?.[post.neighborhood]||null}
function nodeForLink(l,w=currentWorld()){if(!l||!w)return null;const ep=endpoint(l,w.id);if(!ep)return null;return w.transit?.find(t=>t.id===ep.node)||null}
function candidate06Owns(linkId){const i=Game.livingStreetsV134?.transitIncidents?.active;return !!(i&&i.linkId===linkId&&!['crossed','retreated','failed'].includes(i.status))}
function validClearance(linkId){const c=state().clearances?.[linkId];if(!c||c.consumed)return null;if(Number(c.expires||0)<=nowMin()){delete state().clearances[linkId];return null}return c}
function suppressed(linkId,district){const k=`${district}:${linkId}`,r=state().suppressed?.[k];if(!r)return null;if(Number(r.until||0)<=nowMin()){delete state().suppressed[k];return null}return r}
function ecology(l,district){return window.evaluateTransitAccessEcologyV12104?.(l?.id||l,district,'free_roam')||null}
function needsPost(l,e){
 if(!l||!e||l.type==='hidden'||QUIET.has(e.label))return false;
 if(e.blocked||Number(e.costDelta||0)>0||Number(e.minutesDelta||0)>=3||Number(e.riskDelta||0)>=.05)return true;
 const p=e.pressure||{};if(l.type==='security'&&(p.security||0)>=.62)return true;if(l.type==='freight'&&Math.max(p.security||0,p.gang||0)>=.66)return true;if(l.type==='border'&&(p.gang||0)>=.62&&(p.heat||0)>=.30)return true;if(l.type==='metro'&&(p.security||0)>=.68&&(p.heat||0)>=.42)return true;return false
}
function actorFor(l,e){const p=e?.pressure||{};if(l?.type==='security'||e?.label?.includes('SCREEN')||e?.label?.includes('METRO')||e?.label?.includes('LOCKDOWN'))return'security';if(e?.label==='CARGO TOLL'||e?.label==='STREET LEVY'||(p.gang||0)>(p.security||0)+.08)return'gang';if(l?.type==='freight')return'contractor';return(p.security||0)>=(p.gang||0)?'security':'gang'}
function profile(l,e){
 const p=e?.pressure||{},actor=actorFor(l,e),fee=Math.max(0,Math.round(Number(e?.costDelta||0)))||Math.max(90,Math.round(90+(p.heat||0)*120+(p.gang||0)*65)),delay=Math.max(2,Math.round(Number(e?.minutesDelta||0))||3);
 let title=e?.label||'CONTROL POST',text='A temporary control point has hardened around this physical transit approach. The crew must deal with it here or choose another route.';
 if(e?.label==='METRO ID SWEEP'||e?.label==='PLATFORM SCREENING')text='Transit security has occupied the platform approach with scanners, portable barriers and armed identity checks.';
 else if(e?.label==='CARGO TOLL'||e?.label==='FREIGHT INSPECTION')text='Inspection crews have turned the freight approach into a live cargo-control lane.';
 else if(e?.label==='STREET LEVY')text='A local crew has chained off the crossing and is collecting a street levy from everyone trying to pass.';
 else if(e?.label?.includes('LOCKDOWN')||e?.label==='INTENSIVE SCREENING')text='A hardened checkpoint controls the crossing. Credentials, cargo and affiliations are being checked under weapons.';
 else if(e?.label==='CROWD DELAY')text='Improvised barriers and a crowd surge have become a de facto control point across the transit approach.';
 return{actor,fee,delay,title,text}
}
function postForLink(linkId,district=currentWorld()?.id){
 const w=currentWorld();if(!w||w.id!==district)return null;const l=link(linkId);if(!l||!endpoint(l,district)||l.type==='hidden'||candidate06Owns(linkId)||validClearance(linkId)||suppressed(linkId,district))return null;
 const n=nodeForLink(l,w),e=ecology(l,district);if(!n||!e||!needsPost(l,e))return null;const to=other(l,district),prof=profile(l,e);
 return{id:`cp_${district}_${linkId}`,linkId,linkName:l.name,linkType:l.type,district,nodeId:n.id,x:n.x,y:n.y,neighborhood:nearestHood(w,n),toDistrict:to?.district||null,ecology:copy(e),profile:prof,faction:e.faction||e.controller||l.faction||null,controller:e.controller||null}
}
window.controlPostForLinkV12104=postForLink;
function postsForWorld(w=currentWorld()){
 if(!w)return[];const seen=new Set(),out=[];for(const tr of w.transit||[])for(const lid of tr.linkIds||[]){if(seen.has(lid))continue;seen.add(lid);const p=postForLink(lid,w.id);if(p)out.push(p)}return out
}
window.controlPostsForWorldV12104=postsForWorld;
function postNear(q,w=currentWorld()){let best=null,bd=Infinity;for(const p of postsForWorld(w)){const d=Math.hypot(q.x-p.x,q.y-p.y);if(d<=1.55&&d<bd){best=p;bd=d}}return best}
function atPost(p){return !!(p&&Game.ovPlayer&&currentWorld()?.id===p.district&&Math.hypot(Game.ovPlayer.x-p.x,Game.ovPlayer.y-p.y)<=1.7)}
function ensureStyle(){if(document.getElementById('v12104-control-post-style'))return;const s=document.createElement('style');s.id='v12104-control-post-style';s.textContent=`#v12104-control-post-panel{position:fixed;z-index:10045;left:50%;bottom:18px;transform:translateX(-50%);width:min(390px,calc(100vw - 24px));max-height:min(76vh,620px);overflow:auto;background:rgba(4,8,12,.975);border:1px solid rgba(236,171,73,.72);box-shadow:0 14px 48px rgba(0,0,0,.65),0 0 28px rgba(236,171,73,.13);padding:12px;color:#d8e3e8;font:12px/1.42 Share Tech Mono,monospace}#v12104-control-post-panel[hidden]{display:none!important}#v12104-control-post-panel h3{margin:0 0 5px;color:#f2c16f;font:800 14px/1.2 Orbitron,sans-serif;letter-spacing:.06em}#v12104-control-post-panel .cp-sub{color:#91a7b0;margin-bottom:8px}#v12104-control-post-panel .cp-pressure{margin:8px 0;padding:7px;border-left:2px solid #df9d43;background:rgba(223,157,67,.07);font-size:11px}#v12104-control-post-panel .cp-actions{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-top:10px}#v12104-control-post-panel button{min-height:44px;white-space:normal}#v12104-control-post-panel .cp-note{margin-top:7px;color:#80949d;font-size:10px}@media(max-width:520px){#v12104-control-post-panel{bottom:8px;width:calc(100vw - 20px);padding:10px;max-height:72vh}#v12104-control-post-panel .cp-actions{grid-template-columns:1fr}#v12104-control-post-panel button{min-height:46px}}`;document.head.appendChild(s)}
function ensurePanel(){ensureStyle();let p=document.getElementById('v12104-control-post-panel');if(!p){p=document.createElement('section');p.id='v12104-control-post-panel';p.hidden=true;document.body.appendChild(p)}return p}
function hide(){const p=document.getElementById('v12104-control-post-panel');if(p)p.hidden=true}
function crewClasses(){return new Set((window.activeCrewV135?.()||Game.roster||[]).map(x=>x.className))}
function action(box,id,text,fn,disabled=false){const b=document.createElement('button');b.className='btn small';b.id=id;b.textContent=text;b.disabled=!!disabled;b.onclick=fn;box.appendChild(b);return b}
function openPost(linkId){
 const p=postForLink(linkId),box=ensurePanel();if(!p||!atPost(p))return false;const st=state();st.approach=null;st.engaged={district:p.district,linkId:p.linkId,nodeId:p.nodeId,at:nowMin()};st.stats.seen++;const h=p.ecology.pressure||{},fac=p.faction&&(window.FACTIONS?.[p.faction]?.short||p.faction),classes=crewClasses();box.hidden=false;
 box.innerHTML=`<h3>${p.profile.title}</h3><div class="cp-sub">${p.linkName} · ${p.linkType.toUpperCase()}${fac?` · ${fac}`:''}</div><div>${p.profile.text}</div><div class="cp-pressure">HEAT ${Math.round((h.heat||0)*100)} · SECURITY ${Math.round((h.security||0)*5)}/5 · GANG ${Math.round((h.gang||0)*5)}/5 · UNREST ${Math.round((h.unrest||0)*5)}/5<br>LOCAL CLEARANCE · ¢${p.profile.fee} · ${p.profile.delay} MIN</div><div class="cp-actions"></div><div class="cp-note">This post controls a physical city crossing. Clearing it does not bypass the crossing's normal faction/security requirements.</div>`;
 const acts=box.querySelector('.cp-actions');action(acts,'v12104-cp-comply',p.profile.fee?`SUBMIT / PAY ¢${p.profile.fee}`:`SUBMIT TO CHECK`,()=>comply(linkId),Number(Game.credits||0)<p.profile.fee);if(classes.has('AgentEX'))action(acts,'v12104-cp-agentex','AGENTEX · CREDENTIAL PLAY',()=>spoof(linkId,'agentex'));if(classes.has('Hacker'))action(acts,'v12104-cp-hacker','HACKER · SPOOF CONTROL',()=>spoof(linkId,'hacker'));if(p.profile.actor)action(acts,'v12104-cp-fight','FORCE THE CHECKPOINT',()=>fight(linkId));action(acts,'v12104-cp-retreat','BACK OFF',()=>retreat());window.saveGame?.(0,true);return true
}
window.openControlPostV12104=openPost;
function routePost(linkId,{resume=false}={}){
 const p=postForLink(linkId);if(!p||!Game.ovPlayer)return false;if(atPost(p))return openPost(linkId);const path=window.findDistrictPathV133?.(Game.ovPlayer,{x:p.x,y:p.y},currentWorld());if(!path||path.length<2){window.streetToastV134?.('NO STREET ROUTE TO CONTROL POST');return false}Game.pendingPath=path;Game._v133TravelTarget={kind:'v12104controlpost',id:p.id,linkId:p.linkId,label:`CONTROL POST // ${p.profile.title}`};if(Game.ovCamera)Game.ovCamera.follow=true;const st=state();st.approach={district:p.district,linkId:p.linkId,nodeId:p.nodeId,at:st.approach?.at||nowMin()};if(!resume){window.streetToastV134?.(`${p.profile.title} · PHYSICAL APPROACH`);window.saveGame?.(0,true)}return true
}
window.routeControlPostV12104=routePost;
function mutate(post,vals){const h=hoodState(post);if(!h)return;for(const [k,d] of Object.entries(vals||{})){if(k==='localHeat')h[k]=clamp(Number(h[k]||0)+d,0,100);else if(['security','gangPressure','unrest','prosperity'].includes(k))h[k]=clamp(Number(h[k]||0)+d,0,5)}h.events=(h.events||0)+1}
function factionHeat(post,delta){const f=post?.faction;if(!f)return;Game.heat=Game.heat||{};Game.heat[f]=clamp(Number(Game.heat[f]||0)+delta,0,100)}
function grant(post,method,detail={}){
 if(!post)return false;const st=state(),c={linkId:post.linkId,district:post.district,method,at:nowMin(),expires:nowMin()+120,consumed:false,label:'CONTROL POST CLEARED',...detail};st.clearances[post.linkId]=c;st.engaged=null;st.approach=null;st.stats.cleared++;if(method==='comply')st.stats.complied++;if(method==='agentex'||method==='hacker')st.stats.spoofed++;st.history.unshift({type:'clearance',post:post.id,linkId:post.linkId,district:post.district,method,at:c.at,detail:copy(detail)});st.history=st.history.slice(0,48);hide();window.addJournal?.('side','CONTROL POST CLEARED',`${post.profile.title} at ${post.linkName} cleared via ${String(method).toUpperCase()}. Clearance is valid for one physical crossing.`);window.streetToastV134?.(`${post.profile.title} · CLEARED`);window.saveGame?.(0,true);return c
}
function comply(linkId){const p=postForLink(linkId);if(!p||!atPost(p))return false;const fee=p.profile.fee;if(Number(Game.credits||0)<fee)return false;if(fee)Game.credits=Math.max(0,Number(Game.credits||0)-fee);window.advanceTime?.(p.profile.delay);if(p.profile.actor==='gang')mutate(p,{localHeat:-1,gangPressure:1});else mutate(p,{localHeat:-2});if(p.faction)factionHeat(p,-1);return !!grant(p,'comply',{fee,minutes:p.profile.delay})}
window.complyControlPostV12104=comply;
function spoof(linkId,kind){const p=postForLink(linkId);if(!p||!atPost(p)||!['agentex','hacker'].includes(kind))return false;const need=kind==='agentex'?'AgentEX':'Hacker';if(!crewClasses().has(need))return false;const minutes=kind==='agentex'?2:3;window.advanceTime?.(minutes);if(kind==='agentex'){mutate(p,{localHeat:-3});factionHeat(p,-1)}else{mutate(p,{localHeat:2,unrest:1});factionHeat(p,3)}return !!grant(p,kind,{minutes})}
window.spoofControlPostV12104=spoof;
function fight(linkId){const p=postForLink(linkId);if(!p||!atPost(p)||!p.profile.actor)return false;const st=state();st.activeCombat={post:copy(p),linkId:p.linkId,district:p.district,actor:p.profile.actor,at:nowMin()};st.stats.fights++;hide();window.saveGame?.(0,true);const ok=window.launchStreetCombatV134?.(p.profile.actor,currentWorld());if(!ok){st.activeCombat=null;openPost(linkId);return false}return true}
window.fightControlPostV12104=fight;
function retreat(){const st=state();if(!st.engaged&&!st.approach)return false;st.engaged=null;st.approach=null;Game.pendingPath=null;Game._v133TravelTarget=null;st.stats.retreated++;hide();window.streetToastV134?.('CONTROL POST · BACKED OFF');window.saveGame?.(0,true);return true}
window.retreatControlPostV12104=retreat;
function combatSettled(m,success){
 const st=state(),ac=st.activeCombat;if(!ac||!m?.v134StreetEncounter)return false;const post=ac.post;st.activeCombat=null;if(success){st.suppressed[`${post.district}:${post.linkId}`]={until:nowMin()+180,method:'fight',at:nowMin()};const c={linkId:post.linkId,district:post.district,method:'fight',at:nowMin(),expires:nowMin()+120,consumed:false,label:'CONTROL POST BROKEN'};st.clearances[post.linkId]=c;st.engaged=null;st.approach=null;st.stats.cleared++;st.history.unshift({type:'fight',post:post.id,linkId:post.linkId,district:post.district,success:true,at:nowMin(),suppressedUntil:st.suppressed[`${post.district}:${post.linkId}`].until});st.history=st.history.slice(0,48);window.addJournal?.('side','CONTROL POST BROKEN',`${post.linkName}: the crew forced the physical control point. The post will stay suppressed for a time, but street-combat aftermath remains in effect.`);window.streetToastV134?.('CONTROL POST BROKEN · ROUTE OPEN');window.saveGame?.(0,true);return true}
 st.engaged=null;st.approach=null;st.history.unshift({type:'fight',post:post.id,linkId:post.linkId,district:post.district,success:false,at:nowMin()});st.history=st.history.slice(0,48);window.streetToastV134?.('CONTROL POST HELD · ROUTE STILL CLOSED');window.saveGame?.(0,true);return true
}
window.onControlPostStreetCombatSettledV12104=combatSettled;
function draw(ctx,w,W,H,t){if(!ctx||!w)return;for(const p of postsForWorld(w)){const s=window.worldToScreen?.(p.x+.5,p.y+.5);if(!s||s.x<-32||s.y<-32||s.x>W+32||s.y>H+32)continue;const sec=p.profile.actor==='security',gang=p.profile.actor==='gang';ctx.save();ctx.translate(s.x,s.y);ctx.shadowColor=sec?'#5ec8ff':gang?'#ff6f58':'#eeb04c';ctx.shadowBlur=12;ctx.fillStyle='rgba(5,8,10,.92)';ctx.strokeStyle=sec?'#5ec8ff':gang?'#ff6f58':'#eeb04c';ctx.lineWidth=2;ctx.fillRect(-11,-8,22,16);ctx.strokeRect(-11,-8,22,16);ctx.beginPath();ctx.moveTo(-8,0);ctx.lineTo(8,0);ctx.moveTo(-5,-5);ctx.lineTo(-5,5);ctx.moveTo(5,-5);ctx.lineTo(5,5);ctx.stroke();ctx.shadowBlur=0;ctx.fillStyle='#f4f7f8';ctx.font=`800 ${Math.max(6.5,t*.17)}px Orbitron`;ctx.textAlign='center';ctx.fillText('CP',0,3);ctx.restore()}}
window.drawControlPostsV12104=draw;
function tap(q){const p=postNear(q);if(!p)return false;return atPost(p)?openPost(p.linkId):routePost(p.linkId)}
window.handleControlPostTapV12104=tap;
function detect(){const st=state(),a=st.approach;if(!a||currentWorld()?.id!==a.district)return false;const p=postForLink(a.linkId,a.district);if(!p){st.approach=null;return false}if(atPost(p)){Game.pendingPath=null;Game._v133TravelTarget=null;return openPost(p.linkId)}return false}
function resume(){const st=state(),a=st.approach;if(!a||currentWorld()?.id!==a.district||validClearance(a.linkId)||candidate06Owns(a.linkId))return false;return routePost(a.linkId,{resume:true})}
window.resumeControlPostApproachV12104=resume;
function interceptNode(nodeId){const w=currentWorld();if(!w)return false;const tr=w.transit?.find(x=>x.id===nodeId);if(!tr)return false;for(const lid of tr.linkIds||[]){const p=postForLink(lid,w.id);if(p){atPost(p)?openPost(lid):routePost(lid);return true}}return false}
window.interceptControlPostTransitNodeV12104=interceptNode;
function prepareTransit(l,current,mode){const p=postForLink(l?.id,current);if(!p)return{allowed:true};const c=validClearance(l.id);if(c)return{allowed:true,clearance:copy(c)};return{allowed:false,reason:`${p.profile.title} physically controls this crossing. Clear the post at the transit approach first.`}}
window.prepareControlPostTransitV12104=prepareTransit;
function commitTransit(ctx){const st=state(),c=validClearance(ctx?.linkId);if(!c)return false;c.consumed=true;c.consumedAt=nowMin();c.toDistrict=ctx.toDistrict;st.stats.crossings++;st.history.unshift({type:'crossing',linkId:ctx.linkId,fromDistrict:ctx.fromDistrict,toDistrict:ctx.toDistrict,method:c.method,at:nowMin()});st.history=st.history.slice(0,48);st.approach=null;st.engaged=null;window.saveGame?.(0,true);return true}
window.commitControlPostTransitV12104=commitTransit;

const prevDraw=window.drawLivingStreetsV134;if(prevDraw)window.drawLivingStreetsV134=function(ctx,w,W,H,t,hover){const r=prevDraw.apply(this,arguments);draw(ctx,w,W,H,t);return r};
const prevTap=window.handleLivingStreetTapV134;if(prevTap)window.handleLivingStreetTapV134=function(q){if(tap(q))return true;return prevTap.apply(this,arguments)};
const prevStep=window.onStreetStepV134;if(prevStep)window.onStreetStepV134=function(w){const r=prevStep.apply(this,arguments);detect();return r};
const prevInit=window.initOverworldV133;if(prevInit){const wrapped=function(){const r=prevInit.apply(this,arguments);setTimeout(()=>{resume();detect()},0);return r};window.initOverworldV133=wrapped;if(window.initOverworld===prevInit)window.initOverworld=wrapped}
const prevCombatHook=window.onTransitIncidentStreetCombatSettledV12104;window.onTransitIncidentStreetCombatSettledV12104=function(m,success){const a=prevCombatHook?.apply(this,arguments)||false,b=combatSettled(m,success);return a||b};
ensureStyle();window.CR_CITY_CONTROL_POSTS={version:VERSION,state,postsForWorld,postForLink,routePost,openPost,needsPost,prepareTransit,commitTransit};
})();
}''',encoding='utf-8')

# Insert the new module after Candidate 06 and before mission approaches.
manifest=root/'src/bootstrap/module-manifest.js'
s=manifest.read_text(encoding='utf-8')
entry="  'world.controlPosts':{path:'./src/world/district-control-posts-pwa12-104-city-candidate-07.js',kind:'module'},\n"
if 'world.controlPosts' not in s:
    needle="  'world.transitIncidents':{path:'./src/world/transit-incidents-pwa12-104-city-candidate-06.js',kind:'module'},\n"
    if needle not in s: raise SystemExit('Candidate 06 manifest seam missing')
    s=s.replace(needle,needle+entry,1)
    order="'world.accessEcology','world.transitIncidents','missions.approaches'"
    if order not in s: raise SystemExit('Candidate 06 manifest order seam missing')
    s=s.replace(order,"'world.accessEcology','world.transitIncidents','world.controlPosts','missions.approaches'",1)
manifest.write_text(s,encoding='utf-8')

# The rebundler uses SOURCE markers as its authoritative ordered source list.
bundle=root/'src/runtime/runtime-bundle.js'
s=bundle.read_text(encoding='utf-8')
inc='/* SOURCE: src/world/transit-incidents-pwa12-104-city-candidate-06.js */'
cp='/* SOURCE: src/world/district-control-posts-pwa12-104-city-candidate-07.js */'
mission='/* SOURCE: src/missions/contract-approaches-v13-4b.js */'
if inc not in s or mission not in s: raise SystemExit('Candidate 06 runtime-bundle seam missing')
if cp not in s:s=s.replace(mission,cp+'\n'+mission,1)
pos=[s.index(x) for x in (inc,cp,mission)]
if pos!=sorted(pos): raise SystemExit(f'Candidate 07 runtime source order invalid: {pos}')
bundle.write_text(s,encoding='utf-8')

# Patch the actual lexical transit authority so ordinary free-roam transit cannot bypass
# a physical post merely because renderTransitModalV133 calls its local travel function.
p=root/'src/world/district-worlds-v13-3.js'
s=p.read_text(encoding='utf-8')
needle=" const ecology=window.prepareTransitAccessEcologyV12104?.(link,current,mode)||null;if(ecology&&ecology.allowed===false){toast(ecology.reason||ecology.label||'Route closed by live district conditions.');return false}"
repl=" const controlPost=window.prepareControlPostTransitV12104?.(link,current,mode)||null;if(controlPost&&controlPost.allowed===false){toast(controlPost.reason||'A physical control post blocks this crossing.');return false}\n"+needle
if 'prepareControlPostTransitV12104' not in s:
    if needle not in s: raise SystemExit('Candidate 05 transit ecology authority seam missing')
    s=s.replace(needle,repl,1)
needle2="window.onDistrictTransitCompleteV12104?.({linkId:link.id,fromDistrict:current,toDistrict:to.district,mode});window.commitTransitAccessEcologyV12104?.(ecology,{linkId:link.id,fromDistrict:current,toDistrict:to.district,mode});saveGame(0,true);return true"
repl2="window.onDistrictTransitCompleteV12104?.({linkId:link.id,fromDistrict:current,toDistrict:to.district,mode});window.commitTransitAccessEcologyV12104?.(ecology,{linkId:link.id,fromDistrict:current,toDistrict:to.district,mode});window.commitControlPostTransitV12104?.({linkId:link.id,fromDistrict:current,toDistrict:to.district,mode});saveGame(0,true);return true"
if 'commitControlPostTransitV12104' not in s:
    if needle2 not in s: raise SystemExit('Candidate 05 transit completion seam missing')
    s=s.replace(needle2,repl2,1)
needle3="function openTransitNodeV133(id){const tr=currentDistrictV133().transit.find(x=>x.id===id);if(!tr)return false;renderTransitModalV133(tr);return true}"
repl3="function openTransitNodeV133(id){const tr=currentDistrictV133().transit.find(x=>x.id===id);if(!tr)return false;if(window.interceptControlPostTransitNodeV12104?.(id))return true;renderTransitModalV133(tr);return true}"
if 'interceptControlPostTransitNodeV12104' not in s:
    if needle3 not in s: raise SystemExit('canonical openTransitNodeV133 seam missing')
    s=s.replace(needle3,repl3,1)
p.write_text(s,encoding='utf-8')

print('applied Candidate 07 persistent physical District Control Posts')
