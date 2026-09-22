#!/usr/bin/env bash
set -euo pipefail
VERSION='14.0.0-pwa.12.136-narrative-reconciliation-window-candidate.01'
SOURCE_URL=$(tr -d '\r\n' < scripts/cr_pwa12_136_reconciliation_window_source_url.txt)
rm -rf work out base.zip
mkdir -p work out
curl --fail --location --retry 2 --output base.zip "$SOURCE_URL"
unzip -q base.zip -d work
ROOT=$(find work -mindepth 1 -maxdepth 1 -type d -name 'Chrome_Requiem_v14_PWA_pwa12_136_INTEGRATION_RELEASE_CANDIDATE_01_source' -print -quit)
test -n "$ROOT"
ROOT=$(realpath "$ROOT")
python3 - "$ROOT" <<'PY'
import json,sys
from pathlib import Path
root=Path(sys.argv[1]);m=json.loads((root/'build-meta.json').read_text())
assert m['version']=='14.0.0-pwa.12.136-integration-release-candidate.01',m
assert m['buildHash']=='93ded980c47a0abfde407f56',m
assert m['schemaVersion']==14,m
assert (root/'src/narrative/quiet-census-v14.js').exists()
city=(root/'src/legacy/city-life-v13.js').read_text()
assert 'loc_helix_hidden_1' in city and 'Settlement Vault Annex' in city
print('VERIFIED_BASE',m)
PY
python3 scripts/cr_pwa12_136_reconciliation_window_patch.py "$ROOT"
cp scripts/cr_pwa12_136_reconciliation_window_contract.mjs "$ROOT/tests/pwa12_136_reconciliation_window_contract.mjs"
cp scripts/cr_pwa12_136_reconciliation_window_browser.py "$ROOT/tests/pwa12_136_reconciliation_window_browser.py"
(
  cd "$ROOT"
  python3 tools/rebundle_runtime.py
  python3 tools/build_pwa11.py "$VERSION"
) 2>&1 | tee out/build-and-rebundle.log
cp "$ROOT/build-meta.json" out/BUILD_META.json
python3 - "$ROOT" <<'PY'
import json,sys
from pathlib import Path
m=json.loads((Path(sys.argv[1])/'build-meta.json').read_text())
assert m['version']=='14.0.0-pwa.12.136-narrative-reconciliation-window-candidate.01',m
assert m['schemaVersion']==14,m
print('CANDIDATE_META',m)
PY
(
  cd "$ROOT"
  node --check src/runtime/runtime-bundle.js
  node tests/pwa12_136_reconciliation_window_contract.mjs
  node tests/pwa12_104_quiet_census_contract.mjs
  node tests/pwa12_104_paper_ghosts_contract.mjs
  node tests/pwa12_104_market_eyes_contract.mjs
  node tests/pwa12_71_inflight_save_load_contract.mjs
  python3 tests/pwa12_31_save_recovery_contract.py
  python3 tests/pwa12_38_save_snapshot_atomicity_contract.py
  python3 tests/pwa12_39_js_bundle_perf_contract.py
  python3 tests/pwa12_37_css_bundle_perf_contract.py
) 2>&1 | tee out/static-regression.log
(
  cd "$ROOT"
  if [ -f tools/release_preflight.py ]; then python3 tools/release_preflight.py; else echo 'release_preflight.py absent'; fi
) 2>&1 | tee out/release-preflight.log
python3 -m pip install --quiet playwright
python3 -m playwright install --with-deps chromium >/dev/null
PLAYWRIGHT_CHROMIUM=$(python3 -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); print(p.chromium.executable_path); p.stop()")
sudo ln -sf "$PLAYWRIGHT_CHROMIUM" /usr/bin/chromium
(
  cd "$ROOT"
  python3 tests/pwa12_136_reconciliation_window_browser.py
  python3 tests/pwa12_104_quiet_census_browser.py
  python3 tests/pwa12_104_paper_ghosts_browser.py
  python3 tests/pwa12_104_market_eyes_browser.py
  python3 tests/pwa12_71_inflight_save_load_browser.py
  python3 tests/pwa12_79_city_aftermath_browser.py
  STREET=$(find tests -maxdepth 1 -type f -iname '*street*combat*browser*.py' -print -quit)
  if [ -n "$STREET" ]; then python3 "$STREET"; else echo 'No dedicated street-combat browser test found by pattern'; fi
) 2>&1 | tee out/browser-regression.log
META=$(cat "$ROOT/build-meta.json")
cat > "$ROOT/DEVELOPMENT_NOTE_PWA12_136_NARRATIVE_RECONCILIATION_WINDOW_CANDIDATE_01.md" <<EOF
# Chrome Requiem PWA12.136 Narrative — RECONCILIATION WINDOW Candidate 01

