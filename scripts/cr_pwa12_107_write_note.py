#!/usr/bin/env python3
from pathlib import Path
import json,sys
root=Path(sys.argv[1]);out=Path(sys.argv[2]) if len(sys.argv)>2 else root
meta=json.loads((root/'build-meta.json').read_text())
idb=(out/'NATIVE_IDB_STATUS.txt').read_text().strip() if (out/'NATIVE_IDB_STATUS.txt').exists() else 'NOT RUN'
text=f'''# Chrome Requiem PWA12.107 — Load Transaction Rollback Candidate 01

## Baseline and scope

This candidate was rebuilt from the explicit PWA12.104 canonical (`14.0.0-pwa.12.104-street-contact-support`, schema 14), not from an unpromoted specialist/integration candidate. The sole persistence reliability increment is transactional rollback and exclusive ordering around legacy hydration.

Candidate version: `{meta.get('version')}`  
Build hash: `{meta.get('buildHash')}`  
Save schema: `{meta.get('schemaVersion')}` (unchanged)  
IndexedDB database version: 2 (unchanged)  

## Concrete reliability improvement

`src/runtime/legacy-save-bridge.js` now treats hydration as an exclusive transaction. Loads are serialized through a load mutex; compatibility-layer `saveGame()` calls made while hydration is active are buffered instead of writing a half-loaded campaign. On successful hydration those reconstruction saves are coalesced per slot and persisted from the committed state. On a thrown/false hydration, buffered saves are discarded.

Before mutating the compatibility mirror, the bridge captures the live `Game` object as a shared-identity-preserving rollback graph. Plain gameplay objects, arrays, maps and sets are cloned recursively while host objects such as DOM/canvas references stay exact references. The bridge also captures key combat/UI surface nodes and attributes. If hydration fails, it restores the prior `Game` graph, prior v13 compatibility mirror and captured runtime surface, then re-synchronizes presentation where possible. This protects unsaved live session state from the previous partial-hydration failure mode.

Existing primary/backup resolution and checksum validation are preserved. A corrupt primary still falls through to the validated backup before hydration. Save requests issued before a load transaction continue to drain through the existing persistence queue before envelope resolution.

## Schema / storage impact

- Save envelope schema remains **14**.
- IndexedDB remains **DB version 2** with the existing stores (`saves`, `saveBackups`, `metadata`, `settings`).
- No new localStorage or IndexedDB keys were introduced.
- Existing fallback and compatibility key families remain unchanged, including `chrome_requiem_v14_fallback_slot_<n>`, `chrome_requiem_v14_fallback_backup_<n>`, metadata keys and `chrome_requiem_v13_<slot>` mirrors.
- No serializer field was added, removed, renamed or reinterpreted.
- No save reset or destructive migration is performed.

## Migration behavior

Legacy migration remains the existing migration path. The candidate does not rewrite migration rules; it only wraps the subsequent hydration transaction. The focused browser regression seeds a v4-shaped `chrome_requiem_save_2`, reloads through the production bootstrap, loads slot 2 and verifies the migrated player/day/credits. The schema remains 14 after build.

## Tests actually run

The GitHub Actions candidate build ran and required all non-conditional commands below to pass before packaging:

- PWA12.107 deterministic load-transaction rollback contract: failed hydration restores live nested/runtime state and shared identities, restores the previous compatibility mirror, commits zero buffered autosaves, then a healthy retry succeeds; two simultaneous loads are serialized.
- Existing save recovery / IndexedDB recovery / fallback recovery / snapshot atomicity / current-load / safe-load / inflight-order / IndexedDB transaction fixtures selected from PWA12.31, .33, .35, .38, .54, .62 and .71.
- Existing progressed-campaign save/reload browser flow (PWA12.56).
- Existing multi-stage operation checkpoint resume browser flow (PWA12.61).
- Existing inflight save/load browser flow (PWA12.71).
- Existing city-aftermath browser flow (PWA12.79).
- Existing Street Combat / aftermath contracts (PWA12.82/.83 where present).
- New legacy-v4 migration browser regression.
- Production runtime syntax, manifest contract and service-worker tests.
- Real-origin IndexedDB status: **{idb}**

Only tests that completed in the workflow before this note was generated are represented as passing; packaging would not occur after an ordinary regression failure.

## Runtime-only state boundary

The durable format intentionally does not serialize an arbitrary half-completed tactical grid/initiative/DOM tree. Multi-stage operations persist `operationCheckpointV14` at completed area boundaries and reconstruct combat from that checkpoint; Living Streets persists aftermath/world state while tactical presentation remains transient. This candidate therefore rolls back an in-memory failed hydration instead of expanding schema 14 to serialize transient UI/runtime objects.

## Unresolved risks

1. The rollback graph can restore `Game` and captured combat/UI nodes, but cannot generically rewind arbitrary closure-private state in every compatibility module if that module mutates private state and then swallows its own exception. Multi-stage operation code is the highest-value area for a future explicit transaction participant API.
2. Host-side effects started by a loader (for example an untracked timer/requestAnimationFrame/network-like callback) cannot be universally cancelled by object rollback. Current loaders are largely synchronous, but a future async hydrator should register compensating cleanup with the transaction.
3. This candidate is intentionally independent of the unpromoted PWA12.105 WAL/tombstone work and PWA12.106 semantic-load guard. Those should be consolidated explicitly after their individual regressions are accepted, not silently stacked here.

## Next persistence target

Add explicit transaction participants for operation/combat subsystem private state (capture/rollback/commit hooks), then consolidate the independently tested semantic validation and WAL/lifecycle candidates behind one canonical persistence coordinator. This should make late failures atomic across both `Game` and closure-owned mission/combat controllers rather than only the shared runtime graph.
'''
(root/'DEVELOPMENT_NOTE_PWA12_107_LOAD_TRANSACTION_ROLLBACK_CANDIDATE_01.md').write_text(text)
print(root/'DEVELOPMENT_NOTE_PWA12_107_LOAD_TRANSACTION_ROLLBACK_CANDIDATE_01.md')
