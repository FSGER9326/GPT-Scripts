#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json, re, subprocess, sys, textwrap

VERSION='14.0.0-pwa.12.152-combat-intent-telemetry-candidate.01'
MARK='PWA12.152 combat intent telemetry'

OLD_CUE="cue.classList.toggle('scan',intent==='SCAN');cue.classList.toggle('pin',intent==='PIN');cue.classList.toggle('fin',intent==='FIN');cue.classList.toggle('sweep',intent==='SWEEP'||intent==='BASE');cue.classList.toggle('sup',intent==='SUP');cue.classList.toggle('go',intent==='GO');cue.textContent=intent;"
NEW_CUE="cue.classList.toggle('scan',intent==='SCAN');cue.classList.toggle('pin',intent==='PIN');cue.classList.toggle('fin',intent==='FIN');cue.classList.toggle('sweep',intent==='SWEEP'||intent==='BASE');cue.classList.toggle('sup',intent==='SUP');cue.classList.toggle('go',intent==='GO');cue.classList.toggle('watch',intent==='WATCH');cue.dataset.intent=intent;cue.textContent=intent;"

CSS=r'''\n/* PWA12.152 combat intent telemetry — compact, non-interactive mobile tactical cues. */
#combat #board .unit .v133-contact-cue{pointer-events:none}
#combat #board .unit .v133-contact-cue.watch{border-color:rgba(126,215,179,.78);color:#c6f2dc;box-shadow:0 0 8px rgba(88,190,148,.24)}
@media (max-width:680px), (max-height:520px){
 #combat #board .unit .v133-contact-cue{left:50%;right:auto;top:-7px;transform:translateX(-50%);width:24px;min-width:0;max-width:calc(100% - 4px);height:10px;min-height:10px;box-sizing:border-box;padding:0;display:flex;align-items:center;justify-content:center;border-radius:2px;background:rgba(5,10,11,.91);font-size:0;line-height:0;letter-spacing:0;white-space:nowrap;overflow:hidden;opacity:.80;box-shadow:0 1px 2px rgba(0,0,0,.78);pointer-events:none}
 #combat #board .unit .v133-contact-cue::after{content:'INT';display:block;font:800 6px/9px Orbitron,system-ui,sans-serif;letter-spacing:.18px;color:inherit}
 #combat #board .unit .v133-contact-cue[data-intent='CONTACT']::after{content:'CTC'}
 #combat #board .unit .v133-contact-cue[data-intent='SCAN']::after{content:'SCN'}
 #combat #board .unit .v133-contact-cue[data-intent='PIN']::after{content:'PIN'}
 #combat #board .unit .v133-contact-cue[data-intent='FIN']::after{content:'FIN'}
 #combat #board .unit .v133-contact-cue[data-intent='SWEEP']::after{content:'SWP'}
 #combat #board .unit .v133-contact-cue[data-intent='BASE']::after{content:'BAS'}
 #combat #board .unit .v133-contact-cue[data-intent='WATCH']::after{content:'WCH'}
 #combat #board .unit .v133-contact-cue[data-intent='SUP']::after{content:'SUP'}
 #combat #board .unit .v133-contact-cue[data-intent='GO']::after{content:'GO'}
 #combat #board .unit .v133-contact-cue.scan{opacity:.70;background:rgba(5,16,19,.89)}
 #combat #board .unit .v133-contact-cue.pin{opacity:.86;background:rgba(22,18,6,.92)}
 #combat #board .unit .v133-contact-cue.fin{opacity:.95;background:rgba(28,7,12,.94);box-shadow:0 0 5px rgba(255,60,95,.30)}
 #combat #board .unit .v133-contact-cue.sweep{opacity:.86;background:rgba(5,17,24,.93)}
 #combat #board .unit .v133-contact-cue.watch{opacity:.84;background:rgba(7,22,18,.93)}
 #combat #board .unit .v133-contact-cue.sup{opacity:.94;background:rgba(31,14,4,.94);box-shadow:0 0 5px rgba(255,113,36,.34)}
 #combat #board .unit .v133-contact-cue.go{opacity:.94;background:rgba(4,26,18,.94);box-shadow:0 0 5px rgba(54,255,162,.28)}
}
'''

CONTRACT=r'''from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ai=(ROOT/'src/legacy/mercenary-intelligence-v8.js').read_text(encoding='utf-8')
css=(ROOT/'src/styles/24-v14-pwa12-5-fire-control.css').read_text(encoding='utf-8')
bundle=(ROOT/'src/runtime/runtime-bundle.js').read_text(encoding='utf-8')
bcss=(ROOT/'src/styles/runtime-bundle.css').read_text(encoding='utf-8')
core=(ROOT/'src/legacy/core-v5.js').read_text(encoding='utf-8')
gfx=(ROOT/'src/legacy/graphics-v6.js').read_text(encoding='utf-8')
def segment(src,name):
 i=src.index(name); j=src.find('\nfunction ',i+len(name)); return src[i:j if j!=-1 else len(src)]
checks={
 'fire_maneuver_preserved':'function enemyFireManeuverStateV146()' in ai and "intent==='SUP'" in ai and "intent==='GO'" in ai,
 'intent_dataset':"cue.dataset.intent=intent" in ai,
 'watch_class':"intent==='WATCH'" in ai,
 'all_mobile_codes':all((f"data-intent='{x}'" in css) for x in ('CONTACT','SCAN','PIN','FIN','SWEEP','BASE','WATCH','SUP','GO')),
 'pointer_passthrough':'pointer-events:none' in css,
 'compact_mobile':'width:24px' in css and 'height:10px' in css,
 'js_bundle_parity':"cue.dataset.intent=intent" in bundle and 'function enemyFireManeuverStateV146()' in bundle,
 'css_bundle_parity':'PWA12.152 combat intent telemetry' in bcss,
 'combat_core_dpr_cap':'Math.min(window.devicePixelRatio || 1, 2)' in segment(core,'function resizeCombatCanvas'),
 'overworld_core_not_globally_capped':'const dpr = window.devicePixelRatio || 1;' in core,
 'combat_backdrop_dpr_cap':'dpr=Math.min(window.devicePixelRatio||1,2)' in segment(gfx,'function renderCombatBackdrop'),
 'schema_neutral':'enemyFireManeuverV146' not in core,
}
print(json.dumps(checks,sort_keys=True))
failed=[k for k,v in checks.items() if not v]
if failed: raise SystemExit('FAILED: '+', '.join(failed))
print('PWA12.152 combat intent telemetry contract PASS')
'''

