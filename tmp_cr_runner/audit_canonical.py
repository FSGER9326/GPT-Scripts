from pathlib import Path
import urllib.request, zipfile, hashlib, re, os
URL=os.environ['CR_SOURCE_URL']; EXPECTED_SHA='6002ed124aadd1690f0da9170d999cd0e30ed965cca1e04f654efa89d9fd7059'
out=Path('cr_audit'); out.mkdir(exist_ok=True); zp=out/'canonical.zip'
req=urllib.request.Request(URL,headers={'User-Agent':'Mozilla/5.0 Chrome/140 Safari/537.36','Accept':'*/*','Cache-Control':'no-cache'})
with urllib.request.urlopen(req,timeout=60) as r, zp.open('wb') as f:
    while (chunk:=r.read(1024*1024)): f.write(chunk)
sha=hashlib.sha256(zp.read_bytes()).hexdigest(); print('SHA',sha); assert sha==EXPECTED_SHA
with zipfile.ZipFile(zp) as z:
    names=z.namelist(); root=next(n[:-10] for n in names if n.endswith('/index.html'))
    targets=['tools/rebundle_runtime.py','tests/pwa12_39_js_bundle_perf_contract.py','tests/pwa12_37_css_bundle_perf_contract.py','src/bootstrap/bootstrap.js','src/runtime/runtime.js']
    for rel in targets:
        n=root+rel
        if n in names: print(f'\n=== BEGIN {rel} ===\n'+z.read(n).decode('utf-8','replace')+f'\n=== END {rel} ===')
    print('\n=== DIAGNOSTIC RUNNER HITS ===')
    for n in names:
        if not n.endswith('.js'): continue
        txt=z.read(n).decode('utf-8','replace')
        if 'runDiagnosticsV135' in txt and ('runAll' in txt or 'diagnostic' in txt.lower()):
            rel=n[len(root):] if n.startswith(root) else n
            print('FILE',rel)
            for i,l in enumerate(txt.splitlines()):
                if 'runDiagnosticsV13' in l or 'diagnostic' in l.lower(): print(f'{i+1}: {l}')
print('AUDIT_COMPLETE')