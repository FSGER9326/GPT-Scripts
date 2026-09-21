function stableStringify(value){
 if(value===null||typeof value!=='object')return JSON.stringify(value);
 if(Array.isArray(value))return '['+value.map(stableStringify).join(',')+']';
 const keys=Object.keys(value).sort();
 return '{'+keys.map(k=>JSON.stringify(k)+':'+stableStringify(value[k])).join(',')+'}'
}

function sha256Fallback(text){
 const K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
 const H=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
 const bytes=new TextEncoder().encode(text),bitLen=BigInt(bytes.length)*8n;
 const total=Math.ceil((bytes.length+1+8)/64)*64,msg=new Uint8Array(total);msg.set(bytes);msg[bytes.length]=0x80;
 for(let i=0;i<8;i++)msg[total-1-i]=Number((bitLen>>BigInt(i*8))&0xffn);
 const rotr=(x,n)=>(x>>>n)|(x<<(32-n)),w=new Uint32Array(64);
 for(let off=0;off<msg.length;off+=64){
  for(let i=0;i<16;i++){const j=off+i*4;w[i]=((msg[j]<<24)|(msg[j+1]<<16)|(msg[j+2]<<8)|msg[j+3])>>>0}
  for(let i=16;i<64;i++){const s0=rotr(w[i-15],7)^rotr(w[i-15],18)^(w[i-15]>>>3),s1=rotr(w[i-2],17)^rotr(w[i-2],19)^(w[i-2]>>>10);w[i]=(w[i-16]+s0+w[i-7]+s1)>>>0}
  let[a,b,c,d,e,f,g,h]=H;
  for(let i=0;i<64;i++){const S1=rotr(e,6)^rotr(e,11)^rotr(e,25),ch=(e&f)^((~e)&g),t1=(h+S1+ch+K[i]+w[i])>>>0,S0=rotr(a,2)^rotr(a,13)^rotr(a,22),maj=(a&b)^(a&c)^(b&c),t2=(S0+maj)>>>0;h=g;g=f;f=e;e=(d+t1)>>>0;d=c;c=b;b=a;a=(t1+t2)>>>0}
  H[0]=(H[0]+a)>>>0;H[1]=(H[1]+b)>>>0;H[2]=(H[2]+c)>>>0;H[3]=(H[3]+d)>>>0;H[4]=(H[4]+e)>>>0;H[5]=(H[5]+f)>>>0;H[6]=(H[6]+g)>>>0;H[7]=(H[7]+h)>>>0;
 }
 return H.map(x=>x.toString(16).padStart(8,'0')).join('');
}
async function sha256Hex(text){
 const bytes=new TextEncoder().encode(text);
 if(globalThis.crypto?.subtle){const digest=await globalThis.crypto.subtle.digest('SHA-256',bytes);return [...new Uint8Array(digest)].map(b=>b.toString(16).padStart(2,'0')).join('')}
 return sha256Fallback(text);
}

function checksumSource({schemaVersion,gameVersion,slot,payload}){
 return stableStringify({schemaVersion,gameVersion,slot,payload});
}

async function createSaveEnvelope(payload,{gameVersion='14.0',slot=0,now=Date.now(),migratedFrom=null}={}){
 const cloned=structuredClone(payload);
 const base={schemaVersion:14,gameVersion:String(gameVersion),slot:Number(slot),createdAt:now,updatedAt:now,migratedFrom,payload:cloned};
 const checksum=await sha256Hex(checksumSource(base));
 return Object.freeze({...base,checksum});
}

async function validateSaveEnvelope(record){
 if(!record||record.schemaVersion!==14||!record.checksum||!('payload' in record))return false;
 try{return record.checksum===await sha256Hex(checksumSource(record))}catch{return false}
}