NOTE=f'''# PWA12.152 Combat Intent Telemetry Candidate 01\n\nParent reconstruction: exact PWA12.145 Integration RC03 -> qualified PWA12.148 cumulative Heavy suppression/fire-and-maneuver rebase -> PWA12.151 tactical combat DPR cap -> this telemetry pass. Formal PWA12.104 canonical is untouched.\n\n## Player-facing change\nPhone/short-screen combat now keeps the full semantic enemy intent in DOM text while rendering a bounded 24x10 non-interactive telemetry strip: CONTACT=CTC, SCAN=SCN, PIN, FIN, SWEEP=SWP, BASE=BAS, WATCH=WCH, SUP, GO. SUP/GO remain visibly distinct so the Heavy suppression lane and assault handoff are readable as one coordinated enemy maneuver. Desktop retains the full intent words.\n\nThe cue overlay explicitly uses pointer-events:none and does not alter board/cell geometry, AP, initiative, LOS, target selection, damage, routing, suppression rules, world time, persistence, or save schema.\n\n## Preserved cumulative combat\nPWA12.148 Heavy suppression lane/arc planning/fire-and-maneuver handoff remains authoritative. Heavy suppression still costs 1 AP; hard cover counters lane interruption; assault handoff remains route preference rather than free AP/teleportation. Tactical DPR is capped at 2 only inside resizeCombatCanvas() and renderCombatBackdrop(); overworld DPR remains untouched.\n\n## Version\n{VERSION}; schema remains 14.\n'''

def replace_once(text,old,new,label):
 n=text.count(old)
 if n!=1: raise RuntimeError(f'{label}: expected one anchor, found {n}')
 return text.replace(old,new,1)

def patch_function(text,marker,old,new,label):
 start=text.index(marker); nxt=text.find('\nfunction ',start+len(marker)); end=len(text) if nxt<0 else nxt
 seg=text[start:end]
 if seg.count(old)!=1: raise RuntimeError(f'{label}: expected one scoped anchor, found {seg.count(old)}')
 return text[:start]+seg.replace(old,new,1)+text[end:]

def main():
 if len(sys.argv)!=2: raise SystemExit('usage: patch.py CANDIDATE_ROOT')
 root=Path(sys.argv[1]).resolve()
 ai=root/'src/legacy/mercenary-intelligence-v8.js'
 s=ai.read_text(encoding='utf-8')
 if MARK in s: raise RuntimeError('telemetry patch already present')
 s=replace_once(s,OLD_CUE,NEW_CUE,'intent cue router')
 s=s.replace("// PWA12.146: bounded fire-and-maneuver handoff.","// PWA12.152 combat intent telemetry\n// PWA12.146: bounded fire-and-maneuver handoff.",1)
 ai.write_text(s,encoding='utf-8',newline='\n')
 cssp=root/'src/styles/24-v14-pwa12-5-fire-control.css'
 css=cssp.read_text(encoding='utf-8')
 if 'PWA12.152 combat intent telemetry' in css: raise RuntimeError('CSS patch already present')
 cssp.write_text(css.rstrip()+CSS,encoding='utf-8',newline='\n')
 corep=root/'src/legacy/core-v5.js'; core=corep.read_text(encoding='utf-8')
 core=patch_function(core,'function resizeCombatCanvas','const dpr = window.devicePixelRatio || 1;','const dpr = Math.min(window.devicePixelRatio || 1, 2);','combat FX DPR')
 corep.write_text(core,encoding='utf-8',newline='\n')
 gfxp=root/'src/legacy/graphics-v6.js'; gfx=gfxp.read_text(encoding='utf-8')
 gfx=patch_function(gfx,'function renderCombatBackdrop','dpr=window.devicePixelRatio||1','dpr=Math.min(window.devicePixelRatio||1,2)','combat backdrop DPR')
 gfxp.write_text(gfx,encoding='utf-8',newline='\n')
 (root/'tests/pwa12_152_combat_intent_telemetry_contract.py').write_text("import json\n"+CONTRACT,encoding='utf-8',newline='\n')
 (root/'DEVELOPMENT_NOTE_PWA12_152_COMBAT_INTENT_TELEMETRY.md').write_text(NOTE,encoding='utf-8',newline='\n')
 subprocess.run([sys.executable,'tools/rebundle_runtime.py'],cwd=root,check=True)
 subprocess.run([sys.executable,'tools/build_pwa11.py',VERSION],cwd=root,check=True)
 subprocess.run([sys.executable,'tests/pwa12_152_combat_intent_telemetry_contract.py'],cwd=root,check=True)
 print(VERSION)
 return 0
if __name__=='__main__': raise SystemExit(main())
