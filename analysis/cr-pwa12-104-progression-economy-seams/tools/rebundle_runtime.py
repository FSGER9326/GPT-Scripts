"""Reassemble the shipping ordered runtime from its checked-in source markers.

Does not alter ordering, preload semantics or exclude raw development source files.
"""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
for bundle in ('src/runtime/runtime-bundle.js','src/styles/runtime-bundle.css'):
    path=ROOT/bundle
    original=path.read_text(encoding='utf-8')
    names=re.findall(r'/\* SOURCE: ([^*]+?) \*/',original)
    if len(names)<20 or len(names)!=len(set(names)):
        raise RuntimeError(f'{bundle}: unexpected or duplicate module markers')
    content=''.join(f'/* SOURCE: {name} */\n'+(ROOT/name).read_text(encoding='utf-8').rstrip()+'\n\n' for name in names)
    path.write_text(content,encoding='utf-8')
    print(f'{bundle}: bundled {len(names)} ordered sources')
