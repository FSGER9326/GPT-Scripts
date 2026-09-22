from pathlib import Path
import urllib.request, zipfile, hashlib, re, json, sys, os, textwrap
URL=os.environ['CR_SOURCE_URL']
EXPECTED_SHA='6002ed124aadd1690f0da9170d999cd0e30ed965cca1e04f654efa89d9fd7059'
out=Path('cr_audit'); out.mkdir(exist_ok=True)
zp=out/'canonical.zip'
urllib.request.urlretrieve(URL,zp)
data=zp.read_bytes(); sha=hashlib.sha256(data).hexdigest()
print('CANONICAL_BYTES',len(data)); print('CANONICAL_SHA256',sha)
if sha!=EXPECTED_SHA: raise SystemExit('canonical sha mismatch')
with zipfile.ZipFile(zp) as z:
    names=z.namelist()
    root=next((n[:-10] for n in names if n.endswith('/index.html')), '')
    print('ROOT',root,'FILES',len(names))
    pats=('weapon','armory','progress','workshop','company','save','persist','bootstrap','runtime-bundle','build_pwa','combat')
    for n in names:
        rel=n[len(root):] if n.startswith(root) else n
        if any(p in rel.lower() for p in pats) and rel.endswith(('.js','.py','.json','.html','.css')):
            print('PATH',rel)
    tokens=['function applySkillsToUnit','applySkillsToUnit =','renderWeaponBenchV11','weaponMods','safehouse.workshop','Game.salvage','function advanceTime','const advanceTime','function saveGame','activeMission','module-manifest','runtime-bundle']
    print('\n=== TOKEN HITS ===')
    for n in names:
        if not n.endswith(('.js','.py','.html')): continue
        try: txt=z.read(n).decode('utf-8')
        except: continue
        rel=n[len(root):] if n.startswith(root) else n
        lines=txt.splitlines()
        found=[]
        for i,line in enumerate(lines):
            if any(t in line for t in tokens):
                a=max(0,i-3); b=min(len(lines),i+6)
                found.append((i+1,'\n'.join(f'{j+1}: {lines[j]}' for j in range(a,b))))
        if found:
            print('\nFILE',rel)
            for ln,snip in found[:20]: print(snip,'\n---')
    # inspect bundle source markers and builder arrays
    for rel in ['src/runtime/runtime-bundle.js','src/styles/runtime-bundle.css','tools/build_pwa11.py','src/bootstrap/module-manifest.js','src/bootstrap/compatibility-manifest.js','index.html','build-meta.json','precache-manifest.js']:
        n=root+rel
        if n in names:
            txt=z.read(n).decode('utf-8','replace')
            print('\n=== FILE SUMMARY',rel,'bytes',len(txt.encode()),'===')
            if 'runtime-bundle' in rel:
                marks=re.findall(r'/\* SOURCE: ([^*]+?) \*/',txt)
                print('SOURCE_MARKERS',json.dumps(marks[-30:],ensure_ascii=False))
            elif rel.endswith('build_pwa11.py'):
                for i,line in enumerate(txt.splitlines()):
                    if 'src/' in line and any(k in line for k in ('weapon','company','style','runtime','armory')):
                        print(f'{i+1}: {line}')
            elif rel.endswith('module-manifest.js'):
                print('\n'.join(txt.splitlines()[:260]))
            elif rel.endswith('compatibility-manifest.js'):
                print('\n'.join(txt.splitlines()[:260]))
            elif rel=='index.html':
                for i,line in enumerate(txt.splitlines()):
                    if 'CR14_BUILD_VERSION' in line or 'runtime-bundle' in line: print(f'{i+1}: {line}')
            elif rel=='build-meta.json': print(txt)
            elif rel=='precache-manifest.js': print('PRECACHE_ENTRIES',len(re.findall(r'"\./[^\"]+"',txt)))
print('AUDIT_COMPLETE')