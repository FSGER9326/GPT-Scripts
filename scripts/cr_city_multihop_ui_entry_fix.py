from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve();p=root/'src/world/multihop-logistics-pwa12-104-city-candidate-04.js'
s=p.read_text(encoding='utf-8')
a=s.find('function enhanceOffer(){');b=s.find('function update(){',a)
if a<0 or b<0: raise SystemExit('multi-hop offer UI seam missing')
new=r'''function enhanceOffer(){const w=world(),n=nearSource(w);if(!n)return;const o=offer(n.id,w);if(!o)return;const base=document.getElementById('v12104-interdistrict-panel'),local=document.getElementById('v12104-dispatch-panel');if(base&&base.style.display!=='none'){if(base.querySelector('#v12104-multi-accept'))return;const box=document.createElement('div');box.className='choice';box.id='v12104-multi-offer';box.innerHTML=`<div class="k">LONG-HAUL OPTION</div><div class="meta">${o.sourceName} → ${o.handoffName} → ${o.finalName}<br>2 physical crossings · intermediate handoff · ¢${o.estimatedPayout} est.</div><button class="btn small" id="v12104-multi-accept">ACCEPT MULTI-HOP RUN</button>`;base.appendChild(box);box.querySelector('#v12104-multi-accept').onclick=()=>accept(o.id);return}if(local&&local.style.display!=='none'&&!local.querySelector('#v12104-open-multihop')){const wrap=document.createElement('div');wrap.id='v12104-multi-teaser';wrap.className='meta';wrap.innerHTML=`<div style="margin-top:6px"><b>LONG-HAUL:</b> ${o.handoffName} → ${o.finalName} · 2 crossings · ¢${o.estimatedPayout} est.</div>`;const btn=document.createElement('button');btn.className='btn small';btn.id='v12104-open-multihop';btn.textContent='MULTI-HOP RUN · 2 LEGS';btn.title=`${o.sourceName} → ${o.handoffName} → ${o.finalName}`;btn.onclick=()=>accept(o.id);wrap.appendChild(btn);(local.querySelector('.actions')||local).appendChild(wrap)}}
'''
s=s[:a]+new+s[b:]
p.write_text(s,encoding='utf-8')
print('fixed multi-hop discoverability on preserved local dispatch board')
