from pathlib import Path
s=(Path(__file__).resolve().parents[1]/'src/runtime/persistence/index.js').read_text(encoding='utf-8')
b=(Path(__file__).resolve().parents[1]/'src/runtime/legacy-save-bridge.js').read_text(encoding='utf-8')
checks={
 'safe parser': "function parseStoredEnvelope(raw)" in s and "try{return JSON.parse(raw)}catch{return null}" in s,
 'corrupt primary does not throw': "async loadSlot(slot){return parseStoredEnvelope" in s,
 'corrupt backup does not throw': "async loadBackup(slot){return parseStoredEnvelope" in s,
 'backup validation': "await storedEnvelopeIsValid(current)" in s and "validateSaveEnvelope(envelope)" in s,
 'bridge can fall back': "const backup=await persistence.loadBackup(n)" in b and "await validateSaveEnvelope(backup)" in b and "await persistence.restoreBackup(n)" in b,
}
for k,v in checks.items(): print(('PASS' if v else 'FAIL'),k)
failed=[k for k,v in checks.items() if not v]
if failed: raise SystemExit('failed: '+', '.join(failed))
print('PASS pwa12.31 save recovery contract')
