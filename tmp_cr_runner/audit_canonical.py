from pathlib import Path
import urllib.request, zipfile, hashlib, re, json, os
URL=os.environ['CR_SOURCE_URL']
EXPECTED_SHA='6002ed124aadd1690f0da9170d999cd0e30ed965cca1e04f654efa89d9fd7059'
out=Path('cr_audit'); out.mkdir(exist_ok=True)
zp=out/'canonical.zip'
req=urllib.request.Request(URL,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/140 Safari/537.36','Accept':'*/*','Cache-Control':'no-cache'})
with urllib.request.urlopen(req,timeout=60) as r, zp.open('wb') as f:
    while True:
        chunk=r.read(1024*1024)
        if not chunk: break
        f.write(chunk)
data=zp.read_bytes(); sha=hashlib.sha256(data).hexdigest()
print('CANONICAL_BYTES',len(data)); print('CANONICAL_SHA256',sha)
if sha!=EXPECTED_SHA: raise SystemExit('canonical sha mismatch')
with zipfile.ZipFile(zp) as z:
    names=z.namelist(); root=next((n[:-10] for n in names if n.endswith('/index.html')), '')
    print('ROOT',root,'FILES',len(names))
    for rel in ['tools/build_pwa11.py','src/bootstrap/module-manifest.js','src/bootstrap/compatibility-manifest.js','build-meta.json','service-worker.js','index.html']:
        n=root+rel
        if n in names:
            txt=z.read(n).decode('utf-8','replace')
            print('\n=== BEGIN',rel,'===\n'+txt+'\n=== END',rel,'===')
    print('\n=== APPLY-SKILL WRITERS ===')
    for n in names:
        if not n.endswith('.js'): continue
        try: txt=z.read(n).decode('utf-8')
        except: continue
        if re.search(r'applySkillsToUnit\s*=\s*function|function\s+applySkillsToUnit',txt):
            print(n[len(root):] if n.startswith(root) else n)
print('AUDIT_COMPLETE')