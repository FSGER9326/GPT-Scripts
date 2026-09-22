from pathlib import Path
import sys,re
root=Path(sys.argv[1])
patterns=['startNewGame','CLASSES','BACKGROUNDS','renderInventory','createCombatUnits','buildGrid','selectedCrewIndex','crew-body']
for rel in ['src/runtime/runtime-bundle.js','src/runtime/runtime.js','index.html']:
    p=root/rel
    if not p.exists(): continue
    text=p.read_text(errors='replace'); lines=text.splitlines()
    print('\n###',rel)
    for pat in patterns:
        hits=[i for i,l in enumerate(lines) if pat in l]
        print('\nPATTERN',pat,'HITS',len(hits))
        for i in hits[:8]:
            print('\n'.join(f'{j+1}: {lines[j]}' for j in range(max(0,i-4),min(len(lines),i+9))))
            print('---')
print('\n### TEST USES')
for p in sorted((root/'tests').glob('*.py')):
    text=p.read_text(errors='replace')
    if 'startNewGame' in text or 'createCombatUnits' in text or 'renderInventory(' in text:
        print('\nFILE',p.name)
        lines=text.splitlines()
        for i,l in enumerate(lines):
            if any(x in l for x in ('startNewGame','createCombatUnits','renderInventory(')):
                print('\n'.join(f'{j+1}: {lines[j]}' for j in range(max(0,i-3),min(len(lines),i+7))))
                print('---')