## Baseline and canonical status
Built from verified cumulative noncanonical PWA12.136 Integration Release Candidate 01 (14.0.0-pwa.12.136-integration-release-candidate.01, build 93ded980c47a0abfde407f56, schema 14). The explicit PWA12.104 canonical source was not modified.

## Playable slice
QUIET CENSUS outcomes now reveal the existing hidden Helix Financial location loc_helix_hidden_1 / Settlement Vault Annex and create a physical-only RECONCILIATION WINDOW encounter in the ordinary City Network location panel.

The inherited Quiet Census methods remain mechanically distinct: AUTHENTICATED GHOST (evidence 1/3, lowest pressure), EXCEPTION CHANNEL (3/3, highest clean ledger access), CUSTODY CLAIM (2/3, broker-attested and slow), and PURGE WINDOW (2/3, active-record-movement state using authored action time rather than a real-time countdown).

At the physical Annex marker the player must make one irreversible decision. FOLLOW THE PRINCIPAL preserves a principal-side settlement token and writes quiet_census_principal_trace but leaves the live source map addressable. BURN THE SOURCE MAP deauthorizes the mapped clinic/freight/labor/debt source identities and writes quiet_census_source_shelter but destroys the clean principal trace.

The Principal is deliberately not identified here. Juno Voss remains a separate Helix contact. ZERO RECEIPT / Palisade staging remains quarantined and was not merged.

## Exact source changes
- Added src/narrative/reconciliation-window-v14.js.
- Added src/styles/37-v14-reconciliation-window.css with mobile-safe wrapping and >=48px authored action controls.
- Registered narrative.reconciliationWindow immediately after narrative.quietCensus in src/bootstrap/module-manifest.js.
- Added ordered JS/CSS bundle markers and rebuilt runtime-bundle.js / runtime-bundle.css from checked-in sources.
- Added the two raw files to build precache exclusions so shipping keeps using ordered bundles.
- Added tests/pwa12_136_reconciliation_window_contract.mjs and tests/pwa12_136_reconciliation_window_browser.py.

## Persistence
No schema bump. Durable state is additive journal metadata under reconciliation_window_v14, keyed from the Quiet Census source mission. Location discovery uses existing Game.cityLife.discovered; Meridian pressure uses existing Game.heat; action time uses existing advanceTime; save/load remains schema 14.

## Verification
See static-regression.log, release-preflight.log, and browser-regression.log beside this note. The focused contract covers all four incoming access states x two decisions, remote/active-mission gating, location discovery, exclusivity, idempotency, consequences, and save-shaped persistence. The Chromium test executes Market Eyes -> Paper Ghosts -> Quiet Census -> Settlement Vault Annex on 1440x900 desktop and 390x844 mobile, clicks the rendered choices, checks mobile horizontal overflow and >=44px button geometry, captures choice/outcome screenshots, then performs save -> live-state corruption -> runtime reload and compares restored state.

## Unresolved continuity / next target
FOLLOW THE PRINCIPAL should trace a blind settlement principal without prematurely naming a Meridian executive. BURN THE SOURCE MAP should produce a city source-protection consequence demonstrating who becomes harder to correlate and what investigative reach was sacrificed. Keep the two branches distinct for at least one further playable beat.

## Build meta
```json
$META
```
EOF
cp "$ROOT/DEVELOPMENT_NOTE_PWA12_136_NARRATIVE_RECONCILIATION_WINDOW_CANDIDATE_01.md" out/
mkdir -p out/qa
cp -a "$ROOT/qa/pwa12_136_reconciliation_window/." out/qa/
CANDIDATE='Chrome_Requiem_v14_PWA_pwa12_136_NARRATIVE_RECONCILIATION_WINDOW_CANDIDATE_01_source'
mv "$ROOT" "work/$CANDIDATE"
(
  cd work
  zip -qr "../out/${CANDIDATE}.zip" "$CANDIDATE"
)
sha256sum "out/${CANDIDATE}.zip" | tee out/SHA256.txt
cat out/BUILD_META.json
cat out/SHA256.txt
