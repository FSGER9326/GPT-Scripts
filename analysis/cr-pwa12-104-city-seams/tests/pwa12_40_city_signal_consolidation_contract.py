from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
idx=(ROOT/'index.html').read_text()
css=(ROOT/'src/styles/runtime-bundle.css').read_text()
manifest=(ROOT/'precache-manifest.js').read_text()
assert './src/runtime/runtime-bundle.js' in idx
assert 'src/legacy/core-v5.js' not in idx
source_css=(ROOT/'src/styles/26-v14-pwa12-39-city-signal-artpass.css').read_text()
assert '.v13-location-card::after' in source_css and '.v13-contact-portrait::after' in source_css
# Later presentation passes may override literal labels, so verify the City Signal
# selectors survive in the ordered bundle rather than pinning obsolete microcopy.
assert '.v13-location-card::after' in css
assert '.v13-contact-portrait::after' in css
assert (ROOT/'assets/generated/ui/city-signal-grid.svg').exists()
assert './assets/generated/ui/city-signal-grid.svg' in manifest
assert './src/styles/26-v14-pwa12-39-city-signal-artpass.css' not in manifest
print('PASS: PWA12.40 City Signal + runtime-bundle consolidation contract')
