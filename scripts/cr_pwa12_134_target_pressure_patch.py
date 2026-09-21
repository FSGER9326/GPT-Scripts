from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / 'src/legacy/mercenary-intelligence-v8.js'
text = path.read_text(encoding='utf-8')

anchor = "// PWA12.107: route-aware enemy movement for irregular arenas.  The old local\n"
assert text.count(anchor) == 1, 'PWA12.134 insertion anchor missing or ambiguous'

block = r'''// PWA12.134: short-lived pressure / lethal reservations. These are squad intent,
// not knowledge: they can only reference a target the current AI was already allowed to
// choose through PWA12.133 observation/contact rules. The board is transient and bound
// to exact combat identity, so stage replacement/save-load cannot inherit stale claims.
function enemyPressureStateV134(){
  let s=Game.enemyPressureV134;
  if(!s||s.grid!==Game.grid||s.units!==Game.units){
    s=Game.enemyPressureV134={grid:Game.grid,units:Game.units,reservations:new Map()};
  }
  return s;
}
function enemyUnitKeyV134(enemy){
  if(!enemy)return null;const idx=Game.units?.indexOf(enemy)??-1;
  return `${idx}:${enemy.name||enemy.className||'ENEMY'}`;
}
function enemyPressureTargetKeyV134(target){
  if(!target)return null;return target._enemyContactKeyV133||enemyContactKeyV133(target);
}
function enemyPressureTtlV134(kind='pressure'){
  const hostileCount=(Game.units||[]).filter(u=>u.team==='enemy'&&u.hp>0&&!u.dead).length;
  return kind==='lethal'?2:Math.max(2,Math.min(4,Math.ceil(hostileCount/2)));
}
function pruneEnemyPressureV134(){
  const s=enemyPressureStateV134(),now=enemyContactStateV133().epoch;
  for(const [key,r] of s.reservations){
    const staleEnemy=!r?.enemyRef||!Game.units?.includes(r.enemyRef)||r.enemyRef.hp<=0||r.enemyRef.dead;
    const staleTarget=r?.targetRef&&(!Game.units?.includes(r.targetRef)||r.targetRef.hp<=0||r.targetRef.dead);
    if(!r||now>r.expiresAt||staleEnemy||staleTarget)s.reservations.delete(key);
  }
  return s;
}
function clearEnemyPressureForV134(enemy){
  const key=enemyUnitKeyV134(enemy);if(key)enemyPressureStateV134().reservations.delete(key);
}
function enemyPressureDisciplineV134(enemy){
  switch(enemy?.className){
    case 'Boss':return 1.1;
    case 'Drone':case 'Enforcer':return 1;
    case 'Guard':return .85;
    case 'Heavy':return .65;
    case 'Brute':return .55;
    default:return .8;
  }
}
function enemyGuaranteedHitV134(enemy,target){
  if(!enemy||!target||target._lastKnownV133||target.hp<=0)return 0;
  const dist=Math.abs(enemy.x-target.x)+Math.abs(enemy.y-target.y);
  if(dist>(enemy.range||1)||!hasLOS(enemy,target))return 0;
  // Do not reserve a guaranteed finish when an existing defensive build can negate it.
  if(dist===1&&hasSkill(target,'s_parry'))return 0;
  if(hasSkill(target,'s_undying')&&!target._undyingUsed)return 0;
  const cover=coverBonusFor(target,enemy)||0;
  return Math.max(1,Math.floor(enemy.damage||1)-(target.armor||0)-cover);
}
function enemyPressurePenaltyV134(enemy,target){
  const s=pruneEnemyPressureV134(),targetKey=enemyPressureTargetKeyV134(target),self=enemyUnitKeyV134(enemy);
  if(!targetKey)return 0;let raw=0;
  for(const [key,r] of s.reservations)if(key!==self&&r.targetKey===targetKey)raw+=r.kind==='lethal'?56:24;
  return Math.min(90,raw*enemyPressureDisciplineV134(enemy));
}
function chooseEnemyTargetV134(enemy,players){
  let best=null,bestScore=-Infinity;
  for(const p of players||[]){
    if(!p||p.hp<=0)continue;
    const dist=Math.abs(enemy.x-p.x)+Math.abs(enemy.y-p.y),shootable=dist<=(enemy.range||1)&&hasLOS(enemy,p);
    const route=shootable?0:enemyPlanningPathDistanceV116(cellAt(enemy.x,enemy.y),p,enemy);
    let score=scoreThreatV8(enemy,p)-enemyPressurePenaltyV134(enemy,p);
    if(!shootable){if(!Number.isFinite(route))score-=10000;else score-=Math.min(120,route*3)}
    if(score>bestScore){bestScore=score;best=p}
  }
  return best;
}
function reserveEnemyPressureV134(enemy,target,{contact=false,forceKind=null}={}){
  const s=pruneEnemyPressureV134(),enemyKey=enemyUnitKeyV134(enemy),targetKey=enemyPressureTargetKeyV134(target);
  if(!enemyKey||!targetKey){clearEnemyPressureForV134(enemy);return null}
  const kind=forceKind||(!contact&&enemyGuaranteedHitV134(enemy,target)>=target.hp?'lethal':'pressure');
  const r={enemyKey,targetKey,kind,expiresAt:enemyContactStateV133().epoch+enemyPressureTtlV134(kind),enemyRef:enemy,targetRef:contact?null:target};
  s.reservations.set(enemyKey,r);
  if(!contact)setEnemyContactCueV133(enemy,kind==='lethal'?'FIN':'PIN');
  return r;
}

'''
text = text.replace(anchor, block + anchor, 1)

