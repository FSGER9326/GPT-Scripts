from pathlib import Path
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
raw=(ROOT/'index.html').read_text(encoding='utf-8')
shim="""<script>const __crls=(()=>{const s=new Map();return{getItem:k=>s.has(String(k))?s.get(String(k)):null,setItem:(k,v)=>s.set(String(k),String(v)),removeItem:k=>s.delete(String(k)),clear:()=>s.clear(),key:i=>[...s.keys()][i]??null,get length(){return s.size}}})();try{Object.defineProperty(window,'localStorage',{value:__crls,configurable:true})}catch(e){};try{Object.defineProperty(window,'sessionStorage',{value:__crls,configurable:true})}catch(e){}</script>"""
html=raw.replace('<head>','<head><base href="http://cr.local/">'+shim,1).replace('bootChromeRequiemV14({registerPwa:true})','bootChromeRequiemV14({registerPwa:false})')

def run(pw,label,opts):
    b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    ctx=b.new_context(**opts);p=ctx.new_page();miss=[];errs=[]
    def h(route):
        u=route.request.url
        if not u.startswith('http://cr.local/'):return route.abort()
        rel=u[len('http://cr.local/'):].split('?',1)[0] or 'index.html';fp=ROOT/rel
        if fp.exists() and fp.is_file():route.fulfill(status=200,body=fp.read_bytes(),content_type=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream')
        else:miss.append(rel);route.fulfill(status=404,body=b'x',content_type='text/plain')
    p.route('http://cr.local/**',h);p.on('pageerror',lambda e:errs.append(str(e)))
    p.set_content(html,wait_until='domcontentloaded');p.wait_for_function('()=>!!window.ChromeRequiemV14Boot?.ready',timeout=15000);p.wait_for_timeout(80)
    def overflow():return p.evaluate('()=>Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)-innerWidth')
    result={'label':label,'introOverflow':overflow()}
    p.evaluate("showScreen('charcreate');renderCharCreate()");p.wait_for_timeout(60);result['charOverflow']=overflow();result['charDossier']=p.evaluate("()=>document.querySelector('.cr11-cc-dossier')?.getBoundingClientRect().toJSON()||null")
    p.evaluate("""()=>{startNewGame('Vex','Hacker','street');document.getElementById('story-modal')?.classList.remove('open');Game.crewTab='roster';showScreen('crew');renderCrewScreen()}""");p.wait_for_timeout(60);result['crewOverflow']=overflow()
    p.evaluate("Game.crewTab='skills';renderCrewScreen()");p.wait_for_timeout(60);result['skillsOverflow']=overflow()
    p.evaluate("renderMarketV13('s_needle');showScreen('v13-market-screen')");p.wait_for_timeout(60);result['marketOverflow']=overflow()
    p.evaluate("renderClinicV13('s_vela');showScreen('v13-clinic-screen')");p.wait_for_timeout(60);result['clinicOverflow']=overflow()
    p.evaluate("""()=>{showScreen('overworld-screen');activateDistrictV133('old_market',null);initOverworld();Game.ovStaticDirty=true}""");p.wait_for_timeout(100);result['worldOverflow']=overflow();result['wait']=p.evaluate("()=>{let r=document.getElementById('ov-wait-btn')?.getBoundingClientRect();return r?.toJSON()||null}")
    p.evaluate("""()=>{const m={id:'qa_resp',name:'RESPONSIVE QA',desc:'Responsive QA',type:'eliminate',objective:'eliminate',sectorId:'old_market',targetFaction:'spine',enemies:['Guard','Enforcer'],diff:2,reward:1,xp:1,factionRepGain:0,factionRepLoss:{}};Game.activeMission=m;showScreen('combat');initCombat(m);document.getElementById('banner')?.classList.remove('show')}""");p.wait_for_timeout(140);result['combatOverflow']=overflow();result['board']=p.evaluate("()=>document.getElementById('board').getBoundingClientRect().toJSON()");result['actions']=p.evaluate("()=>[...document.querySelectorAll('#actions>button')].map(b=>b.getBoundingClientRect().height)")
    for key in ['introOverflow','charOverflow','crewOverflow','skillsOverflow','marketOverflow','clinicOverflow','worldOverflow','combatOverflow']:
        assert result[key]<=1,(label,key,result)
    assert result['wait'] and result['wait']['height']>=44,(label,result['wait'])
    assert result['board']['width']>220 and result['board']['height']>220,(label,result['board'])
    assert result['actions'] and min(result['actions'])>=44,(label,result['actions'])
    assert not errs,(label,errs); assert not miss,(label,miss)
    ctx.close();b.close();return result

with sync_playwright() as pw:
    phone=dict(pw.devices['Pixel 7']);phone.pop('default_browser_type',None)
    portrait=run(pw,'pixel7',phone)
    landscape=run(pw,'landscape',{'viewport':{'width':915,'height':412},'has_touch':True,'is_mobile':True,'device_scale_factor':1})
    print('PWA11 RESPONSIVE PASS',{'portrait':portrait,'landscape':landscape})
