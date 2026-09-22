#!/usr/bin/env python3
import json,re,sys,zipfile
from pathlib import Path

ZIP=Path(sys.argv[1] if len(sys.argv)>1 else 'canonical.zip')
OUT=Path(sys.argv[2] if len(sys.argv)>2 else 'cr_city_audit.json')
TEXT_EXT={'.js','.mjs','.json','.html','.css','.md','.txt','.py'}
path_re=re.compile(r'(city|district|world|travel|route|location|contact|encounter|street|heat|security|save|persist|state|mission|stage)',re.I)
line_re=re.compile(r'(pendingPath|travel|route|district|world|location|contact|encounter|heat|security|saveGame|loadGame|city|stage|mission|pathfind|move|transit)',re.I)

def decode(b):
    try:return b.decode('utf-8')
    except:return b.decode('utf-8','replace')

with zipfile.ZipFile(ZIP) as z:
    names=z.namelist()
    index=next((n for n in names if n.endswith('/index.html')),None)
    if not index: raise SystemExit('root index.html not found')
    root=index[:-len('index.html')]
    meta={}
    try: meta=json.loads(decode(z.read(root+'build-meta.json')))
    except Exception as e: meta={'error':str(e)}
    relevant=[n for n in names if path_re.search(n) and Path(n).suffix.lower() in TEXT_EXT]
    hits=[]
    summaries=[]
    for n in relevant:
        try: lines=decode(z.read(n)).splitlines()
        except Exception: continue
        local=[]
        for i,line in enumerate(lines):
            if line_re.search(line):
                local.append({'line':i+1,'text':line[:500],'before':lines[max(0,i-2):i],'after':lines[i+1:i+3]})
            if len(local)>=30: break
        if local:
            summaries.append({'path':n[len(root):] if n.startswith(root) else n,'lines':len(lines),'hits':len(local)})
            for h in local[:12]:
                hits.append({'path':n[len(root):] if n.startswith(root) else n,**h})
    # high-value known architecture files / build manifests
    wanted=[]
    for n in names:
        rel=n[len(root):] if n.startswith(root) else n
        if rel in {'index.html','build-meta.json','tools/build_pwa11.py','src/bootstrap/module-manifest.js','src/bootstrap/compatibility-manifest.js'}:
            wanted.append(rel)
        elif re.search(r'(district-world|city.*\.js$|world.*\.js$|travel.*\.js$|contact.*\.js$|encounter.*\.js$|save.*\.js$|persist.*\.js$)',rel,re.I):
            wanted.append(rel)
    report={'archive_files':len(names),'root':root,'meta':meta,'relevant_paths':len(relevant),'summaries':summaries[:150],'hits':hits[:500],'wanted':wanted[:120]}
    OUT.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('CR_CITY_AUDIT_META '+json.dumps(meta,sort_keys=True))
    print('CR_CITY_AUDIT_ROOT '+root)
    print('CR_CITY_AUDIT_FILES '+str(len(names)))
    print('CR_CITY_AUDIT_WANTED '+json.dumps(wanted[:120]))
    print('CR_CITY_AUDIT_SUMMARY '+json.dumps(summaries[:80]))
    for h in hits[:220]:
        print('CR_CITY_HIT '+json.dumps(h,ensure_ascii=False))