old_style = "style.textContent='.v133-contact-cue{position:absolute;left:50%;top:-8px;transform:translateX(-50%);padding:1px 3px;border-radius:2px;background:rgba(5,12,16,.92);border:1px solid rgba(255,172,72,.72);color:#ffd39a;font:700 6px/1.15 Orbitron,system-ui;letter-spacing:.35px;white-space:nowrap;z-index:8;box-shadow:0 0 7px rgba(255,172,72,.28)}.v133-contact-cue.scan{border-color:rgba(123,219,228,.66);color:#bceff2}';"
new_style = "style.textContent='.v133-contact-cue{position:absolute;left:50%;top:-8px;transform:translateX(-50%);padding:1px 3px;border-radius:2px;background:rgba(5,12,16,.92);border:1px solid rgba(255,172,72,.72);color:#ffd39a;font:700 6px/1.15 Orbitron,system-ui;letter-spacing:.35px;white-space:nowrap;z-index:8;box-shadow:0 0 7px rgba(255,172,72,.28)}.v133-contact-cue.scan{border-color:rgba(123,219,228,.66);color:#bceff2}.v133-contact-cue.pin{border-color:rgba(160,145,255,.8);color:#d6d0ff}.v133-contact-cue.fin{border-color:rgba(255,88,110,.86);color:#ffb4c0;box-shadow:0 0 7px rgba(255,50,85,.35)}';"
assert text.count(old_style) == 1, 'contact cue style anchor changed'
text = text.replace(old_style, new_style, 1)

old_toggle = "cue.classList.toggle('scan',intent==='SCAN');cue.textContent=intent;"
new_toggle = "cue.classList.toggle('scan',intent==='SCAN');cue.classList.toggle('pin',intent==='PIN');cue.classList.toggle('fin',intent==='FIN');cue.textContent=intent;"
assert text.count(old_toggle) == 1, 'contact cue class anchor changed'
text = text.replace(old_toggle, new_toggle, 1)

old_activation = "  beginEnemyContactActivationV133();\n  if(enemy.disabledTurns>0)"
new_activation = "  beginEnemyContactActivationV133();\n  clearEnemyPressureForV134(enemy);pruneEnemyPressureV134();\n  if(enemy.disabledTurns>0)"
assert text.count(old_activation) == 1, 'enemy activation anchor changed'
text = text.replace(old_activation, new_activation, 1)

