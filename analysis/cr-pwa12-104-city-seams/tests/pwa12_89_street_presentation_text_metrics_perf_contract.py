from pathlib import Path
root=Path(__file__).resolve().parents[1]
street=(root/'src/visuals/street-presentation-v14.js').read_text()
assert 'function cachedPresentationTextWidthV14' in street
block=street[street.index('function drawLivingStreetsV14'):street.index('function prime()')]
assert 'ctx.measureText(' not in block, 'street presentation still measures unchanged actor labels every active frame'
assert 'cachedPresentationTextWidthV14(ctx,label)' in block
print('PWA12.89 street-presentation text-metrics cache contract PASS')
