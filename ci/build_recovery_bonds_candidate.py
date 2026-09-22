from pathlib import Path
import zipfile, shutil, re, sys

SOURCE=Path(sys.argv[1] if len(sys.argv)>1 else 'source138.zip')
DST=Path(sys.argv[2] if len(sys.argv)>2 else 'Chrome_Requiem_v14_PWA_pwa12_142_RECOVERY_BONDS_CANDIDATE_01_source')
z=zipfile.ZipFile(SOURCE)
names=z.namelist(); idx=next(n for n in names if n.endswith('/index.html')); oldroot=idx[:-len('index.html')]
tmp=Path('extract142');
if tmp.exists(): shutil.rmtree(tmp)
z.extractall(tmp); src=tmp/oldroot
if DST.exists(): shutil.rmtree(DST)
shutil.copytree(src,DST)

js=Path('ci/recovery-support-v14.js').read_text()
js=js.replace("renderRecoverySupportV14:renderSupport,runDiagnosticsRecoverySupportV14", "renderRecoverySupportV14:renderSupport,decorateRecoverySupportBriefingV14:decorateBriefing,runDiagnosticsRecoverySupportV14")
js=js.replace("add('mission exclusion hook',window.createCombatUnits===createCombatUnits)", "add('mission exclusion hook',typeof window.createCombatUnits==='function')")
js=js.replace("if(!(patient.injuries||[]).includes(a.injuryId))return h?.outcome||'treated_elsewhere';", "if(!(patient.injuries||[]).includes(a.injuryId)){if(h?.outcome)return h.outcome;return Number(Game.day||1)>=Number(a.dueDay||Infinity)?'recovered':'treated_elsewhere';}")
(DST/'src/company/recovery-support-v14.js').write_text(js)
css=Path('ci/38-v14-recovery-bonds.css').read_text(); (DST/'src/styles/38-v14-recovery-bonds.css').write_text(css)
shutil.copy2('ci/pwa12_142_recovery_bonds_browser.py',DST/'tests/pwa12_142_recovery_bonds_browser.py')

# Module registry and explicit execution order.
p=DST/'src/bootstrap/module-manifest.js'; t=p.read_text(); lines=t.splitlines(); out=[]; registry=False; order=False
for line in lines:
    out.append(line)
    if "'company.crewIntercession'" in line and 'path:' in line and 'company.recoverySupport' not in t:
        ind=line[:len(line)-len(line.lstrip())]; out.append(ind+"'company.recoverySupport':{path:'./src/company/recovery-support-v14.js',kind:'module'},"); registry=True
    elif line.strip()=="'company.crewIntercession'," and "'company.recoverySupport'," not in t:
        ind=line[:len(line)-len(line.lstrip())]; out.append(ind+"'company.recoverySupport',"); order=True
p.write_text('\n'.join(out)+'\n')
if 'company.recoverySupport' not in p.read_text(): raise SystemExit('module manifest integration failed')

# Compatibility diagnostic list.
p=DST/'src/bootstrap/compatibility-manifest.js'; t=p.read_text()
if 'runDiagnosticsRecoverySupportV14' not in t:
    lines=t.splitlines(); out=[]; inserted=False
    for line in lines:
        out.append(line)
        if 'runDiagnosticsCrewIntercessionV14' in line:
            ind=line[:len(line)-len(line.lstrip())]; out.append(ind+"'runDiagnosticsRecoverySupportV14',"); inserted=True
    if not inserted: raise SystemExit('compatibility insertion anchor missing')
    p.write_text('\n'.join(out)+'\n')

# Exclude separately-copied source/style files because executable bundles contain them.
p=DST/'tools/build_pwa11.py'; t=p.read_text(); lines=t.splitlines(); out=[]
for line in lines:
    out.append(line)
    if 'src/company/crew-intercession-v14.js' in line and 'recovery-support-v14.js' not in t:
        ind=line[:len(line)-len(line.lstrip())]; q='"' if '"' in line else "'"; out.append(ind+q+'src/company/recovery-support-v14.js'+q+',')
    if 'src/styles/37-v14-crew-intercession.css' in line and '38-v14-recovery-bonds.css' not in t:
        ind=line[:len(line)-len(line.lstrip())]; q='"' if '"' in line else "'"; out.append(ind+q+'src/styles/38-v14-recovery-bonds.css'+q+',')
p.write_text('\n'.join(out)+'\n')

def find_bundle(glob,marker):
    for bp in DST.rglob(glob):
        try: text=bp.read_text()
        except Exception: continue
        if marker in text: return bp
    raise SystemExit(f'cannot find bundle containing {marker}')

def insert_after(bp,old,new,text):
    s=bp.read_text(); marker=f'/* SOURCE: {old} */'; pos=s.find(marker)
    if pos<0: raise SystemExit('missing source marker '+marker)
    start=pos+len(marker); m=re.search(r'/\* SOURCE: [^*]+ \*/',s[start:]); ins=start+(m.start() if m else len(s)-start)
    new_marker=f'/* SOURCE: {new} */'
    if new_marker not in s: s=s[:ins]+'\n'+new_marker+'\n'+text.rstrip()+'\n\n'+s[ins:]
    bp.write_text(s)

js_bundle=find_bundle('*.js','/* SOURCE: src/company/crew-intercession-v14.js */')
css_bundle=find_bundle('*.css','/* SOURCE: src/styles/37-v14-crew-intercession.css */')
insert_after(js_bundle,'src/company/crew-intercession-v14.js','src/company/recovery-support-v14.js',js)
insert_after(css_bundle,'src/styles/37-v14-crew-intercession.css','src/styles/38-v14-recovery-bonds.css',css)
(DST/'PWA12_142_BASELINE.txt').write_text('Baseline: PWA12.138 Crew Intercession Rebase Candidate 01 QA Verified\nParent cumulative line: PWA12.136 Integration Release Candidate 01\nNew subsystem: Crew Recovery Bonds / recovery support\n')
print('candidate',DST)
print('runtime bundle',js_bundle.relative_to(DST))
print('style bundle',css_bundle.relative_to(DST))
print('module registry insertion',registry,'order insertion',order)
