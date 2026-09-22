#!/usr/bin/env python3
from pathlib import Path
import json,sys
if len(sys.argv)!=3: raise SystemExit('usage: cr_proc_c04_write_note.py <candidate_root> <out_dir>')
root=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
meta=json.loads((root/'build-meta.json').read_text(encoding='utf-8'))
def read(name):
 p=out/name
 return p.read_text(encoding='utf-8',errors='replace').strip() if p.exists() else '(not recorded)'
note=f'''# Chrome Requiem / New Cyberknights — Procedural Complication Candidate 04

## Build
- Version: `{meta['version']}`
- Build hash: `{meta['buildHash']}`
- Schema: {meta['schemaVersion']}
- Lineage: explicit PWA12.104 canonical → Candidate 01 faction composition → Candidate 02 optional clauses → Candidate 03 egress routes → Candidate 04 complication intel.
- Canonical was not overwritten.

## Systemic improvement
Candidate 04 adds one deterministic, persisted **Compromised Site** complication to eligible generated single-stage contracts. Incidence is seeded from existing procedural provenance plus mission/contact/day/slot, district security, mission difficulty and target-faction response pressure, and is bounded to 28–52%. Authored/story work, unsupported objectives and V14 multistage operations are excluded.

Intel quality derives from existing SERVER/contact-trust state. Low intel reveals only a risk signal, medium intel identifies the exposure family, and high intel states the exact tactical consequence. Before physical staging is committed, the player can fund a deterministic `Exposure Scrub` costing ¢70–¢180. The cost is sunk and persisted; once staging is physically complete, mitigation is locked.

The tactical consequence deliberately reuses the V13.4B physical-infiltration layer. An unmitigated normally quiet approach begins fully alerted. FRONT GATE is already alerted, so the complication adds no redundant penalty there. Candidate 04 does not mutate base reward, XP, target faction, mandatory objective graph, generated enemy array, optional-clause geometry or Candidate 03 egress geometry.

## Integration
`src/missions/procedural-complications-v14.js` is loaded immediately after `multistage-operations-v14.js` and before visual/bootstrap modules. The ordered runtime bundle was rebuilt from source markers and release metadata/precache/service-worker data were regenerated with `tools/build_pwa11.py`.

## Verification actually run
### Candidate 04 + inherited procedural contracts
```text
{read('contract-tests.log')}
```

### Persistence / multistage / release regressions
```text
{read('regression-tests.log')}
```

### Real Chromium Candidate 04 flow
```text
{read('candidate04-browser.log')}
```

### Inherited Candidate 01–03 Chromium flows
```text
{read('inherited-browser.log')}
```

Candidate 04 browser QA exercises actual new-game board generation, contact-card presentation, briefing disclosure, real save/load restoration, mitigation persistence, SERVICE ACCESS selection, physical staging completion, mitigation locking after staging, deployment, unmitigated alert escalation and mitigated quiet-start preservation.

## Edge cases covered
- Authored/non-generated content receives no Candidate 04 metadata.
- Unsupported objectives remain ineligible.
- V14 multistage conflicts remain excluded.
- Seed-no-complication produces stable disabled metadata rather than rerolling.
- Repeated mitigation cannot double-charge.
- Locked mitigation cannot debit credits.
- FRONT GATE receives no redundant alert mutation.
- Quiet unmitigated ingress escalates hostile awareness to 100.
- Quiet mitigated ingress retains native awareness 0 behavior.
- Save/load preserves durable seed/kind/mitigation while attempt-local trigger fields are reset.
- Reward, XP, objective, target and generated enemy-array payload stay invariant under Candidate 04 generation.

## Next procedural target
Add a **second feasibility-gated complication family** only after Candidate 04 integration review: a route/extraction-specific disruption with intel preview and a distinct preparation countermeasure, while preserving a hard maximum of one complication per generated contract and never invalidating mandatory objective/exfil reachability.
'''
name='DEVELOPMENT_NOTE_PWA12_104_PROCEDURAL_COMPLICATION_INTEL_CANDIDATE_04.md'
(root/name).write_text(note,encoding='utf-8');(out/name).write_text(note,encoding='utf-8');(out/'BUILD_META.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
print(name)
