from pathlib import Path
import re
import sys

root = Path(sys.argv[1]).resolve()
VERSION = '14.0.0-pwa.12.104-narrative-second-signature-candidate.01'

module = r'''/* Chrome Requiem PWA12.104 narrative candidate — THE SECOND SIGNATURE.
 * Standalone canonical-line contact beat for Mira / Old Market.
 * Save schema stays 14: durable state lives under Game.storyFlags.secondSignatureV14.
 */
if(typeof window!=='undefined'){
(()=>{
'use strict';
const root=globalThis;
const VERSION='14.0-narrative.1';
const ARC='second_signature_v14';
const CONTACT_ID='c1';
const LOCATION_ID='loc_contact_c1';
const DISTRICT_ID='old_market';
const PLAYER_FEE=300;

function game(){return root.ChromeRequiemCoreV5?.state||(typeof Game!=='undefined'?Game:root.Game)}
function clamp(v,a=0,b=100){return Math.max(a,Math.min(b,Number(v)||0))}
function relation(){const g=game();return g?.contactRelations?.[CONTACT_ID]||null}
function mira(){return game()?.contacts?.find(c=>c.id===CONTACT_ID)||null}
function existingState(){return game()?.storyFlags?.secondSignatureV14||null}
function ensureState(){
 const g=game();if(!g)return null;
 g.storyFlags=g.storyFlags&&typeof g.storyFlags==='object'?g.storyFlags:{};
 const s=g.storyFlags.secondSignatureV14;
 if(s&&typeof s==='object')return s;
 return g.storyFlags.secondSignatureV14={version:1,arc:ARC,stage:'offered',contactId:CONTACT_ID,districtId:DISTRICT_ID,locationId:LOCATION_ID,offeredDay:g.day||1};
}
function adjustHeat(delta){
 const g=game();if(!g)return 0;g.heat=g.heat&&typeof g.heat==='object'?g.heat:{};
 const before=clamp(g.heat.meridian);g.heat.meridian=clamp(before+delta);return g.heat.meridian-before;
}
function physicallyAtMira(){
 const g=game(),c=mira(),p=g?.ovPlayer;
 if(!g||!c||!p||g.activeMission)return false;
 if(g.cityLife?.currentDistrict!==DISTRICT_ID||g.cityLife?.currentLocation!==LOCATION_ID)return false;
 if(!Number.isFinite(p.x)||!Number.isFinite(p.y)||!Number.isFinite(c.x)||!Number.isFinite(c.y))return false;
 return Math.abs(p.x-c.x)+Math.abs(p.y-c.y)<=2;
}
function eligible(){
 const g=game(),r=relation(),s=existingState();
 if(!g||!r||r.known===false||Number(r.trust||0)<25)return false;
 return !s?.outcome;
}
function copyForState(s){
 if(!s?.outcome)return null;
 if(s.outcome==='ledger_witness')return {
  title:'ENTERED IN THE LEDGER',
  body:'The escrow releases in full. The surviving crew gets every credit the dead lead earned—but their borrowed identities now share one clean corporate witness: yours. Somewhere inside Meridian compliance, two people who survived by being administratively separate have become correlatable.',
  facts:['SURVIVORS // FULL SETTLEMENT','IDENTITY // CORRELATABLE','NEXT // AUDIT ECHO']
 };
 return {
  title:'KEPT NAMELESS',
  body:'Mira routes the claim through an Old Market settlement pool. The survivors take the haircut and keep the identities that let them stay alive. No corporate witness is added; no clean principal can prove who received the dead lead’s money. The market remembers the debt instead.',
  facts:['SURVIVORS // 60% SETTLEMENT','IDENTITY // SHELTERED','NEXT // CLAIM MARKET']
 };
}
function resolve(choice){
 const g=game(),s=ensureState();
 if(!g||!s||s.outcome||!eligible()||!physicallyAtMira()||!['enter_ledger','keep_nameless'].includes(choice))return false;
 let outcome,nextHook,heatDelta,trustDelta,minutes,payoutFraction,desc;
 if(choice==='enter_ledger'){
  outcome='ledger_witness';nextHook='second_signature_audit_echo';minutes=10;payoutFraction=1;
  heatDelta=adjustHeat(4);
  trustDelta=root.changeContactTrustV13?.(CONTACT_ID,4,'You put the company name behind Mira’s dead-crew escrow and accepted the audit trail.')||0;
  desc='You become the second living signature on a dead crew lead’s escrow. The survivors receive the full settlement. Their borrowed identities are now linked by one legitimate witness, and Meridian compliance has a clean thread it did not have before.';
 }else{
  outcome='offbook_settlement';nextHook='second_signature_claim_market';minutes=8;payoutFraction=.6;
  heatDelta=adjustHeat(-2);
  trustDelta=root.changeContactTrustV13?.(CONTACT_ID,2,'You let Mira keep the survivors outside corporate identity reconciliation.')||0;
  desc='You refuse to make the survivors legible. Mira sells the claim into an Old Market settlement pool; the crew accepts a forty-percent haircut and keeps its borrowed identities compartmentalized.';
 }
 g.credits=(Number(g.credits)||0)+PLAYER_FEE;
 if(typeof root.advanceTime==='function')root.advanceTime(minutes);
 Object.assign(s,{stage:'resolved',choice,outcome,nextHook,payoutFraction,playerFee:PLAYER_FEE,effects:{meridianHeat:heatDelta,contactTrust:trustDelta,minutes},resolvedDay:g.day||1,sourceProtection:outcome==='offbook_settlement'?'identity_compartmentalized':'identity_correlatable'});
 root.addJournal?.('side','The Second Signature',desc+` Mira pays the same ¢${PLAYER_FEE} witness fee either way.`);
 root.updateOverworldHUD?.();root.saveGame?.(0,true);
 root.renderContactDossierV13?.(CONTACT_ID);
 return true;
}
function panelHtml(local,s){
 const done=copyForState(s);
 if(done)return `<section class="v14-second-signature resolved"><div class="v14-ss-kicker">OLD MARKET // ESCROW RECEIPT</div><h3>${done.title}</h3><p>${done.body}</p><div class="v14-ss-facts">${done.facts.map(x=>`<span>${x}</span>`).join('')}<span>YOUR FEE // ¢${PLAYER_FEE}</span></div></section>`;
 const lock=local?'':' · PHYSICAL MEETING REQUIRED';
 return `<section class="v14-second-signature"><div class="v14-ss-kicker">MIRA // THE SECOND SIGNATURE</div><h3>THE DEAD CANNOT CLOSE ESCROW</h3><p>A contract crew finished the work. Their lead died after extraction and before settlement. Two survivors are still alive under borrowed identities. The employer’s clearing rule will release the dead lead’s escrow only if a living witness signs the close.</p><p>Mira can put your company on the ledger and release every credit. That also gives Meridian a legitimate bridge between identities built to stay separate. Or she can sell the claim into the Old Market, where anonymity costs forty percent and nobody asks for a biometric witness.</p><div class="v14-ss-facts"><span>CONTACT // MIRA</span><span>ESCROW // DEAD LEAD</span><span>YOUR FEE // ¢${PLAYER_FEE} EITHER WAY</span><span>${local?'ACCESS // IN PERSON':'ACCESS // REMOTE'}</span></div><div class="v14-ss-actions"><button type="button" class="v14-ss-choice" data-ss-choice="enter_ledger" ${local?'':'disabled'}><strong>ENTER THE LEDGER</strong><small>Full settlement to the survivors. +4 Meridian heat · +4 Mira trust · 10m. Their borrowed identities become correlatable.${lock}</small></button><button type="button" class="v14-ss-choice" data-ss-choice="keep_nameless" ${local?'':'disabled'}><strong>KEEP THEM NAMELESS</strong><small>60% off-book settlement. −2 Meridian heat · +2 Mira trust · 8m. The survivors keep their identity compartments.${lock}</small></button></div></section>`;
}
function render(contactId){
 if(contactId!==CONTACT_ID)return false;
 const g=game(),host=root.document?.getElementById('v13-dossier');if(!g||!host)return false;
 host.querySelector('.v14-second-signature')?.remove();
 const r=relation(),s=existingState();
 if(!r||r.known===false||Number(r.trust||0)<25)return false;
 const stateNow=s||ensureState(),wrap=root.document.createElement('div');
 wrap.innerHTML=panelHtml(physicallyAtMira(),stateNow);const panel=wrap.firstElementChild;if(!panel)return false;
 panel.querySelectorAll('[data-ss-choice]').forEach(b=>b.addEventListener('click',()=>resolve(b.dataset.ssChoice)));
 host.appendChild(panel);return true;
}
function diagnostics(){
 const s=existingState();return {version:VERSION,arc:ARC,contact:CONTACT_ID,location:LOCATION_ID,eligible:eligible(),physical:physicallyAtMira(),resolved:!!s?.outcome,outcome:s?.outcome||null};
}
root.renderSecondSignatureV14=render;
root.resolveSecondSignatureV14=resolve;
root.runDiagnosticsSecondSignatureV14=diagnostics;
root.CR14SecondSignatureV14=Object.freeze({version:VERSION,arc:ARC,contactId:CONTACT_ID,locationId:LOCATION_ID,districtId:DISTRICT_ID,playerFee:PLAYER_FEE,eligible,ensureState,state:existingState,physicallyAtMira,resolve,render,diagnostics});
})();
}
'''

