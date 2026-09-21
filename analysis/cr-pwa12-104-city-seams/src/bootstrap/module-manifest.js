const MODULES=Object.freeze({
  'legacy.core':{path:'./src/legacy/core-v5.js',kind:'classic'},
  'legacy.coreApi':{path:'./src/legacy/core-v5-api.js',kind:'module'},
  'legacy.graphics':{path:'./src/legacy/graphics-v6.js',kind:'module'},
  'legacy.blackMagic':{path:'./src/legacy/black-magic-v7.js',kind:'module'},
  'legacy.intelligence':{path:'./src/legacy/mercenary-intelligence-v8.js',kind:'module'},
  'legacy.performance':{path:'./src/legacy/performance-v9.js',kind:'module'},
  'legacy.responsive':{path:'./src/legacy/responsive-v10.js',kind:'module'},
  'legacy.megacity':{path:'./src/legacy/megacity-v11.js',kind:'module'},
  'legacy.groundWar':{path:'./src/legacy/ground-war-v12.js',kind:'module'},
  'legacy.cityLife':{path:'./src/legacy/city-life-v13.js',kind:'module'},
  'legacy.cityLifeVisualFixes':{path:'./src/legacy/city-life-v13-visual-fixes.js',kind:'module'},
  'legacy.recovery':{path:'./src/legacy/black-magic-recovery-v13-1.js',kind:'module'},
  'legacy.megaCity132':{path:'./src/legacy/mega-city-v13-2.js',kind:'module'},
  'world.districts':{path:'./src/world/district-worlds-v13-3.js',kind:'module'},
  'world.livingStreets':{path:'./src/world/living-streets-v13-4a.js',kind:'module'},
  'missions.approaches':{path:'./src/missions/contract-approaches-v13-4b.js',kind:'module'},
  'company':{path:'./src/company/company-foundation-v13-5.js',kind:'module'},
  'visuals':{path:'./src/visuals/visual-identity-v13-6.js',kind:'module'},
  'runtime':{path:'./src/bootstrap/bootstrap.js',kind:'module'}
});

const MODULE_ORDER=Object.freeze([
  'legacy.core','legacy.coreApi','legacy.graphics','legacy.blackMagic','legacy.intelligence','legacy.performance','legacy.responsive','legacy.megacity','legacy.groundWar','legacy.cityLife',
  'legacy.cityLifeVisualFixes','legacy.recovery','legacy.megaCity132','world.districts',
  'world.livingStreets','missions.approaches','company','visuals','runtime'
]);
