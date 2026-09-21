from pathlib import Path
ROOT=Path(__file__).parents[1]
s=(ROOT/'src/world/living-streets-v13-4a.js').read_text();c=(ROOT/'src/styles/11-v13-4a.css').read_text()
checks={'persisted clash':'ensureLivingStreetsStateV134().lastStreetCombat' in s,'district scope':'clash.district===world.id' in s,'neighborhood scope':'clash.neighborhood===h.id' in s,'outcome':"clash.success?'BLOCK HELD':'BLOCK CEDED'" in s,'actor':'actorLabelV134(clash.actorType)' in s,'styles':'.v134-clash-status.won' in c and '.v134-clash-status.lost' in c}
for k,v in checks.items():print(('PASS' if v else 'FAIL'),k)
assert all(checks.values())
