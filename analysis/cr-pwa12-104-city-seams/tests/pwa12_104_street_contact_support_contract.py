from pathlib import Path
R=Path(__file__).resolve().parents[1]
for rel in ['src/world/living-streets-v13-4a.js','src/runtime/runtime-bundle.js']:
    s=(R/rel).read_text(encoding='utf-8')
    assert 'function streetContactSupportV134' in s
    assert "d.sectorId===world.id" in s
    assert "Game.contactRelations?.[d.id]?.known" in s
    assert "c.trust>=20" in s
    assert "c.trust>=45?2:1" in s
    assert "diff=Math.max(1,diff-1)" in s
    assert "support.tier>=2&&enemies.length>1" in s
    assert "v134ContactSupport:support?" in s
    assert "contact:support?.id||null" in s
    assert "No timer: initiative advances only when combatants act." in s
print('PWA12.104 street contact support contract PASS')
