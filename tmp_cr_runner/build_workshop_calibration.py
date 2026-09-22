from pathlib import Path
import urllib.request, zipfile, hashlib, os, re, subprocess, json, shutil, textwrap

URL=os.environ['CR_SOURCE_URL']
EXPECTED_SHA='6002ed124aadd1690f0da9170d999cd0e30ed965cca1e04f654efa89d9fd7059'
VERSION='14.0.0-pwa.12.104-workshop-calibration-candidate.02'
OUT=Path('cr_build')
ARCHIVE=OUT/'canonical.zip'
CANDIDATE=OUT/'Chrome_Requiem_v14_PWA_pwa12_104_WORKSHOP_CALIBRATION_CANDIDATE_02_source'
RUNNER=Path('tmp_cr_runner')

def replace_once(text,old,new,label):
    if old not in text: raise RuntimeError(f'{label}: anchor not found')
    if text.count(old)!=1: raise RuntimeError(f'{label}: anchor count {text.count(old)}')
    return text.replace(old,new,1)

def fetch():
    OUT.mkdir(exist_ok=True)
    req=urllib.request.Request(URL,headers={'User-Agent':'Mozilla/5.0 Chrome/140 Safari/537.36','Accept':'*/*','Cache-Control':'no-cache'})
    with urllib.request.urlopen(req,timeout=90) as r, ARCHIVE.open('wb') as f:
        while (chunk:=r.read(1024*1024)): f.write(chunk)
    sha=hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
    print('CANONICAL_BYTES',ARCHIVE.stat().st_size); print('CANONICAL_SHA256',sha)
    if sha!=EXPECTED_SHA: raise RuntimeError(f'canonical SHA mismatch {sha}')

def extract():
    if CANDIDATE.exists(): shutil.rmtree(CANDIDATE)
    tmp=OUT/'extract'
    if tmp.exists(): shutil.rmtree(tmp)
    tmp.mkdir()
    with zipfile.ZipFile(ARCHIVE) as z: z.extractall(tmp)
    roots=[p for p in tmp.iterdir() if p.is_dir() and (p/'index.html').exists()]
    if len(roots)!=1: raise RuntimeError(f'unexpected archive roots: {roots}')
    shutil.move(str(roots[0]),str(CANDIDATE)); shutil.rmtree(tmp)
    meta=json.loads((CANDIDATE/'build-meta.json').read_text())
    assert meta['version']=='14.0.0-pwa.12.104-street-contact-support',meta
    assert meta['buildHash']=='4313da4acd4c324a7672c36e',meta
    assert meta['schemaVersion']==14,meta
    print('BASELINE_META_OK',json.dumps(meta,sort_keys=True))

def write_sources():
    js_path=CANDIDATE/'src/progression/workshop-calibration-v14.js'; js_path.parent.mkdir(parents=True,exist_ok=True)
    js_path.write_text((RUNNER/'workshop-calibration-v14.js').read_text(),encoding='utf-8')
    css_path=CANDIDATE/'src/styles/35-v14-pwa12-104-workshop-calibration.css'
    css_path.write_text((RUNNER/'workshop-calibration-v14.css').read_text(),encoding='utf-8')

def patch_architecture():
    p=CANDIDATE/'src/bootstrap/module-manifest.js'; s=p.read_text()
    s=replace_once(s,"  'company':{path:'./src/company/company-foundation-v13-5.js',kind:'module'},\n  'visuals':", "  'company':{path:'./src/company/company-foundation-v13-5.js',kind:'module'},\n  'progression.workshopCalibration':{path:'./src/progression/workshop-calibration-v14.js',kind:'module'},\n  'visuals':",'module manifest entry')
    s=replace_once(s,"'world.livingStreets','missions.approaches','company','visuals','runtime'", "'world.livingStreets','missions.approaches','company','progression.workshopCalibration','visuals','runtime'",'module order')
    p.write_text(s,encoding='utf-8')
    p=CANDIDATE/'src/bootstrap/compatibility-manifest.js'; s=p.read_text()
    s=replace_once(s,"  runDiagnosticsV136:'v13.6 visual identity diagnostics',", "  runDiagnosticsV14Calibration:'v14 workshop calibration diagnostics',\n  WorkshopCalibrationV14:'v14 workshop calibration API',\n  runDiagnosticsV136:'v13.6 visual identity diagnostics',",'compat exports')
    p.write_text(s,encoding='utf-8')
    p=CANDIDATE/'src/bootstrap/bootstrap.js'; s=p.read_text()
    s=replace_once(s,"const names=['runDiagnosticsV136','runDiagnosticsV135'", "const names=['runDiagnosticsV14Calibration','runDiagnosticsV136','runDiagnosticsV135'",'diagnostic runner')
    p.write_text(s,encoding='utf-8')

