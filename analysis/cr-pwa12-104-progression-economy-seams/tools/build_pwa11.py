from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, sys
ROOT=Path(__file__).resolve().parents[1]
VERSION=sys.argv[1] if len(sys.argv)>1 else '14.0.0-pwa.11'

# Stamp runtime-visible version before hashing the release.
index_path=ROOT/'index.html'
index_text=index_path.read_text(encoding='utf-8')
index_text=re.sub(r'window\.CR14_BUILD_VERSION=\"[^\"]+\"',f'window.CR14_BUILD_VERSION=\"{VERSION}\"',index_text,count=1)
index_path.write_text(index_text,encoding='utf-8')

# Manifest screenshots are install-store presentation assets, not runtime dependencies.
# Keeping them out of the mandatory offline precache avoids adding ~1.5 MB to every
# install/update while the manifest can still fetch them on demand when online.
PRECACHE_EXCLUDE={
    # PWA12.39: source modules are bundled into one ordered classic runtime file.
    'src/legacy/core-v5.js',
    'src/legacy/core-v5-api.js',
    'src/legacy/graphics-v6.js',
    'src/legacy/black-magic-v7.js',
    'src/legacy/mercenary-intelligence-v8.js',
    'src/legacy/performance-v9.js',
    'src/legacy/responsive-v10.js',
    'src/legacy/megacity-v11.js',
    'src/legacy/ground-war-v12.js',
    'src/legacy/city-life-v13.js',
    'src/legacy/city-life-v13-visual-fixes.js',
    'src/legacy/black-magic-recovery-v13-1.js',
    'src/legacy/mega-city-v13-2.js',
    'src/world/district-worlds-v13-3.js',
    'src/world/living-streets-v13-4a.js',
    'src/missions/contract-approaches-v13-4b.js',
    'src/company/company-foundation-v13-5.js',
    'src/world/action-time-v14.js',
    'src/missions/variable-arenas-v14.js',
    'src/missions/multistage-operations-v14.js',
    'src/visuals/visual-identity-v13-6.js',
    'src/bootstrap/module-manifest.js',
    'src/bootstrap/compatibility-manifest.js',
    'src/runtime/save-envelope.js',
    'src/runtime/save-transfer.js',
    'src/runtime/persistence/index.js',
    'src/runtime/migration/v13.js',
    'src/runtime/legacy-save-bridge.js',
    'src/runtime/persistence-lifecycle.js',
    'src/runtime/runtime.js',
    'src/bootstrap/compatibility.js',
    'src/runtime/pwa.js',
    'src/runtime/install.js',
    'src/runtime/connectivity.js',
    'src/visuals/asset-loader-v14.js',
    'src/visuals/urban-materials-v14.js',
    'src/visuals/urban-identity-v14.js',
    'src/visuals/environment-skin-v14.js',
    'src/visuals/district-presentation-v14.js',
    'src/visuals/location-presentation-v14.js',
    'src/visuals/street-presentation-v14.js',
    'src/visuals/tactical-presentation-v14.js',
    'src/visuals/combat-dossier-v14.js',
    'src/visuals/scene-presentation-v14.js',
    'src/visuals/pwa11-presentation-v14.js',
    'src/visuals/tactical-fire-control-v14.js',
    'src/bootstrap/bootstrap.js',
    'src/visuals/battlefield-atmosphere-v14.js',
    'src/styles/01-base.css',
    'src/styles/02-shell-polish.css',
    'src/styles/v14.css',
    'src/styles/22-v14-pwa12-2-environment-artpass.css',
    'src/styles/03-v10.css',
    'src/styles/04-v11.css',
    'src/styles/05-v12.css',
    'src/styles/06-v13.css',
    'src/styles/07-v13-review.css',
    'src/styles/08-v13-1.css',
    'src/styles/09-v13-2.css',
    'src/styles/10-v13-3.css',
    'src/styles/11-v13-4a.css',
    'src/styles/12-v13-4b.css',
    'src/styles/13-v13-5.css',
    'src/styles/14-v13-6.css',
    'src/styles/15-v13-6-dossiers.css',
    'src/styles/16-v13-6-combat.css',
    'src/styles/17-v14-visual-polish.css',
    'src/styles/18-v14-pwa10-unify.css',
    'src/styles/19-v14-pwa11-refine.css',
    'src/styles/20-v14-pwa12-artpass.css',
    'src/styles/21-v14-pwa12-tactical-artpass.css',
    'src/styles/23-v14-pwa12-4-role-silhouettes.css',
    'src/styles/24-v14-pwa12-5-fire-control.css',
    'src/styles/25-v14-pwa12-30-neon-command.css',
    'src/styles/25-v14-pwa12-29-exfil.css',
    'src/styles/26-v14-pwa12-39-city-signal-artpass.css',
    'src/styles/26-v14-variable-arenas.css',
    'src/styles/27-v14-multistage-operations.css',
    'src/styles/28-v14-pwa12-50-industrial-patina.css',
    'src/styles/29-v14-pwa12-59-blacksite-visuals.css',
    'src/styles/30-v14-pwa12-67-architecture.css',
    'src/styles/31-v14-pwa12-71-action-legibility.css',
    'src/styles/31-v14-pwa12-70-physical-patina.css',
    'src/styles/32-v14-grounded-rpg-direction.css',
    'src/styles/32-v14-premium-contact.css',
    'src/styles/33-v14-pwa12-81-grounded-scene.css',
    'assets/screenshots/wide-overworld.png',
    'assets/screenshots/phone-overworld.png',
}