css = r'''/* PWA12.104 NARRATIVE — THE SECOND SIGNATURE */
.v14-second-signature{margin:16px 0 2px;padding:14px;border:1px solid rgba(229,184,87,.34);border-left:3px solid #e5b857;background:linear-gradient(135deg,rgba(31,26,18,.94),rgba(11,18,24,.96));box-shadow:0 12px 26px rgba(0,0,0,.22)}
.v14-second-signature.resolved{border-left-color:#79d9c0;background:linear-gradient(135deg,rgba(12,31,29,.93),rgba(10,17,23,.96))}
.v14-ss-kicker{font-size:.7rem;letter-spacing:.14em;color:#e5b857;margin-bottom:7px}.v14-second-signature.resolved .v14-ss-kicker{color:#79d9c0}
.v14-second-signature h3{margin:0 0 8px;font-size:1.02rem;letter-spacing:.055em;color:#f1eee5}.v14-second-signature p{margin:7px 0;color:#c8d0d2;line-height:1.5;font-size:.82rem}
.v14-ss-facts{display:flex;flex-wrap:wrap;gap:6px;margin:11px 0}.v14-ss-facts span{max-width:100%;overflow-wrap:anywhere;padding:5px 7px;border:1px solid rgba(164,191,198,.2);background:rgba(7,14,19,.6);font-size:.65rem;letter-spacing:.07em;color:#a9c2c7}
.v14-ss-actions{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:12px}.v14-ss-choice{min-width:0;min-height:72px;padding:10px 11px;text-align:left;border:1px solid rgba(229,184,87,.35);background:rgba(20,20,18,.82);color:#e9eef0;cursor:pointer}.v14-ss-choice:hover:not(:disabled){border-color:#e5b857;background:rgba(43,34,19,.84)}.v14-ss-choice:disabled{opacity:.45;cursor:not-allowed}.v14-ss-choice strong,.v14-ss-choice small{display:block}.v14-ss-choice strong{font-size:.77rem;letter-spacing:.08em;color:#f0c96e}.v14-ss-choice small{margin-top:5px;line-height:1.4;color:#aebbc0;font-size:.68rem;overflow-wrap:anywhere}
@media(max-width:680px){.v14-second-signature{margin:12px 0 2px;padding:12px}.v14-ss-actions{grid-template-columns:1fr}.v14-ss-choice{width:100%;min-height:48px}.v14-ss-facts{display:grid;grid-template-columns:1fr}.v14-ss-facts span{width:100%;box-sizing:border-box}.v14-second-signature p{font-size:.8rem}}
'''

