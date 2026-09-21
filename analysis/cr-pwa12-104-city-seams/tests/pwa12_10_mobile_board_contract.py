from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
css=(ROOT/'src/styles/20-v14-pwa12-artpass.css').read_text(encoding='utf-8')
assert '@media(max-width:760px)' in css
assert '#combat.active:not(.v10-landscape-combat)>#board{flex-shrink:0!important}' in css
print('PASS pwa12.10 mobile board contract')
