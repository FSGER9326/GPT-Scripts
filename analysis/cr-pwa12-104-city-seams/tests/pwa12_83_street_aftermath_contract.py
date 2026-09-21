from pathlib import Path
s=Path(__file__).parents[1].joinpath('src/world/living-streets-v13-4a.js').read_text()
checks={
 'street mission records neighborhood': 'v134StreetNeighborhood:hood?.id||null' in s,
 'actor faction is physical encounter faction': "actorFaction={wraith:'wraiths',gang:'iron'" in s,
 'success aftermath event hook': "Events.on('mission:success',m=>settleStreetCombatV134(m,true))" in s,
 'failure aftermath extraction hook': "m?.v134StreetEncounter&&success===false" in s,
 'neighborhood heat reacts': "h.localHeat=clampV134" in s,
 'gang pressure reacts': "h.gangPressure=clampV134" in s,
 'security reacts': "h.security=clampV134" in s,
 'faction heat reacts': "Game.heat[m.targetFaction]" in s,
 'contact trust reacts': "changeContactTrustV13(m.contact,1,'Won a street clash nearby')" in s,
 'outcome persisted': 's.lastStreetCombat=' in s and 'saveGame?.(0,true)' in s,
 'no street combat timer': 'v134StreetEncounter:true' in s and 'timeLimit' not in s[s.index('function launchStreetCombatV134'):s.index('function settleStreetCombatV134')],
}
for k,v in checks.items(): print(('PASS' if v else 'FAIL'),k)
assert all(checks.values())