js_path = root/'src/narrative/second-signature-v14.js'
css_path = root/'src/styles/34-v14-second-signature.css'
js_path.parent.mkdir(parents=True, exist_ok=True)
js_path.write_text(module, encoding='utf-8')
css_path.write_text(css, encoding='utf-8')

# Ensure Mira dossier rendering always offers the slice, even when opened from
# city-life's internal lexical function rather than through window wrappers.
city_path = root/'src/legacy/city-life-v13.js'
city = city_path.read_text(encoding='utf-8')
anchor = "}\nwindow.renderContactDossierV13=renderContactDossierV13;"
if city.count(anchor) != 1:
    raise SystemExit(f'unexpected Mira dossier hook seam count={city.count(anchor)}')
city = city.replace(anchor, " window.renderSecondSignatureV14?.(id);\n}\nwindow.renderContactDossierV13=renderContactDossierV13;", 1)
city_path.write_text(city, encoding='utf-8')

# Register the narrative module after city-life visual fixes, preserving the
# canonical bootstrap order and keeping later recovery/runtime modules intact.
manifest_path = root/'src/bootstrap/module-manifest.js'
manifest = manifest_path.read_text(encoding='utf-8')
a = "  'legacy.cityLifeVisualFixes':{path:'./src/legacy/city-life-v13-visual-fixes.js',kind:'module'},\n  'legacy.recovery'"
b = "  'legacy.cityLifeVisualFixes':{path:'./src/legacy/city-life-v13-visual-fixes.js',kind:'module'},\n  'narrative.secondSignature':{path:'./src/narrative/second-signature-v14.js',kind:'module'},\n  'legacy.recovery'"
if manifest.count(a) != 1:
    raise SystemExit('module manifest object anchor missing')
