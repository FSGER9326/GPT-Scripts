#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 3:
    raise SystemExit('usage: cr_proc_c04_patch.py <candidate_root> <module_source>')
root=Path(sys.argv[1]).resolve()
source=Path(sys.argv[2]).read_text(encoding='utf-8-sig')
module=root/'src/missions/procedural-complications-v14.js'
module.write_text(source,encoding='utf-8')

build=root/'tools/build_pwa11.py'
text=build.read_text(encoding='utf-8')
entry="    'src/missions/procedural-complications-v14.js',\n"
anchor="    'src/missions/multistage-operations-v14.js',\n"
if entry not in text:
    if text.count(anchor)!=1:
        raise SystemExit('build source anchor missing or ambiguous')
    text=text.replace(anchor,anchor+entry,1)
    build.write_text(text,encoding='utf-8')

bundle=root/'src/runtime/runtime-bundle.js'
b=bundle.read_text(encoding='utf-8')
marker='/* SOURCE: src/missions/procedural-complications-v14.js */'
next_marker='/* SOURCE: src/visuals/visual-identity-v13-6.js */'
if marker not in b:
    if b.count(next_marker)!=1:
        raise SystemExit('runtime insertion anchor missing or ambiguous')
    b=b.replace(next_marker,marker+'\n'+source.rstrip()+'\n\n'+next_marker,1)
    bundle.write_text(b,encoding='utf-8')

print(f'integrated {module} ({module.stat().st_size} bytes)')
