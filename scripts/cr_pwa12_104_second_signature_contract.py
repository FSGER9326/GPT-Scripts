from pathlib import Path
import json, re, sys

root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
module=(root/'src/narrative/second-signature-v14.js').read_text(encoding='utf-8')
css=(root/'src/styles/34-v14-second-signature.css').read_text(encoding='utf-8')
city=(root/'src/legacy/city-life-v13.js').read_text(encoding='utf-8')
manifest=(root/'src/bootstrap/module-manifest.js').read_text(encoding='utf-8')
runtime=(root/'src/runtime/runtime-bundle.js').read_text(encoding='utf-8')
styles=(root/'src/styles/runtime-bundle.css').read_text(encoding='utf-8')
build=(root/'tools/build_pwa11.py').read_text(encoding='utf-8')
meta=json.loads((root/'build-meta.json').read_text(encoding='utf-8'))

checks={
 'candidate version': meta['version']=='14.0.0-pwa.12.104-narrative-second-signature-candidate.01',
 'schema remains 14': meta['schemaVersion']==14,
 'arc state key': "secondSignatureV14" in module and "ARC='second_signature_v14'" in module,
 'Mira physical location': "CONTACT_ID='c1'" in module and "LOCATION_ID='loc_contact_c1'" in module and "DISTRICT_ID='old_market'" in module,
 'fresh-game reachable trust gate': "Number(r.trust||0)<25" in module,
 'physical gating': 'physicallyAtMira()' in module and "currentLocation!==LOCATION_ID" in module and 'g.activeMission' in module,
 'two exclusive choices': all(x in module for x in ["'enter_ledger'","'keep_nameless'","if(!g||!s||s.outcome"]),
 'ledger consequences': all(x in module for x in ["adjustHeat(4)","CONTACT_ID,4",'minutes=10','payoutFraction=1',"second_signature_audit_echo"]),
 'nameless consequences': all(x in module for x in ["adjustHeat(-2)","CONTACT_ID,2",'minutes=8','payoutFraction=.6',"second_signature_claim_market"]),
 'equal player fee': "const PLAYER_FEE=300" in module and 'g.credits=(Number(g.credits)||0)+PLAYER_FEE' in module,
 'journal and save': "addJournal?.('side','The Second Signature'" in module and 'saveGame?.(0,true)' in module,
 'dossier hook': 'window.renderSecondSignatureV14?.(id);' in city,
 'module manifest': "'narrative.secondSignature':{path:'./src/narrative/second-signature-v14.js'" in manifest,
 'module order': "'legacy.cityLifeVisualFixes','narrative.secondSignature','legacy.recovery'" in manifest,
 'runtime source marker': runtime.count('/* SOURCE: src/narrative/second-signature-v14.js */')==1,
 'css source marker': styles.count('/* SOURCE: src/styles/34-v14-second-signature.css */')==1,
 'raw js excluded from precache': "'src/narrative/second-signature-v14.js'" in build,
 'raw css excluded from precache': "'src/styles/34-v14-second-signature.css'" in build,
 'mobile single column': '@media(max-width:680px)' in css and '.v14-ss-actions{grid-template-columns:1fr}' in css,
 'mobile control floor': 'min-height:48px' in css,
 'overflow safety': 'overflow-wrap:anywhere' in css,
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items(): print(('PASS' if v else 'FAIL'),k)
if failed: raise SystemExit('Second Signature contract failures: '+', '.join(failed))
print(f'PASS Second Signature contract: {len(checks)}/{len(checks)} checks')