old_target = "  if(direct.length){setEnemyContactCueV133(enemy,'');target=chooseEnemyTargetV118(enemy,direct);}\n  else{\n    contact=chooseEnemyContactV133(enemy);target=enemyContactProxyV133(contact);contactMode=!!target;\n    if(!target){setEnemyContactCueV133(enemy,'SCAN');enemy.overwatch=(enemy.range||0)>1&&enemy.ap>0;logMsg(`${enemy.name} scans — no confirmed contact.`,'sys');finishEnemyTurnV121(session);return}\n    setEnemyContactCueV133(enemy,'CONTACT');logMsg(`${enemy.name} advances on a last-known contact.`,'sys');\n  }"
new_target = "  if(direct.length){target=chooseEnemyTargetV134(enemy,direct);reserveEnemyPressureV134(enemy,target);}\n  else{\n    contact=chooseEnemyContactV133(enemy);target=enemyContactProxyV133(contact);contactMode=!!target;\n    if(!target){clearEnemyPressureForV134(enemy);setEnemyContactCueV133(enemy,'SCAN');enemy.overwatch=(enemy.range||0)>1&&enemy.ap>0;logMsg(`${enemy.name} scans — no confirmed contact.`,'sys');finishEnemyTurnV121(session);return}\n    reserveEnemyPressureV134(enemy,target,{contact:true});setEnemyContactCueV133(enemy,'CONTACT');logMsg(`${enemy.name} advances on a last-known contact.`,'sys');\n  }"
assert text.count(old_target) == 1, 'initial target selection anchor changed'
text = text.replace(old_target, new_target, 1)

old_final = "  const attackTarget=direct.length?chooseEnemyTargetV118(enemy,direct):null;\n  if(!attackTarget&&contactMode&&enemyAtClearedContactV133(enemy,contact)){\n    clearEnemyContactV133(contact);setEnemyContactCueV133(enemy,'SCAN');logMsg(`${enemy.name} clears the last-known position and scans.`,'sys');\n  }\n  if(enemy.hp>0&&!enemy.dead&&attackTarget){const dist=Math.abs(enemy.x-attackTarget.x)+Math.abs(enemy.y-attackTarget.y);if(dist<=enemy.range&&hasLOS(enemy,attackTarget)&&enemy.ap>0){basicAttack(enemy,attackTarget);await sleep(340);if(!enemyTurnSessionCurrentV121(session))return}else if((enemy.range||0)>1&&enemy.ap>0){enemy.overwatch=true;logMsg(`${enemy.name} takes overwatch.`,'sys')}}"
new_final = "  const attackTarget=direct.length?chooseEnemyTargetV134(enemy,direct):null;\n  if(attackTarget)reserveEnemyPressureV134(enemy,attackTarget);\n  if(!attackTarget&&contactMode&&enemyAtClearedContactV133(enemy,contact)){\n    clearEnemyContactV133(contact);clearEnemyPressureForV134(enemy);setEnemyContactCueV133(enemy,'SCAN');logMsg(`${enemy.name} clears the last-known position and scans.`,'sys');\n  }\n  if(enemy.hp>0&&!enemy.dead&&attackTarget){const dist=Math.abs(enemy.x-attackTarget.x)+Math.abs(enemy.y-attackTarget.y);if(dist<=enemy.range&&hasLOS(enemy,attackTarget)&&enemy.ap>0){basicAttack(enemy,attackTarget);await sleep(340);if(!enemyTurnSessionCurrentV121(session))return;if(attackTarget.hp>0)reserveEnemyPressureV134(enemy,attackTarget,{forceKind:'pressure'});else pruneEnemyPressureV134()}else if((enemy.range||0)>1&&enemy.ap>0){enemy.overwatch=true;logMsg(`${enemy.name} takes overwatch.`,'sys')}}"
assert text.count(old_final) == 1, 'final target/attack anchor changed'
text = text.replace(old_final, new_final, 1)

path.write_text(text, encoding='utf-8')
print('patched', path)