def patch_bundle_policy():
    p=CANDIDATE/'tools/build_pwa11.py'; s=p.read_text()
    s=replace_once(s,"    'src/company/company-foundation-v13-5.js',\n", "    'src/company/company-foundation-v13-5.js',\n    'src/progression/workshop-calibration-v14.js',\n",'JS precache exclusion')
    s=replace_once(s,"    'src/styles/33-v14-pwa12-81-grounded-scene.css',\n", "    'src/styles/33-v14-pwa12-81-grounded-scene.css',\n    'src/styles/35-v14-pwa12-104-workshop-calibration.css',\n",'CSS precache exclusion')
    p.write_text(s,encoding='utf-8')
    p=CANDIDATE/'src/runtime/runtime-bundle.js'; s=p.read_text(); anchor='/* SOURCE: src/visuals/visual-identity-v13-6.js */'
    insert='/* SOURCE: src/progression/workshop-calibration-v14.js */\n'+(CANDIDATE/'src/progression/workshop-calibration-v14.js').read_text().rstrip()+'\n\n'
    s=replace_once(s,anchor,insert+anchor,'JS bundle insertion'); p.write_text(s,encoding='utf-8')
    p=CANDIDATE/'src/styles/runtime-bundle.css'; s=p.read_text()
    if '/* SOURCE: src/styles/35-v14-pwa12-104-workshop-calibration.css */' in s: raise RuntimeError('CSS marker already present')
    s=s.rstrip()+"\n\n/* SOURCE: src/styles/35-v14-pwa12-104-workshop-calibration.css */\n"+(CANDIDATE/'src/styles/35-v14-pwa12-104-workshop-calibration.css').read_text().rstrip()+"\n"
    p.write_text(s,encoding='utf-8')
    subprocess.run(['python','tools/rebundle_runtime.py'],cwd=CANDIDATE,check=True)

def add_contract():
    contract=r'''from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1]
js=(ROOT/'src/progression/workshop-calibration-v14.js').read_text()
css=(ROOT/'src/styles/35-v14-pwa12-104-workshop-calibration.css').read_text()
bundle=(ROOT/'src/runtime/runtime-bundle.js').read_text(); cbundle=(ROOT/'src/styles/runtime-bundle.css').read_text()
manifest=(ROOT/'src/bootstrap/module-manifest.js').read_text(); compat=(ROOT/'src/bootstrap/compatibility-manifest.js').read_text(); boot=(ROOT/'src/bootstrap/bootstrap.js').read_text(); builder=(ROOT/'tools/build_pwa11.py').read_text(); meta=json.loads((ROOT/'build-meta.json').read_text())
assert "weaponCalibrationV14" in js and "calibrationProfileV14" in js
assert re.search(r"hasOwnProperty\.call\(synthetic,\s*['\"]calibrationProfileV14['\"]\)",js)
assert "damage:2,range:-1,crit:-5" in js and "damage:-1,range:1,crit:6" in js
assert "Game?.activeMission" in js and "advanceTime(q.minutes)" in js
assert "timeProcessingFault=true" in js and "locked until reload" in js
assert "Game.credits=beforeCredits" in js and "Game.salvage=beforeSalvage" in js
assert "src/progression/workshop-calibration-v14.js" in builder
assert "src/styles/35-v14-pwa12-104-workshop-calibration.css" in builder
assert bundle.count('/* SOURCE: src/progression/workshop-calibration-v14.js */')==1
assert cbundle.count('/* SOURCE: src/styles/35-v14-pwa12-104-workshop-calibration.css */')==1
assert "progression.workshopCalibration" in manifest and "runDiagnosticsV14Calibration" in compat
assert "['runDiagnosticsV14Calibration','runDiagnosticsV136'" in boot
assert "min-height:44px" in css and "@media(max-width:600px)" in css
assert meta['schemaVersion']==14
assert meta['version']=='14.0.0-pwa.12.104-workshop-calibration-candidate.02'
print('PASS pwa12.104 workshop calibration source/build contract')
'''
    (CANDIDATE/'tests/pwa12_104_workshop_calibration_contract.py').write_text(contract,encoding='utf-8')

def build():
    subprocess.run(['node','--check','src/progression/workshop-calibration-v14.js'],cwd=CANDIDATE,check=True)
    subprocess.run(['node','--check','src/runtime/runtime-bundle.js'],cwd=CANDIDATE,check=True)
    subprocess.run(['python','tools/build_pwa11.py',VERSION],cwd=CANDIDATE,check=True)
    meta=json.loads((CANDIDATE/'build-meta.json').read_text())
    print('CANDIDATE_META',json.dumps(meta,sort_keys=True))
    if meta['version']!=VERSION or meta['schemaVersion']!=14: raise RuntimeError(meta)
    subprocess.run(['python','tests/pwa12_104_workshop_calibration_contract.py'],cwd=CANDIDATE,check=True)
    subprocess.run(['python','tests/pwa12_39_js_bundle_perf_contract.py'],cwd=CANDIDATE,check=True)
    subprocess.run(['python','tests/pwa12_37_css_bundle_perf_contract.py'],cwd=CANDIDATE,check=True)
    (OUT/'candidate_path.txt').write_text(str(CANDIDATE))

fetch(); extract(); write_sources(); patch_architecture(); patch_bundle_policy(); add_contract(); build()
print('BUILD_READY',CANDIDATE)
