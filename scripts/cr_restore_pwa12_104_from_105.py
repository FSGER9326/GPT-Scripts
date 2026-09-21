from pathlib import Path
import sys, shutil

root=Path(sys.argv[1]).resolve()

# Reverse only the PWA12.105 Faction Street Favor candidate delta. The restored
# runtime is accepted as canonical only if rebuilding reproduces the recorded
# PWA12.104 deterministic build hash in the caller.
p=root/'src/world/living-streets-v13-4a.js'
s=p.read_text(encoding='utf-8')
new="s.actorCooldown=s.actorCooldown||{};s.stats=s.stats||{events:0,interactions:0,patrolContacts:0,contracts:0,routes:0};s.streetContracts=s.streetContracts||[];s.contactFavors=s.contactFavors||{};s.contactFavorHistory=s.contactFavorHistory||{};"
old="s.actorCooldown=s.actorCooldown||{};s.stats=s.stats||{events:0,interactions:0,patrolContacts:0,contracts:0,routes:0};s.streetContracts=s.streetContracts||[];"
if s.count(new)!=1:
    raise SystemExit(f'unexpected state seam count={s.count(new)}')
s=s.replace(new,old,1)

start='\n\n// PWA12.105 candidate — a local contact who materially supported a won Street Clash\n'
end='window.decorateStreetFavorDossierV134=decorateStreetFavorDossierV134;\n'
a=s.find(start)
if a<0: raise SystemExit('PWA12.105 feature start missing')
b=s.find(end,a)
if b<0: raise SystemExit('PWA12.105 feature end missing')
s=s[:a]+s[b+len(end):]

hook="const relation=m.contact&&Game.contactRelations?.[m.contact];if(success&&relation?.known&&typeof changeContactTrustV13==='function')changeContactTrustV13(m.contact,1,'Won a street clash nearby');"
patched=hook+"if(success)awardStreetFavorV134(m);"
if s.count(patched)!=1:
    raise SystemExit(f'PWA12.105 settlement hook count={s.count(patched)}')
s=s.replace(patched,hook,1)
p.write_text(s,encoding='utf-8')

cityp=root/'src/legacy/city-life-v13.js'
city=cityp.read_text(encoding='utf-8')
needle='\n window.decorateStreetFavorDossierV134?.(id);\n}\nwindow.renderContactDossierV13=renderContactDossierV13;'
original='\n}\nwindow.renderContactDossierV13=renderContactDossierV13;'
if city.count(needle)!=1:
    raise SystemExit(f'PWA12.105 dossier hook count={city.count(needle)}')
city=city.replace(needle,original,1)
cityp.write_text(city,encoding='utf-8')

for rel in [
    'tests/pwa12_105_street_favor_contract.py',
    'tests/pwa12_105_street_favor_browser.py',
    'DEVELOPMENT_NOTE_PWA12_105_FACTION_STREET_FAVORS.md',
    'qa/pwa12-105-street-favor-mobile.png',
]:
    q=root/rel
    if q.exists(): q.unlink()

print('reversed PWA12.105 Street Favor delta from',root)
