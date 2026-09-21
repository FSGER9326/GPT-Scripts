from pathlib import Path
root=Path(__file__).resolve().parents[1]
living=(root/'src/world/living-streets-v13-4a.js').read_text()
arenas=(root/'src/missions/variable-arenas-v14.js').read_text()
assert "tacticalShape:streetShape" in living
assert "actorType==='security'||actorType==='contractor'?'checkpoint'" in living
assert "actorType==='hunter'?'alley'" in living
assert "['undergrid','floodline','dock_nine'].includes(world.id)?'underpass':'alley'" in living
for shape,label in [('alley','NEON SERVICE ALLEY'),('checkpoint','CORPORATE CHECKPOINT'),('underpass','SERVICE UNDERPASS')]:
    assert f"{shape}: {{" in arenas and label in arenas
assert "if (LAYOUTS[mission.tacticalShape]) return mission.tacticalShape" in arenas
print('PASS PWA12.90 street arena contract')
