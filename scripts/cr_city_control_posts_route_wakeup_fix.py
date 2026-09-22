from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve()
mod=root/'src/world/district-control-posts-pwa12-104-city-candidate-07.js'
s=mod.read_text(encoding='utf-8')
old="""function routePost(linkId,{resume=false}={}){
 const p=postForLink(linkId);if(!p||!Game.ovPlayer)return false;if(atPost(p))return openPost(linkId);const path=window.findDistrictPathV133?.(Game.ovPlayer,{x:p.x,y:p.y},currentWorld());if(!path||path.length<2){window.streetToastV134?.('NO STREET ROUTE TO CONTROL POST');return false}Game.pendingPath=path;Game._v133TravelTarget={kind:'v12104controlpost',id:p.id,linkId:p.linkId,label:`CONTROL POST // ${p.profile.title}`};if(Game.ovCamera)Game.ovCamera.follow=true;const st=state();st.approach={district:p.district,linkId:p.linkId,nodeId:p.nodeId,at:st.approach?.at||nowMin()};if(!resume){window.streetToastV134?.(`${p.profile.title} · PHYSICAL APPROACH`);window.saveGame?.(0,true)}return true
}"""
new="""function routePost(linkId,{resume=false}={}){
 const p=postForLink(linkId);if(!p||!Game.ovPlayer)return false;if(atPost(p))return openPost(linkId);
 /* Route through canonical transit-node navigation rather than assigning pendingPath
    directly. Besides using the same A* graph, this wakes the frozen overworld loop,
    updates its route/camera state and preserves canonical long-route behavior. */
 const ok=window.routeToTransitNodeV133?.(p.nodeId);if(!ok){window.streetToastV134?.('NO STREET ROUTE TO CONTROL POST');return false}
 Game._v133TravelTarget={kind:'v12104controlpost',id:p.id,linkId:p.linkId,label:`CONTROL POST // ${p.profile.title}`};const st=state();st.approach={district:p.district,linkId:p.linkId,nodeId:p.nodeId,at:st.approach?.at||nowMin()};if(!resume){window.streetToastV134?.(`${p.profile.title} · PHYSICAL APPROACH`);window.saveGame?.(0,true)}return true
}"""
if new not in s:
    if old not in s:raise SystemExit('Candidate 07 direct pendingPath routing seam missing')
    s=s.replace(old,new,1)
mod.write_text(s,encoding='utf-8')

# Keep the contract aligned with the stronger implementation: the route is delegated to
# canonical routeToTransitNodeV133, whose implementation owns A*, pendingPath, camera and
# scheduleOverworldFrameV133.
test=root/'tests/pwa12_104_city_control_posts_contract.py'
if test.exists():
    t=test.read_text(encoding='utf-8')
    oldc="ck('physical approach uses canonical A-star pathfinder',\"findDistrictPathV133\" in mod)\nck('physical approach writes Game.pendingPath',\"Game.pendingPath=path\" in mod)"
    newc="ck('physical approach delegates to canonical transit-node route authority',\"routeToTransitNodeV133\" in mod)\nck('physical approach does not hand-roll pendingPath movement',\"Game.pendingPath=path\" not in mod)"
    if newc not in t:
        if oldc not in t:raise SystemExit('Candidate 07 contract routing assertions seam missing')
        t=t.replace(oldc,newc,1)
    test.write_text(t,encoding='utf-8')
print('Candidate 07 control-post routing now uses canonical transit-node routing and wakes the overworld loop')
