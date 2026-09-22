from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve()
bundle=root/'src/runtime/runtime-bundle.js'
module_rel='src/world/district-dispatches-pwa12-104-city-candidate-01.js'
module=root/module_rel
if not module.is_file():
    raise SystemExit(f'missing district dispatch module: {module}')
text=bundle.read_text(encoding='utf-8')
marker=f'/* SOURCE: {module_rel} */'
if marker in text:
    print('district dispatch runtime marker already present')
    raise SystemExit(0)
next_marker='/* SOURCE: src/missions/contract-approaches-v13-4b.js */'
prev_marker='/* SOURCE: src/world/living-streets-v13-4a.js */'
if text.count(prev_marker)!=1 or text.count(next_marker)!=1:
    raise SystemExit(f'unexpected runtime seam counts living={text.count(prev_marker)} approaches={text.count(next_marker)}')
if text.index(prev_marker) >= text.index(next_marker):
    raise SystemExit('runtime source order is not living-streets before contract-approaches')
insert=marker+'\n'+module.read_text(encoding='utf-8').rstrip()+'\n\n'
text=text.replace(next_marker,insert+next_marker,1)
bundle.write_text(text,encoding='utf-8')
print('inserted district dispatch runtime source marker between Living Streets and mission approaches')
