"""PWA12.134: squad pressure reservations distribute attacks without omniscient focus fire."""
from pathlib import Path
import mimetypes
import sys
from playwright.sync_api import sync_playwright

ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text(encoding='utf-8')
SHIM="""<script>const __s=new Map();const __ls={getItem:k=>__s.has(String(k))?__s.get(String(k)):null,setItem:(k,v)=>__s.set(String(k),String(v)),removeItem:k=>__s.delete(String(k)),clear:()=>__s.clear(),key:i=>[...__s.keys()][i]??null,get length(){return __s.size}};Object.defineProperty(window,'localStorage',{value:__ls,configurable:true});Object.defineProperty(window,'sessionStorage',{value:__ls,configurable:true});</script>"""
HTML=HTML.replace('<head>','<head><base href="http://cr.local/">'+SHIM,1).replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    page=browser.new_page(viewport={'width':390,'height':844})
    errors=[]
    def route(r):
        rel=r.request.url.split('http://cr.local/',1)[1].split('?',1)[0] or 'index.html'
        fp=ROOT/rel
        if fp.is_file():
            r.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream')
        else:
            r.fulfill(status=404,body=b'not found')
    page.route('http://cr.local/**',route)
    page.on('pageerror',lambda e: errors.append(str(e)))
    page.set_content(HTML,wait_until='domcontentloaded')
    page.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=45000)
    result=page.evaluate("""async()=>{
      startNewGame('Vex','Hacker','street');
      document.getElementById('story-modal')?.classList.remove('open');showScreen('combat');
      const m={id:'pwa134_pressure',type:'eliminate',objective:'eliminate',name:'Pressure Reservation QA',desc:'QA',diff:2,enemies:['Guard','Enforcer','Heavy'],reward:1,xp:1,targetFaction:'meridian'};
      Game.activeMission=m;initCombat(m);Game.alerted=true;
      Game.turnQueue=[];Game.turnIndex=0;Game.turn='player';
      for(const c of Game.grid){c.obstacle=false;c.door=false;c.doorOpen=false;c.doorLocked=false;c.enemyAccessBlockedV14=false;c.unit=null;c.hazard=false;c.fire=0;c.cover=0}
      const hacker=Game.units.find(u=>u.team==='player');
      for(const p of Game.units.filter(u=>u.team==='player'&&u!==hacker)){p.hp=0;p.dead=true}
      const guard=Game.units.find(u=>u.team==='enemy'&&u.className==='Guard');
      const enforcer=Game.units.find(u=>u.team==='enemy'&&u.className==='Enforcer');
      const heavy=Game.units.find(u=>u.team==='enemy'&&u.className==='Heavy');
      const front=makeUnit('Bulwark','Cyber Sword',1);front.team='player';front.dead=false;front.statuses={};front.hp=25;front.maxHp=120;front.damage=20;front.armor=0;front.x=5;front.y=4;Game.units.push(front);
      Object.assign(hacker,{x:6,y:4,team:'player',statuses:{},hp:70,maxHp:70,damage:11,armor:0,dead:false});
      Object.assign(guard,{x:1,y:4,move:0,range:1,damage:9,ap:2,maxAp:2,dead:false});
      Object.assign(enforcer,{x:1,y:5,move:0,range:3,ap:2,maxAp:2,dead:false});
      Object.assign(heavy,{x:1,y:6,move:0,range:1,ap:2,maxAp:2,dead:false});
      cellAt(hacker.x,hacker.y).unit=hacker;cellAt(front.x,front.y).unit=front;cellAt(guard.x,guard.y).unit=guard;cellAt(enforcer.x,enforcer.y).unit=enforcer;cellAt(heavy.x,heavy.y).unit=heavy;
      syncCombatUnits();Game.losCache?.clear();delete Game.enemyContactsV133;delete Game.enemyPressureV134;
      beginEnemyContactActivationV133();
      const beforeGuard=chooseEnemyTargetV134(guard,[hacker,front]);
      const beforeEnforcer=chooseEnemyTargetV134(enforcer,[hacker,front]);
      const oldEnd=endUnitTurn;endUnitTurn=async()=>{};
      try{await enemyAITakeTurn(guard)}finally{endUnitTurn=oldEnd}
      const board=pruneEnemyPressureV134(),claim=[...board.reservations.values()].find(r=>r.enemyRef===guard);
      const afterEnforcer=chooseEnemyTargetV134(enforcer,[hacker,front]);
      const livePressure={beforeGuard:beforeGuard?.name,beforeEnforcer:beforeEnforcer?.name,afterEnforcer:afterEnforcer?.name,kind:claim?.kind||null,targetKey:claim?.targetKey||null,intent:guard.contactIntentV133||'',cue:guard.el?.querySelector('.v133-contact-cue')?.textContent||'',count:board.reservations.size};
      updateCombat();

      // A guaranteed finish is a stronger, shorter reservation and visibly marked FIN.
      delete Game.enemyPressureV134;front.hp=7;cellAt(guard.x,guard.y).unit=null;guard.x=4;guard.y=4;guard.range=2;guard.ap=2;cellAt(4,4).unit=guard;Game.losCache?.clear();
      const lethal=reserveEnemyPressureV134(guard,front);
      const lethalShift=chooseEnemyTargetV134(enforcer,[hacker,front]);
      const lethalCase={kind:lethal?.kind||null,intent:guard.contactIntentV133||'',cue:guard.el?.querySelector('.v133-contact-cue')?.textContent||'',shift:lethalShift?.name||null,ttl:(lethal?.expiresAt??0)-enemyContactStateV133().epoch};

      // Last-known snapshots may carry pressure intent, but can never become a claimed guaranteed hit.
      delete Game.enemyPressureV134;delete Game.enemyContactsV133;front.hp=25;publishEnemyContactV133(guard,hacker);
      const contact=chooseEnemyContactV133(enforcer),proxy=enemyContactProxyV133(contact),contactClaim=reserveEnemyPressureV134(enforcer,proxy,{contact:true});
      const contactCase={lastKnown:!!proxy?._lastKnownV133,kind:contactClaim?.kind||null,targetRef:contactClaim?.targetRef??null,guaranteed:enemyGuaranteedHitV134(enforcer,proxy),x:proxy?.x,y:proxy?.y};

      const serialized=serializeGame(),oldPressure=enemyPressureStateV134(),oldCount=oldPressure.reservations.size;
      Game.grid=[...Game.grid];const freshPressure=enemyPressureStateV134();
      const isolation={saveLeak:serialized.includes('enemyPressureV134')||serialized.includes('pressureIntentV134'),oldCount,freshCount:freshPressure.reservations.size,freshIdentity:freshPressure!==oldPressure};
      return {viewport:innerWidth,livePressure,lethalCase,contactCase,isolation};
    }""")
    assert not errors,errors
    assert result['viewport']==390,result
    assert result['livePressure']['beforeGuard']=='Bulwark',result
    assert result['livePressure']['beforeEnforcer']=='Bulwark',result
    assert result['livePressure']['kind']=='pressure',result
    assert result['livePressure']['afterEnforcer']=='Vex',result
    assert result['livePressure']['intent']=='PIN' and result['livePressure']['cue']=='PIN',result
    assert result['livePressure']['count']>=1,result
    assert result['lethalCase']['kind']=='lethal',result
    assert result['lethalCase']['intent']=='FIN' and result['lethalCase']['cue']=='FIN',result
    assert result['lethalCase']['shift']=='Vex' and result['lethalCase']['ttl']==2,result
    assert result['contactCase']['lastKnown'] is True,result
    assert result['contactCase']['kind']=='pressure' and result['contactCase']['targetRef'] is None,result
    assert result['contactCase']['guaranteed']==0,result
    assert result['isolation']['saveLeak'] is False,result
    assert result['isolation']['oldCount']==1 and result['isolation']['freshCount']==0 and result['isolation']['freshIdentity'] is True,result
    # Restore a real pressure state for the captured mobile combat image.
    page.evaluate("""()=>{Game.grid=enemyPressureStateV134().grid;updateCombat()}""")
    shot=ROOT/'qa/pwa12-134-target-pressure-mobile.png'
    page.screenshot(path=str(shot),full_page=True)
    print('PASS PWA12.134 target pressure reservations',result)
    print('SCREENSHOT',shot)
    browser.close()
