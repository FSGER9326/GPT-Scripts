function installPersistenceLifecycle({target=globalThis,bridge}={}){
  if(!bridge||typeof bridge.flush!=='function')throw new TypeError('bridge with flush() required');
  const doc=target.document;
  const flush=()=>{
    try{
      const result=bridge.flush();
      Promise.resolve(result).catch(err=>console.warn('[CR14] persistence flush failed:',err?.message||err));
      return result;
    }catch(err){
      console.warn('[CR14] persistence flush failed:',err?.message||err);
      return Promise.resolve(false);
    }
  };
  const onVisibility=()=>{if(doc?.visibilityState==='hidden')flush()};
  const onPageHide=()=>flush();

  doc?.addEventListener?.('visibilitychange',onVisibility);
  target.addEventListener?.('pagehide',onPageHide);

  return Object.freeze({
    flush,
    destroy(){
      doc?.removeEventListener?.('visibilitychange',onVisibility);
      target.removeEventListener?.('pagehide',onPageHide);
    }
  });
}