manifest = manifest.replace(a,b,1)
a = "'legacy.cityLifeVisualFixes','legacy.recovery'"
b = "'legacy.cityLifeVisualFixes','narrative.secondSignature','legacy.recovery'"
if manifest.count(a) != 1:
    raise SystemExit('module manifest order anchor missing')
manifest = manifest.replace(a,b,1)
manifest_path.write_text(manifest, encoding='utf-8')

# Add the source into the ordered shipping bundle based on its checked-in source
# markers, then let the repository's canonical rebundler rebuild it normally.
def add_bundle_source(bundle_rel, added, after=None):
    bundle = root/bundle_rel
    text = bundle.read_text(encoding='utf-8')
    names = re.findall(r'/\* SOURCE: ([^*]+?) \*/', text)
    if added in names:
        raise SystemExit(f'{added} already in {bundle_rel}')
    if after is None:
        names.append(added)
    else:
        if after not in names:
            raise SystemExit(f'bundle anchor missing: {after}')
        names.insert(names.index(after)+1, added)
    out=''.join(f'/* SOURCE: {name} */\n'+(root/name).read_text(encoding='utf-8').rstrip()+'\n\n' for name in names)
    bundle.write_text(out, encoding='utf-8')

add_bundle_source('src/runtime/runtime-bundle.js','src/narrative/second-signature-v14.js','src/legacy/city-life-v13-visual-fixes.js')
add_bundle_source('src/styles/runtime-bundle.css','src/styles/34-v14-second-signature.css')

# Raw sources are represented by their ordered bundles in the shipping runtime.
build_path = root/'tools/build_pwa11.py'
build = build_path.read_text(encoding='utf-8')
for anchor, line in [
    ("    'src/legacy/city-life-v13-visual-fixes.js',", "    'src/narrative/second-signature-v14.js',"),
    ("    'src/styles/33-v14-pwa12-81-grounded-scene.css',", "    'src/styles/34-v14-second-signature.css',")
]:
    if build.count(anchor) != 1:
        raise SystemExit(f'build precache anchor missing: {anchor}')
    build = build.replace(anchor, anchor+'\n'+line, 1)
build_path.write_text(build, encoding='utf-8')

# Development note travels inside the candidate source archive.
note = f'''# Chrome Requiem PWA12.104 — The Second Signature Candidate 01\n\n## Baseline\nExact PWA12.104 canonical must be hash-verified before this patch is applied. Canonical is not modified.\n\n## Playable slice\nMira receives an escrow close for a contract crew whose lead died between extraction and settlement. Two survivors use borrowed identities. The player must meet Mira physically in Old Market and choose whether the company becomes the second living signature or the claim is settled off-book.\n\n- ENTER THE LEDGER: full survivor settlement; +4 Meridian heat; +4 Mira trust; 10 action-minutes; identity correlation becomes possible.\n- KEEP THEM NAMELESS: 60% survivor settlement through an Old Market claim pool; -2 Meridian heat; +2 Mira trust; 8 action-minutes; identity compartments remain sheltered.\n- Player fee is ¢{PLAYER_FEE} on both branches so the moral/systemic choice is not distorted by personal payout.\n\n## Integration\nAdds src/narrative/second-signature-v14.js and src/styles/34-v14-second-signature.css, one City Life dossier hook, module/bootstrap registration, ordered bundle markers, and raw-source precache exclusions. Durable state is additive at Game.storyFlags.secondSignatureV14; save schema remains 14.\n\n## Continuity\nThis is a standalone canonical-line beat. It does not import MARKET EYES / PAPER GHOSTS / QUIET CENSUS / RECONCILIATION WINDOW / AFTER THE COUNT or ZERO RECEIPT / PALISADE from noncanonical branches.\n\n## Candidate identity\n{VERSION}\n'''
(root/'DEVELOPMENT_NOTE_PWA12_104_NARRATIVE_SECOND_SIGNATURE_CANDIDATE_01.md').write_text(note,encoding='utf-8')

print('APPLIED', VERSION)
