from pathlib import Path
s=Path('src/world/living-streets-v13-4a.js').read_text()
checks={
 'population aftermath function':'function applyStreetClashPopulationV134' in s,
 'spatial district scope':'clash.district!==world?.id' in s,
 'spatial neighborhood scope':'n.id===clash.neighborhood' in s,
 'gang victory clears visible gang':'if(a.type===\'gang\'||a.type===\'wraith\')a.type=\'courier\'' in s,
 'gang defeat reinforces gang':'a.type=clash.actorType' in s,
 'law victory reinforces patrol':'a.type=\'security\'' in s,
 'law defeat thins patrol':'a.type=\'worker\'' in s,
 'idempotent stamp':'s.populationAftermath?.[world.id]===stamp' in s,
 'applied to existing actors':'return applyStreetClashPopulationV134(world,s.actors[world.id],s)' in s,
 'applied to generated actors':'return applyStreetClashPopulationV134(world,actors,s)' in s,
 'settlement immediate apply':'applyStreetClashPopulationV134(currentWorldV134(),ensureStreetActorsV134(currentWorldV134()),s)' in s,
}
bad=[k for k,v in checks.items() if not v]
assert not bad,bad
print('PASS PWA12.88: Street Clash outcomes reshape visible local street population, spatially scoped and idempotent')
