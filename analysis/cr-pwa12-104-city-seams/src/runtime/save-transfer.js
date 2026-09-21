async function exportSaveText({persistence,slot=0,exportedAt=Date.now()}={}){
 if(!persistence)throw new TypeError('persistence required');
 const envelope=await persistence.loadSlot(Number(slot));
 if(!envelope)throw new Error(`save slot ${slot} is empty`);
 if(!await validateSaveEnvelope(envelope))throw new Error(`save slot ${slot} failed integrity validation`);
 return JSON.stringify({format:'chrome-requiem-save',formatVersion:1,exportedAt,slot:Number(slot),envelope});
}

async function importSaveText({persistence,text,slotOverride=null,now=Date.now()}={}){
 if(!persistence)throw new TypeError('persistence required');
 let doc;try{doc=typeof text==='string'?JSON.parse(text):structuredClone(text)}catch{throw new Error('invalid save JSON')}
 if(doc?.format!=='chrome-requiem-save'||doc?.formatVersion!==1||!doc.envelope)throw new Error('unsupported save export format');
 if(!await validateSaveEnvelope(doc.envelope))throw new Error('save export failed integrity validation');
 const slot=slotOverride===null||slotOverride===undefined?Number(doc.slot??doc.envelope.slot??0):Number(slotOverride);
 let envelope=doc.envelope;
 if(slot!==Number(envelope.slot))envelope=await createSaveEnvelope(envelope.payload,{gameVersion:envelope.gameVersion,slot,now,migratedFrom:envelope.migratedFrom??null});
 await persistence.saveSlot(slot,envelope);
 return Object.freeze({slot,envelope});
}
