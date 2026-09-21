from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
src=(root/'src/legacy/mercenary-intelligence-v8.js').read_text(encoding='utf-8')
bundle=(root/'src/runtime/runtime-bundle.js').read_text(encoding='utf-8')

need=[
    'function enemyPressureStateV134()',
    'function enemyPressurePenaltyV134(enemy,target)',
    'function chooseEnemyTargetV134(enemy,players)',
    'function reserveEnemyPressureV134(enemy,target',
    "kind==='lethal'?56:24",
    "case 'Heavy':return .65",
    "case 'Brute':return .55",
    "target._lastKnownV133",
    "targetRef:contact?null:target",
    "clearEnemyPressureForV134(enemy);pruneEnemyPressureV134();",
    "target=chooseEnemyTargetV134(enemy,direct);reserveEnemyPressureV134(enemy,target);",
    "const attackTarget=direct.length?chooseEnemyTargetV134(enemy,direct):null;",
    "if(attackTarget)reserveEnemyPressureV134(enemy,attackTarget);",
    "forceKind:'pressure'",
    ".v133-contact-cue.pin",
    ".v133-contact-cue.fin",
    "intent==='PIN'",
    "intent==='FIN'",
]
for token in need:
    assert token in src, f'missing source contract: {token}'
    assert token in bundle, f'missing runtime-bundle contract: {token}'

assert src.count('function enemyPressureStateV134()')==1
assert src.count('function chooseEnemyTargetV134(enemy,players)')==1
assert src.count('enemyAITakeTurn=async function(enemy)')==1
assert 'Game.enemyPressureV134={grid:Game.grid,units:Game.units,reservations:new Map()}' in src
assert "kind==='lethal'?2:Math.max(2,Math.min(4,Math.ceil(hostileCount/2)))" in src
assert "if(dist===1&&hasSkill(target,'s_parry'))return 0;" in src
assert "if(hasSkill(target,'s_undying')&&!target._undyingUsed)return 0;" in src
assert "if(!contact)setEnemyContactCueV133(enemy,kind==='lethal'?'FIN':'PIN');" in src
assert 'saveVersion' not in src[src.index('// PWA12.134:'):src.index('// PWA12.107:')]
print('PASS PWA12.134 target-pressure source/runtime contract')