def runtime_files():
    files=[ROOT/'index.html',ROOT/'manifest.webmanifest']
    for base in [ROOT/'assets',ROOT/'src']:
        files += [p for p in base.rglob('*') if p.is_file() and not p.name.startswith('.') and p.suffix != '.tmp']
    return sorted(
        {p for p in files if p.relative_to(ROOT).as_posix() not in PRECACHE_EXCLUDE},
        key=lambda p:p.relative_to(ROOT).as_posix(),
    )

files=runtime_files()
h=hashlib.sha256()
for p in files:
    rel=p.relative_to(ROOT).as_posix().encode()
    data=p.read_bytes()
    h.update(len(rel).to_bytes(4,'big')); h.update(rel)
    h.update(len(data).to_bytes(8,'big')); h.update(data)
build_hash=h.hexdigest()[:24]
entries=['./'+p.relative_to(ROOT).as_posix() for p in files]
pre='self.__CR14_PRECACHE=Object.freeze([\n'+''.join(f'  {json.dumps(x)},\n' for x in entries)+']);\n'
(ROOT/'precache-manifest.js').write_text(pre,encoding='utf-8')
sw=f"""importScripts('./precache-manifest.js');
const CACHE='chrome-requiem-v14-{build_hash}';
const PRECACHE=self.__CR14_PRECACHE||[];
const PRECACHE_BATCH_SIZE=48;
// Reuse one handle to the active build cache. This avoids a CacheStorage-wide
// caches.match() scan and repeated caches.open() calls on every same-origin fetch.
const ACTIVE_CACHE=caches.open(CACHE);
async function installPrecache(){{
  const cache=await ACTIVE_CACHE;
  for(let i=0;i<PRECACHE.length;i+=PRECACHE_BATCH_SIZE){{
    await cache.addAll(PRECACHE.slice(i,i+PRECACHE_BATCH_SIZE));
  }}
}}
self.addEventListener('install',event=>event.waitUntil(installPrecache()));
self.addEventListener('message',event=>{{if(event.data?.type==='CR14_ACTIVATE_UPDATE')self.skipWaiting()}});
self.addEventListener('activate',event=>event.waitUntil((async()=>{{for(const k of await caches.keys())if(k.startsWith('chrome-requiem-v14-')&&k!==CACHE)await caches.delete(k);await self.clients.claim()}})()));
self.addEventListener('fetch',event=>{{if(event.request.method!=='GET')return;const u=new URL(event.request.url);if(u.origin!==self.location.origin)return;if(event.request.mode==='navigate'){{event.respondWith(ACTIVE_CACHE.then(c=>c.match('./index.html')).then(r=>r||fetch(event.request)));return}}event.respondWith(ACTIVE_CACHE.then(c=>c.match(event.request)).then(r=>r||fetch(event.request)))}});
"""
(ROOT/'service-worker.js').write_text(sw,encoding='utf-8')
meta={
  'version':VERSION,
  'buildHash':build_hash,
  'builtAt':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),
  'schemaVersion':14,
  'releaseTarget':'pwa'
}
(ROOT/'build-meta.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'version':VERSION,'buildHash':build_hash,'precache':len(entries)},indent=2))
