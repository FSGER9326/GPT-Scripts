from pathlib import Path
s=Path(__file__).parents[1].joinpath('src/world/living-streets-v13-4a.js').read_text()
checks={
 'street combat effect wired': "case'streetCombat':setTimeout(()=>launchStreetCombatV134" in s,
 'hostile encounter offers tactical combat': "Stand and fight · tactical combat" in s,
 'street combat has no timer field': "v134StreetEncounter:true" in s and "timeLimit" not in s[s.index("function launchStreetCombatV134"):s.index("function triggerActorEncounterV134")],
 'uses normal combat entry': "V10PrevStartMission(m)" in s and "startMission(m)" in s,
 'physical district retained': "sectorId:world.id" in s,
 'street combat persisted': "stats.streetCombats" in s and "saveGame?.(0,true)" in s,
}
for k,v in checks.items(): print(('PASS' if v else 'FAIL'),k)
raise SystemExit(0 if all(checks.values()) else 1)
