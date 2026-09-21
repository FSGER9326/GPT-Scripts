from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
for rel in ["src/visuals/street-presentation-v14.js","src/runtime/runtime-bundle.js"]:
 s=(ROOT/rel).read_text(encoding="utf-8")
 assert re.search(r"function candidateNear\(world,hover,interactables=null,(?:actors|streetActors)=null\)",s), "candidate proximity signature changed"
 assert re.search(r"const actors=(?:streetActors|actors)(?:\?\?|\|\|)window\.ensureStreetActorsV134",s), "actor snapshot not reused by proximity"
 assert "const interactables=window.ensureInteractablesV134?.(world)||[]" in s
 assert "const streetActors=window.ensureStreetActorsV134?.(world)||[]" in s
 assert "updateStreetProximity(world,hover,interactables,streetActors)" in s
 assert "for(const a of streetActors)" in s
print("PASS PWA12.64 street snapshot reuse performance contract")
