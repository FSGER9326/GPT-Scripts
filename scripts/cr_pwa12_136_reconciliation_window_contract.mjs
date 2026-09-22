import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const source=readFileSync(new URL('../src/narrative/reconciliation-window-v14.js',import.meta.url),'utf8');

const profiles={
  quiet_census_clean_access:{branch:'civic',ally:'c9',leverage:'ghost_credential',point:{x:17,y:11},followHeat:2,burnHeat:-4,evidence:1,burnEvidence:1,key:'authenticated_ghost'},
  quiet_census_exception_key:{branch:'civic',ally:'c9',leverage:'exception_snapshot',point:{x:17,y:11},followHeat:6,burnHeat:-1,evidence:3,burnEvidence:2,key:'exception_channel'},
  quiet_census_chain_of_custody:{branch:'market',ally:'c23',leverage:'broker_chain',point:{x:17,y:11},followHeat:3,burnHeat:-2,evidence:2,burnEvidence:2,key:'custody_claim'},
  quiet_census_public_proof:{branch:'market',ally:'c23',leverage:'broker_witnesses',point:{x:17,y:11},followHeat:8,burnHeat:2,evidence:2,burnEvidence:2,key:'purge_window'}
};
function make(modifier,{remote=false}={}){
  const p=profiles[modifier];
  const Game={day:12,hour:20,activeMission:null,journal:[{
    id:`quiet_census_outcome_${modifier}`,narrativeKey:'quiet_census_v14',quietCensusStage:'outcome',branch:p.branch,
    sourceMissionId:'src',allyContactId:p.ally,leverage:p.leverage,nextModifier:modifier,nextHook:'quiet_census_reconciliation_window',
    contractorId:'quiet_census',contractorName:'QUIET CENSUS CIVIC ANALYTICS',day:12
  }],heat:{meridian:30},cityLife:{currentLocation:'loc_helix_hidden_1',discovered:{}},districtWorldsV133:{activeId:'helix_financial'},ovPlayer:remote?{x:0,y:0}:{...p.point}};
  const root={Game,window:null,globalThis:null,console,document:null,saves:0,logs:[],
    generateDistrictV133:(id)=>({locations:id==='helix_financial'?{loc_helix_hidden_1:{...p.point}}:{}}),
    advanceTime:(minutes)=>{Game.hour+=minutes/60},saveGame:()=>{root.saves++},logMsg:(msg)=>root.logs.push(msg)
  };
  root.window=root;root.globalThis=root;const context=vm.createContext(root);vm.runInContext(source,context,{filename:'reconciliation-window-v14.js'});
  return {root,Game,api:root.CR14ReconciliationWindowV14,p};
}

for(const [modifier,p] of Object.entries(profiles)){
  for(const decision of ['follow_principal','burn_source_map']){
    const {Game,api}=make(modifier);
    const lead=api.ensureLead();
    assert.equal(lead.locationId,'loc_helix_hidden_1');
    assert.equal(lead.accessModifier,modifier);
    assert.equal(lead.branch,p.branch);assert.equal(lead.allyContactId,p.ally);assert.equal(lead.priorLeverage,p.leverage);
    assert.equal(Game.cityLife.discovered.loc_helix_hidden_1,true,'lead must reveal physical target');
    assert.equal(api.ensureLead().id,lead.id);assert.equal(Game.journal.filter(x=>x.reconciliationStage==='lead').length,1);
    assert.equal(api.atTarget(),true);assert.equal(api.decisionAvailable(decision),true);
    const before=Game.heat.meridian;
    assert.equal(api.resolve(decision),true,`${modifier} ${decision} should resolve`);
    const out=api.resolution();assert.ok(out);
    assert.equal(out.accessModifier,modifier);assert.equal(out.accessKey,p.key);assert.equal(out.branch,p.branch);assert.equal(out.allyContactId,p.ally);
    assert.equal(out.contractorName,'QUIET CENSUS CIVIC ANALYTICS');
    const delta=decision==='follow_principal'?p.followHeat:p.burnHeat;
    assert.equal(Game.heat.meridian,Math.max(0,Math.min(100,before+delta)));
    if(decision==='follow_principal'){
      assert.equal(out.principalTrace,true);assert.equal(out.sourceMapBurned,false);assert.equal(out.sourceProtection,'exposed');
      assert.equal(out.nextHook,'quiet_census_principal_trace');assert.equal(out.evidenceQuality,p.evidence);
    }else{
      assert.equal(out.principalTrace,false);assert.equal(out.sourceMapBurned,true);assert.equal(out.sourceProtection,'hardened');
      assert.equal(out.nextHook,'quiet_census_source_shelter');assert.equal(out.evidenceQuality,p.burnEvidence);
    }
    assert.deepEqual(Array.from(out.sourceClasses),['clinic_intake','freight_movement','union_discipline','debt_history']);
    assert.equal(api.resolve(decision),false,'outcome must be idempotent');
    assert.equal(Game.journal.filter(x=>x.reconciliationStage==='choice').length,1);
    assert.equal(Game.journal.filter(x=>x.reconciliationStage==='outcome').length,1);
    const saved=JSON.parse(JSON.stringify(Game));Game.journal=[];Game.heat.meridian=99;Game.cityLife.discovered={};Object.assign(Game,saved);
    assert.equal(api.resolution().decision,decision);assert.equal(api.resolution().accessModifier,modifier);assert.equal(Game.cityLife.discovered.loc_helix_hidden_1,true);
  }
}
{
  const {Game,api}=make('quiet_census_clean_access',{remote:true});api.ensureLead();
  assert.equal(api.atTarget(),false);assert.equal(api.decisionAvailable('follow_principal'),false);assert.equal(api.resolve('follow_principal'),false);
  Game.ovPlayer={x:17,y:11};Game.activeMission={id:'busy'};assert.equal(api.decisionAvailable('follow_principal'),false);assert.equal(api.resolve('follow_principal'),false);
  Game.activeMission=null;assert.equal(api.resolve('follow_principal'),true);
}
console.log('PASS PWA12.136 RECONCILIATION WINDOW: four inherited Quiet Census access states x two irreversible decisions, physical gating, target discovery, consequences, exclusivity, idempotency, and save-shaped persistence');
