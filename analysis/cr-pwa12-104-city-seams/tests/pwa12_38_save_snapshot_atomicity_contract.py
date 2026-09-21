from pathlib import Path
s=(Path(__file__).resolve().parents[1]/'src/runtime/legacy-save-bridge.js').read_text(encoding='utf-8')
checks={
 'payload captured synchronously after legacy save': "const ok=legacySave(n,quiet);" in s and "try{payload=JSON.parse(serialize())}" in s,
 'queued persistence receives captured payload': "queue(()=>persistSnapshot(n,payload))" in s,
 'async writer does not reserialize mutable game state': "async function persistSnapshot(slot,payload)" in s and "async function persistSnapshot(slot){" not in s,
 'capture failure does not enqueue corrupt snapshot': "save snapshot capture failed" in s and "return ok;" in s,
}
for k,v in checks.items(): print(('PASS' if v else 'FAIL'),k)
failed=[k for k,v in checks.items() if not v]
if failed: raise SystemExit('failed: '+', '.join(failed))
print('PASS PWA12.38 save snapshot atomicity contract')
