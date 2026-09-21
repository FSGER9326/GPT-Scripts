from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
street=(ROOT/'src/visuals/street-presentation-v14.js').read_text()
loc=(ROOT/'src/visuals/location-presentation-v14.js').read_text()
assert 'const vehicleRowCache=new WeakMap();' in street
assert 'const cached=vehicleRowCache.get(world);if(cached)return cached;' in street
assert 'vehicleRowCache.set(world,rows);return rows;' in street
# One deterministic vehicle placement resolution lives in vehicleRows; drawVehicles only consumes it.
assert street.count("window.nearestWalkableV134?.(world,n.x+Math.cos(ang)*rad") == 1
assert 'function updateSiteProximityHud(world,hover,rows=null)' in loc
assert 'const rows=markerRows(world);let drawn=0;' in loc
assert 'for(const m of rows)' in loc
assert 'state.lastTypes=[...new Set(rows.map(m=>m.type))]' in loc
assert 'updateSiteProximityHud(world,hover,rows);' in loc
print('PASS active-city perf: deterministic vehicle placement cached per district object; location marker snapshot reused across draw/state/HUD')
